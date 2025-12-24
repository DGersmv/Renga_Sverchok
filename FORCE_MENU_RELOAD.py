"""
Принудительная перезагрузка меню Sverchok
"""

import bpy
import os

print("=" * 70)
print("ПРИНУДИТЕЛЬНАЯ ПЕРЕЗАГРУЗКА МЕНЮ SVERCHOK")
print("=" * 70)

# 1. Проверяем меню
print("\n1. ПРОВЕРКА МЕНЮ:")
try:
    blender_version = '.'.join(bpy.app.version_string.split('.')[:2])
    menus_path = os.path.join(
        os.path.expanduser("~"),
        "AppData", "Roaming", "Blender Foundation", "Blender",
        blender_version, "scripts", "addons", "sverchok-master", "menus"
    )
    
    if not os.path.exists(menus_path):
        for ver in ["5.0", "5", "4.0", "4"]:
            alt_path = os.path.join(
                os.path.expanduser("~"),
                "AppData", "Roaming", "Blender Foundation", "Blender",
                ver, "scripts", "addons", "sverchok-master", "menus"
            )
            if os.path.exists(alt_path):
                menus_path = alt_path
                break
    
    if os.path.exists(menus_path):
        print(f"✓ Папка меню: {menus_path}")
        
        # Проверяем файлы
        for menu_file in ['full_by_data_type.yaml', 'full_by_operations.yaml']:
            file_path = os.path.join(menus_path, menu_file)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'Renga:' in content and 'SvRengaConnectNode' in content:
                    print(f"  ✓ {menu_file} - категория Renga найдена")
                else:
                    print(f"  ✗ {menu_file} - категория Renga НЕ найдена")
    else:
        print(f"✗ Папка меню не найдена")
        
except Exception as e:
    print(f"✗ Ошибка: {e}")

# 2. Удаляем кэш меню
print("\n2. УДАЛЕНИЕ КЭША МЕНЮ:")
try:
    cache_path = os.path.join(menus_path, '__pycache__')
    if os.path.exists(cache_path):
        import shutil
        shutil.rmtree(cache_path)
        print(f"✓ Кэш меню удален")
    else:
        print(f"  Кэш не найден (это нормально)")
except Exception as e:
    print(f"  Ошибка удаления кэша: {e}")

# 3. Перезагружаем аддон Sverchok
print("\n3. ПЕРЕЗАГРУЗКА АДДОНА SVERCHOK:")
try:
    # Отключаем
    bpy.ops.preferences.addon_disable(module='sverchok-master')
    print("✓ Аддон отключен")
    
    # Включаем
    bpy.ops.preferences.addon_enable(module='sverchok-master')
    print("✓ Аддон включен")
    
except Exception as e:
    print(f"✗ Ошибка перезагрузки: {e}")
    print("  Попробуйте перезагрузить аддон вручную:")
    print("  Edit > Preferences > Add-ons > Sverchok > Disable/Enable")

print("\n" + "=" * 70)
print("ПЕРЕЗАГРУЗКА ЗАВЕРШЕНА")
print("=" * 70)
print("\nТеперь:")
print("1. Откройте Sverchok")
print("2. Нажмите Add Node или Space")
print("3. Найдите категорию 'Renga'")
print("4. Там должны быть все 3 ноды!")
print("=" * 70)

