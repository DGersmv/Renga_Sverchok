using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using Renga;
using RengaPlugin.Commands;
using RengaPlugin.Connection;
using Newtonsoft.Json.Linq;

namespace RengaPlugin.Handlers
{
    /// <summary>
    /// Handler for get_walls command
    /// </summary>
    public class GetWallsHandler : ICommandHandler
    {
        private Renga.IApplication m_app;

        public GetWallsHandler(Renga.IApplication app)
        {
            m_app = app;
        }

        public ConnectionResponse Handle(ConnectionMessage message)
        {
            try
            {
                var model = m_app.Project.Model;
                if (model == null)
                {
                    return new ConnectionResponse
                    {
                        Id = message.Id,
                        Success = false,
                        Error = "No active model"
                    };
                }

                var walls = new List<object>();
                var objects = model.GetObjects();
                int count = objects.Count;

                for (int i = 0; i < count; i++)
                {
                    try
                    {
                        var obj = objects.GetByIndex(i);
                        if (obj.ObjectType == Renga.ObjectTypes.Wall)
                        {
                            var wall = obj as Renga.ILevelObject;
                            if (wall != null)
                            {
                                var placement = wall.GetPlacement();
                                var modelObject = obj as Renga.IModelObject;
                                
                                // Get wall parameters
                                double height = 0;
                                double thickness = 0;
                                try
                                {
                                    var parameters = modelObject?.GetParameters();
                                    if (parameters != null)
                                    {
                                        try
                                        {
                                            var heightParam = parameters.Get(Renga.ParameterIds.WallHeight);
                                            if (heightParam != null)
                                                height = heightParam.GetDoubleValue();
                                        }
                                        catch { }
                                        
                                        try
                                        {
                                            var thicknessParam = parameters.Get(Renga.ParameterIds.WallThickness);
                                            if (thicknessParam != null)
                                                thickness = thicknessParam.GetDoubleValue();
                                        }
                                        catch { }
                                    }
                                }
                                catch { }
                                
                                // Get baseline curve
                                object baselineData = ExtractBaselineData(obj);
                                
                                // Get mesh geometry
                                object meshData = ExtractMeshData(modelObject);
                                
                                var wallData = new
                                {
                                    id = obj.Id,
                                    name = obj.Name ?? $"Wall {obj.Id}",
                                    position = placement != null ? new
                                    {
                                        x = placement.Origin.X,
                                        y = placement.Origin.Y,
                                        z = placement.Origin.Z
                                    } : null,
                                    height = height,
                                    thickness = thickness,
                                    baseline = baselineData,
                                    mesh = meshData
                                };
                                walls.Add(wallData);
                            }
                        }
                    }
                    catch (Exception ex)
                    {
                        // Skip this object if there's an error
                        System.Diagnostics.Debug.WriteLine($"Error processing wall object: {ex.Message}");
                    }
                }

                var responseData = new JObject
                {
                    ["walls"] = JArray.FromObject(walls)
                };

                return new ConnectionResponse
                {
                    Id = message.Id,
                    Success = true,
                    Data = responseData
                };
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"GetWallsHandler error: {ex.Message}\n{ex.StackTrace}");
                return new ConnectionResponse
                {
                    Id = message.Id,
                    Success = false,
                    Error = $"Error getting walls: {ex.Message}"
                };
            }
        }

