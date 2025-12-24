"""
ПОЛНОЕ ИСПРАВЛЕНИЕ МЕНЮ - Проверяет и исправляет ВСЁ
"""

import bpy
import os
import re

print("=" * 80)
print("ПОЛНОЕ ИСПРАВЛЕНИЕ МЕНЮ RENGA")
print("=" * 80)

try:
    blender_version = '.'.join(bpy.app.version_string.split('.')[:2])
    addon_path = os.path.join(
        os.path.expanduser("~"),
        "AppData", "Roaming", "Blender Foundation", "Blender",
        blender_version, "scripts", "addons", "sverchok-master"
    )
    
    if not os.path.exists(addon_path):
        for ver in ["5.0", "5", "4.0", "4"]:
            alt_path = os.path.join(
                os.path.expanduser("~"),
                "AppData", "Roaming", "Blender Foundation", "Blender",
                ver, "scripts", "addons", "sverchok-master"
            )
            if os.path.exists(alt_path):
                addon_path = alt_path
                break
    
    if not os.path.exists(addon_path):
        print(f"✗ Папка Sverchok не найдена!")
        exit()
    
    print(f"✓ Папка Sverchok: {addon_path}\n")
    
    # 1. Проверяем наличие папки renga
    renga_path = os.path.join(addon_path, "nodes", "renga")
    print("1. ПРОВЕРКА ПАПКИ RENGA:")
    if os.path.exists(renga_path):
        print(f"   ✓ Папка renga найдена: {renga_path}")
        files = os.listdir(renga_path)
        print(f"   ✓ Файлов в папке: {len(files)}")
        for f in files:
            if f.endswith('.py'):
                print(f"     - {f}")
    else:
        print(f"   ✗ Папка renga НЕ найдена!")
        print(f"   Путь: {renga_path}")
        exit()
    
    # 2. Проверяем наличие нод
    print("\n2. ПРОВЕРКА НОД:")
    node_files = ['renga_connect.py', 'renga_create_columns.py', 'renga_get_walls.py']
    for node_file in node_files:
        node_path = os.path.join(renga_path, node_file)
        if os.path.exists(node_path):
            print(f"   ✓ {node_file} найден")
        else:
            print(f"   ✗ {node_file} НЕ найден!")
    
    # 3. Проверяем регистрацию нод
    print("\n3. ПРОВЕРКА РЕГИСТРАЦИИ НОД:")
    node_classes = ['SvRengaConnectNode', 'SvRengaCreateColumnsNode', 'SvRengaGetWallsNode']
    for node_class in node_classes:
        if hasattr(bpy.types, node_class):
            print(f"   ✓ {node_class} зарегистрирован")
        else:
            print(f"   ✗ {node_class} НЕ зарегистрирован!")
    
    # 4. Проверяем и исправляем меню
    print("\n4. ПРОВЕРКА И ИСПРАВЛЕНИЕ МЕНЮ:")
    menus_path = os.path.join(addon_path, "menus")
    menu_files = ['full_by_data_type.yaml', 'full_by_operations.yaml', 'index.yaml']
    
    renga_section = """- Renga:
    - icon_name: PLUGIN
    - extra_menu: ConnectionPartialMenu
    - SvRengaConnectNode
    - SvRengaCreateColumnsNode
    - SvRengaGetWallsNode
"""
    
    for menu_file in menu_files:
        file_path = os.path.join(menus_path, menu_file)
        
        if not os.path.exists(file_path):
            print(f"   ⚠ {menu_file} не найден - пропускаем")
            continue
        
        print(f"\n   Обработка {menu_file}:")
        
        # Читаем файл
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = f.readlines() if hasattr(f, 'readlines') else content.split('\n')
        
        # Перечитываем правильно
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Проверяем наличие категории Renga
        has_renga = 'Renga:' in content and 'SvRengaConnectNode' in content
        
        if has_renga:
            print(f"     ✓ Категория Renga уже есть")
            
            # Проверяем правильность позиции (между Network и Pulga Physics)
            network_idx = -1
            renga_idx = -1
            pulga_idx = -1
            
            for i, line in enumerate(lines):
                if re.match(r'^- Network:', line):
                    network_idx = i
                elif re.match(r'^- Renga:', line):
                    renga_idx = i
                elif re.match(r'^- Pulga Physics:', line, re.IGNORECASE):
                    pulga_idx = i
            
            if network_idx >= 0 and renga_idx >= 0 and pulga_idx >= 0:
                if network_idx < renga_idx < pulga_idx:
                    print(f"     ✓ Позиция правильная (Network < Renga < Pulga Physics)")
                else:
                    print(f"     ⚠ Позиция неправильная! Network={network_idx}, Renga={renga_idx}, Pulga={pulga_idx}")
                    print(f"     → Исправляем позицию...")
                    
                    # Удаляем старую секцию
                    new_lines = []
                    skip_until_next = False
                    for i, line in enumerate(lines):
                        if re.match(r'^- Renga:', line):
                            skip_until_next = True
                            continue
                        elif skip_until_next:
                            if re.match(r'^- [A-Z]', line) or (not line.startswith(' ') and line.strip()):
                                skip_until_next = False
                                new_lines.append(line)
                            continue
                        else:
                            new_lines.append(line)
                    
                    lines = new_lines
                    
                    # Вставляем после Network
                    for i, line in enumerate(lines):
                        if re.match(r'^- Network:', line):
                            j = i + 1
                            while j < len(lines) and (lines[j].startswith(' ') or lines[j].strip() == ''):
                                j += 1
                            lines.insert(j, renga_section)
                            print(f"     ✓ Секция Renga вставлена после Network")
                            break
            else:
                print(f"     ⚠ Не удалось найти позиции категорий")
        else:
            print(f"     ✗ Категория Renga НЕ найдена - добавляем...")
            
            # Ищем место для вставки (после Network)
            insert_idx = len(lines)
            for i, line in enumerate(lines):
                if re.match(r'^- Network:', line):
                    j = i + 1
                    while j < len(lines) and (lines[j].startswith(' ') or lines[j].strip() == ''):
                        j += 1
                    insert_idx = j
                    break
            
            if insert_idx < len(lines):
                lines.insert(insert_idx, renga_section)
                print(f"     ✓ Секция Renga добавлена после Network (строка {insert_idx})")
            else:
                # Если Network не найден, ищем Pulga Physics
                for i, line in enumerate(lines):
                    if re.match(r'^- Pulga Physics:', line, re.IGNORECASE):
                        lines.insert(i, renga_section)
                        print(f"     ✓ Секция Renga добавлена перед Pulga Physics")
                        break
        
        # Сохраняем файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        # Проверяем результат
        with open(file_path, 'r', encoding='utf-8') as f:
            new_content = f.read()
        
        if 'Renga:' in new_content and 'SvRengaConnectNode' in new_content:
            print(f"     ✓✓✓ {menu_file} обновлен успешно!")
        else:
            print(f"     ✗ Ошибка при обновлении {menu_file}")
    
    # 5. Удаляем кэш
    print("\n5. ОЧИСТКА КЭША:")
    cache_paths = [
        os.path.join(menus_path, '__pycache__'),
        os.path.join(addon_path, 'nodes', 'renga', '__pycache__'),
        os.path.join(addon_path, '__pycache__'),
    ]
    
    import shutil
    for cache_path in cache_paths:
        if os.path.exists(cache_path):
            try:
                shutil.rmtree(cache_path)
                print(f"   ✓ Удален кэш: {cache_path}")
            except:
                print(f"   ⚠ Не удалось удалить: {cache_path}")
    
    print("\n" + "=" * 80)
    print("ГОТОВО!")
    print("=" * 80)
    print("\nВАЖНО:")
    print("1. ПОЛНОСТЬЮ перезапустите Blender (закройте и откройте заново)")
    print("2. Откройте Sverchok")
    print("3. Нажмите Add Node или Space")
    print("4. Найдите категорию 'Renga' между 'Network' и 'Pulga Physics'")
    print("5. Там должны быть все 3 ноды!")
    print("=" * 80)
    
except Exception as e:
    print(f"\n✗ ОШИБКА: {e}")
    import traceback
    traceback.print_exc()

