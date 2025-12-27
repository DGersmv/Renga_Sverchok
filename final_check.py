# ФИНАЛЬНАЯ ПРОВЕРКА С ПРАВИЛЬНОЙ РЕГИСТРАЦИЕЙ
# Выполните в Text Editor Blender

import bpy
import sys
import os
import importlib.util

print("\n" + "="*70)
print("ФИНАЛЬНАЯ ПРОВЕРКА И РЕГИСТРАЦИЯ")
print("="*70)

# Пути
renga_path = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga"
sverchok_path = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master"
nodes_path = os.path.join(sverchok_path, "nodes")

# Добавить пути
for path in [sverchok_path, nodes_path]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Создать фиктивные модули для относительных импортов
if "nodes" not in sys.modules:
    nodes_module = type(sys)('nodes')
    nodes_module.__path__ = [nodes_path]
    sys.modules["nodes"] = nodes_module

if "nodes.renga" not in sys.modules:
    renga_module = type(sys)('nodes.renga')
    renga_module.__path__ = [renga_path]
    sys.modules["nodes.renga"] = renga_module

# Регистрация нод
nodes_info = [
    ("renga_connect.py", "SvRengaConnectNode", "nodes.renga.renga_connect"),
    ("renga_create_columns.py", "SvRengaCreateColumnsNode", "nodes.renga.renga_create_columns"),
    ("renga_get_walls.py", "SvRengaGetWallsNode", "nodes.renga.renga_get_walls")
]

print("\nРегистрация:")
print("-" * 70)

for filename, class_name, module_path in nodes_info:
    try:
        # Удалить из кэша если есть
        if module_path in sys.modules:
            del sys.modules[module_path]
        
        # Импортировать
        module = __import__(module_path, fromlist=[class_name])
        
        # Получить класс
        node_class = getattr(module, class_name)
        
        # Проверить, зарегистрирован ли
        if class_name in dir(bpy.types):
            print(f"✓ {class_name}: уже зарегистрирован, перерегистрируем...")
            try:
                bpy.utils.unregister_class(getattr(bpy.types, class_name))
            except:
                pass
        
        # Зарегистрировать
        bpy.utils.register_class(node_class)
        print(f"✓ {class_name}: ЗАРЕГИСТРИРОВАН")
        
    except Exception as e:
        print(f"✗ {class_name}: ошибка - {e}")
        import traceback
        traceback.print_exc()

# Проверка СРАЗУ после регистрации
print("\n" + "="*70)
print("ПРОВЕРКА ПОСЛЕ РЕГИСТРАЦИИ:")
print("="*70)

# Проверка через dir(bpy.types)
for filename, class_name, module_path in nodes_info:
    is_in_dir = class_name in dir(bpy.types)
    print(f"  dir(bpy.types): {class_name} = {is_in_dir}")

# Проверка через hasattr
print("\nПроверка через hasattr:")
for filename, class_name, module_path in nodes_info:
    has_attr = hasattr(bpy.types, class_name)
    print(f"  hasattr(bpy.types, '{class_name}') = {has_attr}")
    if has_attr:
        node_type = getattr(bpy.types, class_name)
        print(f"    Тип: {type(node_type)}")
        print(f"    bl_idname: {getattr(node_type, 'bl_idname', 'N/A')}")

# Проверка через bpy.types напрямую
print("\nПроверка через bpy.types напрямую:")
try:
    print(f"  bpy.types.SvRengaConnectNode: {hasattr(bpy.types, 'SvRengaConnectNode')}")
    if hasattr(bpy.types, 'SvRengaConnectNode'):
        print(f"    Значение: {bpy.types.SvRengaConnectNode}")
except Exception as e:
    print(f"  Ошибка: {e}")

# Попытка создать ноду программно
print("\n" + "="*70)
print("ПОПЫТКА СОЗДАТЬ НОДУ ПРОГРАММНО:")
print("="*70)

try:
    # Получить активное дерево нод Sverchok
    if hasattr(bpy.context, 'space_data') and bpy.context.space_data:
        tree = bpy.context.space_data.node_tree
        if tree and tree.type == 'SverchCustomTreeType':
            print("✓ Найдено дерево нод Sverchok")
            try:
                # Попробовать добавить ноду
                node = tree.nodes.new('SvRengaConnectNode')
                print(f"✓ Нода создана: {node.name}")
                print(f"  bl_idname: {node.bl_idname}")
                print(f"  Тип: {type(node)}")
            except Exception as e:
                print(f"✗ Не удалось создать ноду: {e}")
        else:
            print("✗ Активное дерево нод не найдено или не Sverchok")
            print("  Откройте Sverchok и выберите дерево нод")
    else:
        print("✗ Нет активного пространства")
except Exception as e:
    print(f"✗ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("РЕКОМЕНДАЦИИ:")
print("="*70)
print("1. Если hasattr(bpy.types, 'SvRengaConnectNode') = True:")
print("   - Ноды зарегистрированы правильно")
print("   - Проблема в меню Sverchok")
print("   - Попробуйте поиск в Sverchok (Space -> 'Renga')")
print("2. Если False:")
print("   - Проблема с регистрацией")
print("   - Проверьте ошибки выше")
print("="*70 + "\n")



