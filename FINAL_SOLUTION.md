# ФИНАЛЬНОЕ РЕШЕНИЕ: Регистрация нод Renga в Sverchok

## Проблема
Ноды не появляются в меню Sverchok, несмотря на правильное расположение файлов.

## Решение

### Шаг 1: Убедитесь, что файлы на месте
```
C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga\
├── __init__.py              ← ДОЛЖЕН содержать функции register() и unregister()
├── renga_connect.py
├── renga_create_columns.py
├── renga_get_walls.py
├── renga_client.py
├── commands.py
└── connection_protocol.py
```

### Шаг 2: Проверьте __init__.py
Файл `__init__.py` должен содержать функции `register()` и `unregister()`, которые импортируют и регистрируют все ноды.

### Шаг 3: Явная регистрация через скрипт Blender
Если Sverchok не вызывает register() автоматически, выполните в консоли Python Blender:

```python
import bpy
import sys
import os

# Путь к нодам
renga_path = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga"

# Добавить путь в sys.path
sverchok_nodes_path = os.path.dirname(renga_path)
if sverchok_nodes_path not in sys.path:
    sys.path.insert(0, sverchok_nodes_path)

# Импорт и регистрация
try:
    import nodes.renga.renga_connect as rc
    import nodes.renga.renga_create_columns as rcc
    import nodes.renga.renga_get_walls as rgw
    
    rc.register()
    rcc.register()
    rgw.register()
    
    print("✓ Ноды зарегистрированы!")
    
    # Проверка
    print("Проверка:")
    print(f"  SvRengaConnectNode: {'SvRengaConnectNode' in dir(bpy.types)}")
    print(f"  SvRengaCreateColumnsNode: {'SvRengaCreateColumnsNode' in dir(bpy.types)}")
    print(f"  SvRengaGetWallsNode: {'SvRengaGetWallsNode' in dir(bpy.types)}")
    
except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc()
```

### Шаг 4: Проверка меню Sverchok
После регистрации:
1. Откройте Sverchok
2. Нажмите Add Node (или Space для поиска)
3. Найдите категорию "Renga"
4. Должны быть видны 3 ноды

### Шаг 5: Если ноды все еще не видны
Возможные причины:
1. **Sverchok не обновляет меню** - попробуйте перезапустить Blender
2. **Неправильная категория** - проверьте `sv_category = "Renga"` в каждом файле ноды
3. **Проблема с версией Sverchok** - обновите Sverchok до последней версии

### Альтернатива: Добавить в меню вручную
Если автоматическое обнаружение не работает, можно добавить ноды в меню Sverchok вручную через файл меню, но это требует изменения исходного кода Sverchok.

