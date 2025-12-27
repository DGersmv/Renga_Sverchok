# ФИНАЛЬНАЯ РЕГИСТРАЦИЯ НОД RENGA
# Скопируйте в Text Editor Blender и нажмите Run Script (Alt+P)
# ВАЖНО: Откройте системную консоль Blender: Window > Toggle System Console

import bpy
import sys
import os
import importlib.util

# Функция для вывода (и в консоль, и в Info)
def log(msg):
    print(msg)
    # Также выводим в Info для видимости
    try:
        bpy.ops.info.report({'INFO'}, msg)
    except:
        pass

log("\n" + "="*70)
log("РЕГИСТРАЦИЯ НОД RENGA")
log("="*70)

# Путь к нодам
renga_path = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga"

if not os.path.exists(renga_path):
    log(f"✗ ОШИБКА: Папка не найдена: {renga_path}")
    log("Проверьте путь к Sverchok!")
else:
    log(f"✓ Папка найдена: {renga_path}")

# Добавить путь
sverchok_nodes_path = os.path.dirname(renga_path)
if sverchok_nodes_path not in sys.path:
    sys.path.insert(0, sverchok_nodes_path)
    log(f"✓ Добавлен путь: {sverchok_nodes_path}")

# Регистрация нод
nodes_info = [
    ("renga_connect.py", "SvRengaConnectNode", "renga_connect"),
    ("renga_create_columns.py", "SvRengaCreateColumnsNode", "renga_create_columns"),
    ("renga_get_walls.py", "SvRengaGetWallsNode", "renga_get_walls")
]

log("\nРегистрация нод:")
log("-" * 70)

registered = []
for filename, class_name, module_name in nodes_info:
    filepath = os.path.join(renga_path, filename)
    
    if not os.path.exists(filepath):
        log(f"✗ {filename}: файл не найден")
        continue
    
    try:
        # Загрузить модуль
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        module = importlib.util.module_from_spec(spec)
        module.__package__ = "nodes.renga"
        spec.loader.exec_module(module)
        
        # Проверить наличие класса
        if not hasattr(module, class_name):
            log(f"✗ {filename}: класс {class_name} не найден")
            continue
        
        # Проверить, зарегистрирован ли
        if class_name in dir(bpy.types):
            log(f"✓ {class_name}: уже зарегистрирован")
            registered.append(class_name)
        else:
            # Зарегистрировать
            if hasattr(module, 'register'):
                try:
                    module.register()
                    log(f"✓ {class_name}: зарегистрирован через register()")
                    registered.append(class_name)
                except Exception as e:
                    if "already registered" in str(e).lower():
                        log(f"✓ {class_name}: уже зарегистрирован")
                        registered.append(class_name)
                    else:
                        # Попробовать прямую регистрацию
                        try:
                            node_class = getattr(module, class_name)
                            bpy.utils.register_class(node_class)
                            log(f"✓ {class_name}: зарегистрирован напрямую")
                            registered.append(class_name)
                        except Exception as e2:
                            log(f"✗ {class_name}: ошибка - {e2}")
            else:
                # Прямая регистрация
                try:
                    node_class = getattr(module, class_name)
                    bpy.utils.register_class(node_class)
                    log(f"✓ {class_name}: зарегистрирован напрямую")
                    registered.append(class_name)
                except Exception as e:
                    log(f"✗ {class_name}: ошибка - {e}")
    
    except Exception as e:
        log(f"✗ {filename}: ошибка загрузки - {e}")
        import traceback
        traceback.print_exc()

# Финальная проверка
log("\n" + "="*70)
log("ФИНАЛЬНАЯ ПРОВЕРКА:")
log("="*70)

all_registered = True
for filename, class_name, module_name in nodes_info:
    is_registered = class_name in dir(bpy.types)
    status = "✓" if is_registered else "✗"
    log(f"{status} {class_name}: {'ЗАРЕГИСТРИРОВАН' if is_registered else 'НЕ ЗАРЕГИСТРИРОВАН'}")
    if not is_registered:
        all_registered = False

log("\n" + "="*70)
if all_registered:
    log("✓ ВСЕ НОДЫ ЗАРЕГИСТРИРОВАНЫ!")
    log("\nСледующие шаги:")
    log("1. Откройте Sverchok")
    log("2. Нажмите Space (поиск)")
    log("3. Введите 'Renga' или 'SvRenga'")
    log("4. Ноды должны появиться в результатах поиска")
    log("\nЕсли ноды не видны:")
    log("- Перезапустите Blender")
    log("- Обновите Sverchok до последней версии")
else:
    log("✗ НЕКОТОРЫЕ НОДЫ НЕ ЗАРЕГИСТРИРОВАНЫ")
    log("Проверьте ошибки выше")
log("="*70 + "\n")

# Показать диалог с результатом
if all_registered:
    bpy.ops.ui.reports_to_textblock()
    log("\n✓ Проверьте Info панель (Window > Info) для деталей")




