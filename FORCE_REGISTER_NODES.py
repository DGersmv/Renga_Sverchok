"""
Принудительная регистрация нод Renga
Запустите ПОСЛЕ полной загрузки Sverchok
"""

import bpy
import sys
import importlib

print("=" * 70)
print("ПРИНУДИТЕЛЬНАЯ РЕГИСТРАЦИЯ НОД RENGA")
print("=" * 70)

# Путь к модулям нод
renga_path = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga"

# Добавляем путь в sys.path если нужно
if renga_path not in sys.path:
    sys.path.insert(0, renga_path)

print("\n1. ИМПОРТ МОДУЛЕЙ:")
try:
    # Импортируем модули напрямую
    import sverchok.nodes.renga.renga_connect as renga_connect
    import sverchok.nodes.renga.renga_create_columns as renga_create_columns
    import sverchok.nodes.renga.renga_get_walls as renga_get_walls
    
    print("✓ Модули импортированы")
    print(f"  renga_connect: {renga_connect}")
    print(f"  renga_create_columns: {renga_create_columns}")
    print(f"  renga_get_walls: {renga_get_walls}")
    
    # Проверяем наличие классов
    print("\n2. ПРОВЕРКА КЛАССОВ В МОДУЛЯХ:")
    if hasattr(renga_connect, 'SvRengaConnectNode'):
        print("✓ SvRengaConnectNode найден в renga_connect")
    else:
        print("✗ SvRengaConnectNode НЕ найден в renga_connect")
    
    if hasattr(renga_create_columns, 'SvRengaCreateColumnsNode'):
        print("✓ SvRengaCreateColumnsNode найден в renga_create_columns")
    else:
        print("✗ SvRengaCreateColumnsNode НЕ найден в renga_create_columns")
    
    if hasattr(renga_get_walls, 'SvRengaGetWallsNode'):
        print("✓ SvRengaGetWallsNode найден в renga_get_walls")
    else:
        print("✗ SvRengaGetWallsNode НЕ найден в renga_get_walls")
    
    # Проверяем наличие функций register
    print("\n3. ПРОВЕРКА ФУНКЦИЙ REGISTER:")
    if hasattr(renga_connect, 'register'):
        print("✓ register() найдена в renga_connect")
    else:
        print("✗ register() НЕ найдена в renga_connect")
    
    if hasattr(renga_create_columns, 'register'):
        print("✓ register() найдена в renga_create_columns")
    else:
        print("✗ register() НЕ найдена в renga_create_columns")
    
    if hasattr(renga_get_walls, 'register'):
        print("✓ register() найдена в renga_get_walls")
    else:
        print("✗ register() НЕ найдена в renga_get_walls")
    
    # Принудительно вызываем register
    print("\n4. ПРИНУДИТЕЛЬНАЯ РЕГИСТРАЦИЯ:")
    try:
        if hasattr(renga_connect, 'register'):
            renga_connect.register()
            print("✓ renga_connect.register() вызвана")
    except Exception as e:
        print(f"✗ Ошибка регистрации renga_connect: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        if hasattr(renga_create_columns, 'register'):
            renga_create_columns.register()
            print("✓ renga_create_columns.register() вызвана")
    except Exception as e:
        print(f"✗ Ошибка регистрации renga_create_columns: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        if hasattr(renga_get_walls, 'register'):
            renga_get_walls.register()
            print("✓ renga_get_walls.register() вызвана")
    except Exception as e:
        print(f"✗ Ошибка регистрации renga_get_walls: {e}")
        import traceback
        traceback.print_exc()
    
    # Проверяем регистрацию
    print("\n5. ПРОВЕРКА РЕГИСТРАЦИИ ПОСЛЕ ВЫЗОВА:")
    node_classes = [
        'SvRengaConnectNode',
        'SvRengaCreateColumnsNode',
        'SvRengaGetWallsNode'
    ]
    
    all_registered = True
    for class_name in node_classes:
        if hasattr(bpy.types, class_name):
            node_class = getattr(bpy.types, class_name)
            print(f"✓ {class_name} ЗАРЕГИСТРИРОВАН")
            print(f"  bl_idname: {node_class.bl_idname}")
            print(f"  bl_label: {node_class.bl_label}")
        else:
            print(f"✗ {class_name} НЕ ЗАРЕГИСТРИРОВАН!")
            all_registered = False
    
    # Пробуем создать ноду
    if all_registered:
        print("\n6. ПОПЫТКА СОЗДАТЬ НОДУ:")
        try:
            # Ищем дерево Sverchok
            tree = None
            for area in bpy.context.screen.areas:
                if area.type == 'NODE_EDITOR':
                    space = area.spaces.active
                    if space and hasattr(space, 'tree_type'):
                        if space.tree_type == 'SverchCustomTreeType':
                            tree = space.edit_tree
                            if tree:
                                break
            
            if not tree:
                # Создаем новое дерево
                bpy.ops.node.new_node_tree(type='SverchCustomTreeType')
                for area in bpy.context.screen.areas:
                    if area.type == 'NODE_EDITOR':
                        space = area.spaces.active
                        if space and hasattr(space, 'tree_type'):
                            if space.tree_type == 'SverchCustomTreeType':
                                tree = space.edit_tree
                                break
            
            if tree:
                node = tree.nodes.new('SvRengaConnectNode')
                print(f"✓ НОДА СОЗДАНА! {node.bl_label}")
                print(f"  bl_idname: {node.bl_idname}")
                print(f"  Позиция: {node.location}")
            else:
                print("✗ Не удалось найти или создать дерево Sverchok")
        except Exception as e:
            print(f"✗ Ошибка создания ноды: {e}")
            import traceback
            traceback.print_exc()
    
except ImportError as e:
    print(f"✗ ОШИБКА ИМПОРТА: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"✗ ОШИБКА: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("ПРОВЕРКА ЗАВЕРШЕНА")
print("=" * 70)

