"""
Быстрая проверка после загрузки Blender
Запустите в Blender ПОСЛЕ полной загрузки Sverchok
"""

import bpy
import time

print("=" * 70)
print("БЫСТРАЯ ПРОВЕРКА НОД RENGA")
print("=" * 70)

# Ждем загрузки
time.sleep(2)

# Проверка
nodes = ['SvRengaConnectNode', 'SvRengaCreateColumnsNode', 'SvRengaGetWallsNode']
found = 0

for node_name in nodes:
    if hasattr(bpy.types, node_name):
        print(f"✓ {node_name} ЗАРЕГИСТРИРОВАН")
        found += 1
    else:
        print(f"✗ {node_name} НЕ ЗАРЕГИСТРИРОВАН")

print(f"\nНайдено: {found}/{len(nodes)}")

if found == len(nodes):
    print("\n✓ ВСЕ НОДЫ ЗАРЕГИСТРИРОВАНЫ!")
    print("Проверьте меню Sverchok - категория 'Renga' должна быть там")
else:
    print("\n✗ НОДЫ НЕ ЗАРЕГИСТРИРОВАНЫ")
    print("Проверьте консоль Blender на ошибки при загрузке Sverchok")

