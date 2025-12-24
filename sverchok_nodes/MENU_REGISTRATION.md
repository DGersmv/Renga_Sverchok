# Регистрация категории "Renga" в меню Sverchok

## Важно: Изменение меню Sverchok

Для того, чтобы ноды появились в категории "Renga" в меню Sverchok, необходимо добавить запись в файлы меню Sverchok.

## Расположение файлов меню

Файлы меню находятся в папке Sverchok:
```
C:\Users\[ВашеИмя]\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\menus\
```

## Файлы для изменения

Нужно добавить категорию "Renga" в следующие файлы:

### 1. `menus/index.yaml`

Добавьте в конец файла (или в соответствующее место по алфавиту):

```yaml
- Renga:
    icon_name: PLUGIN
    extra_menu: ConnectionPartialMenu
    - SvRengaConnectNode
    - SvRengaCreateColumnsNode
    - SvRengaGetWallsNode
```

### 2. `menus/full_by_data_type.yaml`

Добавьте в конец файла:

```yaml
- Renga:
    icon_name: PLUGIN
    extra_menu: ConnectionPartialMenu
    - SvRengaConnectNode
    - SvRengaCreateColumnsNode
    - SvRengaGetWallsNode
```

### 3. `menus/full_by_operations.yaml`

Добавьте в конец файла:

```yaml
- Renga:
    icon_name: PLUGIN
    extra_menu: ConnectionPartialMenu
    - SvRengaConnectNode
    - SvRengaCreateColumnsNode
    - SvRengaGetWallsNode
```

## Важные замечания

1. **Формат YAML**: Соблюдайте отступы (используйте пробелы, не табы)
2. **Имена нод**: Должны точно совпадать с `bl_idname` в файлах нод:
   - `SvRengaConnectNode` (из `renga_connect.py`)
   - `SvRengaCreateColumnsNode` (из `renga_create_columns.py`)
   - `SvRengaGetWallsNode` (из `renga_get_walls.py`)
3. **Иконка**: `PLUGIN` - стандартная иконка Blender для плагинов
4. **Меню**: `ConnectionPartialMenu` - подменю для нод подключения

## После изменения

1. Сохраните все три файла
2. Перезапустите Blender полностью
3. Откройте Sverchok
4. Нажмите "Add Node" или "Space" для поиска
5. Найдите категорию "Renga" в меню

## Альтернатива: Автоматическая регистрация

В некоторых версиях Sverchok ноды могут автоматически появляться в меню без изменения YAML файлов, если:
- Ноды правильно зарегистрированы (проверьте через `dir(bpy.types)`)
- У нод установлен `sv_category = "Renga"` (это уже сделано в файлах)
- Sverchok поддерживает автоматическое обнаружение категорий

## Проверка

После изменений проверьте:

1. **Регистрация нод**:
```python
import bpy
print('SvRengaConnectNode' in dir(bpy.types))
print('SvRengaCreateColumnsNode' in dir(bpy.types))
print('SvRengaGetWallsNode' in dir(bpy.types))
```

2. **Поиск в меню**: Нажмите Space в Sverchok и введите "Renga"

3. **Категория в меню**: Откройте меню добавления нод и найдите категорию "Renga"

## Известные проблемы

- **Blender 5.0 + Sverchok v1.4.0**: Могут быть проблемы с отображением категорий в меню. В этом случае используйте поиск (Space) для доступа к нодам.
- **Кэш меню**: Если меню не обновляется, удалите `__pycache__` в папке `menus/` и перезапустите Blender.

