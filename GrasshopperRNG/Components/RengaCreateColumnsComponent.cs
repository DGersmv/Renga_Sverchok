using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Attributes;
using Grasshopper.Kernel.Types;
using Rhino.Geometry;
using GrasshopperRNG.Client;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace GrasshopperRNG.Components
{
    /// <summary>
    /// Component for creating columns in Renga from Grasshopper points
    /// Prepares commands and sends them to main Renga Connect node
    /// </summary>
    public class RengaCreateColumnsComponent : GH_Component
    {
        private bool updateButtonPressed = false;
        private static Dictionary<string, string> pointGuidToColumnGuidMap = new Dictionary<string, string>();
        private static Dictionary<string, Point3d> pointGuidToLastCoordinates = new Dictionary<string, Point3d>();
        private static Dictionary<Point3d, string> pointToGuidMap = new Dictionary<Point3d, string>(new Point3dEqualityComparer());
        private static int guidCounter = 0;

        public RengaCreateColumnsComponent()
            : base("Renga Create Columns", "RengaCreateColumns",
                "Create columns in Renga from Grasshopper points",
                "Renga", "Columns")
        {
        }

        public override void CreateAttributes()
        {
            m_attributes = new RengaCreateColumnsComponentAttributes(this);
        }

        public void OnUpdateButtonClick()
        {
            updateButtonPressed = true;
            ExpireSolution(true);
        }

        protected override void RegisterInputParams(GH_InputParamManager pManager)
        {
            pManager.AddPointParameter("Points", "P", "Points for column placement", GH_ParamAccess.list);
            pManager.AddGenericParameter("RengaConnect", "RC", "Renga Connect component (main node)", GH_ParamAccess.item);
            pManager.AddNumberParameter("Height", "H", "Column height in millimeters (default: 3000)", GH_ParamAccess.item, 3000.0);
        }

        protected override void RegisterOutputParams(GH_OutputParamManager pManager)
        {
            pManager.AddBooleanParameter("Success", "S", "Success status for each column", GH_ParamAccess.list);
            pManager.AddTextParameter("Message", "M", "Messages for each column", GH_ParamAccess.list);
            pManager.AddTextParameter("ColumnGuids", "CG", "Column GUIDs in Renga", GH_ParamAccess.list);
        }

        protected override void SolveInstance(IGH_DataAccess DA)
        {
            List<Point3d> points = new List<Point3d>();
            object rengaConnectObj = null;
            double height = 3000.0;

            // Check if Update button was pressed
            bool wasUpdatePressed = updateButtonPressed;
            updateButtonPressed = false;

            // Validate inputs
            if (!DA.GetDataList(0, points) || points.Count == 0)
            {
                DA.SetDataList(0, new List<bool>());
                DA.SetDataList(1, new List<string> { "No points provided" });
                DA.SetDataList(2, new List<string>());
                return;
            }

            if (!DA.GetData(1, ref rengaConnectObj))
            {
                DA.SetDataList(0, new List<bool>());
                DA.SetDataList(1, new List<string> { "Renga Connect component not connected" });
                DA.SetDataList(2, new List<string>());
                return;
            }

            // Get height parameter
            if (!DA.GetData(2, ref height))
            {
                height = 3000.0; // default
            }

            // Validate height
            if (height <= 0)
            {
                AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "Height must be positive. Using default 3000mm");
                height = 3000.0;
            }

            // Validate points
            string validationError;
            if (!ValidateInputs(points, out validationError))
            {
                DA.SetDataList(0, new List<bool>());
                DA.SetDataList(1, new List<string> { validationError });
                DA.SetDataList(2, new List<string>());
                AddRuntimeMessage(GH_RuntimeMessageLevel.Error, validationError);
                return;
            }

            // Only process if Update button was pressed or points changed
            if (!wasUpdatePressed)
            {
                DA.SetDataList(0, new List<bool>());
                DA.SetDataList(1, new List<string> { "Click Update button to send points to Renga" });
                DA.SetDataList(2, new List<string>());
                return;
            }

            // Extract RengaGhClient from rengaConnectObj
            RengaGhClient client = null;
            
            // Try as RengaGhClientGoo
            if (rengaConnectObj is RengaGhClientGoo goo)
            {
                client = goo.Value;
            }
            // Try direct cast
            else if (rengaConnectObj is RengaGhClient directClient)
            {
                client = directClient;
            }
            // Try as IGH_Goo and cast
            else if (rengaConnectObj is IGH_Goo ghGoo)
            {
                try
                {
                    var scriptVar = ghGoo.ScriptVariable();
                    if (scriptVar is RengaGhClient scriptClient)
                    {
                        client = scriptClient;
                    }
                    else if (ghGoo is RengaGhClientGoo clientGoo)
                    {
                        client = clientGoo.Value;
                    }
                }
                catch
                {
                    // ScriptVariable may throw, ignore
                }
            }

            if (client == null || !client.IsConnected)
            {
                DA.SetDataList(0, new List<bool>());
                DA.SetDataList(1, new List<string> { "Renga Connect is not connected. Connect to Renga first." });
                DA.SetDataList(2, new List<string>());
                return;
            }

            // Prepare command with points, heights and GUIDs
            var command = PrepareCommand(points, height);
            if (command == null)
            {
                DA.SetDataList(0, new List<bool>());
                DA.SetDataList(1, new List<string> { "Failed to prepare command" });
                DA.SetDataList(2, new List<string>());
                return;
            }

            // Send command to server
            string responseJson = null;
            try
            {
                var json = JsonConvert.SerializeObject(command);
                responseJson = client.Send(json);
            }
            catch (System.Net.Sockets.SocketException ex)
            {
                AddRuntimeMessage(GH_RuntimeMessageLevel.Error, $"Network error: {ex.Message}");
                for (int i = 0; i < points.Count; i++)
                {
                    DA.SetDataList(0, new List<bool> { false });
                    DA.SetDataList(1, new List<string> { $"Network error: {ex.Message}" });
                    DA.SetDataList(2, new List<string> { "" });
                }
                return;
            }
            catch (JsonException ex)
            {
                AddRuntimeMessage(GH_RuntimeMessageLevel.Error, $"JSON serialization error: {ex.Message}");
                for (int i = 0; i < points.Count; i++)
                {
                    DA.SetDataList(0, new List<bool> { false });
                    DA.SetDataList(1, new List<string> { $"JSON error: {ex.Message}" });
                    DA.SetDataList(2, new List<string> { "" });
                }
                return;
            }
            catch (Exception ex)
            {
                AddRuntimeMessage(GH_RuntimeMessageLevel.Error, $"Unexpected error: {ex.Message}");
                for (int i = 0; i < points.Count; i++)
                {
                    DA.SetDataList(0, new List<bool> { false });
                    DA.SetDataList(1, new List<string> { $"Error: {ex.Message}" });
                    DA.SetDataList(2, new List<string> { "" });
                }
                return;
            }
            
            var successes = new List<bool>();
            var messages = new List<string>();
            var columnGuids = new List<string>();

            if (string.IsNullOrEmpty(responseJson))
            {
                // No response - assume failure
                for (int i = 0; i < points.Count; i++)
                {
                    successes.Add(false);
                    messages.Add("Failed to send data to Renga or no response");
                    columnGuids.Add("");
                }
            }
            else
            {
                // Parse response
                try
                {
                    var response = JsonConvert.DeserializeObject<JObject>(responseJson);
                    var results = response?["results"] as JArray;

                    if (results != null && results.Count == points.Count)
                    {
                        for (int i = 0; i < points.Count; i++)
                        {
                            var result = results[i] as JObject;
                            var success = result?["success"]?.Value<bool>() ?? false;
                            var message = result?["message"]?.ToString() ?? "Unknown";
                            var columnId = result?["columnId"]?.ToString() ?? "";

                            successes.Add(success);
                            messages.Add(message);
                            columnGuids.Add(columnId);

                            // Update mapping
                            if (success && !string.IsNullOrEmpty(columnId))
                            {
                                var pointGuid = GetPointGuid(points[i]);
                                pointGuidToColumnGuidMap[pointGuid] = columnId;
                            }
                        }
                    }
                    else
                    {
                        // Response format doesn't match
                        for (int i = 0; i < points.Count; i++)
                        {
                            successes.Add(false);
                            messages.Add("Invalid response format from Renga");
                            columnGuids.Add("");
                        }
                    }
                }
                catch (Exception ex)
                {
                    // Error parsing response
                    for (int i = 0; i < points.Count; i++)
                    {
                        successes.Add(false);
                        messages.Add($"Error parsing response: {ex.Message}");
                        columnGuids.Add("");
                    }
                }
            }

            DA.SetDataList(0, successes);
            DA.SetDataList(1, messages);
            DA.SetDataList(2, columnGuids);
        }

        protected override Bitmap Icon
        {
            get
            {
                // TODO: Add icon
                return null;
            }
        }

        private object PrepareCommand(List<Point3d> points, double height)
        {
            var pointData = new List<object>();

            foreach (var point in points)
            {
                var pointGuid = GetPointGuid(point);
                var rengaColumnGuid = pointGuidToColumnGuidMap.ContainsKey(pointGuid) 
                    ? pointGuidToColumnGuidMap[pointGuid] 
                    : null;

                pointData.Add(new
                {
                    x = point.X,
                    y = point.Y,
                    z = point.Z,
                    height = height,
                    grasshopperGuid = pointGuid,
                    rengaColumnGuid = rengaColumnGuid
                });
            }

            return new
            {
                command = "update_points",
                points = pointData,
                timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
            };
        }

        private string GetPointGuid(Point3d point)
        {
            // Try to get GUID from point if it's a GH_Point with Rhino geometry
            if (point is GH_Point ghPoint && ghPoint.Value != null)
            {
                var rhinoPoint = ghPoint.Value;
                // Try to get GUID from Rhino geometry if available
                // Note: Rhino Point3d doesn't have GUID, but we can check if it's from geometry
            }

            // Use stable GUID based on point coordinates with fallback to counter
            // Check if we already have a GUID for this point (within tolerance)
            const double tolerance = 0.001;
            foreach (var kvp in pointToGuidMap)
            {
                var existingPoint = kvp.Key;
                if (Math.Abs(existingPoint.X - point.X) < tolerance &&
                    Math.Abs(existingPoint.Y - point.Y) < tolerance &&
                    Math.Abs(existingPoint.Z - point.Z) < tolerance)
                {
                    return kvp.Value;
                }
            }

            // Generate new GUID for this point
            var newGuid = $"GH_Point_{++guidCounter}_{Guid.NewGuid():N}";
            pointToGuidMap[point] = newGuid;
            return newGuid;
        }

        private bool ValidateInputs(List<Point3d> points, out string errorMessage)
        {
            errorMessage = "";

            if (points == null || points.Count == 0)
            {
                errorMessage = "No points provided";
                return false;
            }

            foreach (var point in points)
            {
                if (point == null)
                {
                    errorMessage = "One or more points are null";
                    return false;
                }

                if (double.IsNaN(point.X) || double.IsInfinity(point.X) ||
                    double.IsNaN(point.Y) || double.IsInfinity(point.Y) ||
                    double.IsNaN(point.Z) || double.IsInfinity(point.Z))
                {
                    errorMessage = $"Invalid point coordinates: ({point.X}, {point.Y}, {point.Z})";
                    return false;
                }

                // Check for reasonable coordinate values (within ±1000000)
                if (Math.Abs(point.X) > 1000000 || Math.Abs(point.Y) > 1000000 || Math.Abs(point.Z) > 1000000)
                {
                    errorMessage = $"Point coordinates out of reasonable range: ({point.X}, {point.Y}, {point.Z})";
                    return false;
                }
            }

            return true;
        }

        private bool HasCoordinatesChanged(string pointGuid, Point3d currentPoint)
        {
            if (!pointGuidToLastCoordinates.ContainsKey(pointGuid))
            {
                // New point
                pointGuidToLastCoordinates[pointGuid] = currentPoint;
                return true;
            }

            var lastPoint = pointGuidToLastCoordinates[pointGuid];
            const double tolerance = 0.001; // Tolerance in Grasshopper units

            if (Math.Abs(currentPoint.X - lastPoint.X) > tolerance ||
                Math.Abs(currentPoint.Y - lastPoint.Y) > tolerance ||
                Math.Abs(currentPoint.Z - lastPoint.Z) > tolerance)
            {
                // Coordinates changed
                pointGuidToLastCoordinates[pointGuid] = currentPoint;
                return true;
            }

            return false; // Coordinates haven't changed
        }

        // Helper class for Point3d equality comparison
        private class Point3dEqualityComparer : IEqualityComparer<Point3d>
        {
            private const double tolerance = 0.001;

            public bool Equals(Point3d x, Point3d y)
            {
                return Math.Abs(x.X - y.X) < tolerance &&
                       Math.Abs(x.Y - y.Y) < tolerance &&
                       Math.Abs(x.Z - y.Z) < tolerance;
            }

            public int GetHashCode(Point3d obj)
            {
                return obj.X.GetHashCode() ^ obj.Y.GetHashCode() ^ obj.Z.GetHashCode();
            }
        }