        private object ExtractBaselineData(Renga.IModelObject wallObj)
        {
            try
            {
                // Cast to ILevelObject to access wall-specific methods
                var levelObj = wallObj as Renga.ILevelObject;
                if (levelObj == null)
                    return null;

                // Try multiple approaches to get baseline
                object baseline = null;
                
                // Approach 1: Try GetBaseline method via reflection (case-insensitive, check all methods)
                try
                {
                    var wallType = wallObj.GetType();
                    var allMethods = wallType.GetMethods(System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic);
                    
                    // Look for GetBaseline method (case-insensitive)
                    var getBaselineMethod = Array.Find(allMethods, m => 
                        m.Name.Equals("GetBaseline", StringComparison.OrdinalIgnoreCase) && 
                        m.GetParameters().Length == 0);
                    
                    if (getBaselineMethod != null)
                    {
                        baseline = getBaselineMethod.Invoke(wallObj, null);
                        System.Diagnostics.Debug.WriteLine($"Found GetBaseline method, result: {(baseline != null ? "not null" : "null")}");
                    }
                    else
                    {
                        System.Diagnostics.Debug.WriteLine($"GetBaseline method not found. Available methods: {string.Join(", ", allMethods.Select(m => m.Name))}");
                    }
                }
                catch (Exception ex)
                {
                    System.Diagnostics.Debug.WriteLine($"Error getting baseline via reflection: {ex.Message}\n{ex.StackTrace}");
                }

                // Approach 2: Try using dynamic
                if (baseline == null)
                {
                    try
                    {
                        dynamic wallDynamic = wallObj;
                        baseline = wallDynamic.GetBaseline();
                        System.Diagnostics.Debug.WriteLine($"Dynamic approach result: {(baseline != null ? "not null" : "null")}");
                    }
                    catch (Exception ex)
                    {
                        System.Diagnostics.Debug.WriteLine($"Error with dynamic approach: {ex.Message}");
                    }
                }

                // Approach 3: Try to get baseline from placement or other properties
                if (baseline == null)
                {
                    try
                    {
                        // Maybe baseline is accessible through placement or other properties
                        var placement = levelObj.GetPlacement();
                        if (placement != null)
                        {
                            System.Diagnostics.Debug.WriteLine($"Placement found: Origin=({placement.Origin.X}, {placement.Origin.Y}, {placement.Origin.Z})");
                            // Check if there's a way to get baseline from placement
                            // This might not work, but worth trying
                        }
                    }
                    catch (Exception ex)
                    {
                        System.Diagnostics.Debug.WriteLine($"Error getting placement: {ex.Message}");
                    }
                }

                if (baseline != null)
                {
                    return ExtractBaselineFromCurve(baseline);
                }

                System.Diagnostics.Debug.WriteLine("All approaches failed to get baseline");
                return null;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error extracting baseline: {ex.Message}\n{ex.StackTrace}");
                return null;
            }
        }

