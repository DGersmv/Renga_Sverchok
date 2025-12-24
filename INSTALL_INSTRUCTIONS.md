# Инструкция по установке нод Renga для Sverchok

## 📦 Исходные файлы

Все файлы находятся в папке проекта:
```
C:\Program Files\Renga Standard\RengaSDK\Samples\C#\Renga_Sverchok\sverchok_nodes\
```

## 🚀 Установка на любой компьютер с Blender

### Шаг 1: Найдите папку Sverchok

Путь зависит от версии Blender:
- **Blender 5.0**: `%APPDATA%\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\`
- **Blender 4.x**: `%APPDATA%\Blender Foundation\Blender\4.x\scripts\addons\sverchok-master\nodes\`
- **Blender 3.x**: `%APPDATA%\Blender Foundation\Blender\3.x\scripts\addons\sverchok-master\nodes\`

Или полный путь:
```
C:\Users\[ВашеИмя]\AppData\Roaming\Blender Foundation\Blender\[Версия]\scripts\addons\sverchok-master\nodes\
```

### Шаг 2: Скопируйте папку renga

1. Скопируйте **всю папку** `sverchok_nodes` из проекта
2. Переименуйте её в `renga`
3. Вставьте в папку `nodes\` Sverchok

**Итоговая структура должна быть:**
```
sverchok-master/
  nodes/
    renga/                    ← ВОТ СЮДА
      __init__.py
      renga_connect.py
      renga_create_columns.py
      renga_get_walls.py
      renga_client.py
      commands.py
      connection_protocol.py
      README.md
      TROUBLESHOOTING.md
```

### Шаг 3: Удалите кэш Python

Удалите папку `__pycache__` в `nodes\renga\` (если есть)

### Шаг 4: Перезапустите Blender

Полностью закройте и запустите Blender заново.

### Шаг 5: Проверьте регистрацию

Выполните в консоли Python Blender (Text Editor > Run Script):

```python
import bpy
print("Проверка нод:")
print("SvRengaConnectNode:", 'SvRengaConnectNode' in dir(bpy.types))
print("SvRengaCreateColumnsNode:", 'SvRengaCreateColumnsNode' in dir(bpy.types))
print("SvRengaGetWallsNode:", 'SvRengaGetWallsNode' in dir(bpy.types))
```

Если все три команды вернут `True` - ноды зарегистрированы.

### Шаг 6: Поиск нод в Sverchok

Если ноды зарегистрированы, но не видны в меню:
1. Откройте Sverchok
2. Нажмите **Space** (или кнопку поиска)
3. Введите **"Renga"** или **"SvRenga"**
4. Ноды должны появиться в результатах поиска

## ⚠️ Если ноды не регистрируются автоматически

Выполните скрипт регистрации (скопируйте в Text Editor Blender):

```python
import bpy
import sys
import os
import importlib.util

# Путь к нодам (ИЗМЕНИТЕ ПОД СВОЙ ПУТЬ!)
renga_path = r"C:\Users\[ВашеИмя]\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga"
sverchok_path = os.path.dirname(os.path.dirname(renga_path))
nodes_path = os.path.dirname(renga_path)

# Добавить пути
for path in [sverchok_path, nodes_path]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Создать фиктивные модули
if "nodes" not in sys.modules:
    nodes_module = type(sys)('nodes')
    nodes_module.__path__ = [nodes_path]
    sys.modules["nodes"] = nodes_module

if "nodes.renga" not in sys.modules:
    renga_module = type(sys)('nodes.renga')
    renga_module.__path__ = [renga_path]
    sys.modules["nodes.renga"] = renga_module

# Регистрация
nodes_info = [
    ("renga_connect.py", "SvRengaConnectNode", "nodes.renga.renga_connect"),
    ("renga_create_columns.py", "SvRengaCreateColumnsNode", "nodes.renga.renga_create_columns"),
    ("renga_get_walls.py", "SvRengaGetWallsNode", "nodes.renga.renga_get_walls")
]

for filename, class_name, module_path in nodes_info:
    try:
        if module_path in sys.modules:
            del sys.modules[module_path]
        module = __import__(module_path, fromlist=[class_name])
        node_class = getattr(module, class_name)
        if class_name in dir(bpy.types):
            try:
                bpy.utils.unregister_class(getattr(bpy.types, class_name))
            except:
                pass
        bpy.utils.register_class(node_class)
        print(f"✓ {class_name} зарегистрирован")
    except Exception as e:
        print(f"✗ {class_name}: {e}")

# Проверка
print("\nПроверка:")
for filename, class_name, module_path in nodes_info:
    print(f"{class_name}: {'✓' if class_name in dir(bpy.types) else '✗'}")
```

## 📝 Важные замечания

1. **Все файлы должны быть в папке `sverchok_nodes` проекта** - это исходная папка для копирования
2. **Папка должна называться `renga`** в Sverchok (не `sverchok_nodes`)
3. **Удаляйте `__pycache__`** после каждого копирования
4. **Перезапускайте Blender полностью** после установки

## 🔧 Совместимость

- ✅ Blender 5.0 + Sverchok v1.4.0 (может быть проблема с меню)
- ✅ Blender 4.x + Sverchok (должно работать)
- ✅ Blender 3.x + Sverchok (должно работать)

Если ноды не видны в меню, но зарегистрированы - используйте поиск (Space) в Sverchok.


