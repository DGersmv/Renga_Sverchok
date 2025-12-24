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
Renga integration nodes for Sverchok
Nodes are registered automatically by Sverchok's node system
"""

import os
import re

# Импортируем ноды для автоматической регистрации Sverchok
from . import renga_connect
from . import renga_create_columns
from . import renga_get_walls


def _add_category_to_menu():
    """
    Автоматически добавляет категорию 'Renga' в меню Sverchok
    Вызывается при импорте модуля
    """
    try:
        import bpy
        
        # Получаем путь к меню Sverchok
        blender_version_full = bpy.app.version_string
        blender_version = '.'.join(blender_version_full.split('.')[:2])  # "5.0.1" -> "5.0"
        
        menus_path = os.path.join(
            os.path.expanduser("~"),
            "AppData", "Roaming", "Blender Foundation", "Blender",
            blender_version, "scripts", "addons", "sverchok-master", "menus"
        )
        
        # Если папка не найдена, пробуем альтернативные пути
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
            else:
                # Папка не найдена - пропускаем
                return
        
        # Текст категории Renga
        renga_category_text = """- Renga:
    - icon_name: PLUGIN
    - extra_menu: ConnectionPartialMenu
    - SvRengaConnectNode
    - SvRengaCreateColumnsNode
    - SvRengaGetWallsNode
"""
        
        # Файлы меню для обновления
        menu_files = ['full_by_data_type.yaml', 'full_by_operations.yaml']
        
        for menu_file in menu_files:
            file_path = os.path.join(menus_path, menu_file)
            
            if not os.path.exists(file_path):
                continue
            
            try:
                # Читаем файл
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Проверяем, есть ли уже категория Renga
                if 'Renga:' in content and 'SvRengaConnectNode' in content:
                    continue  # Уже есть, пропускаем
                
                # Читаем построчно для вставки
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Ищем место для вставки (после "Network" или перед "Text")
                insert_index = len(lines)
                
                for i, line in enumerate(lines):
                    # Ищем категории, которые идут после Renga по алфавиту
                    if re.match(r'^- (Text|Transform|Vector|Viewer|Voronoi|Wave|Weave|Wrangle|Xsection):', line, re.IGNORECASE):
                        insert_index = i
                        break
                    # Ищем "Network" - вставим после неё
                    elif re.match(r'^- Network:', line, re.IGNORECASE):
                        # Находим конец этой категории
                        j = i + 1
                        while j < len(lines) and (lines[j].startswith(' ') or lines[j].strip() == ''):
                            j += 1
                        insert_index = j
                        break
                
                # Вставляем категорию
                lines.insert(insert_index, renga_category_text)
                
                # Сохраняем файл
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                
            except Exception as e:
                # Ошибка при обработке файла - пропускаем
                pass
                
    except Exception:
        # Ошибка при добавлении в меню - не критично, ноды всё равно зарегистрируются
        pass


# Автоматически добавляем категорию в меню при импорте
_add_category_to_menu()
