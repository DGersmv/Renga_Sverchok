@echo off
chcp 65001 >nul
echo ======================================================================
echo ВОССТАНОВЛЕНИЕ НОД RENGA
echo ======================================================================
echo.

set TARGET=C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga

echo 1. Копирование файлов...
if exist "%TARGET%" rmdir /S /Q "%TARGET%"
xcopy /E /I /Y "sverchok_nodes" "%TARGET%"

echo.
echo 2. Файлы скопированы в: %TARGET%
echo.
echo 3. Теперь нужно добавить категорию в меню:
echo    - Откройте Blender
echo    - Text Editor ^> New
echo    - Скопируйте содержимое файла: sverchok_nodes\ADD_TO_MENU.py
echo    - Run Script
echo.
echo ИЛИ добавьте вручную в 3 файла:
echo    C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\menus\
echo.
echo Добавьте в index.yaml, full_by_data_type.yaml, full_by_operations.yaml:
echo.
echo - Renga:
echo     icon_name: PLUGIN
echo     extra_menu: ConnectionPartialMenu
echo     - SvRengaConnectNode
echo     - SvRengaCreateColumnsNode
echo     - SvRengaGetWallsNode
echo.
echo 4. Перезапустите Blender ПОЛНОСТЬЮ
echo.
pause

