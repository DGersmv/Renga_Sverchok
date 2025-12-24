# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

"""
Renga Get Walls Node
Gets walls from Renga with baseline curves and mesh geometry
Similar to RengaGetWallsComponent in Grasshopper
"""

import bpy
from bpy.props import BoolProperty
from mathutils import Vector
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
import os
import sys
import uuid
from datetime import datetime

# Добавить путь к папке для импорта модулей
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

# Импорт модулей
try:
    import renga_client
except ImportError:
    try:
        import importlib.util
        client_file = os.path.join(_current_dir, "renga_client.py")
        if os.path.exists(client_file):
            spec = importlib.util.spec_from_file_location("renga_client", client_file)
            renga_client = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(renga_client)
        else:
            renga_client = None
    except:
        renga_client = None

# Встроенная функция create_get_walls_message (чтобы не зависеть от commands)
def create_get_walls_message():
    return {
        "id": str(uuid.uuid4()),
        "command": "get_walls",
        "data": {},
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }

# Try to import curve utilities (may not be available in all Sverchok versions)
try:
    from sverchok.utils.curve.primitives import SvLine
    from sverchok.utils.curve.splines import SvSplineCurve
    from sverchok.utils.curve.algorithms import concatenate_curves
    CURVE_UTILS_AVAILABLE = True
except ImportError:
    CURVE_UTILS_AVAILABLE = False
    print("Renga Get Walls: Curve utilities not available, baseline curves will be limited")


