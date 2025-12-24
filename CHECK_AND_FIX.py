"""
Проверка и исправление установки нод Renga
Запустите в Blender ПОСЛЕ полной загрузки Sverchok
"""

import bpy
import os
import re

print("=" * 70)
print("ПРОВЕРКА И ИСПРАВЛЕНИЕ НОД RENGA")
print("=" * 70)

# 1. Проверка регистрации нод
print("\n1. ПРОВЕРКА РЕГИСТРАЦИИ НОД:")
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

# 2. Принудительная регистрация если нужно
if not all_registered:
    print("\n2. ПРИНУДИТЕЛЬНАЯ РЕГИСТРАЦИЯ:")
    try:
        import sverchok.nodes.renga.renga_connect as renga_connect
        import sverchok.nodes.renga.renga_create_columns as renga_create_columns
        import sverchok.nodes.renga.renga_get_walls as renga_get_walls
        
        if hasattr(renga_connect, 'register'):
            renga_connect.register()
            print("✓ renga_connect.register() вызвана")
        if hasattr(renga_create_columns, 'register'):
            renga_create_columns.register()
            print("✓ renga_create_columns.register() вызвана")
        if hasattr(renga_get_walls, 'register'):
            renga_get_walls.register()
            print("✓ renga_get_walls.register() вызвана")
        
        # Проверяем снова
        print("\n3. ПРОВЕРКА ПОСЛЕ РЕГИСТРАЦИИ:")
        for class_name in node_classes:
            if hasattr(bpy.types, class_name):
                print(f"✓ {class_name} теперь зарегистрирован")
            else:
                print(f"✗ {class_name} всё ещё не зарегистрирован")
                
    except Exception as e:
        print(f"✗ Ошибка принудительной регистрации: {e}")
        import traceback
        traceback.print_exc()

# 3. Проверка и добавление в меню
print("\n4. ПРОВЕРКА МЕНЮ:")
try:
    blender_version_full = bpy.app.version_string
    blender_version = '.'.join(blender_version_full.split('.')[:2])
    
    menus_path = os.path.join(
        os.path.expanduser("~"),
        "AppData", "Roaming", "Blender Foundation", "Blender",
        blender_version, "scripts", "addons", "sverchok-master", "menus"
    )
    
    if not os.path.exists(menus_path):
        for ver in ["5.0", "5", "4.0", "4"]:
            alt_path = os.path.join(
                os.path.expanduser("~"),
                "AppData", "Roaming", "Blender Foundation", "Blender",
                ver, "scripts", "addons", "sverchok-master", "menus"
            )
            if os.path.exists(alt_path):
                menus_path = alt_path
                break
    
    if os.path.exists(menus_path):
        print(f"✓ Папка меню найдена: {menus_path}")
        
        menu_files = ['full_by_data_type.yaml', 'full_by_operations.yaml']
        renga_category_text = """- Renga:
    - icon_name: PLUGIN
    - extra_menu: ConnectionPartialMenu
    - SvRengaConnectNode
    - SvRengaCreateColumnsNode
    - SvRengaGetWallsNode
"""
        
        for menu_file in menu_files:
            file_path = os.path.join(menus_path, menu_file)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'Renga:' in content and 'SvRengaConnectNode' in content:
                    print(f"✓ Категория Renga уже есть в {menu_file}")
                else:
                    print(f"✗ Категория Renga НЕ найдена в {menu_file}")
                    print(f"  Добавляю...")
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    insert_index = len(lines)
                    for i, line in enumerate(lines):
                        if re.match(r'^- (Text|Transform|Vector):', line, re.IGNORECASE):
                            insert_index = i
                            break
                        elif re.match(r'^- Network:', line, re.IGNORECASE):
                            j = i + 1
                            while j < len(lines) and (lines[j].startswith(' ') or lines[j].strip() == ''):
                                j += 1
                            insert_index = j
                            break
                    
                    lines.insert(insert_index, renga_category_text)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(lines)
                    
                    print(f"✓ Категория добавлена в {menu_file}")
            else:
                print(f"⚠ Файл {menu_file} не найден")
    else:
        print(f"✗ Папка меню не найдена")
        
except Exception as e:
    print(f"✗ Ошибка проверки меню: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("ПРОВЕРКА ЗАВЕРШЕНА")
print("=" * 70)
print("\nТеперь:")
print("1. Полностью перезапустите Blender")
print("2. Откройте Sverchok")
print("3. Нажмите Add Node или Space")
print("4. Найдите категорию 'Renga'")
print("=" * 70)

