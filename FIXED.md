# ✅ ИСПРАВЛЕНО!

## Что было найдено и исправлено:

1. **Убрал `sv_category` из нод** - как у других нод Sverchok (например, UdpClientNode), категория определяется только в YAML файлах меню

2. **Исправил формат в меню** - добавил правильные отступы (тире перед `icon_name` и `extra_menu`), как у категории Network:
   ```yaml
   - Renga:
       - icon_name: PLUGIN
       - extra_menu: ConnectionPartialMenu
       - SvRengaConnectNode
       - SvRengaCreateColumnsNode
       - SvRengaGetWallsNode
   ```

3. **Обновил файлы нод** в папке `renga/` - убрал `sv_category`

## ✅ Теперь всё должно работать!

1. **Перезапустите Blender ПОЛНОСТЬЮ**
2. Откройте Sverchok
3. Нажмите **Add Node** или **Space**
4. Найдите категорию **"Renga"** в меню

Формат теперь точно такой же, как у категории Network, которая работает!

