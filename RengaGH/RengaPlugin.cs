/*  Renga_Grasshopper Integration Plugin
 *
 *  This plugin creates a TCP server to receive data from Grasshopper
 *  and creates/updates columns in Renga based on point coordinates.
 *
 *  Copyright Renga Software LLC, 2025. All rights reserved.
 */

#nullable disable
using System;
using Renga;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Threading.Tasks;
using System.Text;
using System.Windows.Forms;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace RengaPlugin
{
    public class RengaPlugin : Renga.IPlugin
    {
        private Renga.IApplication m_app;
        private TcpListener tcpListener;
        private bool isServerRunning = false;
        private int serverPort = 50100; // Default port
        private Dictionary<string, int> guidToColumnIdMap = new Dictionary<string, int>(); // Grasshopper Point GUID -> Renga Column ID

        private List<Renga.ActionEventSource> m_eventSources = new List<Renga.ActionEventSource>();

        public bool Initialize(string pluginFolder)
        {
            m_app = new Renga.Application();
            var ui = m_app.UI;
            var panelExtension = ui.CreateUIPanelExtension();

            // Add button for server settings
            var settingsAction = ui.CreateAction();
            settingsAction.DisplayName = "Server Settings";
            settingsAction.ToolTip = "Configure TCP server port and manage server";

            var settingsEvents = new Renga.ActionEventSource(settingsAction);
            settingsEvents.Triggered += (s, e) =>
            {
                ShowServerSettings();
            };
            m_eventSources.Add(settingsEvents);
            panelExtension.AddToolButton(settingsAction);

            ui.AddExtensionToPrimaryPanel(panelExtension);

            // Don't start server automatically - user will start it from settings
            // StartTcpServer(serverPort);

            return true;
        }

        private void ShowServerSettings()
        {
            using (var form = new ServerSettingsForm(serverPort, isServerRunning))
            {
                form.StartServerRequested += (s, e) =>
                {
                    StartTcpServer(form.Port);
                    form.UpdateServerStatus(isServerRunning);
                };
                form.StopServerRequested += (s, e) =>
                {
                    StopTcpServer();
                    form.UpdateServerStatus(isServerRunning);
                };
                form.PortChanged += (s, port) =>
                {
                    serverPort = port;
                };

                form.ShowDialog();
            }
        }

        public void Stop()
        {
            StopTcpServer();
            foreach (var eventSource in m_eventSources)
                eventSource.Dispose();
            m_eventSources.Clear();
        }

        private void StartTcpServer(int port)
        {
            try
            {
                if (port < 1024 || port > 65535)
                {
                    m_app.UI.ShowMessageBox(
                        Renga.MessageIcon.MessageIcon_Error,
                        "Renga_Grasshopper Plugin",
                        $"Invalid port number: {port}. Port must be in range 1024-65535.");
                    return;
                }

                serverPort = port;
                tcpListener = new TcpListener(IPAddress.Any, port);
                tcpListener.Start();
                isServerRunning = true;

                // Start accepting connections asynchronously
                _ = Task.Run(async () => await AcceptConnectionsAsync());

                // Server started successfully - message will be shown in settings form
                System.Diagnostics.Debug.WriteLine($"TCP server started on port {port}");
            }
            catch (Exception ex)
            {
                m_app.UI.ShowMessageBox(
                    Renga.MessageIcon.MessageIcon_Error,
                    "Renga_Grasshopper Plugin",
                    $"Failed to start TCP server: {ex.Message}");
            }
        }

        private void StopTcpServer()
        {
            isServerRunning = false;
            tcpListener?.Stop();
        }

        private async Task AcceptConnectionsAsync()
        {
            while (isServerRunning)
            {
                try
                {
                    var client = await tcpListener!.AcceptTcpClientAsync();
                    _ = Task.Run(async () => await HandleClientAsync(client));
                }
                catch (ObjectDisposedException)
                {
                    // Server was stopped
                    break;
                }
                catch (Exception ex)
                {
                    // Log error but continue accepting connections
                    System.Diagnostics.Debug.WriteLine($"Error accepting connection: {ex.Message}");
                }
            }
        }

        private async Task HandleClientAsync(TcpClient client)
        {
            try
            {
                var stream = client.GetStream();
                var buffer = new byte[8192]; // Increased buffer size
                var totalBytesRead = 0;
                
                // Read data in chunks until we have complete JSON
                while (client.Connected && stream.DataAvailable)
                {
                    var bytesRead = await stream.ReadAsync(buffer, totalBytesRead, buffer.Length - totalBytesRead);
                    if (bytesRead == 0) break;
                    totalBytesRead += bytesRead;
                }

                if (totalBytesRead > 0)
                {
                    var json = Encoding.UTF8.GetString(buffer, 0, totalBytesRead);
                    var command = ParseAndProcessCommand(json);
                    
                    // Send response back to client
                    var response = CreateResponse(command);
                    var responseJson = JsonConvert.SerializeObject(response);
                    var responseData = Encoding.UTF8.GetBytes(responseJson);
                    await stream.WriteAsync(responseData, 0, responseData.Length);
                    await stream.FlushAsync();
                }
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error handling client: {ex.Message}");
            }
            finally
            {
                client.Close();
            }
        }

        private CommandResult ParseAndProcessCommand(string json)
        {
            try
            {
                var jsonObj = JObject.Parse(json);
                var command = jsonObj["command"]?.ToString();
                var points = jsonObj["points"] as JArray;

                if (points == null || points.Count == 0)
                {
                    return new CommandResult { Success = false, Message = "No points provided" };
                }

                var results = new List<PointResult>();

                foreach (var pointObj in points)
                {
                    var pointResult = ProcessPoint(pointObj as JObject);
                    results.Add(pointResult);
                }

                return new CommandResult
                {
                    Success = true,
                    Message = $"Processed {results.Count} points",
                    Results = results
                };
            }
            catch (Exception ex)
            {
                return new CommandResult
                {
                    Success = false,
                    Message = $"Error parsing command: {ex.Message}"
                };
            }
        }

        private PointResult ProcessPoint(JObject? pointObj)
        {
            if (pointObj == null)
            {
                return new PointResult { Success = false, Message = "Invalid point data" };
            }

            try
            {
                var x = pointObj["x"]?.Value<double>() ?? 0;
                var y = pointObj["y"]?.Value<double>() ?? 0;
                var z = pointObj["z"]?.Value<double>() ?? 0;
                var grasshopperGuid = pointObj["grasshopperGuid"]?.ToString();
                var rengaColumnGuid = pointObj["rengaColumnGuid"]?.ToString();

                if (string.IsNullOrEmpty(grasshopperGuid))
                {
                    return new PointResult { Success = false, Message = "Missing grasshopperGuid" };
                }

                // Check if column already exists
                int columnId = 0;
                bool columnExists = false;

                // First check by grasshopperGuid in our map
                if (guidToColumnIdMap.ContainsKey(grasshopperGuid))
                {
                    columnId = guidToColumnIdMap[grasshopperGuid];
                    columnExists = true;
                }
                // If not found, check by rengaColumnGuid (if provided)
                else if (!string.IsNullOrEmpty(rengaColumnGuid))
                {
                    if (int.TryParse(rengaColumnGuid, out int parsedId))
                    {
                        // Check if this column ID exists in our map
                        if (guidToColumnIdMap.ContainsValue(parsedId))
                        {
                            columnId = parsedId;
                            columnExists = true;
                            // Update mapping with grasshopperGuid
                            var existingKey = guidToColumnIdMap.FirstOrDefault(kvp => kvp.Value == parsedId).Key;
                            if (!string.IsNullOrEmpty(existingKey))
                            {
                                guidToColumnIdMap.Remove(existingKey);
                            }
                            guidToColumnIdMap[grasshopperGuid] = parsedId;
                        }
                    }
                }
                else
                {
                    columnId = 0;
                }

                if (columnExists)
                {
                    // Update column position
                    return UpdateColumn(columnId, x, y, z, grasshopperGuid);
                }
                else
                {
                    // Create new column
                    return CreateColumn(x, y, z, grasshopperGuid);
                }
            }
            catch (Exception ex)
            {
                return new PointResult { Success = false, Message = $"Error processing point: {ex.Message}" };
            }
        }

        private PointResult CreateColumn(double x, double y, double z, string grasshopperGuid)
        {
            try
            {
                var model = m_app.Project.Model;
                if (model == null)
                {
                    return new PointResult { Success = false, Message = "No active model" };
                }

                // Get active level or first level
                Renga.ILevel? level = GetActiveLevel();
                if (level == null)
                {
                    return new PointResult { Success = false, Message = "No active level found" };
                }

                var args = model.CreateNewEntityArgs();
                args.TypeId = Renga.ObjectTypes.Column;

                var op = m_app.Project.CreateOperationWithUndo(model.Id);
                op.Start();
                var column = model.CreateObject(args) as Renga.ILevelObject;
                
                if (column == null)
                {
                    op.Rollback();
                    return new PointResult { Success = false, Message = m_app.LastError };
                }

                // Set placement - get existing placement and modify origin
                var placement = column.GetPlacement();
                if (placement != null)
                {
                    // Create a copy and move it to the new position
                    var newPlacement = placement.GetCopy();
                    var moveVector = new Renga.Vector3D 
                    { 
                        X = x - placement.Origin.X, 
                        Y = y - placement.Origin.Y, 
                        Z = z - placement.Origin.Z 
                    };
                    newPlacement.Move(moveVector);
                    column.SetPlacement(newPlacement);
                }
                op.Apply();

                // Store mapping - get ID from column object (cast to IModelObject)
                int columnId = (column as Renga.IModelObject).Id;
                
                guidToColumnIdMap[grasshopperGuid] = columnId;

                return new PointResult
                {
                    Success = true,
                    Message = "Column created",
                    ColumnId = columnId.ToString(),
                    GrasshopperGuid = grasshopperGuid
                };
            }
            catch (Exception ex)
            {
                return new PointResult { Success = false, Message = $"Error creating column: {ex.Message}" };
            }
        }

        private PointResult UpdateColumn(int columnId, double x, double y, double z, string grasshopperGuid)
        {
            try
            {
                var model = m_app.Project.Model;
                if (model == null)
                {
                    return new PointResult { Success = false, Message = "No active model" };
                }

                var column = model.GetObjects().GetById(columnId) as ILevelObject;
                if (column == null)
                {
                    return new PointResult { Success = false, Message = "Column not found" };
                }

                var op = m_app.Project.CreateOperationWithUndo(model.Id);
                op.Start();

                // Update placement - get existing placement and move it to new position
                var placement = column.GetPlacement();
                if (placement != null)
                {
                    // Create a copy and move it to the new position
                    var newPlacement = placement.GetCopy();
                    var moveVector = new Renga.Vector3D 
                    { 
                        X = x - placement.Origin.X, 
                        Y = y - placement.Origin.Y, 
                        Z = z - placement.Origin.Z 
                    };
                    newPlacement.Move(moveVector);
                    column.SetPlacement(newPlacement);
                }
                
                op.Apply();

                return new PointResult
                {
                    Success = true,
                    Message = "Column updated",
                    ColumnId = columnId.ToString(),
                    GrasshopperGuid = grasshopperGuid
                };
            }
            catch (Exception ex)
            {
                return new PointResult { Success = false, Message = $"Error updating column: {ex.Message}" };
            }
        }

        private Renga.ILevel? GetActiveLevel()
        {
            try
            {
                var view = m_app.ActiveView;
                if (view?.Type == Renga.ViewType.ViewType_View3D || view?.Type == Renga.ViewType.ViewType_Level)
                {
                    var model = m_app.Project.Model;
                    if (model != null)
                    {
                        var objects = model.GetObjects();
                        int count = objects.Count;
                        for (int i = 0; i < count; i++)
                        {
                            var obj = objects.GetByIndex(i);
                            if (obj.ObjectType == Renga.ObjectTypes.Level)
                            {
                                return obj as Renga.ILevel;
                            }
                        }
                    }
                }
            }
            catch
            {
                // Fall through
            }
            return null;
        }

        private object CreateResponse(CommandResult result)
        {
            return new
            {
                success = result.Success,
                message = result.Message,
                results = result.Results?.Select(r => new
                {
                    success = r.Success,
                    message = r.Message,
                    columnId = r.ColumnId,
                    grasshopperGuid = r.GrasshopperGuid
                })
            };
        }
    }

    // Helper classes
    internal class CommandResult
    {
        public bool Success { get; set; }
        public string Message { get; set; } = "";
        public List<PointResult>? Results { get; set; }
    }

    internal class PointResult
    {
        public bool Success { get; set; }
        public string Message { get; set; } = "";
        public string? ColumnId { get; set; }
        public string? GrasshopperGuid { get; set; }
    }
}

