"""
Добавление категории Renga в index.yaml (главное меню)
"""

import bpy
import os
import re

print("=" * 70)
print("ДОБАВЛЕНИЕ КАТЕГОРИИ RENGA В INDEX.YAML")
print("=" * 70)

try:
    blender_version = '.'.join(bpy.app.version_string.split('.')[:2])
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
    
    index_file = os.path.join(menus_path, 'index.yaml')
    
    if os.path.exists(index_file):
        print(f"✓ Файл index.yaml найден")
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'Renga:' in content:
            print("✓ Категория Renga уже есть в index.yaml")
        else:
            print("✗ Категория Renga НЕ найдена в index.yaml")
            print("  Добавляю...")
            
            # Читаем построчно
            with open(index_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Ищем место для вставки (после Network)
            insert_index = len(lines)
            for i, line in enumerate(lines):
                if re.match(r'^- Network:', line):
                    # Находим конец секции Network
                    j = i + 1
                    while j < len(lines) and (lines[j].startswith(' ') or lines[j].strip() == ''):
                        j += 1
                    insert_index = j
                    break
            
            # Создаем секцию Renga
            renga_section = """- Renga:
    - icon_name: PLUGIN
    - extra_menu: ConnectionPartialMenu
    - SvRengaConnectNode
    - SvRengaCreateColumnsNode
    - SvRengaGetWallsNode
"""
            
            # Вставляем
            lines.insert(insert_index, renga_section)
            
            # Сохраняем
            with open(index_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            print("✓ Категория Renga добавлена в index.yaml")
    else:
        print(f"✗ Файл index.yaml не найден: {index_file}")
        
except Exception as e:
    print(f"✗ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("ГОТОВО!")
print("=" * 70)
print("\nТеперь:")
print("1. Запустите FORCE_MENU_RELOAD.py для перезагрузки меню")
print("2. Или перезапустите Blender")
print("3. Откройте Sverchok → Add Node → категория 'Renga'")
print("=" * 70)

