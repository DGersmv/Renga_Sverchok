"""
Прямое создание ноды без проверки регистрации
"""

import bpy

print("=" * 70)
print("ПРЯМОЕ СОЗДАНИЕ НОДЫ БЕЗ ПРОВЕРКИ РЕГИСТРАЦИИ")
print("=" * 70)

# 1. Создаем дерево Sverchok
print("\n1. СОЗДАНИЕ ДЕРЕВА SVERCHOK:")
try:
    # Пробуем создать дерево
    bpy.ops.node.new_node_tree(type='SverchCustomTreeType')
    print("✓ Команда создания дерева выполнена")
    
    # Ждем немного
    import time
    time.sleep(1)
    
    # Ищем дерево
    tree = None
    for area in bpy.context.screen.areas:
        if area.type == 'NODE_EDITOR':
            space = area.spaces.active
            if space and hasattr(space, 'tree_type'):
                if space.tree_type == 'SverchCustomTreeType':
                    tree = space.edit_tree
                    if tree:
                        print(f"✓ Дерево найдено: {tree.name}")
                        print(f"  Тип: {type(tree)}")
                        break
    
    if not tree:
        print("✗ Дерево не найдено после создания")
        print("Попробуем найти существующее дерево...")
        
        # Ищем в blend файле
        for node_tree in bpy.data.node_groups:
            if node_tree.bl_idname == 'SverchCustomTreeType':
                print(f"✓ Найдено дерево в данных: {node_tree.name}")
                tree = node_tree
                break
    
    if tree:
        print(f"✓ Дерево готово: {tree.name}")
        
        # 2. Пробуем создать ноду напрямую
        print("\n2. СОЗДАНИЕ НОДЫ НАПРЯМУЮ:")
        
        if hasattr(tree, 'nodes'):
            print("✓ У дерева есть атрибут 'nodes'")
            
            # Пробуем создать нашу ноду
            try:
                node = tree.nodes.new('SvRengaConnectNode')
                print(f"✓✓✓ НОДА СОЗДАНА! {node.bl_label}")
                print(f"  bl_idname: {node.bl_idname}")
                print(f"  Тип: {type(node)}")
                print(f"  Позиция: {node.location}")
                
                # Проверяем, что нода работает
                print(f"  Входы: {[s.name for s in node.inputs]}")
                print(f"  Выходы: {[s.name for s in node.outputs]}")
                
            except Exception as e:
                print(f"✗ Ошибка создания ноды: {e}")
                import traceback
                traceback.print_exc()
                
                # Пробуем создать любую ноду Sverchok для проверки
                print("\n3. ПРОВЕРКА - СОЗДАНИЕ ЛЮБОЙ НОДЫ SVERCHOK:")
                try:
                    # Пробуем создать простую ноду
                    test_node = tree.nodes.new('SvTextInNode')
                    print(f"✓ Тестовая нода Sverchok создана: {test_node.bl_label}")
                    tree.nodes.remove(test_node)
                    print("✓ Тестовая нода удалена")
                except Exception as e2:
                    print(f"✗ Не удалось создать тестовую ноду: {e2}")
        else:
            print("✗ У дерева нет атрибута 'nodes'")
            print(f"  Доступные атрибуты: {[a for a in dir(tree) if not a.startswith('_')][:20]}")
    else:
        print("✗ Дерево не найдено")
        
except Exception as e:
    print(f"✗ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("ТЕСТ ЗАВЕРШЕН")
print("=" * 70)
print("\nВАЖНО: Если нода создалась - значит она зарегистрирована!")
print("Проблема может быть в том, как мы проверяем регистрацию.")
print("=" * 70)

