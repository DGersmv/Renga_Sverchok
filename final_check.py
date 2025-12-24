"""
Финальная проверка и исправление нод Renga
Запустите в Blender: Text Editor > Run Script
"""

import bpy
import os

print("=" * 70)
print("ФИНАЛЬНАЯ ПРОВЕРКА НОД RENGA")
print("=" * 70)

# Проверка регистрации
node_classes = {
    'SvRengaConnectNode': 'Renga Connect',
    'SvRengaCreateColumnsNode': 'Renga Create Columns',
    'SvRengaGetWallsNode': 'Renga Get Walls'
}

print("\n1. ПРОВЕРКА РЕГИСТРАЦИИ:")
all_ok = True
for class_name, expected_label in node_classes.items():
    if hasattr(bpy.types, class_name):
        node_class = getattr(bpy.types, class_name)
        actual_label = node_class.bl_label
        print(f"✓ {class_name}")
        print(f"  bl_idname: {node_class.bl_idname}")
        print(f"  bl_label: {actual_label}")
        if actual_label != expected_label:
            print(f"  ⚠ bl_label не совпадает! Ожидалось: {expected_label}")
            all_ok = False
    else:
        print(f"✗ {class_name} НЕ ЗАРЕГИСТРИРОВАН!")
        all_ok = False

print("\n2. ПРОВЕРКА ДОСТУПНОСТИ В ДЕРЕВЕ НОД:")
try:
    # Пробуем найти активное дерево Sverchok
    for area in bpy.context.screen.areas:
        if area.type == 'NODE_EDITOR':
            space = area.spaces.active
            if space and space.tree_type == 'SverchCustomTreeType':
                tree = space.edit_tree
                if tree:
                    print("✓ Дерево нод Sverchok активно")
                    
                    # Пробуем создать ноду
                    try:
                        test_node = tree.nodes.new('SvRengaConnectNode')
                        print("✓ Нода может быть создана программно!")
                        print(f"  Создана нода: {test_node.bl_label}")
                        tree.nodes.remove(test_node)
                    except Exception as e:
                        print(f"✗ Не удалось создать ноду: {e}")
                        all_ok = False
                    break
            else:
                print("⚠ Дерево нод Sverchok не активно")
                print("  Откройте Sverchok в редакторе нод")
except Exception as e:
    print(f"⚠ Ошибка проверки дерева: {e}")

print("\n3. ПРОВЕРКА ФАЙЛОВ:")
renga_path = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga"
required_files = [
    '__init__.py',
    'renga_connect.py',
    'renga_create_columns.py',
    'renga_get_walls.py'
]

if os.path.exists(renga_path):
    print(f"✓ Папка найдена: {renga_path}")
    for filename in required_files:
        filepath = os.path.join(renga_path, filename)
        if os.path.exists(filepath):
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} НЕ НАЙДЕН!")
            all_ok = False
else:
    print(f"✗ Папка не найдена: {renga_path}")
    all_ok = False

print("\n4. ПРОВЕРКА МЕНЮ:")
menus_path = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\menus"
menu_files = ['full_by_data_type.yaml', 'full_by_operations.yaml']

if os.path.exists(menus_path):
    print(f"✓ Папка меню найдена: {menus_path}")
    for menu_file in menu_files:
        filepath = os.path.join(menus_path, menu_file)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'Renga:' in content and 'SvRengaConnectNode' in content:
                    print(f"  ✓ {menu_file} - категория Renga найдена")
                else:
                    print(f"  ✗ {menu_file} - категория Renga НЕ найдена!")
                    all_ok = False
        else:
            print(f"  ✗ {menu_file} НЕ НАЙДЕН!")
            all_ok = False
else:
    print(f"✗ Папка меню не найдена: {menus_path}")
    all_ok = False

print("\n" + "=" * 70)
if all_ok:
    print("✓ ВСЁ ПРОВЕРЕНО - ДОЛЖНО РАБОТАТЬ!")
    print("\nЕсли ноды все еще не видны:")
    print("1. Удалите __pycache__ в папках nodes/renga/ и menus/")
    print("2. Полностью перезапустите Blender")
    print("3. Откройте Sverchok")
    print("4. Нажмите Add Node или Space для поиска")
    print("5. Введите 'Renga' в поиске")
else:
    print("✗ ОБНАРУЖЕНЫ ПРОБЛЕМЫ - см. выше")
print("=" * 70)
