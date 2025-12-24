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
Renga Connect Node - ПЕРЕПИСАННАЯ ВЕРСИЯ БЕЗ ОТНОСИТЕЛЬНЫХ ИМПОРТОВ
"""

import bpy
from bpy.props import IntProperty, BoolProperty
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
import os
import sys

# Добавить путь к папке renga для импорта модулей
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

# Импорт модулей (теперь они в той же папке)
try:
    import renga_client
except ImportError:
    # Fallback: попробовать импорт как модуль
    try:
        import importlib.util
        client_file = os.path.join(_current_dir, "renga_client.py")
        if os.path.exists(client_file):
            spec = importlib.util.spec_from_file_location("renga_client", client_file)
            renga_client = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(renga_client)
        else:
            raise ImportError("renga_client.py not found")
    except Exception as e:
        print(f"Renga Connect: Failed to import renga_client: {e}")
        renga_client = None


class SvRengaConnectNode(SverchCustomTreeNode, bpy.types.Node):
    """
    Renga Connect Node
    Connects to Renga TCP server and provides client object for other nodes
    """
    bl_idname = 'SvRengaConnectNode'
    bl_label = 'Renga Connect'
    bl_icon = 'NETWORK_DRIVE'
    sv_category = "Renga"
    sv_icon = 'NETWORK_DRIVE'
    
    port: IntProperty(
        name='Port',
        description='TCP server port number (default: 50100)',
        default=50100,
        min=1024,
        max=65535,
        update=updateNode
    )
    
    connect: BoolProperty(
        name='Connect',
        description='Enable/disable connection',
        default=False,
        update=updateNode
    )
    
    def sv_init(self, context):
        """Initialize node inputs and outputs"""
        self.inputs.new('SvStringsSocket', 'Port').prop_name = 'port'
        self.inputs.new('SvStringsSocket', 'Connect').prop_name = 'connect'
        
        self.outputs.new('SvStringsSocket', 'Connected')
        self.outputs.new('SvStringsSocket', 'Message')
        self.outputs.new('SvStringsSocket', 'Client')
    
    def sv_draw_buttons(self, context, layout):
        """Draw node UI"""
        layout.prop(self, 'port', text='Port')
        layout.prop(self, 'connect', text='Connect')
    
    def process(self):
        """Process node"""
        try:
            # Get inputs with safe defaults
            try:
                port_input = self.inputs['Port'].sv_get(default=[[self.port]])
            except:
                port_input = [[self.port]]
            
            try:
                connect_input = self.inputs['Connect'].sv_get(default=[[self.connect]])
            except:
                connect_input = [[self.connect]]
            
            # Use first value from input
            try:
                port = port_input[0][0] if port_input and port_input[0] and len(port_input[0]) > 0 else self.port
            except (IndexError, TypeError):
                port = self.port
            
            try:
                connect = connect_input[0][0] if connect_input and connect_input[0] and len(connect_input[0]) > 0 else self.connect
            except (IndexError, TypeError):
                connect = self.connect
            
            # Ensure port is a number
            try:
                port = int(float(port))
            except (ValueError, TypeError):
                port = self.port
            
            # Validate port
            if port < 1024 or port > 65535:
                self.outputs['Connected'].sv_set([[False]])
                self.outputs['Message'].sv_set([["Invalid port number. Port must be in range 1024-65535."]])
                self.outputs['Client'].sv_set([[]])
                return
            
            # Create or update client
            if renga_client is None:
                self.outputs['Connected'].sv_set([[False]])
                self.outputs['Message'].sv_set([["Renga client module not available"]])
                self.outputs['Client'].sv_set([[]])
                return
            
            if not hasattr(self, '_client') or not hasattr(self._client, 'port') or self._client.port != port:
                self._client = renga_client.RengaConnectionClient(
                    host="127.0.0.1",
                    port=port,
                    timeout=2.0
                )
            
            # Check connection status
            if connect:
                try:
                    is_reachable = self._client.is_server_reachable()
                    if is_reachable:
                        self.outputs['Connected'].sv_set([[True]])
                        self.outputs['Message'].sv_set([[f"Server reachable on port {port}"]])
                        self.outputs['Client'].sv_set([[port]])
                    else:
                        self.outputs['Connected'].sv_set([[False]])
                        self.outputs['Message'].sv_set([[f"Server not reachable on port {port}. Make sure Renga plugin is running and server is started."]])
                        self.outputs['Client'].sv_set([[]])
                except Exception as e:
                    self.outputs['Connected'].sv_set([[False]])
                    self.outputs['Message'].sv_set([[f"Connection check error: {str(e)}"]])
                    self.outputs['Client'].sv_set([[]])
            else:
                self.outputs['Connected'].sv_set([[False]])
                self.outputs['Message'].sv_set([["Not connected"]])
                self.outputs['Client'].sv_set([[]])
        except Exception as e:
            print(f"ERROR in SvRengaConnectNode.process(): {e}")
            import traceback
            traceback.print_exc()
            try:
                self.outputs['Connected'].sv_set([[False]])
                self.outputs['Message'].sv_set([[f"Error: {str(e)}"]])
                self.outputs['Client'].sv_set([[]])
            except:
                pass
    
    def get_client(self):
        """Get Renga client object for other nodes"""
        if hasattr(self, '_client'):
            return self._client
        return None


def register():
    bpy.utils.register_class(SvRengaConnectNode)


def unregister():
    bpy.utils.unregister_class(SvRengaConnectNode)

