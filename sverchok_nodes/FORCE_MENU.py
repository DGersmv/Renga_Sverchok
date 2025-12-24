"""
Скрипт для принудительного добавления нод Renga в меню Sverchok
Скопируйте этот скрипт в Blender Text Editor и запустите (Run Script)
"""

import bpy
import sys
import os

# Автоматическое определение пути
blender_version = bpy.app.version_string.split('.')[0]
addons_path = os.path.join(
    os.path.expanduser("~"),
    "AppData", "Roaming", "Blender Foundation", "Blender",
    blender_version, "scripts", "addons"
)

renga_path = None
for root, dirs, files in os.walk(addons_path):
    if 'renga' in dirs and '__init__.py' in os.listdir(os.path.join(root, 'renga')):
        renga_path = os.path.join(root, 'renga')
        break

if not renga_path:
    print("✗ Папка renga не найдена!")
    print("Укажите путь вручную в скрипте")
    renga_path = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga"

sverchok_path = os.path.dirname(os.path.dirname(renga_path))
nodes_path = os.path.dirname(renga_path)

print("=" * 70)
print("ПРИНУДИТЕЛЬНАЯ РЕГИСТРАЦИЯ НОД RENGA")
print("=" * 70)
print(f"Путь к нодам: {renga_path}")

# Добавить пути
for path in [sverchok_path, nodes_path]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Создать фиктивные модули
if "nodes" not in sys.modules:
    nodes_module = type(sys)('nodes')
    nodes_module.__path__ = [nodes_path]
    sys.modules["nodes"] = nodes_module

if "nodes.renga" not in sys.modules:
    renga_module = type(sys)('nodes.renga')
    renga_module.__path__ = [renga_path]
    sys.modules["nodes.renga"] = renga_module

# Импорт и регистрация
nodes_info = [
    ("renga_connect", "SvRengaConnectNode"),
    ("renga_create_columns", "SvRengaCreateColumnsNode"),
    ("renga_get_walls", "SvRengaGetWallsNode")
]

registered = []

for module_name, class_name in nodes_info:
    try:
        module_path = f"nodes.renga.{module_name}"
        if module_path in sys.modules:
            del sys.modules[module_path]
        
        module = __import__(module_path, fromlist=[class_name])
        node_class = getattr(module, class_name)
        
        if class_name in dir(bpy.types):
            try:
                bpy.utils.unregister_class(getattr(bpy.types, class_name))
            except:
                pass
        
        bpy.utils.register_class(node_class)
        registered.append(node_class)
        print(f"✓ {class_name} зарегистрирован")
    except Exception as e:
        print(f"✗ {class_name}: {e}")

# Попытка обновить меню Sverchok
print("\n" + "=" * 70)
print("ОБНОВЛЕНИЕ МЕНЮ SVERCHOK")
print("=" * 70)

try:
    import sverchok
    # Попытка обновить меню
    if hasattr(sverchok, 'update_node_menu'):
        sverchok.update_node_menu()
        print("✓ Меню обновлено")
    
    # Попытка через UI
    try:
        from sverchok.ui import nodeview_space_menu
        if hasattr(nodeview_space_menu, 'update_node_menu'):
            nodeview_space_menu.update_node_menu()
            print("✓ Меню UI обновлено")
    except:
        pass
    
    # Попытка обновить категории
    try:
        from sverchok.node_tree import SverchCustomTreeNode
        # Принудительно обновить категории
        if hasattr(SverchCustomTreeNode, 'categories'):
            SverchCustomTreeNode.categories.add("Renga")
            print("✓ Категория 'Renga' добавлена")
    except Exception as e:
        print(f"⚠ Не удалось обновить категории: {e}")
        
except Exception as e:
    print(f"⚠ Ошибка обновления меню: {e}")

# Проверка (после небольшой задержки для завершения регистрации)
import time
time.sleep(0.5)  # Дать время на завершение регистрации

print("\n" + "=" * 70)
print("ПРОВЕРКА")
print("=" * 70)

all_ok = True
for module_name, class_name in nodes_info:
    # Проверка через bpy.types
    try:
        node_type = getattr(bpy.types, class_name, None)
        status = node_type is not None
    except:
        status = class_name in dir(bpy.types)
    
    print(f"{'✓' if status else '✗'} {class_name}: {'ЗАРЕГИСТРИРОВАН' if status else 'НЕ ЗАРЕГИСТРИРОВАН'}")
    if not status:
        all_ok = False

print("\n" + "=" * 70)
if all_ok:
    print("✓ ВСЕ НОДЫ ЗАРЕГИСТРИРОВАНЫ!")
    print("\nТеперь:")
    print("1. Откройте Sverchok")
    print("2. Нажмите Space (поиск)")
    print("3. Введите 'Renga'")
    print("4. Ноды должны появиться!")
else:
    print("⚠ НЕКОТОРЫЕ НОДЫ НЕ ЗАРЕГИСТРИРОВАНЫ В ЭТОТ МОМЕНТ")
    print("НО: Sverchok может зарегистрировать их автоматически при загрузке!")
    print("\nПроверьте после полной загрузки Sverchok:")
    print("1. Откройте Sverchok")
    print("2. Нажмите Space (поиск)")
    print("3. Введите 'Renga'")
    print("4. Если ноды есть - всё работает!")
print("=" * 70)