        private object ExtractBaselineFromCurve(dynamic baseline)
        {
            try
            {
                if (baseline == null)
                    return null;

                var baselineObj = new Dictionary<string, object>();
                var baselineType = baseline.GetType();
                
                // Get curve type
                string curveTypeStr = "LineSegment";
                try
                {
                    var getCurveTypeMethod = baselineType.GetMethod("GetCurveType");
                    if (getCurveTypeMethod != null)
                    {
                        var curveType = getCurveTypeMethod.Invoke(baseline, null);
                        curveTypeStr = curveType?.ToString() ?? "LineSegment";
                        baselineObj["type"] = curveTypeStr;
                    }
                }
                catch
                {
                    baselineObj["type"] = curveTypeStr;
                }

                // Get start and end points
                try
                {
                    var getStartPointMethod = baselineType.GetMethod("GetStartPoint");
                    var getEndPointMethod = baselineType.GetMethod("GetEndPoint");
                    if (getStartPointMethod != null && getEndPointMethod != null)
                    {
                        var startPoint = getStartPointMethod.Invoke(baseline, null);
                        var endPoint = getEndPointMethod.Invoke(baseline, null);
                        
                        if (startPoint != null && endPoint != null)
                        {
                            var pointType = startPoint.GetType();
                            var xProp = pointType.GetProperty("X");
                            var yProp = pointType.GetProperty("Y");
                            var zProp = pointType.GetProperty("Z");
                            
                            if (xProp != null && yProp != null && zProp != null)
                            {
                                baselineObj["startPoint"] = new { 
                                    x = (double)xProp.GetValue(startPoint), 
                                    y = (double)yProp.GetValue(startPoint), 
                                    z = (double)zProp.GetValue(startPoint) 
                                };
                                baselineObj["endPoint"] = new { 
                                    x = (double)xProp.GetValue(endPoint), 
                                    y = (double)yProp.GetValue(endPoint), 
                                    z = (double)zProp.GetValue(endPoint) 
                                };
                            }
                        }
                    }
                }
                catch (Exception ex)
                {
                    System.Diagnostics.Debug.WriteLine($"Error getting start/end points: {ex.Message}");
                }

                // For polycurves, extract segments with exact 3D coordinates
                if (curveTypeStr.Contains("PolyCurve") || curveTypeStr.Contains("Polyline"))
                {
                    var segments = new List<object>();
                    try
                    {
                        // Try to get segment count
                        var getSegmentCountMethod = baselineType.GetMethod("GetSegmentCount");
                        if (getSegmentCountMethod != null)
                        {
                            int segmentCount = (int)getSegmentCountMethod.Invoke(baseline, null);
                            
                            // Get each segment
                            var getSegmentMethod = baselineType.GetMethod("GetSegment", new Type[] { typeof(int) });
                            if (getSegmentMethod != null)
                            {
                                for (int i = 0; i < segmentCount; i++)
                                {
                                    try
                                    {
                                        var segment = getSegmentMethod.Invoke(baseline, new object[] { i });
                                        if (segment != null)
                                        {
                                            var segmentType = segment.GetType();
                                            var segObj = new Dictionary<string, object>();
                                            
                                            // Get segment type
                                            var segGetCurveTypeMethod = segmentType.GetMethod("GetCurveType");
                                            if (segGetCurveTypeMethod != null)
                                            {
                                                var segCurveType = segGetCurveTypeMethod.Invoke(segment, null);
                                                segObj["type"] = segCurveType?.ToString() ?? "LineSegment";
                                            }
                                            else
                                            {
                                                segObj["type"] = "LineSegment";
                                            }
                                            
                                            // Get segment start and end points with 3D coordinates
                                            var segGetStartMethod = segmentType.GetMethod("GetStartPoint");
                                            var segGetEndMethod = segmentType.GetMethod("GetEndPoint");
                                            if (segGetStartMethod != null && segGetEndMethod != null)
                                            {
                                                var segStart = segGetStartMethod.Invoke(segment, null);
                                                var segEnd = segGetEndMethod.Invoke(segment, null);
                                                
                                                if (segStart != null && segEnd != null)
                                                {
                                                    var pointType = segStart.GetType();
                                                    var xProp = pointType.GetProperty("X");
                                                    var yProp = pointType.GetProperty("Y");
                                                    var zProp = pointType.GetProperty("Z");
                                                    
                                                    if (xProp != null && yProp != null && zProp != null)
                                                    {
                                                        segObj["start3DX"] = (double)xProp.GetValue(segStart);
                                                        segObj["start3DY"] = (double)yProp.GetValue(segStart);
                                                        segObj["start3DZ"] = (double)zProp.GetValue(segStart);
                                                        segObj["end3DX"] = (double)xProp.GetValue(segEnd);
                                                        segObj["end3DY"] = (double)yProp.GetValue(segEnd);
                                                        segObj["end3DZ"] = (double)zProp.GetValue(segEnd);
                                                    }
                                                }
                                            }
                                            
                                            // For arcs, get center and radius
                                            if (segObj["type"].ToString().Contains("Arc"))
                                            {
                                                try
                                                {
                                                    var segGetCenterMethod = segmentType.GetMethod("GetCenter");
                                                    var segGetRadiusMethod = segmentType.GetMethod("GetRadius");
                                                    if (segGetCenterMethod != null && segGetRadiusMethod != null)
                                                    {
                                                        var center = segGetCenterMethod.Invoke(segment, null);
                                                        var radius = segGetRadiusMethod.Invoke(segment, null);
                                                        
                                                        if (center != null)
                                                        {
                                                            var pointType = center.GetType();
                                                            var xProp = pointType.GetProperty("X");
                                                            var yProp = pointType.GetProperty("Y");
                                                            var zProp = pointType.GetProperty("Z");
                                                            
                                                            if (xProp != null && yProp != null && zProp != null)
                                                            {
                                                                segObj["center3DX"] = (double)xProp.GetValue(center);
                                                                segObj["center3DY"] = (double)yProp.GetValue(center);
                                                                segObj["center3DZ"] = (double)zProp.GetValue(center);
                                                            }
                                                        }
                                                        
                                                        if (radius != null)
                                                        {
                                                            segObj["radius"] = (double)radius;
                                                        }
                                                    }
                                                }
                                                catch { }
                                            }
                                            
                                            segments.Add(segObj);
                                        }
                                    }
                                    catch (Exception ex)
                                    {
                                        System.Diagnostics.Debug.WriteLine($"Error extracting segment {i}: {ex.Message}");
                                    }
                                }
                            }
                        }
                    }
                    catch (Exception ex)
                    {
                        System.Diagnostics.Debug.WriteLine($"Error extracting segments: {ex.Message}");
                    }
                    
                    baselineObj["segments"] = segments;
                }
                // For arcs, get center and radius
                else if (curveTypeStr.Contains("Arc"))
                {
                    try
                    {
                        var getCenterMethod = baselineType.GetMethod("GetCenter");
                        var getRadiusMethod = baselineType.GetMethod("GetRadius");
                        if (getCenterMethod != null && getRadiusMethod != null)
                        {
                            var center = getCenterMethod.Invoke(baseline, null);
                            var radius = getRadiusMethod.Invoke(baseline, null);
                            
                            if (center != null)
                            {
                                var pointType = center.GetType();
                                var xProp = pointType.GetProperty("X");
                                var yProp = pointType.GetProperty("Y");
                                var zProp = pointType.GetProperty("Z");
                                
                                if (xProp != null && yProp != null && zProp != null)
                                {
                                    baselineObj["center"] = new { 
                                        x = (double)xProp.GetValue(center), 
                                        y = (double)yProp.GetValue(center), 
                                        z = (double)zProp.GetValue(center) 
                                    };
                                }
                            }
                            
                            if (radius != null)
                            {
                                baselineObj["radius"] = (double)radius;
                            }
                        }
                    }
                    catch { }
                }

                return baselineObj;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error extracting baseline from curve: {ex.Message}");
                return null;
            }
        }

