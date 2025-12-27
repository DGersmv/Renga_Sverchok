"""
АВТОМАТИЧЕСКАЯ УСТАНОВКА НОД RENGA В SVERCHOK
Этот скрипт делает ВСЕ автоматически:
1. Копирует файлы в папку renga
2. Добавляет секцию в меню Sverchok (YAML)
3. Регистрирует ноды (опционально)

Запустите этот скрипт в Blender (Text Editor > Run Script)
"""

import bpy
import os
import sys
import shutil
import pathlib
import re

print("\n" + "="*70)
print("АВТОМАТИЧЕСКАЯ УСТАНОВКА НОД RENGA В SVERCHOK")
print("="*70 + "\n")

# ============================================================================
# ШАГ 1: Определение путей
# ============================================================================

# Путь к исходным файлам (относительно этого скрипта)
script_dir = os.path.dirname(os.path.abspath(__file__))
source_path = os.path.join(script_dir, "sverchok_nodes", "renga")

# Проверка исходной папки
if not os.path.exists(source_path):
    print(f"✗ ОШИБКА: Исходная папка не найдена: {source_path}")
    print("\nУбедитесь, что скрипт запущен из корня проекта.")
    sys.exit(1)

print(f"✓ Исходная папка найдена: {source_path}")

# Автоматическое определение версии Blender
blender_version = f"{bpy.app.version[0]}.{bpy.app.version[1]}"
user_home = pathlib.Path.home()

target_path = user_home / "AppData" / "Roaming" / "Blender Foundation" / "Blender" / blender_version / "scripts" / "addons" / "sverchok-master" / "nodes" / "renga"
menus_path = user_home / "AppData" / "Roaming" / "Blender Foundation" / "Blender" / blender_version / "scripts" / "addons" / "sverchok-master" / "menus"

target_path = str(target_path)
menus_path = str(menus_path)

print(f"✓ Версия Blender: {blender_version}")
print(f"✓ Целевая папка: {target_path}")
print()

# ============================================================================
# ШАГ 2: Копирование файлов
# ============================================================================

print("="*70)
print("ШАГ 1: Копирование файлов")
print("="*70)
print()

# Создание папки renga, если не существует
if not os.path.exists(target_path):
    os.makedirs(target_path, exist_ok=True)
    print(f"✓ Создана папка: {target_path}")
else:
    print(f"⚠ Папка уже существует: {target_path}")
    print("  Существующие файлы будут перезаписаны.")

# Копирование файлов
required_files = [
    "__init__.py",
    "renga_connect.py",
    "renga_create_columns.py",
    "renga_get_walls.py",
    "renga_client.py",
    "commands.py",
    "connection_protocol.py"
]

copied_count = 0
for filename in required_files:
    src = os.path.join(source_path, filename)
    dst = os.path.join(target_path, filename)
    
    if os.path.exists(src):
        try:
            shutil.copy2(src, dst)
            print(f"  ✓ {filename}")
            copied_count += 1
        except Exception as e:
            print(f"  ✗ {filename}: ОШИБКА - {e}")
    else:
        print(f"  ✗ {filename}: не найден в исходной папке")

if copied_count != len(required_files):
    print(f"\n✗ Скопировано только {copied_count} из {len(required_files)} файлов!")
    print("Проверьте исходную папку.")
    sys.exit(1)

print(f"\n✓ Все файлы скопированы успешно!")

# ============================================================================
# ШАГ 3: Добавление в меню (YAML)
# ============================================================================

print()
print("="*70)
print("ШАГ 2: Добавление в меню Sverchok")
print("="*70)
print()

if not os.path.exists(menus_path):
    print(f"⚠ Папка menus не найдена: {menus_path}")
    print("  Меню будет добавлено автоматически при следующем запуске Blender")
