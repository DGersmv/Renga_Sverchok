"""
Скрипт для автоматического добавления категории "Renga" в меню Sverchok
Скопируйте этот скрипт в Blender Text Editor и запустите (Run Script)
"""

import bpy
import os
import yaml

# Путь к меню Sverchok
blender_version = bpy.app.version_string.split('.')[0]
menus_path = os.path.join(
    os.path.expanduser("~"),
    "AppData", "Roaming", "Blender Foundation", "Blender",
    blender_version, "scripts", "addons", "sverchok-master", "menus"
)

# Категория для добавления
renga_category = {
    'icon_name': 'PLUGIN',
    'extra_menu': 'ConnectionPartialMenu',
    'nodes': [
        'SvRengaConnectNode',
        'SvRengaCreateColumnsNode',
        'SvRengaGetWallsNode'
    ]
}

# Файлы для изменения
menu_files = [
    'index.yaml',
    'full_by_data_type.yaml',
    'full_by_operations.yaml'
]

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
            # Читаем YAML файл
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Проверяем, есть ли уже категория Renga
            if 'Renga:' in content or '- Renga:' in content:
                print(f"✓ Категория 'Renga' уже есть в {menu_file}")
                continue
            
            # Парсим YAML
            try:
                data = yaml.safe_load(content)
                if data is None:
                    data = []
            except:
                print(f"⚠ Не удалось распарсить {menu_file}, пропускаем")
                continue
            
            # Проверяем, что data - это список
            if not isinstance(data, list):
                print(f"⚠ Неверный формат {menu_file}, пропускаем")
                continue
            
            # Ищем, где добавить категорию (по алфавиту)
            insert_index = len(data)
            for i, item in enumerate(data):
                if isinstance(item, dict):
                    for key in item.keys():
                        if key.lower() > 'renga':
                            insert_index = i
                            break
                    if insert_index < len(data):
                        break
            
            # Добавляем категорию
            renga_entry = {
                'Renga': {
                    'icon_name': 'PLUGIN',
                    'extra_menu': 'ConnectionPartialMenu',
                    'nodes': [
                        'SvRengaConnectNode',
                        'SvRengaCreateColumnsNode',
                        'SvRengaGetWallsNode'
                    ]
                }
            }
            
            data.insert(insert_index, renga_entry)
            
            # Сохраняем обратно
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
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

