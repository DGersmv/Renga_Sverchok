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

def _ensure_renga_category_in_menus():
    """
    Автоматически добавляет категорию 'Renga' в меню Sverchok при загрузке
    Проверяет и добавляет в index.yaml, full_by_data_type.yaml, full_by_operations.yaml
    """
    try:
        import bpy
        
        # Получаем путь к меню Sverchok
        blender_version_full = bpy.app.version_string
        blender_version = '.'.join(blender_version_full.split('.')[:2])  # "5.0.1" -> "5.0"

        addon_path = os.path.join(
            os.path.expanduser("~"),
            "AppData", "Roaming", "Blender Foundation", "Blender",
            blender_version, "scripts", "addons", "sverchok-master"
        )

        # Если папка не найдена, пробуем альтернативные пути
        if not os.path.exists(addon_path):
            for ver in ["5.0", "5", "4.0", "4"]:
                alt_path = os.path.join(
                    os.path.expanduser("~"),
                    "AppData", "Roaming", "Blender Foundation", "Blender",
                    ver, "scripts", "addons", "sverchok-master"
                )
                if os.path.exists(alt_path):
                    addon_path = alt_path
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
        menu_files = {
            'index.yaml': os.path.join(addon_path, 'index.yaml'),
            'full_by_data_type.yaml': os.path.join(addon_path, 'menus', 'full_by_data_type.yaml'),
            'full_by_operations.yaml': os.path.join(addon_path, 'menus', 'full_by_operations.yaml')
        }

        for menu_name, file_path in menu_files.items():
            if not os.path.exists(file_path):
                continue

            try:
                # Читаем файл
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = f.readlines()

                # Проверяем, есть ли уже категория Renga
                if 'Renga:' in content and 'SvRengaConnectNode' in content:
                    continue  # Уже есть, пропускаем

                # Удаляем старую секцию Renga если есть (на случай неправильного формата)
                new_lines = []
                skip_until_next_category = False
                for i, line in enumerate(lines):
                    if re.match(r'^- Renga:', line):
                        skip_until_next_category = True
                        continue
                    elif skip_until_next_category:
                        if re.match(r'^- [A-Z]', line) or (not line.startswith(' ') and line.strip() and not line.startswith('#')):
                            skip_until_next_category = False
                            new_lines.append(line)
                        # Пропускаем строки внутри секции Renga
                        continue
                    else:
                        new_lines.append(line)

                lines = new_lines

                # Ищем место для вставки (между Network и Pulga Physics)
                insert_index = len(lines)
                network_found = False

                for i, line in enumerate(lines):
                    if re.match(r'^- Network:', line):
                        network_found = True
                        # Находим конец секции Network
                        j = i + 1
                        while j < len(lines) and (lines[j].startswith(' ') or lines[j].strip() == '' or lines[j].startswith('#')):
                            j += 1
                        insert_index = j
                        break

                if not network_found:
                    # Если Network не найден, ищем Pulga Physics
                    for i, line in enumerate(lines):
                        if re.match(r'^- Pulga Physics:', line, re.IGNORECASE):
                            insert_index = i
                            break

                # Вставляем секцию Renga
                lines.insert(insert_index, renga_category_text)

                # Сохраняем файл
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

            except Exception as e:
                # Ошибка при обработке файла - пропускаем, не критично
                pass

    except Exception:
        # Ошибка при добавлении в меню - не критично, ноды всё равно зарегистрируются
        pass


# Импортируем ноды для автоматической регистрации Sverchok
# Sverchok автоматически вызовет register() на каждом модуле
from . import renga_connect
from . import renga_create_columns
from . import renga_get_walls

# Автоматически добавляем категорию в меню при импорте
# Вызываем только если bpy доступен (не во время начальной загрузки)
try:
    import bpy
    # Проверяем, что bpy полностью загружен
    if hasattr(bpy, 'app') and hasattr(bpy.app, 'version_string'):
        _ensure_renga_category_in_menus()
except:
    # bpy ещё не готов - это нормально, функция вызовется позже
    pass
