# ФИНАЛЬНАЯ ПРОВЕРКА И РЕГИСТРАЦИЯ НОД RENGA
# Выполните в консоли Python Blender (Text Editor > Run Script)

import bpy
import sys
import os
import importlib.util

print("=" * 70)
print("ФИНАЛЬНАЯ ПРОВЕРКА И РЕГИСТРАЦИЯ НОД RENGA")
print("=" * 70)

# Путь к нодам
renga_path = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga"

if not os.path.exists(renga_path):
    print(f"✗ ОШИБКА: Папка не найдена: {renga_path}")
    sys.exit(1)

print(f"✓ Папка найдена: {renga_path}")

# Добавить путь в sys.path
sverchok_nodes_path = os.path.dirname(renga_path)
if sverchok_nodes_path not in sys.path:
    sys.path.insert(0, sverchok_nodes_path)
    print(f"✓ Добавлен путь: {sverchok_nodes_path}")

# Список нод для регистрации
nodes_to_register = [
    ("renga_connect.py", "SvRengaConnectNode"),
    ("renga_create_columns.py", "SvRengaCreateColumnsNode"),
    ("renga_get_walls.py", "SvRengaGetWallsNode")
]

print()
print("РЕГИСТРАЦИЯ НОД:")
print("-" * 70)

registered_count = 0
for filename, class_name in nodes_to_register:
    filepath = os.path.join(renga_path, filename)
    
    if not os.path.exists(filepath):
        print(f"✗ {filename}: файл не найден")
        continue
    
    try:
        # Загрузить модуль
        spec = importlib.util.spec_from_file_location(filename[:-3], filepath)
        module = importlib.util.module_from_spec(spec)
        # Установить package для относительных импортов
        module.__package__ = "nodes.renga"
        spec.loader.exec_module(module)
        
        # Проверить наличие класса
        if not hasattr(module, class_name):
            print(f"✗ {filename}: класс {class_name} не найден")
            continue
        
        # Проверить, зарегистрирован ли уже
        if class_name in dir(bpy.types):
            print(f"✓ {filename}: {class_name} уже зарегистрирован")
            registered_count += 1
        else:
            # Зарегистрировать
            if hasattr(module, 'register'):
                try:
                    module.register()
                    print(f"✓ {filename}: {class_name} зарегистрирован")
                    registered_count += 1
                except Exception as e:
                    if "already registered" in str(e).lower():
                        print(f"✓ {filename}: {class_name} уже зарегистрирован (через register())")
                        registered_count += 1
                    else:
                        print(f"✗ {filename}: ошибка регистрации - {e}")
            else:
                # Регистрировать класс напрямую
                try:
                    node_class = getattr(module, class_name)
                    bpy.utils.register_class(node_class)
                    print(f"✓ {filename}: {class_name} зарегистрирован напрямую")
                    registered_count += 1
                except Exception as e:
                    if "already registered" in str(e).lower():
                        print(f"✓ {filename}: {class_name} уже зарегистрирован")
                        registered_count += 1
                    else:
                        print(f"✗ {filename}: ошибка прямой регистрации - {e}")
                        import traceback
                        traceback.print_exc()
    
    except Exception as e:
        print(f"✗ {filename}: ошибка загрузки - {e}")
        import traceback
        traceback.print_exc()

print()
print("=" * 70)
print("ИТОГОВАЯ ПРОВЕРКА:")
print("=" * 70)

all_registered = True
for filename, class_name in nodes_to_register:
    is_registered = class_name in dir(bpy.types)
    status = "✓" if is_registered else "✗"
    print(f"{status} {class_name}: {'ЗАРЕГИСТРИРОВАН' if is_registered else 'НЕ ЗАРЕГИСТРИРОВАН'}")
    if not is_registered:
        all_registered = False

print()
if all_registered:
    print("=" * 70)
    print("✓ ВСЕ НОДЫ ЗАРЕГИСТРИРОВАНЫ!")
    print("=" * 70)
    print()
    print("Если ноды не видны в меню Sverchok, это может быть проблема:")
    print("1. Sverchok не обновляет меню автоматически")
    print("2. Нужно перезапустить Blender")
    print("3. Или проблема с версией Sverchok и Blender 5.0")
    print()
    print("Попробуйте:")
    print("- Перезапустить Blender")
    print("- Обновить Sverchok до последней версии")
    print("- Проверить меню через поиск (Space) в Sverchok")
else:
    print("=" * 70)
    print("✗ НЕКОТОРЫЕ НОДЫ НЕ ЗАРЕГИСТРИРОВАНЫ")
    print("=" * 70)
    print("Проверьте ошибки выше")


