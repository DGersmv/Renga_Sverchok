# КРИТИЧЕСКОЕ РЕШЕНИЕ: Ноды не появляются в меню и поиске

## Проблема

Ноды регистрируются (видно в логах), но не появляются:
- ❌ Нет категории "Renga" в меню Add Node
- ❌ Ноды не появляются в поиске (Space)

## Решение

### Шаг 1: Добавить категорию в меню YAML

**ОБЯЗАТЕЛЬНО** нужно добавить категорию "Renga" в файлы меню Sverchok.

#### Автоматический способ (рекомендуется):

1. Откройте Blender
2. Перейдите в **Text Editor**
3. Создайте новый текст (New)
4. Скопируйте содержимое файла `ADD_TO_MENU.py` из папки `sverchok_nodes`
5. Запустите скрипт (Run Script или Alt+P)
6. Скрипт автоматически добавит категорию во все нужные файлы меню

#### Ручной способ:

Откройте файлы в папке:
```
C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\menus\
```

Добавьте в каждый из файлов (`index.yaml`, `full_by_data_type.yaml`, `full_by_operations.yaml`):

```yaml
- Renga:
    icon_name: PLUGIN
    extra_menu: ConnectionPartialMenu
    - SvRengaConnectNode
    - SvRengaCreateColumnsNode
    - SvRengaGetWallsNode
```

**Важно**: 
- Соблюдайте отступы (используйте пробелы, не табы)
- Добавьте в соответствующее место по алфавиту (между "Pulga Physics" и "Text")

### Шаг 2: Удалить кэш меню

1. Закройте Blender
2. Удалите папку `__pycache__` в:
   ```
   C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\menus\__pycache__\
   ```
3. Также удалите `__pycache__` в папке `nodes/renga/` (если есть)

### Шаг 3: Перезапустить Blender

**Полностью закройте и запустите Blender заново** (не просто перезагрузите аддон).

### Шаг 4: Проверка

1. Откройте Sverchok
2. Нажмите **Add Node** (или правой кнопкой мыши в редакторе нод)
3. Найдите категорию **"Renga"** в меню
4. Или нажмите **Space** и введите **"Renga"**

## Если ноды все еще не появляются

### Проверка регистрации:

Выполните в консоли Python Blender:

```python
import bpy

# Проверка регистрации
print("Проверка нод:")
print("SvRengaConnectNode:", hasattr(bpy.types, 'SvRengaConnectNode'))
print("SvRengaCreateColumnsNode:", hasattr(bpy.types, 'SvRengaCreateColumnsNode'))
print("SvRengaGetWallsNode:", hasattr(bpy.types, 'SvRengaGetWallsNode'))

# Проверка категории
if hasattr(bpy.types, 'SvRengaConnectNode'):
    node = bpy.types.SvRengaConnectNode
    print(f"Категория ноды: {getattr(node, 'sv_category', 'НЕТ')}")
```

### Альтернативный способ доступа к нодам:

Если меню не работает, можно добавить ноды через Python:

```python
import bpy

# Создать дерево нод Sverchok (если еще не создано)
tree = bpy.context.space_data.edit_tree
if tree and tree.bl_idname == 'SverchCustomTreeType':
    # Добавить ноду
    node = tree.nodes.new('SvRengaConnectNode')
    node.location = (0, 0)
    print("✓ Нода добавлена!")
```

## Важно

**Без добавления категории в YAML файлы меню ноды НЕ появятся в меню и поиске**, даже если они правильно зарегистрированы!

Это требование Sverchok - все категории должны быть явно указаны в файлах меню.

