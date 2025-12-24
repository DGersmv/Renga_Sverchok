# КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ: Ошибка импорта Sverchok

## Проблема

Ошибка: `ModuleNotFoundError: No module named 'sverchok.nodes.sverchok_nodes'`

## Причина

Sverchok автоматически обнаруживает все папки в `nodes/` и пытается их импортировать. Если папка называется `sverchok_nodes`, Sverchok пытается импортировать `sverchok.nodes.sverchok_nodes`, что вызывает ошибку.

## Решение

**ВАЖНО**: Папка ДОЛЖНА называться `renga`, а НЕ `sverchok_nodes`!

### Правильная установка:

1. **Скопируйте папку `sverchok_nodes` из проекта**

2. **ПЕРЕИМЕНОВАТЬ её в `renga`** (обязательно!)

3. **Скопируйте переименованную папку `renga` в:**
   ```
   C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga\
   ```

4. **Итоговая структура должна быть:**
   ```
   sverchok-master/
     nodes/
       renga/              ← ВОТ ТАК, а НЕ sverchok_nodes!
         __init__.py
         renga_connect.py
         renga_create_columns.py
         renga_get_walls.py
         renga_client.py
         commands.py
         connection_protocol.py
         ...
   ```

5. **Удалите папку `sverchok_nodes` из `nodes/`** (если она там есть)

6. **Удалите `__pycache__`** в папке `renga` (если есть)

7. **Перезапустите Blender полностью**

## Проверка

После правильной установки:
1. Blender должен загрузиться без ошибок
2. Sverchok должен загрузиться
3. Ноды должны быть доступны через поиск (Space -> "Renga")

## Почему это важно?

Sverchok использует имя папки как имя модуля для импорта:
- `nodes/renga/` → импортирует как `sverchok.nodes.renga` ✅
- `nodes/sverchok_nodes/` → пытается импортировать как `sverchok.nodes.sverchok_nodes` ❌

Имя `sverchok_nodes` конфликтует с внутренней структурой Sverchok и вызывает ошибку импорта.

