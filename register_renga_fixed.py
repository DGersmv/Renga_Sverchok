# ИСПРАВЛЕННАЯ РЕГИСТРАЦИЯ НОД RENGA
# Проблема: относительные импорты (from . import ...) не работают
# Решение: правильно настроить sys.path и __package__

import bpy
import sys
import os
import importlib.util

print("\n" + "="*70)
print("ИСПРАВЛЕННАЯ РЕГИСТРАЦИЯ НОД RENGA")
print("="*70)

# Путь к нодам
renga_path = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga"
sverchok_path = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master"

if not os.path.exists(renga_path):
    print(f"✗ ОШИБКА: Папка не найдена: {renga_path}")
    sys.exit(1)

print(f"✓ Папка найдена: {renga_path}")

# КРИТИЧНО: Добавить путь к sverchok-master в sys.path
# Это нужно для того, чтобы Python мог найти модуль 'nodes'
if sverchok_path not in sys.path:
    sys.path.insert(0, sverchok_path)
    print(f"✓ Добавлен путь к sverchok: {sverchok_path}")

# Также добавить путь к nodes
nodes_path = os.path.join(sverchok_path, "nodes")
if nodes_path not in sys.path:
    sys.path.insert(0, nodes_path)
    print(f"✓ Добавлен путь к nodes: {nodes_path}")

# Теперь можно использовать абсолютные импорты
print("\nРегистрация нод:")
print("-" * 70)

# Список нод для регистрации
nodes_to_register = [
    ("renga_connect.py", "SvRengaConnectNode", "nodes.renga.renga_connect"),
    ("renga_create_columns.py", "SvRengaCreateColumnsNode", "nodes.renga.renga_create_columns"),
    ("renga_get_walls.py", "SvRengaGetWallsNode", "nodes.renga.renga_get_walls")
]

registered_count = 0

for filename, class_name, module_path in nodes_to_register:
    filepath = os.path.join(renga_path, filename)
    
    if not os.path.exists(filepath):
        print(f"✗ {filename}: файл не найден")
        continue
    
    try:
        # Вариант 1: Попробовать импортировать как модуль пакета
        try:
            # Удалить модуль из кэша если он уже загружен
            if module_path in sys.modules:
                del sys.modules[module_path]
            
            # Импортировать как часть пакета nodes.renga
            module = __import__(module_path, fromlist=[class_name])
            print(f"✓ {filename}: импортирован как {module_path}")
            
        except ImportError as e:
            # Вариант 2: Загрузить напрямую через importlib
            print(f"  Попытка прямой загрузки {filename}...")
            spec = importlib.util.spec_from_file_location(module_path, filepath)
            module = importlib.util.module_from_spec(spec)
            
            # КРИТИЧНО: Установить правильный __package__
            module.__package__ = "nodes.renga"
            module.__name__ = module_path
            
            # КРИТИЧНО: Добавить модуль в sys.modules ПЕРЕД выполнением
            # чтобы относительные импорты работали
            sys.modules[module_path] = module
            
            # Также добавить родительские модули
            if "nodes.renga" not in sys.modules:
                # Создать фиктивный модуль для nodes.renga
                renga_module = type(sys)('nodes.renga')
                renga_module.__path__ = [renga_path]
                sys.modules["nodes.renga"] = renga_module
            
            if "nodes" not in sys.modules:
                # Создать фиктивный модуль для nodes
                nodes_module = type(sys)('nodes')
                nodes_module.__path__ = [nodes_path]
                sys.modules["nodes"] = nodes_module
            
            # Теперь выполнить модуль
            spec.loader.exec_module(module)
            print(f"✓ {filename}: загружен напрямую")
        
        # Проверить наличие класса
        if not hasattr(module, class_name):
            print(f"✗ {filename}: класс {class_name} не найден")
            continue
        
        # Проверить, зарегистрирован ли уже
        if class_name in dir(bpy.types):
            print(f"✓ {class_name}: уже зарегистрирован")
            registered_count += 1
        else:
            # Зарегистрировать
            if hasattr(module, 'register'):
                try:
                    module.register()
                    print(f"✓ {class_name}: зарегистрирован через register()")
                    registered_count += 1
                except Exception as e:
                    if "already registered" in str(e).lower():
                        print(f"✓ {class_name}: уже зарегистрирован")
                        registered_count += 1
                    else:
                        # Попробовать прямую регистрацию
                        try:
                            node_class = getattr(module, class_name)
                            bpy.utils.register_class(node_class)
                            print(f"✓ {class_name}: зарегистрирован напрямую")
                            registered_count += 1
                        except Exception as e2:
                            print(f"✗ {class_name}: ошибка регистрации - {e2}")
            else:
                # Прямая регистрация
                try:
                    node_class = getattr(module, class_name)
                    bpy.utils.register_class(node_class)
                    print(f"✓ {class_name}: зарегистрирован напрямую")
                    registered_count += 1
                except Exception as e:
                    print(f"✗ {class_name}: ошибка - {e}")
    
    except Exception as e:
        print(f"✗ {filename}: КРИТИЧЕСКАЯ ОШИБКА - {e}")
        import traceback
        traceback.print_exc()

# Финальная проверка
print("\n" + "="*70)
print("ФИНАЛЬНАЯ ПРОВЕРКА:")
print("="*70)

all_registered = True
for filename, class_name, module_path in nodes_to_register:
    is_registered = class_name in dir(bpy.types)
    status = "✓" if is_registered else "✗"
    print(f"{status} {class_name}: {'ЗАРЕГИСТРИРОВАН' if is_registered else 'НЕ ЗАРЕГИСТРИРОВАН'}")
    if not is_registered:
        all_registered = False

print("\n" + "="*70)
if all_registered:
    print("✓ ВСЕ НОДЫ ЗАРЕГИСТРИРОВАНЫ!")
    print("\nПопробуйте найти ноды в Sverchok через поиск (Space -> 'Renga')")
else:
    print("✗ НЕКОТОРЫЕ НОДЫ НЕ ЗАРЕГИСТРИРОВАНЫ")
    print("Проверьте ошибки выше")
print("="*70 + "\n")



