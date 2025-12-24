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

# Renga integration nodes for Sverchok
# Register all nodes when this module is loaded

# Import all node modules
try:
    from . import renga_connect
    from . import renga_create_columns
    from . import renga_get_walls
    
    # List of all node classes for Sverchok's auto-registration
    imported_modules = [
        renga_connect,
        renga_create_columns,
        renga_get_walls,
    ]
except ImportError as e:
    print(f"Renga nodes: Import error: {e}")
    imported_modules = []

def register():
    """Register all Renga nodes"""
    if not imported_modules:
        print("Renga nodes: No modules to register")
        return
    
    for module in imported_modules:
        if hasattr(module, 'register'):
            try:
                module.register()
                print(f"Renga nodes: Registered {module.__name__}")
            except Exception as e:
                print(f"Renga nodes: Error registering {module.__name__}: {e}")
                import traceback
                traceback.print_exc()

def unregister():
    """Unregister all Renga nodes"""
    if not imported_modules:
        return
    
    for module in imported_modules:
        if hasattr(module, 'unregister'):
            try:
                module.unregister()
            except Exception as e:
                print(f"Renga nodes: Error unregistering {module.__name__}: {e}")

