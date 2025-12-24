# Скрипт для регистрации нод Renga в Blender
# Выполните этот код в консоли Python Blender (Text Editor > Run Script)

import bpy
import sys
import os

print("=" * 60)
print("РЕГИСТРАЦИЯ НОД RENGA")
print("=" * 60)

# Путь к папке renga
renga_path = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga"

if not os.path.exists(renga_path):
    print(f"✗ ОШИБКА: Папка не найдена: {renga_path}")
    print("Проверьте путь к Sverchok")
    sys.exit(1)

# Добавляем путь к nodes в sys.path если нужно
sverchok_nodes_path = os.path.dirname(renga_path)
if sverchok_nodes_path not in sys.path:
    sys.path.insert(0, sverchok_nodes_path)
    print(f"✓ Добавлен путь: {sverchok_nodes_path}")

# Импорт и регистрация нод
try:
    # Вариант 1: Прямой импорт из папки
    import importlib.util
    
    # Регистрация renga_connect
    connect_file = os.path.join(renga_path, "renga_connect.py")
    if os.path.exists(connect_file):
        spec = importlib.util.spec_from_file_location("renga_connect", connect_file)
        renga_connect = importlib.util.module_from_spec(spec)
        # Устанавливаем __package__ для относительных импортов
        renga_connect.__package__ = "nodes.renga"
        spec.loader.exec_module(renga_connect)
        
        if hasattr(renga_connect, 'register'):
            renga_connect.register()
            print("✓ renga_connect зарегистрирован")
        else:
            print("✗ renga_connect не имеет функции register()")
    
    # Регистрация renga_create_columns
    columns_file = os.path.join(renga_path, "renga_create_columns.py")
    if os.path.exists(columns_file):
        spec = importlib.util.spec_from_file_location("renga_create_columns", columns_file)
        renga_create_columns = importlib.util.module_from_spec(spec)
        renga_create_columns.__package__ = "nodes.renga"
        spec.loader.exec_module(renga_create_columns)
        
        if hasattr(renga_create_columns, 'register'):
            renga_create_columns.register()
            print("✓ renga_create_columns зарегистрирован")
    
    # Регистрация renga_get_walls
    walls_file = os.path.join(renga_path, "renga_get_walls.py")
    if os.path.exists(walls_file):
        spec = importlib.util.spec_from_file_location("renga_get_walls", walls_file)
        renga_get_walls = importlib.util.module_from_spec(spec)
        renga_get_walls.__package__ = "nodes.renga"
        spec.loader.exec_module(renga_get_walls)
        
        if hasattr(renga_get_walls, 'register'):
            renga_get_walls.register()
            print("✓ renga_get_walls зарегистрирован")
    
except Exception as e:
    print(f"✗ Ошибка при регистрации: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)
print("ПРОВЕРКА РЕГИСТРАЦИИ")
print("=" * 60)

# Проверка в bpy.types
nodes_to_check = [
    'SvRengaConnectNode',
    'SvRengaCreateColumnsNode',
    'SvRengaGetWallsNode'
]

all_registered = True
for node_name in nodes_to_check:
    is_registered = node_name in dir(bpy.types)
    status = "✓" if is_registered else "✗"
    print(f"{status} {node_name}: {'ЗАРЕГИСТРИРОВАН' if is_registered else 'НЕ ЗАРЕГИСТРИРОВАН'}")
    if not is_registered:
        all_registered = False

print()
if all_registered:
    print("=" * 60)
    print("✓ ВСЕ НОДЫ УСПЕШНО ЗАРЕГИСТРИРОВАНЫ!")
    print("=" * 60)
    print("Теперь проверьте меню Sverchok:")
    print("1. Откройте Sverchok")
    print("2. Нажмите Add Node (или Space)")
    print("3. Найдите категорию 'Renga'")
    print("4. Должны быть видны 3 ноды")
else:
    print("=" * 60)
    print("✗ НЕКОТОРЫЕ НОДЫ НЕ ЗАРЕГИСТРИРОВАНЫ")
    print("=" * 60)
    print("Проверьте консоль Blender на ошибки выше")


