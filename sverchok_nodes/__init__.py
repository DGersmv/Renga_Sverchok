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
Renga integration nodes for Sverchok
ЯВНАЯ РЕГИСТРАЦИЯ ДЛЯ ПОЯВЛЕНИЯ В МЕНЮ
"""

import bpy
import sys
import os

# Добавить путь к папке для импорта
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

# Создать фиктивные модули для относительных импортов
_nodes_path = os.path.dirname(_current_dir)
if "nodes" not in sys.modules:
    nodes_module = type(sys)('nodes')
    nodes_module.__path__ = [_nodes_path]
    sys.modules["nodes"] = nodes_module

if "nodes.renga" not in sys.modules:
    renga_module = type(sys)('nodes.renga')
    renga_module.__path__ = [_current_dir]
    sys.modules["nodes.renga"] = renga_module

# Импорт нод
try:
    from . import renga_connect
    from . import renga_create_columns
    from . import renga_get_walls
except ImportError as e:
    print(f"Renga nodes import error: {e}")
    # Попробовать прямой импорт
    try:
        import importlib.util
        for module_name in ['renga_connect', 'renga_create_columns', 'renga_get_walls']:
            module_file = os.path.join(_current_dir, f"{module_name}.py")
            if os.path.exists(module_file):
                spec = importlib.util.spec_from_file_location(module_name, module_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                sys.modules[f"nodes.renga.{module_name}"] = module
    except Exception as e2:
        print(f"Renga nodes direct import error: {e2}")

# Список классов нод для регистрации
_node_classes = []

def register():
    """Явная регистрация всех нод Renga"""
    global _node_classes
    
    # Очистить список
    _node_classes = []
    
    # Регистрация нод
    try:
        if hasattr(renga_connect, 'SvRengaConnectNode'):
            bpy.utils.register_class(renga_connect.SvRengaConnectNode)
            _node_classes.append(renga_connect.SvRengaConnectNode)
            print("✓ SvRengaConnectNode зарегистрирован")
    except Exception as e:
        print(f"✗ Ошибка регистрации SvRengaConnectNode: {e}")
    
    try:
        if hasattr(renga_create_columns, 'SvRengaCreateColumnsNode'):
            bpy.utils.register_class(renga_create_columns.SvRengaCreateColumnsNode)
            _node_classes.append(renga_create_columns.SvRengaCreateColumnsNode)
            print("✓ SvRengaCreateColumnsNode зарегистрирован")
    except Exception as e:
        print(f"✗ Ошибка регистрации SvRengaCreateColumnsNode: {e}")
    
    try:
        if hasattr(renga_get_walls, 'SvRengaGetWallsNode'):
            bpy.utils.register_class(renga_get_walls.SvRengaGetWallsNode)
            _node_classes.append(renga_get_walls.SvRengaGetWallsNode)
            print("✓ SvRengaGetWallsNode зарегистрирован")
    except Exception as e:
        print(f"✗ Ошибка регистрации SvRengaGetWallsNode: {e}")
    
    # Попытка добавить в меню Sverchok
    try:
        # Импорт Sverchok для добавления в меню
        import sverchok
        from sverchok.ui import nodeview_space_menu
        
        # Попытка добавить категорию в меню
        if hasattr(nodeview_space_menu, 'add_node_menu'):
            for node_class in _node_classes:
                if hasattr(node_class, 'sv_category'):
                    category = node_class.sv_category
                    nodeview_space_menu.add_node_menu(category, node_class)
                    print(f"✓ Нода {node_class.bl_label} добавлена в меню категории {category}")
    except Exception as e:
        print(f"⚠ Не удалось добавить в меню Sverchok (это нормально, Sverchok может сделать это автоматически): {e}")
    
    print(f"Renga nodes: Зарегистрировано {len(_node_classes)} нод")

def unregister():
    """Отмена регистрации всех нод Renga"""
    global _node_classes
    
    # Отмена регистрации в обратном порядке
    for node_class in reversed(_node_classes):
        try:
            bpy.utils.unregister_class(node_class)
        except Exception as e:
            print(f"⚠ Ошибка при отмене регистрации {node_class.__name__}: {e}")
    
    _node_classes = []
    print("Renga nodes: Все ноды отменены")

# Автоматическая регистрация при импорте (для Sverchok)
# Sverchok может вызвать register() сам, но мы также вызываем для надежности
if 'bpy' in sys.modules:
    try:
        register()
    except Exception as e:
        print(f"⚠ Автоматическая регистрация не удалась: {e}")
