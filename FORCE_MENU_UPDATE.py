"""
ПРИНУДИТЕЛЬНОЕ ОБНОВЛЕНИЕ МЕНЮ - Добавляем Renga между Network и Pulga Physics
"""

import bpy
import os
import re

print("=" * 70)
print("ПРИНУДИТЕЛЬНОЕ ОБНОВЛЕНИЕ МЕНЮ SVERCHOK")
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
    
    if not os.path.exists(menus_path):
        print(f"✗ Папка меню не найдена!")
        exit()
    
    print(f"✓ Папка меню: {menus_path}\n")
    
    # Правильная секция Renga
    renga_section = """- Renga:
    - icon_name: PLUGIN
    - extra_menu: ConnectionPartialMenu
    - SvRengaConnectNode
    - SvRengaCreateColumnsNode
    - SvRengaGetWallsNode
"""
    
    menu_files = ['full_by_data_type.yaml', 'full_by_operations.yaml']
    
    for menu_file in menu_files:
        file_path = os.path.join(menus_path, menu_file)
        
        if not os.path.exists(file_path):
            print(f"⚠ {menu_file} не найден")
            continue
        
        print(f"Обработка {menu_file}:")
        
        # Читаем файл
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            content = ''.join(lines)
        
        # Удаляем старую секцию Renga если есть
        new_lines = []
        skip_until_next_category = False
        for i, line in enumerate(lines):
            if re.match(r'^- Renga:', line):
                print("  ✓ Найдена старая секция Renga - удаляю")
                skip_until_next_category = True
                continue
            elif skip_until_next_category:
                if re.match(r'^- [A-Z]', line):  # Новая категория
                    skip_until_next_category = False
                    new_lines.append(line)
                elif not (line.startswith(' ') or line.strip() == ''):
                    skip_until_next_category = False
                    new_lines.append(line)
                # Пропускаем строки внутри секции Renga
                continue
            else:
                new_lines.append(line)
        
        lines = new_lines
        
        # Ищем место для вставки (между Network и Pulga Physics)
        insert_index = len(lines)
        network_found = False
        
        for i, line in enumerate(lines):
            if re.match(r'^- Network:', line):
                print("  ✓ Найдена категория Network")
                network_found = True
                # Находим конец секции Network
                j = i + 1
                while j < len(lines) and (lines[j].startswith(' ') or lines[j].strip() == ''):
                    j += 1
                insert_index = j
                print(f"  ✓ Место для вставки найдено после Network (строка {insert_index})")
                break
        
        if not network_found:
            # Если Network не найден, ищем Pulga Physics
            for i, line in enumerate(lines):
                if re.match(r'^- Pulga Physics:', line, re.IGNORECASE):
                    print("  ✓ Найдена категория Pulga Physics - вставляю перед ней")
                    insert_index = i
                    break
        
        # Вставляем секцию Renga
        lines.insert(insert_index, renga_section)
        print(f"  ✓ Секция Renga вставлена")
        
        # Сохраняем файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        # Проверяем результат
        with open(file_path, 'r', encoding='utf-8') as f:
            new_content = f.read()
        
        if 'Renga:' in new_content and 'SvRengaConnectNode' in new_content:
            print(f"  ✓✓✓ Категория Renga успешно добавлена в {menu_file}!")
        else:
            print(f"  ✗ Ошибка: категория не добавлена")
    
    # Удаляем кэш
    cache_path = os.path.join(menus_path, '__pycache__')
    if os.path.exists(cache_path):
        import shutil
        shutil.rmtree(cache_path)
        print(f"\n✓ Кэш меню удален")
    
    print("\n" + "=" * 70)
    print("МЕНЮ ОБНОВЛЕНО!")
    print("=" * 70)
    print("\nТеперь:")
    print("1. ПОЛНОСТЬЮ перезапустите Blender")
    print("2. Откройте Sverchok")
    print("3. Нажмите Add Node")
    print("4. Найдите категорию 'Renga' между 'Network' и 'Pulga Physics'")
    print("5. Там должны быть все 3 ноды!")
    print("=" * 70)
    
except Exception as e:
    print(f"✗ Ошибка: {e}")
    import traceback
    traceback.print_exc()

