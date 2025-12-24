"""
Проверка нод Renga ПОСЛЕ полной загрузки Sverchok
Запустите этот скрипт ПОСЛЕ того, как Sverchok полностью загрузился
(подождите несколько секунд после открытия Blender)
"""

import bpy
import time

print("=" * 70)
print("ПРОВЕРКА НОД RENGA ПОСЛЕ ЗАГРУЗКИ SVERCHOK")
print("=" * 70)

# Ждем немного, чтобы Sverchok успел загрузиться
print("\nОжидание загрузки Sverchok...")
time.sleep(2)

# Проверка регистрации
node_classes = [
    'SvRengaConnectNode',
    'SvRengaCreateColumnsNode',
    'SvRengaGetWallsNode'
]

print("\n1. ПРОВЕРКА РЕГИСТРАЦИИ:")
all_registered = True
for class_name in node_classes:
    if hasattr(bpy.types, class_name):
        node_class = getattr(bpy.types, class_name)
        print(f"✓ {class_name}")
        print(f"  bl_idname: {node_class.bl_idname}")
        print(f"  bl_label: {node_class.bl_label}")
        print(f"  bl_icon: {getattr(node_class, 'bl_icon', 'NONE')}")
    else:
        print(f"✗ {class_name} НЕ ЗАРЕГИСТРИРОВАН!")
        all_registered = False

# Проверка доступности в дереве нод
print("\n2. ПРОВЕРКА ДОСТУПНОСТИ В ДЕРЕВЕ НОД:")
try:
    # Ищем активное дерево Sverchok
    found_tree = False
    for area in bpy.context.screen.areas:
        if area.type == 'NODE_EDITOR':
            space = area.spaces.active
            if space and hasattr(space, 'tree_type'):
                if space.tree_type == 'SverchCustomTreeType':
                    tree = space.edit_tree
                    if tree:
                        found_tree = True
                        print("✓ Дерево нод Sverchok активно")
                        
                        # Пробуем создать ноду программно
                        try:
                            test_node = tree.nodes.new('SvRengaConnectNode')
                            print(f"✓ Нода может быть создана программно!")
                            print(f"  Создана нода: {test_node.bl_label}")
                            print(f"  bl_idname: {test_node.bl_idname}")
                            tree.nodes.remove(test_node)
                            print("✓ Нода успешно удалена")
                        except Exception as e:
                            print(f"✗ Не удалось создать ноду: {e}")
                            import traceback
                            traceback.print_exc()
                        break
    
    if not found_tree:
        print("⚠ Дерево нод Sverchok не активно")
        print("  Откройте Sverchok в редакторе нод")
        
except Exception as e:
    print(f"⚠ Ошибка проверки дерева: {e}")
    import traceback
    traceback.print_exc()

# Проверка через Sverchok API
print("\n3. ПРОВЕРКА ЧЕРЕЗ SVERCHOK API:")
try:
    import sverchok
    from sverchok.node_tree import SverchCustomTreeNode
    
    # Получаем все зарегистрированные ноды Sverchok
    all_sverchok_nodes = []
    for attr_name in dir(bpy.types):
        if attr_name.startswith('Sv') and attr_name.endswith('Node'):
            try:
                node_class = getattr(bpy.types, attr_name)
                if issubclass(node_class, SverchCustomTreeNode):
                    all_sverchok_nodes.append(attr_name)
            except:
                pass
    
    print(f"Найдено нод Sverchok: {len(all_sverchok_nodes)}")
    
    renga_nodes_found = []
    for class_name in node_classes:
        if class_name in all_sverchok_nodes:
            renga_nodes_found.append(class_name)
            print(f"✓ {class_name} найден в списке нод Sverchok")
        else:
            print(f"✗ {class_name} НЕ найден в списке нод Sverchok")
    
    if len(renga_nodes_found) == len(node_classes):
        print("\n✓ ВСЕ НОДЫ RENGA НАЙДЕНЫ В SVERCHOK!")
    else:
        print(f"\n⚠ Найдено только {len(renga_nodes_found)} из {len(node_classes)} нод")
        
except Exception as e:
    print(f"⚠ Ошибка проверки через Sverchok API: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
if all_registered:
    print("✓ НОДЫ ЗАРЕГИСТРИРОВАНЫ!")
    print("\nЕсли ноды не видны в меню:")
    print("1. Проверьте формат YAML файлов меню")
    print("2. Удалите __pycache__ в папках nodes/renga/ и menus/")
    print("3. Полностью перезапустите Blender")
    print("4. Откройте Sverchok и нажмите Add Node")
    print("5. Или используйте поиск (Space) и введите 'Renga Connect'")
else:
    print("✗ НОДЫ НЕ ЗАРЕГИСТРИРОВАНЫ")
    print("Проверьте консоль Blender на ошибки при загрузке")
print("=" * 70)

