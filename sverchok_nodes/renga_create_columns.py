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
Renga Create Columns Node
Creates columns in Renga from Sverchok points
Similar to RengaCreateColumnsComponent in Grasshopper
"""

import bpy
from bpy.props import BoolProperty
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from . import commands


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
            
            # Check for False->True transition (trigger)
            update_value = update_input[0][0] if update_input and update_input[0] else False
            should_update = update_value and not self._last_update_value
            self._last_update_value = update_value
            
            # Validate inputs
            if not points_input or len(points_input) == 0:
                self.outputs['Success'].sv_set([[]])
                self.outputs['Message'].sv_set([["No points provided"]])
                self.outputs['ColumnGuids'].sv_set([[]])
                return
            
            # Flatten points list (Sverchok uses nested lists)
            points = []
            for point_list in points_input:
                points.extend(point_list)
            
            if len(points) == 0:
                self.outputs['Success'].sv_set([[]])
                self.outputs['Message'].sv_set([["No points provided"]])
                self.outputs['ColumnGuids'].sv_set([[]])
                return
            
            # Get port from Renga Connect input (if connected) or use default
            port = 50100
            if renga_connect_input and renga_connect_input[0]:
                # Try to get port from connected node
                # Check if input is connected
                if self.inputs['RengaConnect'].links:
                    # Get connected node
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
            
            # Only process if Update trigger occurred (False->True)
            if not should_update:
                self.outputs['Success'].sv_set([[]])
                self.outputs['Message'].sv_set([["Set Update to True to send points to Renga"]])
                self.outputs['ColumnGuids'].sv_set([[]])
                return
            
            # Create client with port from Connect node or default
            from . import renga_client
            client = renga_client.RengaConnectionClient(port=port)
            
            if not client or not client.is_server_reachable():
                self.outputs['Success'].sv_set([[]])
                self.outputs['Message'].sv_set([["Renga Connect is not connected. Connect to Renga first."]])
                self.outputs['ColumnGuids'].sv_set([[]])
                return
            
            # Prepare command
            message = commands.create_update_points_message(points, heights)
            
            # Send command to server
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
                error_msg = response.get('error', 'Failed to send data to Renga or no response') if response else 'No response'
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
                                    commands.update_mapping(point_guid, column_id)
                    else:
                        # Response format doesn't match
                        for _ in points:
                            successes.append(False)
                            messages.append("Invalid response format from Renga")
                            column_guids.append("")
                except Exception as e:
                    # Error parsing response
                    for _ in points:
                        successes.append(False)
                        messages.append(f"Error parsing response: {str(e)}")
                        column_guids.append("")
            
            self.outputs['Success'].sv_set([successes])
            self.outputs['Message'].sv_set([messages])
            self.outputs['ColumnGuids'].sv_set([column_guids])
        except Exception as e:
            # Catch any unexpected errors to prevent Blender crash
            print(f"ERROR in SvRengaCreateColumnsNode.process(): {e}")
            import traceback
            traceback.print_exc()
            # Set safe defaults
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