        private object ExtractMeshData(Renga.IModelObject modelObject)
        {
            try
            {
                if (modelObject == null)
                    return null;

                var meshArray = new List<object>();
                
                // Try to get geometry using reflection with multiple approaches
                try
                {
                    var objType = modelObject.GetType();
                    
                    // Try GetGeometry method (case-insensitive)
                    var allMethods = objType.GetMethods(System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic);
                    var getGeometryMethod = Array.Find(allMethods, m => 
                        m.Name.Equals("GetGeometry", StringComparison.OrdinalIgnoreCase) && 
                        m.GetParameters().Length == 0);
                    
                    if (getGeometryMethod != null)
                    {
                        var geometry = getGeometryMethod.Invoke(modelObject, null);
                        System.Diagnostics.Debug.WriteLine($"GetGeometry result: {(geometry != null ? "not null" : "null")}");
                        
                        if (geometry != null)
                        {
                            var geometryType = geometry.GetType();
                            var geometryMethods = geometryType.GetMethods(System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic);
                            var getMeshMethod = Array.Find(geometryMethods, m => 
                                m.Name.Equals("GetMesh", StringComparison.OrdinalIgnoreCase) && 
                                m.GetParameters().Length == 0);
                            
                            if (getMeshMethod != null)
                            {
                                var mesh = getMeshMethod.Invoke(geometry, null);
                                System.Diagnostics.Debug.WriteLine($"GetMesh result: {(mesh != null ? "not null" : "null")}");
                                
                                if (mesh != null)
                                {
                                    var meshType = mesh.GetType();
                                    var grid = new Dictionary<string, object>();
                                    var vertices = new List<object>();
                                    var triangles = new List<object>();

                                    // Get vertices
                                    var meshMethods = meshType.GetMethods(System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic);
                                    var getVertexCountMethod = Array.Find(meshMethods, m => 
                                        m.Name.Equals("GetVertexCount", StringComparison.OrdinalIgnoreCase) && 
                                        m.GetParameters().Length == 0);
                                    var getVertexMethod = Array.Find(meshMethods, m => 
                                        m.Name.Equals("GetVertex", StringComparison.OrdinalIgnoreCase) && 
                                        m.GetParameters().Length == 1 && 
                                        m.GetParameters()[0].ParameterType == typeof(int));
                                        
                                    if (getVertexCountMethod != null && getVertexMethod != null)
                                    {
                                        int vertexCount = (int)getVertexCountMethod.Invoke(mesh, null);
                                        System.Diagnostics.Debug.WriteLine($"Vertex count: {vertexCount}");
                                        
                                        for (int i = 0; i < vertexCount; i++)
                                        {
                                            var vertex = getVertexMethod.Invoke(mesh, new object[] { i });
                                            if (vertex != null)
                                            {
                                                var vertexType = vertex.GetType();
                                                var xProp = vertexType.GetProperty("X");
                                                var yProp = vertexType.GetProperty("Y");
                                                var zProp = vertexType.GetProperty("Z");
                                                if (xProp != null && yProp != null && zProp != null)
                                                {
                                                    double x = (double)xProp.GetValue(vertex);
                                                    double y = (double)yProp.GetValue(vertex);
                                                    double z = (double)zProp.GetValue(vertex);
                                                    vertices.Add(new { x = x, y = y, z = z });
                                                }
                                            }
                                        }
                                    }

                                    // Get triangles
                                    var getTriangleCountMethod = Array.Find(meshMethods, m => 
                                        m.Name.Equals("GetTriangleCount", StringComparison.OrdinalIgnoreCase) && 
                                        m.GetParameters().Length == 0);
                                    var getTriangleMethod = Array.Find(meshMethods, m => 
                                        m.Name.Equals("GetTriangle", StringComparison.OrdinalIgnoreCase) && 
                                        m.GetParameters().Length == 1 && 
                                        m.GetParameters()[0].ParameterType == typeof(int));
                                        
                                    if (getTriangleCountMethod != null && getTriangleMethod != null)
                                    {
                                        int triangleCount = (int)getTriangleCountMethod.Invoke(mesh, null);
                                        System.Diagnostics.Debug.WriteLine($"Triangle count: {triangleCount}");
                                        
                                        for (int i = 0; i < triangleCount; i++)
                                        {
                                            var triangle = getTriangleMethod.Invoke(mesh, new object[] { i });
                                            if (triangle != null)
                                            {
                                                var triangleType = triangle.GetType();
                                                var v0Prop = triangleType.GetProperty("Vertex0");
                                                var v1Prop = triangleType.GetProperty("Vertex1");
                                                var v2Prop = triangleType.GetProperty("Vertex2");
                                                if (v0Prop != null && v1Prop != null && v2Prop != null)
                                                {
                                                    int v0 = (int)v0Prop.GetValue(triangle);
                                                    int v1 = (int)v1Prop.GetValue(triangle);
                                                    int v2 = (int)v2Prop.GetValue(triangle);
                                                    triangles.Add(new int[] { v0, v1, v2 });
                                                }
                                            }
                                        }
                                    }

                                    if (vertices.Count > 0)
                                    {
                                        grid["vertices"] = vertices;
                                        grid["triangles"] = triangles;
                                        meshArray.Add(new Dictionary<string, object> { ["grids"] = new object[] { grid } });
                                        System.Diagnostics.Debug.WriteLine($"Mesh extracted: {vertices.Count} vertices, {triangles.Count} triangles");
                                    }
                                }
                            }
                            else
                            {
                                System.Diagnostics.Debug.WriteLine($"GetMesh method not found in geometry. Available methods: {string.Join(", ", geometryMethods.Select(m => m.Name))}");
                            }
                        }
                    }
                    else
                    {
                        System.Diagnostics.Debug.WriteLine($"GetGeometry method not found. Available methods: {string.Join(", ", allMethods.Select(m => m.Name))}");
                    }
                }
                catch (Exception ex)
                {
                    System.Diagnostics.Debug.WriteLine($"Error extracting mesh: {ex.Message}\n{ex.StackTrace}");
                }

                return meshArray.Count > 0 ? meshArray : null;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error extracting mesh data: {ex.Message}\n{ex.StackTrace}");
                return null;
            }
        }
    }
}

