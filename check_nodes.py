# Скрипт для проверки регистрации нод Renga в Blender
# Выполните этот код в консоли Python Blender

import bpy

print("=" * 50)
print("ПРОВЕРКА РЕГИСТРАЦИИ НОД RENGA")
print("=" * 50)

# Проверка 1: Импорт классов
try:
    from nodes.renga.renga_connect import SvRengaConnectNode
    from nodes.renga.renga_create_columns import SvRengaCreateColumnsNode
    from nodes.renga.renga_get_walls import SvRengaGetWallsNode
    print("✓ Классы нод успешно импортированы")
    print(f"  - SvRengaConnectNode: {SvRengaConnectNode}")
    print(f"  - SvRengaCreateColumnsNode: {SvRengaCreateColumnsNode}")
    print(f"  - SvRengaGetWallsNode: {SvRengaGetWallsNode}")
except Exception as e:
    print(f"✗ Ошибка импорта: {e}")
    import traceback
    traceback.print_exc()

print()

# Проверка 2: Регистрация в bpy.types
nodes_to_check = [
    'SvRengaConnectNode',
    'SvRengaCreateColumnsNode', 
    'SvRengaGetWallsNode'
]

print("Проверка регистрации в bpy.types:")
for node_name in nodes_to_check:
    is_registered = node_name in dir(bpy.types)
    status = "✓" if is_registered else "✗"
    print(f"  {status} {node_name}: {'ЗАРЕГИСТРИРОВАН' if is_registered else 'НЕ ЗАРЕГИСТРИРОВАН'}")

print()

# Проверка 3: Попытка явной регистрации
print("Попытка явной регистрации:")
try:
    from nodes.renga import renga_connect, renga_create_columns, renga_get_walls
    
    if hasattr(renga_connect, 'register'):
        renga_connect.register()
        print("  ✓ renga_connect.register() вызван")
    
    if hasattr(renga_create_columns, 'register'):
        renga_create_columns.register()
        print("  ✓ renga_create_columns.register() вызван")
    
    if hasattr(renga_get_walls, 'register'):
        renga_get_walls.register()
        print("  ✓ renga_get_walls.register() вызван")
    
    # Проверка после регистрации
    print()
    print("Проверка после явной регистрации:")
    for node_name in nodes_to_check:
        is_registered = node_name in dir(bpy.types)
        status = "✓" if is_registered else "✗"
        print(f"  {status} {node_name}: {'ЗАРЕГИСТРИРОВАН' if is_registered else 'НЕ ЗАРЕГИСТРИРОВАН'}")
        
except Exception as e:
    print(f"  ✗ Ошибка при регистрации: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 50)


