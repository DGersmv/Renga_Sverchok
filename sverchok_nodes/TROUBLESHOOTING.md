# Устранение проблем с нодами Renga в Sverchok

## Проблема: Ноды не видны в меню Sverchok

### Решение 1: Перезагрузка аддона Sverchok

1. Откройте Blender
2. Перейдите в `Edit > Preferences > Add-ons`
3. Найдите "Sverchok" в списке
4. Снимите галочку (отключите аддон)
5. Поставьте галочку обратно (включите аддон)

### Решение 2: Проверка расположения файлов

Убедитесь, что папка `renga` находится в правильном месте:
```
C:\Program Files\Renga Standard\RengaSDK\Sverchok\nodes\renga\
```

Структура должна быть:
```
nodes/
  renga/
    __init__.py
    renga_connect.py
    renga_create_columns.py
    renga_get_walls.py
    renga_client.py
    commands.py
    connection_protocol.py
```

### Решение 3: Проверка регистрации нод

В консоли Blender (Window > Toggle System Console) проверьте наличие ошибок при загрузке аддона.

### Решение 4: Ручная проверка регистрации

В консоли Blender выполните:
```python
import bpy
# Проверка, зарегистрированы ли ноды
print('SvRengaConnectNode' in dir(bpy.types))
print('SvRengaCreateColumnsNode' in dir(bpy.types))
print('SvRengaGetWallsNode' in dir(bpy.types))
```

Если все три команды возвращают `True`, ноды зарегистрированы правильно.

### Решение 5: Проверка меню

Убедитесь, что в файле `menus/full_by_data_type.yaml` есть секция:
```yaml
- Renga:
    - icon_name: NETWORK_DRIVE
    - extra_menu: ConnectionPartialMenu
    - SvRengaConnectNode
    - SvRengaCreateColumnsNode
    - SvRengaGetWallsNode
```

### Решение 6: Очистка кэша Python

1. Закройте Blender
2. Удалите папку `__pycache__` в `nodes/renga/` (если есть)
3. Запустите Blender снова

### Решение 7: Проверка версии Sverchok

Убедитесь, что используется совместимая версия Sverchok (1.4.0 или новее).

