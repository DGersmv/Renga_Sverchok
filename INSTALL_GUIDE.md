# Инструкция по установке нод Renga для Sverchok

## Описание

Эта инструкция описывает процесс установки нод Renga в аддон Sverchok для Blender.

## Требования

- **Blender** (версия 5.0 или выше)
- **Sverchok** - установленный и активированный аддон
- **Renga** с установленным плагином RengaGH (TCP сервер)

## Пошаговая инструкция по установке

### Шаг 1: Найдите папку Sverchok

Откройте папку аддона Sverchok. Обычно она находится по пути:

```
C:\Users\<ВашеИмя>\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\
```

**Примечание:** Версия Blender может отличаться (например, 4.2, 4.3 и т.д.). Путь будет соответствующим.

### Шаг 2: Создайте папку `renga`

В папке `nodes\` создайте новую папку с именем `renga`:

```
C:\Users\<ВашеИмя>\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga\
```

### Шаг 3: Скопируйте файлы нод

Скопируйте **все файлы** из папки:

```
C:\Program Files\Renga Standard\RengaSDK\Samples\C#\Renga_Sverchok\sverchok_nodes\renga\
```

В папку, созданную на шаге 2:

```
C:\Users\<ВашеИмя>\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga\
```

**Файлы, которые должны быть скопированы:**
- `__init__.py`
- `renga_connect.py`
- `renga_create_columns.py`
- `renga_get_walls.py`
- `renga_client.py`
- `commands.py`
- `connection_protocol.py`

### Шаг 4: Проверьте структуру

После копирования структура должна выглядеть так:

```
C:\Users\<ВашеИмя>\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga\
├── __init__.py
├── renga_connect.py
├── renga_create_columns.py
├── renga_get_walls.py
├── renga_client.py
├── commands.py
└── connection_protocol.py
```

### Шаг 5: Перезапустите Blender

1. **Полностью закройте Blender** (если он был открыт)
2. **Запустите Blender заново**
3. Убедитесь, что аддон Sverchok активирован

### Шаг 6: Проверьте установку

#### Вариант A: Проверка через меню Sverchok

1. Откройте Sverchok (добавьте ноду в дерево нод)
2. Нажмите `Add Node` (или `Space` для поиска)
3. Найдите категорию **"Renga"** в меню
4. Должны быть видны три ноды:
   - **Renga Connect** - подключение к Renga
   - **Renga Create Columns** - создание колонн
   - **Renga Get Walls** - получение стен

#### Вариант B: Проверка через Python консоль

1. Откройте Blender
2. Перейдите в `Scripting` workspace
3. В консоли Python выполните:

```python
import bpy

# Проверка регистрации нод
print('SvRengaConnectNode' in dir(bpy.types))
print('SvRengaCreateColumnsNode' in dir(bpy.types))
print('SvRengaGetWallsNode' in dir(bpy.types))
```

Если все три команды возвращают `True` - ноды установлены правильно!

#### Вариант C: Использование скрипта проверки

1. Откройте файл `simple_check.py` в Text Editor Blender
2. Обновите путь в строке 13 (если нужно):
   ```python
   renga_path = r"C:\Users\<ВашеИмя>\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga"
   ```
3. Нажмите `Run Script` (Alt+P)
4. Проверьте вывод в консоли

## Автоматизация установки (опционально)

Для упрощения процесса можно использовать PowerShell скрипт. Создайте файл `install_to_sverchok.ps1`:

```powershell
# Установка нод Renga в Sverchok
$sourcePath = "C:\Program Files\Renga Standard\RengaSDK\Samples\C#\Renga_Sverchok\sverchok_nodes\renga"
$blenderVersion = "5.0"  # Измените на вашу версию Blender
$userName = $env:USERNAME
$targetPath = "C:\Users\$userName\AppData\Roaming\Blender Foundation\Blender\$blenderVersion\scripts\addons\sverchok-master\nodes\renga"

# Создать папку, если не существует
if (-not (Test-Path $targetPath)) {
    New-Item -ItemType Directory -Path $targetPath -Force
    Write-Host "Создана папка: $targetPath"
}

# Копировать файлы
Copy-Item -Path "$sourcePath\*" -Destination $targetPath -Recurse -Force
Write-Host "Файлы скопированы в: $targetPath"
Write-Host "Теперь перезапустите Blender!"
```

## Устранение проблем

### Проблема: Ноды не появляются в меню

**Решение 1:** Перезагрузите аддон Sverchok
1. `Edit > Preferences > Add-ons`
2. Найдите "Sverchok"
3. Снимите галочку (отключите)
4. Поставьте галочку обратно (включите)

**Решение 2:** Проверьте консоль Blender на ошибки
1. `Window > Toggle System Console`
2. Перезагрузите аддон Sverchok
3. Ищите ошибки импорта или регистрации

**Решение 3:** Удалите кэш Python
1. Закройте Blender
2. Удалите папку `__pycache__` в `nodes\renga\` (если есть)
3. Запустите Blender заново

**Решение 4:** Проверьте версию Sverchok
- Убедитесь, что используется совместимая версия Sverchok
- Рекомендуется последняя стабильная версия

### Проблема: Ошибки импорта в консоли

Если видите ошибки типа `ImportError` или `ModuleNotFoundError`:
1. Проверьте, что все файлы скопированы правильно
2. Убедитесь, что файл `__init__.py` присутствует в папке `renga`
3. Проверьте, что пути к файлам корректны

### Проблема: Blender падает при загрузке

1. Проверьте версию Blender и Sverchok на совместимость
2. Попробуйте с Blender 4.x для проверки
3. Обновите Sverchok до последней версии

## Пример использования

После успешной установки:

1. **В Renga:**
   - Запустите Renga с плагином RengaGH
   - Откройте меню плагина → "Server Settings"
   - Запустите TCP сервер на порту 50100

2. **В Sverchok (Blender):**
   - Добавьте ноду **"Renga Connect"**
   - Установите `Port = 50100` и `Connect = True`
   - Добавьте ноду **"Renga Create Columns"**
   - Подключите точки и установите `Update = True`
   - Добавьте ноду **"Renga Get Walls"**
   - Установите `Update = True` для получения стен

## Дополнительная информация

- Подробная документация по нодам: `sverchok_nodes/README.md`
- Устранение проблем: `sverchok_nodes/TROUBLESHOOTING.md`
- Проверка установки: `simple_check.py`

## Контакты

При возникновении проблем:
1. Проверьте консоль Blender на ошибки
2. Укажите версию Blender и Sverchok
3. Опишите шаги, которые вы выполнили

