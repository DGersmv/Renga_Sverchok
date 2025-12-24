# Тест правильного импорта нод Renga в Blender
# Выполните этот код в консоли Python Blender

import sys
import os

print("=" * 60)
print("ПОИСК ПУТИ К НОДАМ RENGA")
print("=" * 60)

# Вариант 1: Прямой импорт из папки nodes
try:
    import nodes.renga.renga_connect as renga_connect
    print("✓ Вариант 1: import nodes.renga.renga_connect - РАБОТАЕТ")
except Exception as e:
    print(f"✗ Вариант 1: {e}")

# Вариант 2: Через sverchok
try:
    from sverchok.nodes.renga import renga_connect
    print("✓ Вариант 2: from sverchok.nodes.renga import - РАБОТАЕТ")
except Exception as e:
    print(f"✗ Вариант 2: {e}")

# Вариант 3: Добавить путь в sys.path
sverchok_path = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master"
if os.path.exists(sverchok_path):
    if sverchok_path not in sys.path:
        sys.path.insert(0, sverchok_path)
    try:
        from nodes.renga import renga_connect
        print("✓ Вариант 3: Добавлен путь в sys.path - РАБОТАЕТ")
    except Exception as e:
        print(f"✗ Вариант 3: {e}")
else:
    print(f"✗ Путь не найден: {sverchok_path}")

# Вариант 4: Прямой импорт из файла
renga_file = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga\renga_connect.py"
if os.path.exists(renga_file):
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("renga_connect", renga_file)
        renga_connect = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(renga_connect)
        print("✓ Вариант 4: Прямой импорт из файла - РАБОТАЕТ")
    except Exception as e:
        print(f"✗ Вариант 4: {e}")
else:
    print(f"✗ Файл не найден: {renga_file}")

print()
print("=" * 60)
print("ПРОВЕРКА РЕГИСТРАЦИИ")
print("=" * 60)

# Попытка регистрации если импорт удался
try:
    if 'renga_connect' in locals():
        if hasattr(renga_connect, 'register'):
            renga_connect.register()
            print("✓ renga_connect зарегистрирован")
        
        # Проверка в bpy.types
        import bpy
        if 'SvRengaConnectNode' in dir(bpy.types):
            print("✓ SvRengaConnectNode найден в bpy.types")
        else:
            print("✗ SvRengaConnectNode НЕ найден в bpy.types")
except Exception as e:
    print(f"Ошибка при регистрации: {e}")
    import traceback
    traceback.print_exc()


