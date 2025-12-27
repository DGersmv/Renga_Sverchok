# 🎯 КРИТИЧНО: Добавление категории Renga в меню Sverchok

## 📍 ГДЕ НАХОДИТСЯ ФАЙЛ:

```
C:\Users\ВАШЕ_ИМЯ\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\menus\full_by_data_type.yaml
```

Или для Blender 4.2:
```
C:\Users\ВАШЕ_ИМЯ\AppData\Roaming\Blender Foundation\Blender\4.2\scripts\addons\sverchok-master\menus\full_by_data_type.yaml
```

---

## ✏️ ЧТО НУЖНО ДОБАВИТЬ:

### 1. Откройте файл `full_by_data_type.yaml` в текстовом редакторе

### 2. Найдите секцию с "Network" и "Pulga Physics"

Она должна выглядеть примерно так:
```yaml
- Network:
    - icon_name: NETWORK_DRIVE
    - extra_menu: ConnectionPartialMenu
    - SvNetworkNode
    # ... другие ноды Network

- Pulga Physics:
    - icon_name: PHYSICS
    - SvPulgaNode
    # ... другие ноды Pulga Physics
```

### 3. Добавьте секцию "Renga" МЕЖДУ "Network" и "Pulga Physics":

```yaml
- Network:
    - icon_name: NETWORK_DRIVE
    - extra_menu: ConnectionPartialMenu
    - SvNetworkNode
    # ... другие ноды Network

- Renga:
    - icon_name: NETWORK_DRIVE
    - SvRengaConnectNode
    - SvRengaCreateColumnsNode
    - SvRengaGetWallsNode

- Pulga Physics:
    - icon_name: PHYSICS
    - SvPulgaNode
    # ... другие ноды Pulga Physics
```

---

## 📝 ПОЛНЫЙ ПРИМЕР СЕКЦИИ:

```yaml
# ... предыдущие категории ...

- Network:
    - icon_name: NETWORK_DRIVE
    - extra_menu: ConnectionPartialMenu
    - SvNetworkNode
    # ... другие ноды Network

- Renga:
    - icon_name: NETWORK_DRIVE
    - SvRengaConnectNode
    - SvRengaCreateColumnsNode
    - SvRengaGetWallsNode

- Pulga Physics:
    - icon_name: PHYSICS
    - SvPulgaNode
    # ... другие ноды Pulga Physics

# ... следующие категории ...
```

---

## ✅ ПРОВЕРКА:

1. Сохраните файл
2. Перезапустите Blender ПОЛНОСТЬЮ
3. Откройте Sverchok (Shift+A в Node Editor)
4. Найдите категорию "Renga" в меню между "Network" и "Pulga Physics"

---

## ⚠️ ВАЖНО:

- **Отступы в YAML критичны!** Используйте пробелы (не табы)
- Каждая нода должна быть с дефисом `-` и правильным отступом
- Имя категории должно точно совпадать с `sv_category = "Renga"` в коде нод

---

## 🔧 АЛЬТЕРНАТИВНЫЙ СПОСОБ (если файл не найден):

Если файл `full_by_data_type.yaml` не существует или не содержит нужных секций, можно создать скрипт для автоматического добавления:

```python
import os
import yaml

# Путь к файлу меню
menu_path = r"C:\Users\ВАШЕ_ИМЯ\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\menus\full_by_data_type.yaml"

# Загрузить существующий YAML
with open(menu_path, 'r', encoding='utf-8') as f:
    menu_data = yaml.safe_load(f) or []

# Найти индекс "Network" или "Pulga Physics"
network_idx = None
pulga_idx = None

for i, item in enumerate(menu_data):
    if isinstance(item, dict):
        if 'Network' in item:
            network_idx = i
        elif 'Pulga Physics' in item:
            pulga_idx = i

# Добавить секцию Renga
renga_section = {
    'Renga': [
        {'icon_name': 'NETWORK_DRIVE'},
        'SvRengaConnectNode',
        'SvRengaCreateColumnsNode',
        'SvRengaGetWallsNode'
    ]
}

# Вставить после Network или перед Pulga Physics
if network_idx is not None:
    menu_data.insert(network_idx + 1, renga_section)
elif pulga_idx is not None:
    menu_data.insert(pulga_idx, renga_section)
else:
    # Добавить в конец, если не найдено
    menu_data.append(renga_section)

# Сохранить обратно
with open(menu_path, 'w', encoding='utf-8') as f:
    yaml.dump(menu_data, f, default_flow_style=False, allow_unicode=True)

print("✓ Секция Renga добавлена в меню!")
```

---

## 🎉 ПОСЛЕ ДОБАВЛЕНИЯ:

Категория "Renga" появится в меню Sverchok между "Network" и "Pulga Physics" и будет содержать все три ноды:
- Renga Connect
- Renga Create Columns  
- Renga Get Walls

