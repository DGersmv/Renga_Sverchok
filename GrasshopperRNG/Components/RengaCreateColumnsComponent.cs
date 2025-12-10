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
            : base("Input", "Input",
                "Input: Add columns to Renga from Grasshopper points",
                "RNG", "Input")
        {
        }

        public override void AppendAdditionalMenuItems(System.Windows.Forms.ToolStripDropDown menu)
        {
            base.AppendAdditionalMenuItems(menu);
            menu.Items.Add(new System.Windows.Forms.ToolStripSeparator());
            var updateItem = new System.Windows.Forms.ToolStripMenuItem("Update - Send to Renga");
            updateItem.Click += (s, e) => OnUpdateButtonClick();
            menu.Items.Add(updateItem);
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
                DA.SetDataList(1, new List<string> { "Renga Connect component not connected. Connect output 'Client' from RNG component to Input component." });
                DA.SetDataList(2, new List<string>());
                return;
            }
            
            // Debug: log what we received
            if (rengaConnectObj == null)
            {
                DA.SetDataList(0, new List<bool>());
                DA.SetDataList(1, new List<string> { "Received null from RNG component. Make sure RNG component is solved and 'Client' output is connected." });
                DA.SetDataList(2, new List<string>());
                return;
            }

            // Only process if Update button was pressed (via menu)
            if (!wasUpdatePressed)
            {
                DA.SetDataList(0, new List<bool>());
                DA.SetDataList(1, new List<string> { "Right-click component → 'Update - Send to Renga' to send points" });
                DA.SetDataList(2, new List<string>());
                return;
            }

            // Extract RengaGhClient from rengaConnectObj
            RengaGhClient client = null;
            
            // Try as RengaGhClientGoo (most common case)
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
                // Try to cast to RengaGhClientGoo
                if (ghGoo is RengaGhClientGoo clientGoo)
                {
                    client = clientGoo.Value;
                }
                else
                {
                    // Try ScriptVariable
                    try
                    {
                        var scriptVar = ghGoo.ScriptVariable();
                        if (scriptVar is RengaGhClient scriptClient)
                        {
                            client = scriptClient;
                        }
                    }
                    catch
                    {
                        // ScriptVariable may throw, ignore
                    }
                }
            }

            // Debug: check what we got
            if (client == null)
            {
                DA.SetDataList(0, new List<bool>());
                var errorMsg = "❌ Wrong output connected! ";
                if (rengaConnectObj == null)
                    errorMsg += "No connection. ";
                else
                {
                    var receivedType = rengaConnectObj.GetType().Name;
                    if (receivedType == "GH_Boolean" || receivedType.Contains("Boolean"))
                        errorMsg += "You connected 'Connected' (boolean) output. ";
                    else
                        errorMsg += $"Received type: {receivedType}. ";
                }
                errorMsg += "⚠️ Connect the 'Client' output (3rd output) from RNG component to 'RengaConnect' input of Input component!";
                DA.SetDataList(1, new List<string> { errorMsg });
                DA.SetDataList(2, new List<string>());
                return;
            }

            if (!client.IsConnected)
            {
                DA.SetDataList(0, new List<bool>());
                DA.SetDataList(1, new List<string> { 
                    "Renga Connect is not connected. " +
                    "Steps: 1) Set 'Connect' to True in RNG component, 2) Make sure Renga server is running (click RNG button in Renga), 3) Check port matches (default 50100)" 
                });
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
            System.Diagnostics.Debug.WriteLine($"Sending command to Renga: {json.Substring(0, Math.Min(200, json.Length))}...");
            
            var responseJson = client.Send(json);
            
            var successes = new List<bool>();
            var messages = new List<string>();
            var columnGuids = new List<string>();

            if (string.IsNullOrEmpty(responseJson))
            {
                // No response - check connection status
                var errorMsg = "Failed to send data to Renga or no response. ";
                if (!client.IsConnected)
                    errorMsg += "Connection lost. Check Renga server status.";
                else
                    errorMsg += "Server may be busy or not responding. Check Renga server logs.";
                
                for (int i = 0; i < points.Count; i++)
                {
                    successes.Add(false);
                    messages.Add(errorMsg);
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

        private string GetPointGuid(Point3d point)
        {
            // Try to get Rhino GUID if available (from GH_Point)
            // For now, generate a stable GUID based on point coordinates
            // Round coordinates to 1mm precision for stability
            var roundedX = Math.Round(point.X, 0);
            var roundedY = Math.Round(point.Y, 0);
            var roundedZ = Math.Round(point.Z, 0);
            
            // Create a stable key
            var key = $"Point_{roundedX}_{roundedY}_{roundedZ}";
            
            // Use MD5 hash to generate a GUID-like string
            using (var md5 = System.Security.Cryptography.MD5.Create())
            {
                var hash = md5.ComputeHash(System.Text.Encoding.UTF8.GetBytes(key));
                return new Guid(hash).ToString();
            }
        }

        public override Guid ComponentGuid => new Guid("8B9C0D1E-2F34-5678-9ABC-DEF012345678");
    }
}

