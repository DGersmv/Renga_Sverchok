# Проверка регистрации нод Renga

## ✅ Важно: Ноды работают!

Если вы видите в консоли Blender сообщения:
```
Info: Registering node class: 'SvRengaConnectNode'...
Info: Registering node class: 'SvRengaCreateColumnsNode'...
Info: Registering node class: 'SvRengaGetWallsNode'...
```

**Это означает, что ноды успешно зарегистрированы Sverchok!**

## Проверка после загрузки Sverchok

После полной загрузки Sverchok выполните в консоли Python Blender:

```python
import bpy

# Проверка регистрации
print("Проверка нод Renga:")
print("SvRengaConnectNode:", hasattr(bpy.types, 'SvRengaConnectNode'))
print("SvRengaCreateColumnsNode:", hasattr(bpy.types, 'SvRengaCreateColumnsNode'))
print("SvRengaGetWallsNode:", hasattr(bpy.types, 'SvRengaGetWallsNode'))
```

Если все три команды возвращают `True` - ноды зарегистрированы!

## Поиск нод в Sverchok

1. Откройте Sverchok в Blender
2. Нажмите **Space** (или кнопку поиска)
3. Введите **"Renga"** или **"SvRenga"**
4. Ноды должны появиться в результатах поиска

## Известные проблемы

### Ошибка `NODE_OT_tree_importer`

Ошибка:
```
ValueError: bpy_struct "NODE_OT_tree_importer" registration error: 'io_panel_properties' PointerProperty...
```

**Это известная проблема Sverchok с Blender 5.0**, не связанная с нашими нодами. Она не влияет на работу нод Renga.

### Скрипт проверки показывает "не зарегистрированы"

Если скрипт `FORCE_MENU.py` показывает, что ноды не зарегистрированы, но в логе Sverchok видно их регистрацию - это нормально. Скрипт проверяет до полной загрузки Sverchok.

**Решение**: Проверьте ноды после полной загрузки Sverchok через поиск (Space -> "Renga").

## Итог

Если в логе Sverchok видно регистрацию нод - всё работает! Используйте поиск в Sverchok для доступа к нодам.

