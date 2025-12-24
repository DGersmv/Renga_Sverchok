"""
Поиск всех нод Sverchok - может быть они называются по-другому
"""

import bpy

print("=" * 70)
print("ПОИСК ВСЕХ НОД SVERCHOK")
print("=" * 70)

# 1. Все ноды с 'Sv' в имени
print("\n1. ВСЕ НОДЫ С 'Sv' В ИМЕНИ:")
sv_nodes = [n for n in dir(bpy.types) if 'Sv' in n and 'Node' in n]
print(f"Найдено: {len(sv_nodes)}")
for node in sv_nodes[:20]:
    print(f"  - {node}")

# 2. Все ноды с 'Sverchok' в имени
print("\n2. ВСЕ НОДЫ С 'Sverchok' В ИМЕНИ:")
sverchok_nodes = [n for n in dir(bpy.types) if 'Sverchok' in n or 'Sverch' in n]
print(f"Найдено: {len(sverchok_nodes)}")
for node in sverchok_nodes:
    print(f"  - {node}")

# 3. Проверка через SverchCustomTreeNode
print("\n3. ПРОВЕРКА ЧЕРЕЗ SverchCustomTreeNode:")
try:
    from sverchok.node_tree import SverchCustomTreeNode
    print("✓ SverchCustomTreeNode импортирован")
    
    # Ищем все классы, которые наследуются от SverchCustomTreeNode
    all_sverchok_nodes = []
    for attr_name in dir(bpy.types):
        try:
            obj = getattr(bpy.types, attr_name)
            if (hasattr(obj, '__bases__') and 
                SverchCustomTreeNode in obj.__bases__):
                all_sverchok_nodes.append(attr_name)
        except:
            pass
    
    print(f"Найдено нод Sverchok (наследуются от SverchCustomTreeNode): {len(all_sverchok_nodes)}")
    print("Примеры (первые 20):")
    for node in all_sverchok_nodes[:20]:
        print(f"  - {node}")
    
    # Проверяем наши ноды
    print("\n4. НАШИ НОДЫ:")
    our_nodes = ['SvRengaConnectNode', 'SvRengaCreateColumnsNode', 'SvRengaGetWallsNode']
    for node_name in our_nodes:
        if node_name in all_sverchok_nodes:
            print(f"✓ {node_name} НАЙДЕН!")
            node_class = getattr(bpy.types, node_name)
            print(f"  bl_idname: {node_class.bl_idname}")
            print(f"  bl_label: {node_class.bl_label}")
        else:
            print(f"✗ {node_name} НЕ НАЙДЕН")
            
except Exception as e:
    print(f"✗ Ошибка: {e}")
    import traceback
    traceback.print_exc()

# 5. Проверка через tree.nodes
print("\n5. ПРОВЕРКА ЧЕРЕЗ ДЕРЕВО НОД:")
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
                        break
    
    if tree:
        print(f"✓ Дерево найдено: {tree.name}")
        print(f"  Тип: {type(tree)}")
        
        # Пробуем получить доступные типы нод
        if hasattr(tree, 'nodes'):
            print(f"✓ У дерева есть атрибут 'nodes'")
            # Пробуем создать простую ноду Sverchok для проверки
            try:
                # Ищем любую ноду Sverchok
                test_node = tree.nodes.new('SvTextInNode')  # Обычная нода Sverchok
                print(f"✓ Тестовая нода Sverchok создана: {test_node.bl_label}")
                tree.nodes.remove(test_node)
            except Exception as e:
                print(f"✗ Не удалось создать тестовую ноду Sverchok: {e}")
                
            # Пробуем создать нашу ноду
            try:
                node = tree.nodes.new('SvRengaConnectNode')
                print(f"✓✓✓ НАША НОДА СОЗДАНА! {node.bl_label}")
                print(f"  bl_idname: {node.bl_idname}")
            except Exception as e:
                print(f"✗ Не удалось создать нашу ноду: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"✗ У дерева нет атрибута 'nodes'")
    else:
        print("✗ Дерево не найдено")
        
except Exception as e:
    print(f"✗ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("ПОИСК ЗАВЕРШЕН")
print("=" * 70)

