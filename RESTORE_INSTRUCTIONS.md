# БЫСТРОЕ ВОССТАНОВЛЕНИЕ - ВСЁ РАБОТАЛО!

## ✅ Файлы уже скопированы!

Файлы нод скопированы в:
```
C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga\
```

## 🔧 Осталось добавить категорию в меню

### Способ 1: Автоматический (в Blender)

1. Откройте Blender
2. Text Editor → New
3. Скопируйте **весь** файл `sverchok_nodes/ADD_TO_MENU.py`
4. Run Script (или Alt+P)
5. Скрипт добавит категорию во все файлы меню

### Способ 2: Ручной (быстрее)

Откройте эти 3 файла:
```
C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\menus\index.yaml
C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\menus\full_by_data_type.yaml
C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\menus\full_by_operations.yaml
```

В **каждый** файл добавьте (найдите место после "Pulga Physics" или перед "Text"):

```yaml
- Renga:
    icon_name: PLUGIN
    extra_menu: ConnectionPartialMenu
    - SvRengaConnectNode
    - SvRengaCreateColumnsNode
    - SvRengaGetWallsNode
```

**Важно**: Соблюдайте отступы (пробелы, не табы)!

## ✅ После добавления

1. Удалите `__pycache__` в папке `menus/` (если есть)
2. **Полностью перезапустите Blender**
3. Откройте Sverchok
4. Нажмите Add Node или Space
5. Найдите категорию "Renga"

## 🎯 Всё должно заработать!

Ноды уже регистрируются (видно в логах), просто нужно добавить категорию в меню - и всё вернется как было!

