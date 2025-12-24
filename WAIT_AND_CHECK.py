"""
Проверка после полной загрузки Sverchok
Запустите в Blender и подождите
"""

import bpy
import time

print("=" * 70)
print("ПРОВЕРКА ПОСЛЕ ПОЛНОЙ ЗАГРУЗКИ SVERCHOK")
print("=" * 70)

print("\nОжидание полной загрузки Sverchok (15 секунд)...")
for i in range(15, 0, -1):
    print(f"  {i}...", end='\r')
    time.sleep(1)
print("\n")

# Проверка всех нод
print("1. ВСЕ НОДЫ В bpy.types:")
all_nodes = []
for attr_name in dir(bpy.types):
    if 'Node' in attr_name:
        all_nodes.append(attr_name)

print(f"Найдено нод (с 'Node' в имени): {len(all_nodes)}")
print("Примеры (первые 20):")
for node in all_nodes[:20]:
    print(f"  - {node}")

# Проверка нод Sverchok
print("\n2. НОДЫ SVERCHOK:")
sverchok_nodes = [n for n in all_nodes if n.startswith('Sv')]
print(f"Найдено нод Sverchok (начинаются с 'Sv'): {len(sverchok_nodes)}")
print("Примеры (первые 10):")
for node in sverchok_nodes[:10]:
    print(f"  - {node}")

# Проверка наших нод
print("\n3. НАШИ НОДЫ:")
our_nodes = ['SvRengaConnectNode', 'SvRengaCreateColumnsNode', 'SvRengaGetWallsNode']
for node_name in our_nodes:
    if node_name in all_nodes:
        print(f"✓ {node_name} НАЙДЕН!")
        try:
            node_class = getattr(bpy.types, node_name)
            print(f"  bl_idname: {node_class.bl_idname}")
            print(f"  bl_label: {node_class.bl_label}")
        except:
            print(f"  ⚠ Не удалось получить класс")
    else:
        print(f"✗ {node_name} НЕ НАЙДЕН")

# Проверка через hasattr
print("\n4. ПРОВЕРКА ЧЕРЕЗ hasattr:")
for node_name in our_nodes:
    if hasattr(bpy.types, node_name):
        print(f"✓ {node_name} найден через hasattr")
        node_class = getattr(bpy.types, node_name)
        print(f"  bl_idname: {node_class.bl_idname}")
    else:
        print(f"✗ {node_name} НЕ найден через hasattr")

# Попытка создать ноду
print("\n5. ПОПЫТКА СОЗДАТЬ НОДУ:")
try:
    # Ищем дерево
    tree = None
    for area in bpy.context.screen.areas:
        if area.type == 'NODE_EDITOR':
            space = area.spaces.active
            if space and hasattr(space, 'tree_type'):
                if space.tree_type == 'SverchCustomTreeType':
                    tree = space.edit_tree
                    if tree:
                        print("✓ Дерево Sverchok найдено")
                        break
    
    if not tree:
        print("⚠ Дерево не найдено, создаем...")
        try:
            bpy.ops.node.new_node_tree(type='SverchCustomTreeType')
            time.sleep(1)
            for area in bpy.context.screen.areas:
                if area.type == 'NODE_EDITOR':
                    space = area.spaces.active
                    if space and hasattr(space, 'tree_type'):
                        if space.tree_type == 'SverchCustomTreeType':
                            tree = space.edit_tree
                            if tree:
                                print("✓ Дерево создано")
                                break
        except Exception as e:
            print(f"✗ Ошибка создания дерева: {e}")
    
    if tree:
        print(f"✓ Дерево: {tree.name}")
        print(f"  Тип: {type(tree)}")
        
        # Пробуем создать ноду
        if hasattr(tree, 'nodes'):
            try:
                node = tree.nodes.new('SvRengaConnectNode')
                print(f"✓✓✓ НОДА СОЗДАНА! {node.bl_label}")
                print(f"  bl_idname: {node.bl_idname}")
                print(f"  Позиция: {node.location}")
            except Exception as e:
                print(f"✗ Ошибка создания ноды: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"✗ У дерева нет атрибута 'nodes'")
            print(f"  Доступные атрибуты: {[a for a in dir(tree) if not a.startswith('_')][:10]}")
    else:
        print("✗ Дерево не найдено")
        
except Exception as e:
    print(f"✗ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("ПРОВЕРКА ЗАВЕРШЕНА")
print("=" * 70)

