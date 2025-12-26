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
Renga Create Columns Node - ПЕРЕПИСАННАЯ ВЕРСИЯ БЕЗ ОТНОСИТЕЛЬНЫХ ИМПОРТОВ
"""

import bpy
from bpy.props import BoolProperty
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
import os
import sys
import json
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

# Встроенные функции commands (чтобы не зависеть от импорта)
_point_guid_map = {}
_point_to_guid_map = {}
_guid_counter = 0

def _get_point_guid(point, tolerance=0.001):
    global _point_to_guid_map, _guid_counter
    for existing_point, guid in _point_to_guid_map.items():
        if (abs(existing_point[0] - point[0]) < tolerance and
            abs(existing_point[1] - point[1]) < tolerance and
            abs(existing_point[2] - point[2]) < tolerance):
            return guid
    new_guid = f"SV_Point_{_guid_counter}_{uuid.uuid4().hex[:8]}"
    _point_to_guid_map[tuple(point)] = new_guid
    _guid_counter += 1
    return new_guid

def create_update_points_message(points, heights=None):
    global _point_guid_map
    if heights is None:
        heights = [3000.0]
    if len(heights) < len(points):
        last_height = heights[-1] if heights else 3000.0
        heights.extend([last_height] * (len(points) - len(heights)))
    
    point_data = []
    for i, point in enumerate(points):
        if isinstance(point, tuple):
            point = list(point)
        x, y, z = point[0], point[1], point[2]
        height = heights[i] if i < len(heights) else heights[-1]
        if height <= 0:
            height = 3000.0
        
        point_guid = _get_point_guid(point)
        renga_column_guid = _point_guid_map.get(point_guid)
        
        point_obj = {
            "x": float(x),
            "y": float(y),
            "z": float(z),
            "height": float(height),
            "grasshopperGuid": point_guid,
            "rengaColumnGuid": renga_column_guid if renga_column_guid else None
        }
        point_data.append(point_obj)
    
    return {
        "id": str(uuid.uuid4()),
        "command": "update_points",
        "data": {"points": point_data},
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }

def update_mapping(point_guid, column_id):
    global _point_guid_map
    if column_id:
        _point_guid_map[point_guid] = str(column_id)


class SvRengaCreateColumnsNode(SverchCustomTreeNode, bpy.types.Node):
    """
    Renga Create Columns Node
    Creates columns in Renga from points
    """
    bl_idname = 'SvRengaCreateColumnsNode'
    bl_label = 'Renga Create Columns'
    bl_icon = 'MESH_CYLINDER'
    sv_category = "Renga"
    
    update_trigger: BoolProperty(
        name='Update',
        description='Trigger update on False->True change',
        default=False,
        update=updateNode
    )
    
    _last_update_value = False
    
    def sv_init(self, context):
        """Initialize node inputs and outputs"""
        self.inputs.new('SvVerticesSocket', 'Points')
        self.inputs.new('SvStringsSocket', 'RengaConnect')
        self.inputs.new('SvStringsSocket', 'Height').prop_name = 'height'
        self.inputs.new('SvStringsSocket', 'Update').prop_name = 'update_trigger'
        
        self.outputs.new('SvStringsSocket', 'Success')
        self.outputs.new('SvStringsSocket', 'Message')
        self.outputs.new('SvStringsSocket', 'ColumnGuids')
    
    def sv_draw_buttons(self, context, layout):
        """Draw node UI"""
        layout.prop(self, 'update_trigger', text='Update')
    
    def process(self):
        """Process node"""
        try:
            # Get inputs
            points_input = self.inputs['Points'].sv_get(default=[])
            renga_connect_input = self.inputs['RengaConnect'].sv_get(default=[])
            height_input = self.inputs['Height'].sv_get(default=[[3000.0]])
            update_input = self.inputs['Update'].sv_get(default=[[False]])
            
            # Check for False->True transition
            update_value = update_input[0][0] if update_input and update_input[0] else False
            should_update = update_value and not self._last_update_value
            self._last_update_value = update_value
            
            # Validate inputs
            if not points_input or len(points_input) == 0:
                self.outputs['Success'].sv_set([[]])
                self.outputs['Message'].sv_set([["No points provided"]])
                self.outputs['ColumnGuids'].sv_set([[]])
                return
            
            # Flatten points
            points = []
            for point_list in points_input:
                points.extend(point_list)
            
            if len(points) == 0:
                self.outputs['Success'].sv_set([[]])
                self.outputs['Message'].sv_set([["No points provided"]])
                self.outputs['ColumnGuids'].sv_set([[]])
                return
            
            # Get port
            port = 50100
            if renga_connect_input and renga_connect_input[0]:
                if self.inputs['RengaConnect'].links:
                    connected_node = self.inputs['RengaConnect'].links[0].from_node
                    if hasattr(connected_node, 'port'):
                        port = connected_node.port
            
            # Get heights
            heights = []
            if height_input and height_input[0]:
                heights = height_input[0]
            
            # Normalize heights
            if len(heights) < len(points):
                last_height = heights[-1] if heights else 3000.0
                heights.extend([last_height] * (len(points) - len(heights)))
            
            # Validate heights
            for i in range(len(heights)):
                if heights[i] <= 0:
                    heights[i] = 3000.0
            
            # Only process if Update trigger occurred
            if not should_update:
                self.outputs['Success'].sv_set([[]])
                self.outputs['Message'].sv_set([["Set Update to True to send points to Renga"]])
                self.outputs['ColumnGuids'].sv_set([[]])
                return
            
            # Create client
            if renga_client is None:
                self.outputs['Success'].sv_set([[]])
                self.outputs['Message'].sv_set([["Renga client module not available"]])
                self.outputs['ColumnGuids'].sv_set([[]])
                return
            
            client = renga_client.RengaConnectionClient(port=port)
            
            if not client.is_server_reachable():
                self.outputs['Success'].sv_set([[]])
                self.outputs['Message'].sv_set([["Renga Connect is not connected. Connect to Renga first."]])
                self.outputs['ColumnGuids'].sv_set([[]])
                return
            
            # Prepare command
            message = create_update_points_message(points, heights)
            
            # Send command
            try:
                response = client.send(message)
            except Exception as e:
                self.outputs['Success'].sv_set([[False] * len(points)])
                self.outputs['Message'].sv_set([[f"Error: {str(e)}"] * len(points)])
                self.outputs['ColumnGuids'].sv_set([[""] * len(points)])
                return
            
            # Parse response
            successes = []
            messages = []
            column_guids = []
            
            if not response or not response.get('success', False):
                error_msg = response.get('error', 'Failed to send data to Renga') if response else 'No response'
                for _ in points:
                    successes.append(False)
                    messages.append(error_msg)
                    column_guids.append("")
            else:
                try:
                    results = response.get('data', {}).get('results', [])
                    
                    if results and len(results) == len(points):
                        for result in results:
                            success = result.get('success', False)
                            result_message = result.get('message', 'Unknown')
                            column_id = result.get('columnId', '')
                            
                            successes.append(success)
                            messages.append(result_message)
                            column_guids.append(str(column_id) if column_id else "")
                            
                            # Update mapping
                            if success and column_id:
                                point_guid = result.get('grasshopperGuid')
                                if point_guid:
                                    update_mapping(point_guid, column_id)
                    else:
                        for _ in points:
                            successes.append(False)
                            messages.append("Invalid response format from Renga")
                            column_guids.append("")
                except Exception as e:
                    for _ in points:
                        successes.append(False)
                        messages.append(f"Error parsing response: {str(e)}")
                        column_guids.append("")
            
            self.outputs['Success'].sv_set([successes])
            self.outputs['Message'].sv_set([messages])
            self.outputs['ColumnGuids'].sv_set([column_guids])
        except Exception as e:
            print(f"ERROR in SvRengaCreateColumnsNode.process(): {e}")
            import traceback
            traceback.print_exc()
            try:
                self.outputs['Success'].sv_set([[]])
                self.outputs['Message'].sv_set([[f"Error: {str(e)}"]])
                self.outputs['ColumnGuids'].sv_set([[]])
            except:
                pass


def register():
    bpy.utils.register_class(SvRengaCreateColumnsNode)


def unregister():
    bpy.utils.unregister_class(SvRengaCreateColumnsNode)

