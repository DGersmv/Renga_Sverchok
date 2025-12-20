# Renga Integration Nodes for Sverchok

Интеграция между Sverchok (Blender) и Renga для автоматического размещения колонн в Renga на основе точек, заданных в Sverchok, и получения стен из Renga.

## Описание

Этот модуль предоставляет три ноды Sverchok для работы с Renga:

1. **Renga Connect** - подключение к TCP серверу Renga
2. **Renga Create Columns** - создание колонн в Renga из точек Sverchok
3. **Renga Get Walls** - получение стен из Renga в Sverchok

## Требования

- **Blender** с установленным аддоном **Sverchok**
- **Renga** с установленным плагином **RengaGH** (TCP сервер)
- **Python 3.x** (встроен в Blender)

## Установка

1. Скопируйте папку `renga` в `nodes/` директорию Sverchok:
   ```
   C:\Program Files\Renga Standard\RengaSDK\Sverchok\nodes\renga\
   ```

2. Перезапустите Blender

3. Ноды появятся в меню Sverchok в категории "Renga"

## Использование

### 1. Renga Connect

**Назначение**: Подключение к TCP серверу Renga

**Входы**:
- `Port` (Integer) - номер порта TCP сервера (по умолчанию 50100)
- `Connect` (Boolean) - включить/выключить подключение

**Выходы**:
- `Connected` (Boolean) - статус подключения
- `Message` (String) - сообщение о статусе/ошибке
- `Client` (Integer) - порт для использования в других нодах

**Использование**:
1. Добавьте ноду "Renga Connect" в дерево нод Sverchok
2. Укажите порт (по умолчанию 50100)
3. Установите `Connect = True`
4. Проверьте статус в выходе `Connected`

### 2. Renga Create Columns

**Назначение**: Создание колонн в Renga из точек Sverchok

**Входы**:
- `Points` (Vertices) - список точек для размещения колонн
- `RengaConnect` (String) - подключение к ноде "Renga Connect" (опционально)
- `Height` (Float) - высота колонн в миллиметрах (по умолчанию 3000)
- `Update` (Boolean) - триггер обновления (False->True)

**Выходы**:
- `Success` (Boolean) - успешность операции для каждой колонны
- `Message` (String) - сообщения о результате для каждой колонны
- `ColumnGuids` (String) - GUID колонн в Renga

**Использование**:
1. Добавьте ноду "Renga Create Columns"
2. Подключите точки из других нод Sverchok к входу `Points`
3. (Опционально) Подключите выход `Client` от ноды "Renga Connect"
4. Установите высоту колонн (по умолчанию 3000 мм)
5. Установите `Update = True` для отправки данных в Renga

**Важно**: 
- Колонны создаются на активном уровне в Renga
- При повторной отправке тех же точек (по GUID) колонны обновляются, а не создаются заново
- Для создания новых колонн используйте новые точки

### 3. Renga Get Walls

**Назначение**: Получение стен из Renga в Sverchok

**Входы**:
- `RengaConnect` (String) - подключение к ноде "Renga Connect" (опционально)
- `Update` (Boolean) - триггер обновления (False->True)

**Выходы**:
- `Success` (Boolean) - успешность операции
- `Message` (String) - сообщение о статусе
- `Baselines` (Curve) - базовые линии стен (кривые)
- `Meshes` (Mesh) - меш геометрия стен

**Использование**:
1. Добавьте ноду "Renga Get Walls"
2. (Опционально) Подключите выход `Client` от ноды "Renga Connect"
3. Установите `Update = True` для получения стен из Renga
4. Используйте выходы `Baselines` и `Meshes` для дальнейшей обработки

## Протокол связи

Ноды используют TCP/IP протокол с длиной сообщения:
- Формат: 4 байта (big-endian) длина + JSON данные
- Порт по умолчанию: 50100
- Host: 127.0.0.1 (localhost)

## Совместимость

- Совместимо с плагином RengaGH (C#) версии 1.0+
- Использует тот же протокол, что и интеграция Grasshopper-Renga
- Работает с существующим TCP сервером в Renga

## Примеры использования

### Пример 1: Создание колонн из точек

```
[Point Generator] -> [Renga Create Columns] -> [Renga Connect]
```

1. Создайте точки в Sverchok (например, через ноду "Point Generator")
2. Подключите точки к ноде "Renga Create Columns"
3. Подключите "Renga Connect" и установите `Connect = True`
4. Установите `Update = True` в "Renga Create Columns"
5. Колонны появятся в Renga

### Пример 2: Получение стен из Renga

```
[Renga Connect] -> [Renga Get Walls] -> [Mesh Viewer]
```

1. Подключите "Renga Connect" и установите `Connect = True`
2. Подключите к "Renga Get Walls"
3. Установите `Update = True` в "Renga Get Walls"
4. Стены появятся в Sverchok как кривые и меши

## Отладка

При возникновении проблем:

1. Проверьте, что плагин RengaGH запущен в Renga
2. Проверьте, что TCP сервер запущен (кнопка "Server Settings" в Renga)
3. Проверьте порт (по умолчанию 50100)
4. Проверьте сообщения об ошибках в выходах нод

## Лицензия

Copyright © 2025 Renga Software LLC. All rights reserved.