class SvRengaGetWallsNode(SverchCustomTreeNode, bpy.types.Node):
    """
    Renga Get Walls Node
    Gets walls from Renga
    """
    bl_idname = 'SvRengaGetWallsNode'
    bl_label = 'Renga Get Walls'
    bl_icon = 'MESH_CUBE'
    sv_category = "Renga"
    sv_icon = 'MESH_CUBE'
    
    update_trigger: BoolProperty(
        name='Update',
        description='Trigger update on False->True change',
        default=False,
        update=updateNode
    )
    
    _last_update_value = False
    
    def sv_init(self, context):
        """Initialize node inputs and outputs"""
        self.inputs.new('SvStringsSocket', 'RengaConnect')
        self.inputs.new('SvStringsSocket', 'Update').prop_name = 'update_trigger'
        
        self.outputs.new('SvStringsSocket', 'Success')
        self.outputs.new('SvStringsSocket', 'Message')
        self.outputs.new('SvCurveSocket', 'Baselines')
        self.outputs.new('SvVerticesSocket', 'Vertices')
        self.outputs.new('SvStringsSocket', 'Faces')
    
    def sv_draw_buttons(self, context, layout):
        """Draw node UI"""
        layout.prop(self, 'update_trigger', text='Update')
    
    def process(self):
        """Process node"""
        try:
            # Get inputs
            renga_connect_input = self.inputs['RengaConnect'].sv_get(default=[])
            update_input = self.inputs['Update'].sv_get(default=[[False]])
            
            # Check for False->True transition (trigger)
            update_value = update_input[0][0] if update_input and update_input[0] else False
            should_update = update_value and not self._last_update_value
            self._last_update_value = update_value
            
            # Get port from Renga Connect input (if connected) or use default
            port = 50100
            if renga_connect_input and renga_connect_input[0]:
                # Check if input is connected
                if self.inputs['RengaConnect'].links:
                    # Get connected node
                    connected_node = self.inputs['RengaConnect'].links[0].from_node
                    if hasattr(connected_node, 'port'):
                        port = connected_node.port
            
            # Create client with port from Connect node or default
            if renga_client is None:
                self.outputs['Success'].sv_set([[False]])
                self.outputs['Message'].sv_set([["Renga client module not available"]])
                self.outputs['Baselines'].sv_set([[]])
                self.outputs['Vertices'].sv_set([[]])
                self.outputs['Faces'].sv_set([[]])
                return
            
            client = renga_client.RengaConnectionClient(port=port)
            
            if not client.is_server_reachable():
                self.outputs['Success'].sv_set([[False]])
                self.outputs['Message'].sv_set([["Renga Connect is not connected. Connect to Renga first."]])
                self.outputs['Baselines'].sv_set([[]])
                self.outputs['Vertices'].sv_set([[]])
                self.outputs['Faces'].sv_set([[]])
                return
            
            # Only process if Update trigger occurred (False->True)
            if not should_update:
                self.outputs['Success'].sv_set([[False]])
                self.outputs['Message'].sv_set([["Set Update to True to get walls from Renga"]])
                self.outputs['Baselines'].sv_set([[]])
                self.outputs['Vertices'].sv_set([[]])
                self.outputs['Faces'].sv_set([[]])
                return
            
            # Prepare command
            message = create_get_walls_message()
            
            # Send command to server
            try:
                response = client.send(message)
            except Exception as e:
                self.outputs['Success'].sv_set([[False]])
                self.outputs['Message'].sv_set([[f"Error: {str(e)}"]])
                self.outputs['Baselines'].sv_set([[]])
                self.outputs['Vertices'].sv_set([[]])
                self.outputs['Faces'].sv_set([[]])
                return
            
            if not response or not response.get('success', False):
                error_msg = response.get('error', 'Failed to get walls from Renga or no response') if response else 'No response'
                self.outputs['Success'].sv_set([[False]])
                self.outputs['Message'].sv_set([[error_msg]])
                self.outputs['Baselines'].sv_set([[]])
                self.outputs['Vertices'].sv_set([[]])
                self.outputs['Faces'].sv_set([[]])
                return
            
            # Parse response
            try:
                walls = response.get('data', {}).get('walls', [])
                if not walls:
                    self.outputs['Success'].sv_set([[False]])
                    self.outputs['Message'].sv_set([["No walls found in response"]])
                    self.outputs['Baselines'].sv_set([[]])
                    self.outputs['Vertices'].sv_set([[]])
                    self.outputs['Faces'].sv_set([[]])
                    return
                
                baselines = []
                all_verts = []
                all_faces = []
                
                for wall in walls:
                    wall_id = wall.get('id', 0)
                    
                    # Process baseline
                    baseline_obj = wall.get('baseline')
                    if baseline_obj:
                        baseline_curve = self._parse_baseline(baseline_obj)
                        if baseline_curve:
                            baselines.append(baseline_curve)
                    
                    # Process mesh
                    mesh_array = wall.get('mesh', [])
                    if mesh_array:
                        for mesh_obj in mesh_array:
                            grids = mesh_obj.get('grids', [])
                            if grids:
                                for grid in grids:
                                    mesh_data = self._parse_mesh(grid)
                                    if mesh_data:
                                        verts, faces = mesh_data
                                        # Accumulate vertices and faces
                                        base_vert_idx = len(all_verts)
                                        all_verts.extend(verts)
                                        # Adjust face indices
                                        adjusted_faces = [[f[0] + base_vert_idx, f[1] + base_vert_idx, f[2] + base_vert_idx] for f in faces]
                                        all_faces.extend(adjusted_faces)
                
                self.outputs['Success'].sv_set([[True]])
                self.outputs['Message'].sv_set([[f"Found {len(walls)} walls"]])
                self.outputs['Baselines'].sv_set(baselines)
                self.outputs['Vertices'].sv_set([all_verts] if all_verts else [[]])
                self.outputs['Faces'].sv_set([all_faces] if all_faces else [[]])
            
            except Exception as e:
                self.outputs['Success'].sv_set([[False]])
                self.outputs['Message'].sv_set([[f"Error parsing response: {str(e)}"]])
                self.outputs['Baselines'].sv_set([[]])
                self.outputs['Vertices'].sv_set([[]])
                self.outputs['Faces'].sv_set([[]])
        except Exception as e:
            # Catch any unexpected errors to prevent Blender crash
            print(f"ERROR in SvRengaGetWallsNode.process(): {e}")
            import traceback
            traceback.print_exc()
            # Set safe defaults
            try:
                self.outputs['Success'].sv_set([[False]])
                self.outputs['Message'].sv_set([[f"Error: {str(e)}"]])
                self.outputs['Baselines'].sv_set([[]])
                self.outputs['Vertices'].sv_set([[]])
                self.outputs['Faces'].sv_set([[]])
            except:
                pass
    
    def _parse_baseline(self, baseline_obj):
        """
        Parse baseline curve from JSON object
        Returns Sverchok curve object (SvLine or SvSplineCurve) or list of points
        Similar to RengaGetWallsComponent.ParseBaseline in C#
        """
        try:
            baseline_type = baseline_obj.get('type', '')
            start_point_obj = baseline_obj.get('startPoint')
            end_point_obj = baseline_obj.get('endPoint')
            
            if not start_point_obj or not end_point_obj:
                return None
            
            # Use sampled points if available (especially for arcs)
            sampled_points = baseline_obj.get('sampledPoints', [])
            if sampled_points and len(sampled_points) >= 2:
                points = []
                for pt_obj in sampled_points:
                    x = pt_obj.get('x', 0)
                    y = pt_obj.get('y', 0)
                    z = pt_obj.get('z', 0)
                    points.append([x, y, z])
                
                if len(points) >= 2:
                    # Try to create Sverchok curve if utilities are available
                    if CURVE_UTILS_AVAILABLE:
                        try:
                            if len(points) == 2:
                                # Simple line for 2 points
                                return SvLine.from_two_points(points[0], points[1])
                            else:
                                # Spline curve for multiple points
                                return SvSplineCurve.from_points(points, is_cyclic=False)
                        except Exception as e:
                            print(f"Renga Get Walls: Error creating curve, using point list: {e}")
                            # Fallback to point list
                            return points
                    else:
                        # Return as list of points if curve utils not available
                        return points
            
            # Fallback: simple line (start and end points)
            start_x = start_point_obj.get('x', 0)
            start_y = start_point_obj.get('y', 0)
            start_z = start_point_obj.get('z', 0)
            end_x = end_point_obj.get('x', 0)
            end_y = end_point_obj.get('y', 0)
            end_z = end_point_obj.get('z', 0)
            
            start_pt = [start_x, start_y, start_z]
            end_pt = [end_x, end_y, end_z]
            
            # Try to create Sverchok curve if utilities are available
            if CURVE_UTILS_AVAILABLE:
                try:
                    return SvLine.from_two_points(start_pt, end_pt)
                except Exception as e:
                    print(f"Renga Get Walls: Error creating line, using point list: {e}")
                    # Fallback to point list
                    return [start_pt, end_pt]
            else:
                # Return as list of points if curve utils not available
                return [start_pt, end_pt]
        
        except Exception as e:
            print(f"Error parsing baseline: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def _parse_mesh(self, grid_obj):
        """
        Parse mesh from JSON object
        Returns tuple (vertices, faces) for Sverchok mesh
        Similar to RengaGetWallsComponent.ParseMesh in C#
        """
        try:
            vertices = grid_obj.get('vertices', [])
            triangles = grid_obj.get('triangles', [])
            
            if not vertices or not triangles:
                return None
            
            # Convert vertices to list of lists
            verts = []
            for v_obj in vertices:
                x = v_obj.get('x', 0)
                y = v_obj.get('y', 0)
                z = v_obj.get('z', 0)
                verts.append([x, y, z])
            
            # Convert triangles to list of indices
            faces = []
            for t_array in triangles:
                if len(t_array) >= 3:
                    i0 = t_array[0]
                    i1 = t_array[1]
                    i2 = t_array[2]
                    faces.append([i0, i1, i2])
            
            if len(verts) > 0 and len(faces) > 0:
                # Return tuple (vertices, faces) for Sverchok mesh
                return (verts, faces)
            
            return None
        
        except Exception as e:
            print(f"Error parsing mesh: {str(e)}")
            return None


def register():
    bpy.utils.register_class(SvRengaGetWallsNode)


def unregister():
    bpy.utils.unregister_class(SvRengaGetWallsNode)

