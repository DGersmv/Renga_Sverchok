# ПРОСТАЯ ПРОВЕРКА НОД RENGA
# Скопируйте этот код в Text Editor Blender и нажмите Run Script

import bpy
import sys
import os

print("\n" + "="*60)
print("ПРОВЕРКА НОД RENGA")
print("="*60 + "\n")

# Путь к нодам
renga_path = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga"

# Проверка 1: Существует ли папка
if os.path.exists(renga_path):
    print("✓ Папка renga найдена")
else:
    print("✗ Папка renga НЕ найдена:", renga_path)
    print("  Проверьте путь!")

# Проверка 2: Существуют ли файлы нод
files_to_check = [
    "renga_connect.py",
    "renga_create_columns.py", 
    "renga_get_walls.py"
]

print("\nПроверка файлов:")
for filename in files_to_check:
    filepath = os.path.join(renga_path, filename)
    if os.path.exists(filepath):
        print(f"  ✓ {filename}")
    else:
        print(f"  ✗ {filename} - НЕ НАЙДЕН")

# Проверка 3: Зарегистрированы ли ноды в bpy.types
print("\nПроверка регистрации в bpy.types:")
nodes = ["SvRengaConnectNode", "SvRengaCreateColumnsNode", "SvRengaGetWallsNode"]
for node_name in nodes:
    is_registered = node_name in dir(bpy.types)
    status = "✓" if is_registered else "✗"
    print(f"  {status} {node_name}: {'ДА' if is_registered else 'НЕТ'}")

# Попытка регистрации
print("\nПопытка регистрации:")
try:
    import importlib.util
    
    # Регистрация renga_connect
    connect_file = os.path.join(renga_path, "renga_connect.py")
    if os.path.exists(connect_file):
        spec = importlib.util.spec_from_file_location("renga_connect", connect_file)
        rc = importlib.util.module_from_spec(spec)
        rc.__package__ = "nodes.renga"
        spec.loader.exec_module(rc)
        
        if hasattr(rc, 'register'):
            try:
                rc.register()
                print("  ✓ renga_connect зарегистрирован")
            except Exception as e:
                if "already registered" in str(e).lower():
                    print("  ✓ renga_connect уже зарегистрирован")
                else:
                    print(f"  ✗ Ошибка: {e}")
    
    # Регистрация renga_create_columns
    columns_file = os.path.join(renga_path, "renga_create_columns.py")
    if os.path.exists(columns_file):
        spec = importlib.util.spec_from_file_location("renga_create_columns", columns_file)
        rcc = importlib.util.module_from_spec(spec)
        rcc.__package__ = "nodes.renga"
        spec.loader.exec_module(rcc)
        
        if hasattr(rcc, 'register'):
            try:
                rcc.register()
                print("  ✓ renga_create_columns зарегистрирован")
            except Exception as e:
                if "already registered" in str(e).lower():
                    print("  ✓ renga_create_columns уже зарегистрирован")
                else:
                    print(f"  ✗ Ошибка: {e}")
    
    # Регистрация renga_get_walls
    walls_file = os.path.join(renga_path, "renga_get_walls.py")
    if os.path.exists(walls_file):
        spec = importlib.util.spec_from_file_location("renga_get_walls", walls_file)
        rgw = importlib.util.module_from_spec(spec)
        rgw.__package__ = "nodes.renga"
        spec.loader.exec_module(rgw)
        
        if hasattr(rgw, 'register'):
            try:
                rgw.register()
                print("  ✓ renga_get_walls зарегистрирован")
            except Exception as e:
                if "already registered" in str(e).lower():
                    print("  ✓ renga_get_walls уже зарегистрирован")
                else:
                    print(f"  ✗ Ошибка: {e}")

except Exception as e:
    print(f"  ✗ КРИТИЧЕСКАЯ ОШИБКА: {e}")
    import traceback
    traceback.print_exc()

# Финальная проверка
print("\n" + "="*60)
print("ФИНАЛЬНАЯ ПРОВЕРКА:")
print("="*60)
all_ok = True
for node_name in nodes:
    is_registered = node_name in dir(bpy.types)
    status = "✓" if is_registered else "✗"
    print(f"  {status} {node_name}: {'ЗАРЕГИСТРИРОВАН' if is_registered else 'НЕ ЗАРЕГИСТРИРОВАН'}")
    if not is_registered:
        all_ok = False

print("\n" + "="*60)
if all_ok:
    print("✓ ВСЕ НОДЫ ЗАРЕГИСТРИРОВАНЫ!")
    print("\nЕсли ноды не видны в меню Sverchok:")
    print("1. Перезапустите Blender")
    print("2. Попробуйте поиск в Sverchok (Space -> введите 'Renga')")
    print("3. Проверьте версию Sverchok (может быть несовместима с Blender 5.0)")
else:
    print("✗ НЕКОТОРЫЕ НОДЫ НЕ ЗАРЕГИСТРИРОВАНЫ")
    print("Проверьте ошибки выше")
print("="*60 + "\n")


