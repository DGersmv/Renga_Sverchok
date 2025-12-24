"""
ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ МЕНЮ - Убедимся что ноды появляются в меню
"""

import bpy
import os
import re

print("=" * 70)
print("ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ МЕНЮ SVERCHOK")
print("=" * 70)

# 1. Проверяем bl_idname наших нод
print("\n1. ПРОВЕРКА bl_idname НАШИХ НОД:")
try:
    from sverchok.nodes.renga import renga_connect, renga_create_columns, renga_get_walls
    
    node_ids = {
        'SvRengaConnectNode': renga_connect.SvRengaConnectNode.bl_idname,
        'SvRengaCreateColumnsNode': renga_create_columns.SvRengaCreateColumnsNode.bl_idname,
        'SvRengaGetWallsNode': renga_get_walls.SvRengaGetWallsNode.bl_idname,
    }
    
    for class_name, bl_idname in node_ids.items():
        print(f"✓ {class_name}: bl_idname = '{bl_idname}'")
        
except Exception as e:
    print(f"✗ Ошибка проверки: {e}")
    import traceback
    traceback.print_exc()
    node_ids = {
        'SvRengaConnectNode': 'SvRengaConnectNode',
        'SvRengaCreateColumnsNode': 'SvRengaCreateColumnsNode',
        'SvRengaGetWallsNode': 'SvRengaGetWallsNode',
    }

# 2. Проверяем и исправляем меню
print("\n2. ПРОВЕРКА И ИСПРАВЛЕНИЕ МЕНЮ:")
try:
    blender_version_full = bpy.app.version_string
    blender_version = '.'.join(blender_version_full.split('.')[:2])
    
    menus_path = os.path.join(
        os.path.expanduser("~"),
        "AppData", "Roaming", "Blender Foundation", "Blender",
        blender_version, "scripts", "addons", "sverchok-master", "menus"
    )
    
    if not os.path.exists(menus_path):
        for ver in ["5.0", "5", "4.0", "4"]:
            alt_path = os.path.join(
                os.path.expanduser("~"),
                "AppData", "Roaming", "Blender Foundation", "Blender",
                ver, "scripts", "addons", "sverchok-master", "menus"
            )
            if os.path.exists(alt_path):
                menus_path = alt_path
                break
    
    if os.path.exists(menus_path):
        print(f"✓ Папка меню найдена: {menus_path}")
        
        menu_files = ['full_by_data_type.yaml', 'full_by_operations.yaml']
        
        for menu_file in menu_files:
            file_path = os.path.join(menus_path, menu_file)
            
            if not os.path.exists(file_path):
                print(f"⚠ Файл {menu_file} не найден")
                continue
            
            print(f"\nОбработка {menu_file}:")
            
            # Читаем файл
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = f.readlines() if hasattr(f, 'readlines') else content.split('\n')
            
            # Проверяем наличие категории Renga
            has_renga = 'Renga:' in content
            has_all_nodes = all(node_id in content for node_id in node_ids.values())
            
            if has_renga and has_all_nodes:
                print(f"  ✓ Категория Renga найдена со всеми нодами")
                
                # Проверяем формат
                renga_section = re.search(r'- Renga:.*?(?=\n- [A-Z]|\Z)', content, re.DOTALL)
                if renga_section:
                    section = renga_section.group(0)
                    print(f"  ✓ Секция найдена")
                    
                    # Проверяем каждую ноду
                    for class_name, bl_idname in node_ids.items():
                        if bl_idname in section:
                            print(f"    ✓ {bl_idname} найден в секции")
                        else:
                            print(f"    ✗ {bl_idname} НЕ найден в секции!")
                else:
                    print(f"  ⚠ Секция Renga не найдена в правильном формате")
            else:
                print(f"  ✗ Категория Renga не найдена или неполная")
                print(f"    has_renga: {has_renga}, has_all_nodes: {has_all_nodes}")
                
                # Исправляем
                print(f"  Исправляю...")
                
                # Читаем построчно
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Ищем место для вставки
                insert_index = len(lines)
                for i, line in enumerate(lines):
                    if re.match(r'^- (Text|Transform|Vector):', line, re.IGNORECASE):
                        insert_index = i
                        break
                    elif re.match(r'^- Network:', line, re.IGNORECASE):
                        j = i + 1
                        while j < len(lines) and (lines[j].startswith(' ') or lines[j].strip() == ''):
                            j += 1
                        insert_index = j
                        break
                
                # Создаем правильную секцию
                renga_section = f"""- Renga:
    - icon_name: PLUGIN
    - extra_menu: ConnectionPartialMenu
    - {node_ids['SvRengaConnectNode']}
    - {node_ids['SvRengaCreateColumnsNode']}
    - {node_ids['SvRengaGetWallsNode']}
"""
                
                # Вставляем
                lines.insert(insert_index, renga_section)
                
                # Сохраняем
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                
                print(f"  ✓ Категория Renga добавлена/обновлена")
    else:
        print(f"✗ Папка меню не найдена")
        
except Exception as e:
    print(f"✗ Ошибка: {e}")
    import traceback
    traceback.print_exc()

# 3. Проверяем, можно ли создать ноды
print("\n3. ПРОВЕРКА СОЗДАНИЯ НОД:")
try:
    # Ищем дерево
    tree = None
    for area in bpy.context.screen.areas:
        if area.type == 'NODE_EDITOR':
            space = area.spaces.active
            if space and hasattr(space, 'tree_type'):
                if space.tree_type == 'SverchCustomTreeType':
                    tree = space.edit_tree
                    if tree:
                        break
    
    if not tree:
        bpy.ops.node.new_node_tree(type='SverchCustomTreeType')
        import time
        time.sleep(1)
        for area in bpy.context.screen.areas:
            if area.type == 'NODE_EDITOR':
                space = area.spaces.active
                if space and hasattr(space, 'tree_type'):
                    if space.tree_type == 'SverchCustomTreeType':
                        tree = space.edit_tree
                        if tree:
                            break
    
    if tree and hasattr(tree, 'nodes'):
        print("✓ Дерево найдено")
        
        # Пробуем создать все три ноды
        created = []
        for class_name, bl_idname in node_ids.items():
            try:
                node = tree.nodes.new(bl_idname)
                created.append(f"✓ {bl_idname} создана: {node.bl_label}")
                tree.nodes.remove(node)
            except Exception as e:
                created.append(f"✗ {bl_idname} НЕ создана: {e}")
        
        for msg in created:
            print(f"  {msg}")
    else:
        print("✗ Дерево не найдено")
        
except Exception as e:
    print(f"✗ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("ИСПРАВЛЕНИЕ ЗАВЕРШЕНО")
print("=" * 70)
print("\nТеперь:")
print("1. Полностью перезапустите Blender")
print("2. Откройте Sverchok")
print("3. Нажмите Add Node или Space")
print("4. Найдите категорию 'Renga' - там должны быть все 3 ноды!")
print("=" * 70)