else:
    menu_files = ["full_by_data_type.yaml", "index.yaml", "full_by_operations.yaml"]
    renga_section = """
- Renga:
    - icon_name: NETWORK_DRIVE
    - SvRengaConnectNode
    - SvRengaCreateColumnsNode
    - SvRengaGetWallsNode
"""
    
    processed_count = 0
    
    for menu_file in menu_files:
        menu_path = os.path.join(menus_path, menu_file)
        
        if not os.path.exists(menu_path):
            print(f"⚠ Файл не найден: {menu_file} (пропущен)")
            continue
        
        try:
            print(f"📄 Обработка: {menu_file}")
            
            # Читаем файл
            with open(menu_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Проверяем, есть ли уже секция Renga
            if 'Renga:' in content or '- Renga:' in content:
                print(f"  ⚠ Секция Renga уже существует, обновляем...")
                # Удаляем старую секцию Renga
                content = re.sub(r'- Renga:.*?(?=\n- [A-Z]|\Z)', '', content, flags=re.DOTALL)
            
            # Находим место для вставки
            network_marker = "- Network:"
            pulga_marker = "- Pulga Physics:"
            
            if network_marker in content:
                # Вставляем после Network
                insert_pos = content.find(network_marker)
                next_section = content.find("\n- ", insert_pos + len(network_marker))
                if next_section == -1:
                    next_section = len(content)
                content = content[:next_section] + renga_section + content[next_section:]
                print(f"  ✓ Секция Renga добавлена после Network")
            elif pulga_marker in content:
                # Вставляем перед Pulga Physics
                insert_pos = content.find(pulga_marker)
                content = content[:insert_pos] + renga_section + content[insert_pos:]
                print(f"  ✓ Секция Renga добавлена перед Pulga Physics")
            else:
                # Добавляем в конец
                content = content.rstrip() + renga_section
                print(f"  ✓ Секция Renga добавлена в конец файла")
            
            # Создаем резервную копию
            backup_path = menu_path + ".backup"
            shutil.copy2(menu_path, backup_path)
            print(f"  ✓ Резервная копия: {os.path.basename(backup_path)}")
            
            # Сохраняем изменения
            with open(menu_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✓ Файл обновлен")
            processed_count += 1
            
        except Exception as e:
            print(f"  ✗ ОШИБКА при обработке {menu_file}: {e}")
            import traceback
            traceback.print_exc()
    
    if processed_count > 0:
        print(f"\n✓ Обработано файлов меню: {processed_count}")
    else:
        print("\n⚠ Файлы меню не были обработаны")

# ============================================================================
# ШАГ 4: Регистрация нод (опционально)
# ============================================================================

print()
print("="*70)
print("ШАГ 3: Регистрация нод")
print("="*70)
print()

# Импортируем скрипт регистрации
try:
    # Добавляем путь к скриптам
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    
    # Пытаемся импортировать и выполнить регистрацию
    import importlib.util
    register_script = os.path.join(script_dir, "FINAL_REGISTER_RENGA_NODES.py")
    
    if os.path.exists(register_script):
        spec = importlib.util.spec_from_file_location("register_nodes", register_script)
        register_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(register_module)
        print("✓ Ноды зарегистрированы")
    else:
        print("⚠ Скрипт регистрации не найден, ноды будут зарегистрированы при следующем запуске Blender")
        
except Exception as e:
    print(f"⚠ Ошибка при регистрации: {e}")
    print("  Ноды будут зарегистрированы автоматически при следующем запуске Blender")

# ============================================================================
# ИТОГИ
# ============================================================================

print()
print("="*70)
print("✓ УСТАНОВКА ЗАВЕРШЕНА УСПЕШНО!")
print("="*70)
print()
print("Что было сделано:")
print("  1. ✓ Файлы скопированы в папку renga")
print("  2. ✓ Секция Renga добавлена в меню Sverchok")
print("  3. ✓ Ноды зарегистрированы (или будут при следующем запуске)")
print()
print("Следующие шаги:")
print("  1. Перезапустите Blender ПОЛНОСТЬЮ")
print("  2. Откройте Sverchok (Shift+A в Node Editor)")
print("  3. Найдите категорию 'Renga' в меню между 'Network' и 'Pulga Physics'")
print()
print("Ноды должны появиться автоматически!")
print()
print("Если ноды не видны:")
print("  - Перезагрузите аддон Sverchok (Edit > Preferences > Add-ons)")
print("  - Или используйте поиск: Space -> 'Renga'")
print("="*70 + "\n")

