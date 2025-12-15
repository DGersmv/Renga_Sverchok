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

            // Check if Update button was pressed
            bool wasUpdatePressed = updateButtonPressed;
            updateButtonPressed = false;

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

            // Prepare command with points and GUIDs
            var command = PrepareCommand(points);
            if (command == null)
            {
                DA.SetDataList(0, new List<bool>());
                DA.SetDataList(1, new List<string> { "Failed to prepare command" });
                DA.SetDataList(2, new List<string>());
                return;
            }

            // Send command to server
            var json = JsonConvert.SerializeObject(command);
            var responseJson = client.Send(json);
            
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

        private object PrepareCommand(List<Point3d> points)
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
