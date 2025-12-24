"""
Проверка регистрации нод Renga в Blender
Запустите в Blender: Text Editor > Run Script
"""

import bpy

print("=" * 70)
print("ПРОВЕРКА РЕГИСТРАЦИИ НОД RENGA")
print("=" * 70)

# Проверка регистрации
node_classes = [
    'SvRengaConnectNode',
    'SvRengaCreateColumnsNode',
    'SvRengaGetWallsNode'
]

all_registered = True
for class_name in node_classes:
    is_registered = hasattr(bpy.types, class_name)
    status = "✓ ЗАРЕГИСТРИРОВАН" if is_registered else "✗ НЕ ЗАРЕГИСТРИРОВАН"
    print(f"{status}: {class_name}")
    
    if is_registered:
        # Получаем класс ноды
        node_class = getattr(bpy.types, class_name)
        print(f"  bl_idname: {node_class.bl_idname}")
        print(f"  bl_label: {node_class.bl_label}")
        if hasattr(node_class, 'bl_icon'):
            print(f"  bl_icon: {node_class.bl_icon}")
        if hasattr(node_class, 'sv_icon'):
            print(f"  sv_icon: {node_class.sv_icon}")
    
    if not is_registered:
        all_registered = False

print("\n" + "=" * 70)
print("ПРОВЕРКА МЕНЮ")
print("=" * 70)

# Проверка, есть ли ноды в меню Sverchok
try:
    import sverchok
    from sverchok.ui import nodeview_space_menu
    
    # Пробуем найти ноды в меню
    print("Проверка доступности нод в меню...")
    
    # Проверка через поиск в дереве нод
    if hasattr(bpy.context, 'space_data') and bpy.context.space_data:
        tree = bpy.context.space_data.edit_tree
        if tree and tree.bl_idname == 'SverchCustomTreeType':
            print("✓ Дерево нод Sverchok активно")
            
            # Пробуем создать ноду программно
            try:
                test_node = tree.nodes.new('SvRengaConnectNode')
                print("✓ Нода SvRengaConnectNode может быть создана программно!")
                tree.nodes.remove(test_node)
            except Exception as e:
                print(f"✗ Не удалось создать ноду программно: {e}")
        else:
            print("⚠ Дерево нод Sverchok не активно (откройте Sverchok)")
    else:
        print("⚠ Нет активного пространства (откройте Sverchok)")
        
except Exception as e:
    print(f"⚠ Ошибка проверки меню: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
if all_registered:
    print("✓ ВСЕ НОДЫ ЗАРЕГИСТРИРОВАНЫ!")
    print("\nЕсли ноды не видны в меню:")
    print("1. Удалите __pycache__ в папках nodes/renga/ и menus/")
    print("2. Полностью перезапустите Blender")
    print("3. Откройте Sverchok и нажмите Add Node")
    print("4. Или используйте поиск (Space) и введите 'Renga'")
else:
    print("✗ НЕКОТОРЫЕ НОДЫ НЕ ЗАРЕГИСТРИРОВАНЫ")
    print("Проверьте консоль Blender на ошибки при загрузке")
print("=" * 70)
