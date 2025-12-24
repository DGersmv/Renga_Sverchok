"""
Прямая проверка и создание нод Renga
Запустите ПОСЛЕ полной загрузки Sverchok (подождите 10 секунд после открытия Blender)
"""

import bpy
import time

print("=" * 70)
print("ПРЯМАЯ ПРОВЕРКА НОД RENGA")
print("=" * 70)

# Ждем загрузки
print("\nОжидание загрузки Sverchok (10 секунд)...")
time.sleep(10)

# Проверка регистрации
print("\n1. ПРОВЕРКА РЕГИСТРАЦИИ:")
node_classes = {
    'SvRengaConnectNode': 'Renga Connect',
    'SvRengaCreateColumnsNode': 'Renga Create Columns',
    'SvRengaGetWallsNode': 'Renga Get Walls'
}

all_registered = True
for class_name, expected_label in node_classes.items():
    if hasattr(bpy.types, class_name):
        node_class = getattr(bpy.types, class_name)
        actual_label = node_class.bl_label
        print(f"✓ {class_name}")
        print(f"  bl_idname: {node_class.bl_idname}")
        print(f"  bl_label: {actual_label}")
        if actual_label != expected_label:
            print(f"  ⚠ bl_label не совпадает! Ожидалось: {expected_label}")
    else:
        print(f"✗ {class_name} НЕ ЗАРЕГИСТРИРОВАН!")
        all_registered = False

# Попытка создать ноду напрямую
print("\n2. ПОПЫТКА СОЗДАТЬ НОДУ НАПРЯМУЮ:")
try:
    # Ищем активное дерево Sverchok
    tree = None
    for area in bpy.context.screen.areas:
        if area.type == 'NODE_EDITOR':
            space = area.spaces.active
            if space and hasattr(space, 'tree_type'):
                if space.tree_type == 'SverchCustomTreeType':
                    tree = space.edit_tree
                    if tree:
                        print("✓ Дерево нод Sverchok найдено")
                        break
    
    if not tree:
        # Создаем новое дерево
        print("⚠ Дерево не найдено, создаем новое...")
        bpy.ops.node.new_node_tree(type='SverchCustomTreeType')
        for area in bpy.context.screen.areas:
            if area.type == 'NODE_EDITOR':
                space = area.spaces.active
                if space and hasattr(space, 'tree_type'):
                    if space.tree_type == 'SverchCustomTreeType':
                        tree = space.edit_tree
                        break
    
    if tree:
        print(f"✓ Дерево: {tree.name}")
        
        # Пробуем создать каждую ноду
        for class_name, label in node_classes.items():
            try:
                print(f"\nПопытка создать {class_name}...")
                node = tree.nodes.new(class_name)
                print(f"✓ УСПЕХ! Создана нода: {node.bl_label}")
                print(f"  bl_idname: {node.bl_idname}")
                print(f"  Позиция: {node.location}")
                # Не удаляем - оставляем для проверки
            except Exception as e:
                print(f"✗ ОШИБКА создания {class_name}: {e}")
                import traceback
                traceback.print_exc()
    else:
        print("✗ Не удалось найти или создать дерево Sverchok")
        
except Exception as e:
    print(f"✗ ОШИБКА: {e}")
    import traceback
    traceback.print_exc()

# Проверка через Sverchok API
print("\n3. ПРОВЕРКА ЧЕРЕЗ SVERCHOK API:")
try:
    from sverchok.node_tree import SverchCustomTreeNode
    
    all_sverchok_nodes = []
    for attr_name in dir(bpy.types):
        if attr_name.startswith('Sv') and attr_name.endswith('Node'):
            try:
                node_class = getattr(bpy.types, attr_name)
                if issubclass(node_class, SverchCustomTreeNode):
                    all_sverchok_nodes.append(attr_name)
            except:
                pass
    
    print(f"Всего нод Sverchok найдено: {len(all_sverchok_nodes)}")
    
    renga_found = []
    for class_name in node_classes.keys():
        if class_name in all_sverchok_nodes:
            renga_found.append(class_name)
            print(f"✓ {class_name} найден в Sverchok")
        else:
            print(f"✗ {class_name} НЕ найден в Sverchok")
    
    if len(renga_found) == len(node_classes):
        print("\n✓ ВСЕ НОДЫ RENGA НАЙДЕНЫ В SVERCHOK!")
    else:
        print(f"\n⚠ Найдено только {len(renga_found)} из {len(node_classes)}")
        
except Exception as e:
    print(f"⚠ Ошибка проверки через API: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
if all_registered:
    print("✓ НОДЫ ЗАРЕГИСТРИРОВАНЫ!")
    print("\nЕсли ноды созданы выше - они должны быть видны в дереве нод!")
    print("Проверьте дерево нод Sverchok - там должны быть ноды Renga")
else:
    print("✗ НОДЫ НЕ ЗАРЕГИСТРИРОВАНЫ")
print("=" * 70)

