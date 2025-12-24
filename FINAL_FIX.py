"""
ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ - Принудительная регистрация нод Renga
Запустите в Blender ПОСЛЕ полной загрузки Sverchok
"""

import bpy
import importlib
import sys

print("=" * 70)
print("ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ РЕГИСТРАЦИИ НОД RENGA")
print("=" * 70)

# 1. Сначала отменяем регистрацию если есть
print("\n1. ОТМЕНА СТАРОЙ РЕГИСТРАЦИИ:")
node_classes = ['SvRengaConnectNode', 'SvRengaCreateColumnsNode', 'SvRengaGetWallsNode']

for class_name in node_classes:
    if hasattr(bpy.types, class_name):
        try:
            node_class = getattr(bpy.types, class_name)
            bpy.utils.unregister_class(node_class)
            print(f"✓ Отменена регистрация {class_name}")
        except:
            pass

# 2. Перезагружаем модули
print("\n2. ПЕРЕЗАГРУЗКА МОДУЛЕЙ:")
try:
    # Удаляем модули из кэша
    modules_to_reload = [
        'sverchok.nodes.renga',
        'sverchok.nodes.renga.renga_connect',
        'sverchok.nodes.renga.renga_create_columns',
        'sverchok.nodes.renga.renga_get_walls',
    ]
    
    for module_name in modules_to_reload:
        if module_name in sys.modules:
            del sys.modules[module_name]
            print(f"✓ Удален из кэша: {module_name}")
    
    # Импортируем заново
    import sverchok.nodes.renga.renga_connect as renga_connect
    import sverchok.nodes.renga.renga_create_columns as renga_create_columns
    import sverchok.nodes.renga.renga_get_walls as renga_get_walls
    
    print("✓ Модули импортированы заново")
    
except Exception as e:
    print(f"✗ Ошибка перезагрузки: {e}")
    import traceback
    traceback.print_exc()

# 3. Регистрируем ноды
print("\n3. РЕГИСТРАЦИЯ НОД:")
try:
    if hasattr(renga_connect, 'register'):
        renga_connect.register()
        print("✓ renga_connect зарегистрирован")
    
    if hasattr(renga_create_columns, 'register'):
        renga_create_columns.register()
        print("✓ renga_create_columns зарегистрирован")
    
    if hasattr(renga_get_walls, 'register'):
        renga_get_walls.register()
        print("✓ renga_get_walls зарегистрирован")
        
except Exception as e:
    print(f"✗ Ошибка регистрации: {e}")
    import traceback
    traceback.print_exc()

# 4. Проверка
print("\n4. ФИНАЛЬНАЯ ПРОВЕРКА:")
all_ok = True
for class_name in node_classes:
    if hasattr(bpy.types, class_name):
        node_class = getattr(bpy.types, class_name)
        print(f"✓ {class_name} ЗАРЕГИСТРИРОВАН")
        print(f"  bl_idname: {node_class.bl_idname}")
        print(f"  bl_label: {node_class.bl_label}")
    else:
        print(f"✗ {class_name} НЕ ЗАРЕГИСТРИРОВАН!")
        all_ok = False

# 5. Попытка создать ноду
if all_ok:
    print("\n5. ПОПЫТКА СОЗДАТЬ НОДУ:")
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
        else:
            print("✗ Не удалось найти или создать дерево Sverchok")
    except Exception as e:
        print(f"✗ Ошибка создания ноды: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 70)
if all_ok:
    print("✓ ВСЕ НОДЫ ЗАРЕГИСТРИРОВАНЫ!")
    print("Проверьте меню Sverchok - категория 'Renga' должна быть там")
else:
    print("✗ НЕКОТОРЫЕ НОДЫ НЕ ЗАРЕГИСТРИРОВАНЫ")
    print("Проверьте консоль Blender на ошибки")
print("=" * 70)

