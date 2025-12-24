# Инструкция по установке нод Renga для Sverchok

## Проблема: Ноды не появляются в меню или Blender падает

### Шаг 1: Проверьте структуру файлов

Убедитесь, что файлы скопированы правильно:

```
C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga\
├── __init__.py              ← ОБЯЗАТЕЛЬНО должен быть
├── renga_connect.py
├── renga_create_columns.py
├── renga_get_walls.py
├── renga_client.py
├── commands.py
├── connection_protocol.py
└── README.md
```

### Шаг 2: Удалите кэш Python

1. Закройте Blender полностью
2. Удалите папку `__pycache__` в `nodes\renga\` (если есть)
3. Также удалите файлы `.pyc` если они есть

### Шаг 3: Проверьте консоль Blender на ошибки

1. Запустите Blender
2. Откройте консоль: `Window > Toggle System Console` (или `Window > Toggle System Console` в меню)
3. Перезагрузите аддон Sverchok:
   - `Edit > Preferences > Add-ons`
   - Найдите "Sverchok"
   - Снимите галочку (отключите)
   - Поставьте галочку обратно (включите)
4. Смотрите в консоль - должны появиться сообщения:
   - `Renga nodes: Registered renga_connect`
   - `Renga nodes: Registered renga_create_columns`
   - `Renga nodes: Registered renga_get_walls`

Если видите ошибки - скопируйте их и сообщите разработчику.

### Шаг 4: Проверьте регистрацию нод вручную

В консоли Python Blender (или в Text Editor > Python консоль) выполните:

```python
import bpy

# Проверка регистрации
print('SvRengaConnectNode' in dir(bpy.types))
print('SvRengaCreateColumnsNode' in dir(bpy.types))
print('SvRengaGetWallsNode' in dir(bpy.types))
```

Если все три команды возвращают `True` - ноды зарегистрированы правильно.

### Шаг 5: Проверьте меню Sverchok

1. Откройте Sverchok (добавьте ноду в дерево нод)
2. Нажмите `Add Node` (или `Space` для поиска)
3. Найдите категорию "Renga" в меню
4. Должны быть видны три ноды:
   - Renga Connect
   - Renga Create Columns
   - Renga Get Walls

### Если ноды все еще не появляются

#### Вариант A: Проблема с автоматической регистрацией

В некоторых версиях Sverchok ноды регистрируются автоматически. Попробуйте:

1. Убедитесь, что в `__init__.py` есть функции `register()` и `unregister()`
2. Попробуйте явно вызвать регистрацию в консоли Python:

```python
import sys
import os

# Добавьте путь к нодам
nodes_path = r"C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes"
if nodes_path not in sys.path:
    sys.path.insert(0, nodes_path)

# Импортируйте и зарегистрируйте
from renga import renga_connect, renga_create_columns, renga_get_walls
renga_connect.register()
renga_create_columns.register()
renga_get_walls.register()
```

#### Вариант B: Проблема с версией Sverchok

Убедитесь, что используется совместимая версия Sverchok:
- Минимальная версия: 1.4.0
- Рекомендуемая: последняя стабильная версия

#### Вариант C: Проблема с Blender 5.0

Blender 5.0 может иметь изменения в API. Если проблема сохраняется:
1. Попробуйте с Blender 4.x для проверки
2. Или обновите Sverchok до последней версии, совместимой с Blender 5.0

### Отладка ошибок импорта

Если видите ошибки импорта в консоли, проверьте:

1. **Ошибка импорта `sverchok.utils.curve`**:
   - Это нормально для некоторых версий Sverchok
   - Ноды должны работать, но кривые будут возвращаться как списки точек

2. **Ошибка импорта `mathutils`**:
   - Это встроенный модуль Blender
   - Если его нет - проблема с установкой Blender

3. **Ошибка импорта `bpy`**:
   - Это основной модуль Blender
   - Если его нет - вы не в контексте Blender

### Контакты для поддержки

Если проблема не решена:
1. Скопируйте полный лог ошибок из консоли Blender
2. Укажите версию Blender и Sverchok
3. Опишите шаги, которые вы выполнили


