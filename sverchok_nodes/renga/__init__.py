# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

"""
Renga Integration Nodes for Sverchok

Этот модуль содержит ноды для интеграции Sverchok с Renga:
- Renga Connect - подключение к TCP серверу Renga
- Renga Create Columns - создание колонн в Renga
- Renga Get Walls - получение стен из Renga
"""

import os
import pathlib

# КРИТИЧНО: Регистрируем ноды при импорте модуля, а не через register()
# Sverchok не вызывает register() из подпапок автоматически

def _add_to_menu_automatically():
    """Автоматически добавляет секцию Renga в меню Sverchok"""
    try:
        import bpy
        
        # Определяем путь к папке sverchok-master
        blender_version = f"{bpy.app.version[0]}.{bpy.app.version[1]}"
        user_home = pathlib.Path.home()
        sverchok_path = user_home / "AppData" / "Roaming" / "Blender Foundation" / "Blender" / blender_version / "scripts" / "addons" / "sverchok-master"
        
        if not os.path.exists(str(sverchok_path)):
            # Пробуем альтернативные версии
            for version in ["5.0", "4.2", "4.1", "4.0"]:
                test_path = user_home / "AppData" / "Roaming" / "Blender Foundation" / "Blender" / version / "scripts" / "addons" / "sverchok-master"
                if os.path.exists(str(test_path)):
                    sverchok_path = test_path
                    break
            else:
                print("Renga nodes: Папка sverchok-master не найдена, меню не будет обновлено")
                return
        
        sverchok_path = str(sverchok_path)
        menus_path = os.path.join(sverchok_path, "menus")
        print(f"Renga nodes: Найдена папка sverchok-master: {sverchok_path}")
        
        # Секция Renga для добавления (правильный формат YAML)
        renga_section_lines = [
            "- Renga:\n",
            "    - icon_name: NETWORK_DRIVE\n",
            "    - SvRengaConnectNode\n",
            "    - SvRengaCreateColumnsNode\n",
            "    - SvRengaGetWallsNode\n"
        ]
        
        # Файлы меню для обработки (index.yaml - главный файл!)
        menu_files = [
            ("index.yaml", sverchok_path),  # В корне
            ("full_by_data_type.yaml", menus_path),  # В папке menus
        ]
        
        processed_count = 0
        
        for menu_file, base_path in menu_files:
            menu_path = os.path.join(base_path, menu_file)
            
            if not os.path.exists(menu_path):
                continue  # Пропускаем, если файл не существует
            
            try:
                # Читаем файл
                with open(menu_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Проверяем, есть ли уже секция Renga
                if 'Renga:' in content:
                    # Для index.yaml - принудительно обновляем
                    if menu_file == "index.yaml":
                        print(f"Renga nodes: Обновление секции Renga в {menu_file}...")
                        # Удаляем старую секцию Renga (от "- Renga:" до следующей секции или конца)
                        import re
                        # Удаляем секцию Renga и все её элементы до следующей секции
                        content = re.sub(r'- Renga:.*?(?=\n- [A-Z]|\Z)', '', content, flags=re.DOTALL)
                    else:
                        print(f"Renga nodes: Секция Renga уже есть в {menu_file}")
                        continue
                
                # Читаем файл построчно для вставки
                with open(menu_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Просто добавляем в конец файла (перед последней пустой строкой, если есть)
                # Удаляем последние пустые строки
                while lines and not lines[-1].strip():
                    lines.pop()
                
                # Добавляем пустую строку и секцию Renga
                lines.append('\n')
                lines.extend(renga_section_lines)
                
                # Сохраняем
                with open(menu_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                
                print(f"Renga nodes: ✓ Секция Renga добавлена в {menu_file}")
                processed_count += 1
                    
            except Exception as e:
                print(f"Renga nodes: ОШИБКА при обработке {menu_file}: {e}")
                import traceback
                traceback.print_exc()
        
        if processed_count > 0:
            print(f"Renga nodes: Обработано файлов меню: {processed_count}")
                
    except Exception as e:
        print(f"Renga nodes: КРИТИЧЕСКАЯ ОШИБКА при добавлении в меню: {e}")
        import traceback
        traceback.print_exc()

def register():
    """Регистрация всех нод Renga (вызывается Sverchok автоматически)"""
    # НЕ регистрируем ноды здесь - Sverchok сам вызывает register() из каждого файла ноды
    # Мы только добавляем секцию в меню
    
    # АВТОМАТИЧЕСКИ добавляем в меню при регистрации модуля
    _add_to_menu_automatically()

# АВТОМАТИЧЕСКОЕ ДОБАВЛЕНИЕ В МЕНЮ ПРИ ИМПОРТЕ МОДУЛЯ
# Sverchok импортирует модули из подпапок и вызывает register() из файлов нод
# Мы используем это для добавления в меню
try:
    import bpy
    # Добавляем в меню при импорте (если bpy доступен)
    _add_to_menu_automatically()
except:
    pass  # Игнорируем ошибки при импорте (может быть вызвано до инициализации bpy)

def unregister():
    """Отмена регистрации всех нод Renga"""
    import bpy
    
    try:
        from . import renga_connect
        from . import renga_create_columns
        from . import renga_get_walls
        
        if hasattr(renga_get_walls, 'unregister'):
            renga_get_walls.unregister()
        if hasattr(renga_create_columns, 'unregister'):
            renga_create_columns.unregister()
        if hasattr(renga_connect, 'unregister'):
            renga_connect.unregister()
    except ImportError:
        try:
            import renga_connect
            import renga_create_columns
            import renga_get_walls
            
            if hasattr(renga_get_walls, 'unregister'):
                renga_get_walls.unregister()
            if hasattr(renga_create_columns, 'unregister'):
                renga_create_columns.unregister()
            if hasattr(renga_connect, 'unregister'):
                renga_connect.unregister()
        except:
            pass
