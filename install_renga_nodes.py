"""
Автоматическая установка нод Renga для Sverchok
Запустите этот скрипт в Blender (Text Editor > Run Script)
Или через командную строку: blender --python install_renga_nodes.py
"""

import bpy
import os
import shutil
import sys

print("=" * 70)
print("АВТОМАТИЧЕСКАЯ УСТАНОВКА НОД RENGA ДЛЯ SVERCHOK")
print("=" * 70)

# Определяем пути
blender_version = bpy.app.version_string.split('.')[0]
addons_path = os.path.join(
    os.path.expanduser("~"),
    "AppData", "Roaming", "Blender Foundation", "Blender",
    blender_version, "scripts", "addons"
)

sverchok_path = os.path.join(addons_path, "sverchok-master")
nodes_path = os.path.join(sverchok_path, "nodes")
renga_path = os.path.join(nodes_path, "renga")
menus_path = os.path.join(sverchok_path, "menus")

# Путь к исходным файлам (где находится этот скрипт)
script_dir = os.path.dirname(os.path.abspath(__file__))
source_nodes_dir = os.path.join(script_dir, "sverchok_nodes")

# Если скрипт запущен из Blender, ищем исходные файлы относительно проекта
if not os.path.exists(source_nodes_dir):
    # Пробуем найти в стандартных местах
    possible_paths = [
        r"C:\Program Files\Renga Standard\RengaSDK\Samples\C#\Renga_Sverchok\sverchok_nodes",
        os.path.join(os.path.dirname(script_dir), "sverchok_nodes"),
        os.path.join(script_dir, "sverchok_nodes"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            source_nodes_dir = path
            break

print(f"Исходная папка: {source_nodes_dir}")
print(f"Целевая папка: {renga_path}")
print(f"Путь к меню: {menus_path}")

# Проверка существования Sverchok
if not os.path.exists(sverchok_path):
    print(f"\n✗ ОШИБКА: Sverchok не найден в {sverchok_path}")
    print("Установите аддон Sverchok сначала!")
    sys.exit(1)

if not os.path.exists(source_nodes_dir):
    print(f"\n✗ ОШИБКА: Исходная папка не найдена: {source_nodes_dir}")
    print("Укажите путь к папке sverchok_nodes вручную в скрипте")
    sys.exit(1)

print(f"\n✓ Sverchok найден: {sverchok_path}")

# ШАГ 1: Копирование файлов
print("\n" + "=" * 70)
print("ШАГ 1: КОПИРОВАНИЕ ФАЙЛОВ")
print("=" * 70)

# Удаляем старую папку renga (если есть)
if os.path.exists(renga_path):
    print(f"Удаление старой папки: {renga_path}")
    try:
        shutil.rmtree(renga_path)
    except Exception as e:
        print(f"⚠ Не удалось удалить старую папку: {e}")

# Создаем папку renga
os.makedirs(renga_path, exist_ok=True)
print(f"✓ Создана папка: {renga_path}")

# Копируем файлы
files_to_copy = [
    "__init__.py",
    "renga_connect.py",
    "renga_create_columns.py",
    "renga_get_walls.py",
    "renga_client.py",
    "commands.py",
    "connection_protocol.py",
]

copied_count = 0
for filename in files_to_copy:
    src = os.path.join(source_nodes_dir, filename)
    dst = os.path.join(renga_path, filename)
    
    if os.path.exists(src):
        try:
            shutil.copy2(src, dst)
            print(f"✓ Скопирован: {filename}")
            copied_count += 1
        except Exception as e:
            print(f"✗ Ошибка копирования {filename}: {e}")
    else:
        print(f"⚠ Файл не найден: {filename}")

print(f"\n✓ Скопировано файлов: {copied_count}/{len(files_to_copy)}")

# ШАГ 2: Добавление категории в меню
print("\n" + "=" * 70)
print("ШАГ 2: ДОБАВЛЕНИЕ КАТЕГОРИИ В МЕНЮ")
print("=" * 70)

menu_files = [
    'index.yaml',
    'full_by_data_type.yaml',
    'full_by_operations.yaml'
]

renga_category_text = """- Renga:
    icon_name: PLUGIN
    extra_menu: ConnectionPartialMenu
    - SvRengaConnectNode
    - SvRengaCreateColumnsNode
    - SvRengaGetWallsNode
"""

if not os.path.exists(menus_path):
    print(f"⚠ Папка меню не найдена: {menus_path}")
    print("Пропускаем добавление в меню (можно добавить вручную)")
else:
    for menu_file in menu_files:
        file_path = os.path.join(menus_path, menu_file)
        
        if not os.path.exists(file_path):
            print(f"⚠ Файл не найден: {menu_file}")
            continue
        
        try:
            # Читаем файл
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Проверяем, есть ли уже категория Renga
            if 'Renga:' in content or '- Renga:' in content:
                print(f"✓ Категория 'Renga' уже есть в {menu_file}")
                continue
            
            # Читаем построчно
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Ищем место для вставки (после "Pulga Physics" или перед "Text")
            import re
            insert_index = len(lines)
            
            for i, line in enumerate(lines):
                # Ищем категории, которые идут после Renga по алфавиту
                if re.match(r'^- (Text|Transform|Vector|Viewer|Voronoi|Wave|Weave|Wrangle|Xsection):', line, re.IGNORECASE):
                    insert_index = i
                    break
                # Ищем "Pulga Physics" - вставим после неё
                elif re.match(r'^- Pulga Physics:', line, re.IGNORECASE):
                    # Находим конец этой категории
                    j = i + 1
                    while j < len(lines) and (lines[j].startswith(' ') or lines[j].strip() == ''):
                        j += 1
                    insert_index = j
                    break
            
            # Вставляем категорию
            lines.insert(insert_index, renga_category_text)
            
            # Сохраняем файл
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            print(f"✓ Категория 'Renga' добавлена в {menu_file}")
            
        except Exception as e:
            print(f"✗ Ошибка при обработке {menu_file}: {e}")
            import traceback
            traceback.print_exc()

# ШАГ 3: Удаление кэша
print("\n" + "=" * 70)
print("ШАГ 3: ОЧИСТКА КЭША")
print("=" * 70)

cache_dirs = [
    os.path.join(renga_path, "__pycache__"),
    os.path.join(menus_path, "__pycache__"),
]

for cache_dir in cache_dirs:
    if os.path.exists(cache_dir):
        try:
            shutil.rmtree(cache_dir)
            print(f"✓ Удален кэш: {cache_dir}")
        except Exception as e:
            print(f"⚠ Не удалось удалить кэш {cache_dir}: {e}")

# ИТОГ
print("\n" + "=" * 70)
print("УСТАНОВКА ЗАВЕРШЕНА!")
print("=" * 70)
print("\nТеперь:")
print("1. ПЕРЕЗАПУСТИТЕ Blender ПОЛНОСТЬЮ")
print("2. Откройте Sverchok")
print("3. Нажмите 'Add Node' или Space для поиска")
print("4. Найдите категорию 'Renga' в меню")
print("\nЕсли категория не появилась:")
print("- Проверьте, что файлы скопированы в:")
print(f"  {renga_path}")
print("- Проверьте, что категория добавлена в меню:")
print(f"  {menus_path}")
print("=" * 70)

