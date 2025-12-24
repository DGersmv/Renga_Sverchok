"""
Глубокий анализ проблемы регистрации нод
"""

import bpy
import sys

print("=" * 70)
print("ГЛУБОКИЙ АНАЛИЗ РЕГИСТРАЦИИ НОД")
print("=" * 70)

# 1. Проверка всех нод Sverchok
print("\n1. ВСЕ НОДЫ SVERCHOK В bpy.types:")
sverchok_nodes = []
for attr_name in dir(bpy.types):
    if attr_name.startswith('Sv') and attr_name.endswith('Node'):
        sverchok_nodes.append(attr_name)

print(f"Найдено нод Sverchok: {len(sverchok_nodes)}")
print("Примеры (первые 10):")
for node in sverchok_nodes[:10]:
    print(f"  - {node}")

# 2. Проверка наших нод
print("\n2. ПРОВЕРКА НАШИХ НОД:")
our_nodes = ['SvRengaConnectNode', 'SvRengaCreateColumnsNode', 'SvRengaGetWallsNode']
for node_name in our_nodes:
    if node_name in sverchok_nodes:
        print(f"✓ {node_name} НАЙДЕН в списке нод Sverchok!")
        node_class = getattr(bpy.types, node_name)
        print(f"  bl_idname: {node_class.bl_idname}")
        print(f"  bl_label: {node_class.bl_label}")
    elif hasattr(bpy.types, node_name):
        print(f"⚠ {node_name} есть в bpy.types, но не в списке Sverchok")
        node_class = getattr(bpy.types, node_name)
        print(f"  bl_idname: {node_class.bl_idname}")
        print(f"  bl_label: {node_class.bl_label}")
    else:
        print(f"✗ {node_name} НЕ НАЙДЕН")

# 3. Попытка импорта и регистрации
print("\n3. ПРЯМОЙ ИМПОРТ И РЕГИСТРАЦИЯ:")
try:
    # Удаляем из кэша
    modules_to_clear = [
        'sverchok.nodes.renga',
        'sverchok.nodes.renga.renga_connect',
        'sverchok.nodes.renga.renga_create_columns',
        'sverchok.nodes.renga.renga_get_walls',
    ]
    
    for mod_name in modules_to_clear:
        if mod_name in sys.modules:
            del sys.modules[mod_name]
    
    # Импортируем
    from sverchok.nodes.renga import renga_connect, renga_create_columns, renga_get_walls
    
    print("✓ Модули импортированы")
    
    # Проверяем классы в модулях
    print("\n4. КЛАССЫ В МОДУЛЯХ:")
    if hasattr(renga_connect, 'SvRengaConnectNode'):
        cls = renga_connect.SvRengaConnectNode
        print(f"✓ SvRengaConnectNode найден в модуле")
        print(f"  bl_idname: {cls.bl_idname}")
        print(f"  bl_label: {cls.bl_label}")
        print(f"  MRO: {cls.__mro__}")
    
    # Регистрируем
    print("\n5. РЕГИСТРАЦИЯ:")
    try:
        renga_connect.register()
        print("✓ register() вызвана для renga_connect")
        
        # Сразу проверяем
        if hasattr(bpy.types, 'SvRengaConnectNode'):
            print("✓ SvRengaConnectNode СРАЗУ после register() найден в bpy.types!")
        else:
            print("✗ SvRengaConnectNode НЕ найден в bpy.types после register()")
            
    except Exception as e:
        print(f"✗ Ошибка регистрации: {e}")
        import traceback
        traceback.print_exc()
    
    # Проверяем через dir
    print("\n6. ПРОВЕРКА ЧЕРЕЗ dir(bpy.types):")
    all_types = dir(bpy.types)
    for node_name in our_nodes:
        if node_name in all_types:
            print(f"✓ {node_name} найден через dir()")
        else:
            print(f"✗ {node_name} НЕ найден через dir()")
    
    # Попытка создать ноду
    print("\n7. ПОПЫТКА СОЗДАТЬ НОДУ:")
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
            for area in bpy.context.screen.areas:
                if area.type == 'NODE_EDITOR':
                    space = area.spaces.active
                    if space and hasattr(space, 'tree_type'):
                        if space.tree_type == 'SverchCustomTreeType':
                            tree = space.edit_tree
                            break
        
        if tree:
            # Пробуем создать через bl_idname
            try:
                node = tree.nodes.new('SvRengaConnectNode')
                print(f"✓ НОДА СОЗДАНА через bl_idname! {node.bl_label}")
            except Exception as e1:
                print(f"✗ Ошибка создания через bl_idname: {e1}")
                
                # Пробуем через класс
                try:
                    node = tree.nodes.new(renga_connect.SvRengaConnectNode.bl_idname)
                    print(f"✓ НОДА СОЗДАНА через класс! {node.bl_label}")
                except Exception as e2:
                    print(f"✗ Ошибка создания через класс: {e2}")
        else:
            print("✗ Дерево Sverchok не найдено")
            
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        
except Exception as e:
    print(f"✗ Ошибка импорта: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("АНАЛИЗ ЗАВЕРШЕН")
print("=" * 70)

