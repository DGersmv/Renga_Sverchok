"""
Скрипт для принудительного добавления нод Renga в меню Sverchok
Запустите этот скрипт в Blender (Text Editor > Run Script)
"""

import bpy
import sys
import os

# Путь к нодам (ИЗМЕНИТЕ ПОД СВОЙ ПУТЬ!)
renga_path = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga"
sverchok_path = os.path.dirname(os.path.dirname(renga_path))
nodes_path = os.path.dirname(renga_path)

# Добавить пути
for path in [sverchok_path, nodes_path]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Создать фиктивные модули
if "nodes" not in sys.modules:
    nodes_module = type(sys)('nodes')
    nodes_module.__path__ = [nodes_path]
    sys.modules["nodes"] = nodes_module

if "nodes.renga" not in sys.modules:
    renga_module = type(sys)('nodes.renga')
    renga_module.__path__ = [renga_path]
    sys.modules["nodes.renga"] = renga_module

# Импорт и регистрация нод
print("=" * 70)
print("ПРИНУДИТЕЛЬНАЯ РЕГИСТРАЦИЯ НОД RENGA В МЕНЮ SVERCHOK")
print("=" * 70)

nodes_info = [
    ("renga_connect.py", "SvRengaConnectNode", "nodes.renga.renga_connect"),
    ("renga_create_columns.py", "SvRengaCreateColumnsNode", "nodes.renga.renga_create_columns"),
    ("renga_get_walls.py", "SvRengaGetWallsNode", "nodes.renga.renga_get_walls")
]

registered_nodes = []

for filename, class_name, module_path in nodes_info:
    try:
        # Удалить модуль из кэша если есть
        if module_path in sys.modules:
            del sys.modules[module_path]
        
        # Импорт модуля
        module = __import__(module_path, fromlist=[class_name])
        node_class = getattr(module, class_name)
        
        # Отменить регистрацию если уже зарегистрирован
        if class_name in dir(bpy.types):
            try:
                bpy.utils.unregister_class(getattr(bpy.types, class_name))
            except:
                pass
        
        # Регистрация
        bpy.utils.register_class(node_class)
        registered_nodes.append(node_class)
        print(f"✓ {class_name} зарегистрирован")
        
    except Exception as e:
        print(f"✗ {class_name}: {e}")
        import traceback
        traceback.print_exc()

# Попытка добавить в меню Sverchok
print("\n" + "=" * 70)
print("ПОПЫТКА ДОБАВИТЬ В МЕНЮ SVERCHOK")
print("=" * 70)

try:
    # Импорт Sverchok
    import sverchok
    from sverchok.ui import nodeview_space_menu
    
    # Попытка обновить меню
    if hasattr(nodeview_space_menu, 'update_node_menu'):
        nodeview_space_menu.update_node_menu()
        print("✓ Меню Sverchok обновлено")
    
    # Попытка добавить категорию вручную
    try:
        from sverchok.core import register_node
        for node_class in registered_nodes:
            if hasattr(node_class, 'sv_category'):
                category = node_class.sv_category
                register_node(node_class, category)
                print(f"✓ {node_class.bl_label} добавлена в категорию {category}")
    except Exception as e:
        print(f"⚠ Не удалось добавить через register_node: {e}")
    
    # Попытка обновить категории
    try:
        from sverchok.node_tree import SverchCustomTreeNode
        # Обновить список категорий
        if hasattr(SverchCustomTreeNode, 'update_categories'):
            SverchCustomTreeNode.update_categories()
            print("✓ Категории обновлены")
    except Exception as e:
        print(f"⚠ Не удалось обновить категории: {e}")
        
except Exception as e:
    print(f"⚠ Не удалось добавить в меню Sverchok: {e}")
    import traceback
    traceback.print_exc()

# Проверка регистрации
print("\n" + "=" * 70)
print("ПРОВЕРКА РЕГИСТРАЦИИ")
print("=" * 70)

for filename, class_name, module_path in nodes_info:
    status = "✓" if class_name in dir(bpy.types) else "✗"
    print(f"{status} {class_name}: {'ЗАРЕГИСТРИРОВАН' if class_name in dir(bpy.types) else 'НЕ ЗАРЕГИСТРИРОВАН'}")

# Попытка найти ноды через поиск
print("\n" + "=" * 70)
print("ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ")
print("=" * 70)
print("1. Откройте Sverchok в Blender")
print("2. Нажмите Space (или кнопку поиска)")
print("3. Введите 'Renga' или 'SvRenga'")
print("4. Ноды должны появиться в результатах поиска")
print("\nЕсли ноды не видны в меню, но зарегистрированы - это известная")
print("проблема Sverchok v1.4.0 с Blender 5.0. Используйте поиск!")



