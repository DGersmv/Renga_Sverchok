# Ноды Renga для Sverchok

Готовый плагин для установки в любой Blender с Sverchok.

## Установка

### Автоматическая установка (Windows)

1. Запустите `INSTALL_RENGA.bat` из корня проекта
2. Скрипт автоматически найдет папку Sverchok и скопирует файлы
3. Перезапустите Blender

### Ручная установка

1. Скопируйте всю папку `renga` в:
   ```
   %APPDATA%\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga\
   ```
   
   Или для Blender 4.x:
   ```
   %APPDATA%\Blender Foundation\Blender\4.0\scripts\addons\sverchok-master\nodes\renga\
   ```

2. Добавьте категорию "Renga" в меню Sverchok (см. ниже)

3. Перезапустите Blender

## Добавление категории в меню

Откройте файлы меню Sverchok:
```
%APPDATA%\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\menus\
```

Добавьте в `full_by_data_type.yaml` и `full_by_operations.yaml`:

```yaml
- Renga:
    - icon_name: PLUGIN
    - extra_menu: ConnectionPartialMenu
    - SvRengaConnectNode
    - SvRengaCreateColumnsNode
    - SvRengaGetWallsNode
```

Или используйте скрипт `ADD_TO_MENU.py` из корня проекта.

## Проверка

После установки:
1. Откройте Blender
2. Откройте Sverchok
3. Нажмите Add Node или Space
4. Найдите категорию "Renga"

## Файлы в плагине

- `__init__.py` - инициализация модуля
- `renga_connect.py` - нода подключения к Renga
- `renga_create_columns.py` - нода создания колонн
- `renga_get_walls.py` - нода получения стен
- `renga_client.py` - TCP клиент
- `commands.py` - команды для Renga
- `connection_protocol.py` - протокол связи

