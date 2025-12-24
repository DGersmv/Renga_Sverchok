"""
Скрипт для автоматического добавления категории "Renga" в меню Sverchok
Скопируйте этот скрипт в Blender Text Editor и запустите (Run Script)
РАБОТАЕТ БЕЗ YAML - использует простую обработку текста
"""

import bpy
import os
import re

# Путь к меню Sverchok
blender_version = bpy.app.version_string.split('.')[0]
menus_path = os.path.join(
    os.path.expanduser("~"),
    "AppData", "Roaming", "Blender Foundation", "Blender",
    blender_version, "scripts", "addons", "sverchok-master", "menus"
)

# Файлы для изменения
menu_files = [
    'index.yaml',
    'full_by_data_type.yaml',
    'full_by_operations.yaml'
]

# Текст для добавления категории Renga
renga_category_text = """- Renga:
    icon_name: PLUGIN
    extra_menu: ConnectionPartialMenu
    - SvRengaConnectNode
    - SvRengaCreateColumnsNode
    - SvRengaGetWallsNode
"""

print("=" * 70)
print("ДОБАВЛЕНИЕ КАТЕГОРИИ 'Renga' В МЕНЮ SVERCHOK")
print("=" * 70)
print(f"Путь к меню: {menus_path}")

if not os.path.exists(menus_path):
    print(f"✗ Папка меню не найдена: {menus_path}")
    print("Укажите путь вручную в скрипте")
    menus_path = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\menus"

if not os.path.exists(menus_path):
    print(f"✗ Папка меню не найдена!")
    print("Проверьте путь к Sverchok")
else:
    print(f"✓ Папка меню найдена: {menus_path}")
    
    # Обработка каждого файла меню
    for menu_file in menu_files:
        file_path = os.path.join(menus_path, menu_file)
        
        if not os.path.exists(file_path):
            print(f"⚠ Файл не найден: {menu_file}")
            continue
        
        try:
            # Читаем файл
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Проверяем, есть ли уже категория Renga
            content = ''.join(lines)
            if 'Renga:' in content or '- Renga:' in content:
                print(f"✓ Категория 'Renga' уже есть в {menu_file}")
                continue
            
            # Ищем место для вставки (после "Pulga Physics" или перед "Text", или в конец)
            insert_index = len(lines)
            renga_inserted = False
            
            # Ищем паттерны для вставки
            for i, line in enumerate(lines):
                # Ищем категории, которые идут после Renga по алфавиту
                if re.match(r'^- (Text|Transform|Vector|Viewer|Voronoi|Wave|Weave|Wrangle|Xsection):', line, re.IGNORECASE):
                    insert_index = i
                    renga_inserted = True
                    break
                # Ищем "Pulga Physics" - вставим после неё
                elif re.match(r'^- Pulga Physics:', line, re.IGNORECASE):
                    # Находим конец этой категории
                    j = i + 1
                    while j < len(lines) and (lines[j].startswith(' ') or lines[j].strip() == ''):
                        j += 1
                    insert_index = j
                    renga_inserted = True
                    break
            
            # Если не нашли место, вставляем в конец
            if not renga_inserted:
                insert_index = len(lines)
            
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

print("\n" + "=" * 70)
print("ПРОВЕРКА РЕГИСТРАЦИИ НОД")
print("=" * 70)

# Проверка регистрации нод
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
    if not is_registered:
        all_registered = False

print("\n" + "=" * 70)
if all_registered:
    print("✓ ВСЕ НОДЫ ЗАРЕГИСТРИРОВАНЫ!")
    print("\nТеперь:")
    print("1. Перезапустите Blender ПОЛНОСТЬЮ")
    print("2. Откройте Sverchok")
    print("3. Нажмите 'Add Node' или Space для поиска")
    print("4. Найдите категорию 'Renga' в меню")
    print("5. Или введите 'Renga' в поиске")
else:
    print("⚠ НЕКОТОРЫЕ НОДЫ НЕ ЗАРЕГИСТРИРОВАНЫ")
    print("Проверьте консоль Blender на ошибки")
print("=" * 70)

