# Renga_Sverchok Integration

Интеграция между Sverchok (Blender) и Renga для автоматического размещения колонн в Renga на основе точек, заданных в Sverchok, и получения стен из Renga.

## Описание проекта

Проект состоит из двух частей:
- **Плагин Renga** (C#) - TCP сервер, который принимает данные от Sverchok и создает/обновляет колонны, а также отправляет данные о стенах
- **Ноды Sverchok** (Python) - три ноды для подключения к Renga, создания колонн и получения стен

## Структура проекта

```
Renga_Sverchok/
├── RengaGH/              # Плагин для Renga (TCP сервер, C#)
│   ├── RengaPlugin.cs
│   ├── RengaGH.csproj
│   └── RengaGH.rndesc
├── sverchok_nodes/       # Ноды для Sverchok (Python)
│   ├── renga_connect.py
│   ├── renga_create_columns.py
│   ├── renga_get_walls.py
│   ├── renga_client.py
│   ├── connection_protocol.py
│   └── commands.py
├── Renga_Sverchok.sln    # Решение Visual Studio
└── build_solution.bat    # Скрипт для сборки
```

## Требования

- **Renga SDK** - установлен в стандартном месте
- **Blender** с установленным аддоном **Sverchok**
- **Visual Studio 2022** или новее (для сборки плагина Renga)
- **.NET 8.0** (для плагина Renga)
- **Python 3.x** (встроен в Blender)

## Сборка проекта

### Плагин Renga

1. Откройте `Renga_Sverchok.sln` в Visual Studio
2. Соберите решение (Build Solution) или запустите `build_solution.bat`
3. После сборки скопируйте `RengaGH.dll` и `RengaGH.rndesc` из `bin\Release\RengaGH\` в папку плагинов Renga
4. Перезапустите Renga

### Ноды Sverchok

#### Автоматическая установка (рекомендуется)

**Просто запустите скрипт установки:**

1. **Windows**: Двойной клик на `install.bat`
2. **Или в Blender**: Text Editor → скопируйте `install_renga_nodes.py` → Run Script
3. Перезапустите Blender полностью
4. Готово! Ноды появятся в категории "Renga" в меню Sverchok

Скрипт автоматически:
- ✅ Найдет папку Sverchok
- ✅ Скопирует все файлы в правильное место
- ✅ Добавит категорию "Renga" в меню
- ✅ Удалит старый кэш

#### Ручная установка (если автоматическая не работает)

1. Скопируйте папку `sverchok_nodes` из проекта
2. **ПЕРЕИМЕНОВАТЬ её в `renga`** (обязательно!)
3. Скопируйте переименованную папку `renga` в:
   ```
   %APPDATA%\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga\
   ```
4. Добавьте категорию в меню (см. `sverchok_nodes/MENU_REGISTRATION.md` или используйте `sverchok_nodes/ADD_TO_MENU.py`)
5. Перезапустите Blender

**Подробные инструкции**: см. `INSTALL.md`

## Использование

### В Renga:

1. Запустите Renga с установленным плагином RengaGH
2. Откройте меню плагина и нажмите "Server Settings"
3. Запустите TCP сервер на порту 50100 (по умолчанию)
4. Сервер будет принимать подключения от Sverchok

### В Sverchok (Blender):

1. Добавьте ноду **"Renga Connect"**:
   - Укажите порт (по умолчанию 50100)
   - Включите подключение (Connect = True)
2. Добавьте ноду **"Renga Create Columns"**:
   - Подключите точки (Points)
   - Подключите выход Client от ноды "Renga Connect" (опционально)
   - Установите высоту колонн (по умолчанию 3000 мм)
   - Установите Update = True для отправки данных в Renga
3. Добавьте ноду **"Renga Get Walls"**:
   - Подключите выход Client от ноды "Renga Connect" (опционально)
   - Установите Update = True для получения стен из Renga

## Функциональность

- ✅ Создание колонн в Renga на основе точек из Sverchok
- ✅ Отслеживание точек по GUID для обновления позиций
- ✅ Получение стен из Renga в Sverchok (кривые и меши)
- ✅ Не создает дубликаты колонн для существующих точек
- ✅ UI для настройки порта в Renga

## Технические детали

- **Протокол**: TCP/IP
- **Порт по умолчанию**: 50100
- **Формат данных**: JSON с длиной сообщения (4 байта big-endian + JSON)
- **Отслеживание**: GUID точек для синхронизации колонн

## Команды протокола

- `update_points` - создание/обновление колонн в Renga
- `get_walls` - получение стен из Renga

## Лицензия

Copyright © 2025 Renga Software LLC. All rights reserved.
