"""
Простая проверка меню - без создания деревьев
"""

import bpy
import os

print("=" * 70)
print("ПРОВЕРКА МЕНЮ SVERCHOK")
print("=" * 70)

# Проверяем меню
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
        print(f"✓ Папка меню: {menus_path}\n")
        
        menu_files = ['full_by_data_type.yaml', 'full_by_operations.yaml']
        
        for menu_file in menu_files:
            file_path = os.path.join(menus_path, menu_file)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                print(f"{menu_file}:")
                if 'Renga:' in content:
                    print("  ✓ Категория 'Renga' найдена")
                    
                    # Проверяем ноды
                    nodes_found = []
                    for node in ['SvRengaConnectNode', 'SvRengaCreateColumnsNode', 'SvRengaGetWallsNode']:
                        if node in content:
                            nodes_found.append(node)
                            print(f"    ✓ {node}")
                        else:
                            print(f"    ✗ {node} НЕ найден")
                    
                    if len(nodes_found) == 3:
                        print(f"  ✓ Все 3 ноды найдены в меню!")
                    else:
                        print(f"  ⚠ Найдено только {len(nodes_found)} из 3 нод")
                else:
                    print("  ✗ Категория 'Renga' НЕ найдена")
            else:
                print(f"  ✗ Файл не найден: {menu_file}")
    else:
        print(f"✗ Папка меню не найдена")
        
except Exception as e:
    print(f"✗ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("ПРОВЕРКА ЗАВЕРШЕНА")
print("=" * 70)
print("\nЕсли все ноды найдены в меню, но не видны в Blender:")
print("1. Полностью перезапустите Blender")
print("2. Удалите кэш: menus/__pycache__ (если есть)")
print("3. Откройте Sverchok → Add Node → категория 'Renga'")
print("=" * 70)

