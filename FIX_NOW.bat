@echo off
echo ======================================================================
echo БЫСТРОЕ ВОССТАНОВЛЕНИЕ НОД RENGA
echo ======================================================================
echo.

REM Копируем файлы
echo Копирование файлов...
if not exist "sverchok_nodes" (
    echo ОШИБКА: Папка sverchok_nodes не найдена!
    echo Убедитесь, что вы запускаете скрипт из папки проекта
    pause
    exit /b 1
)

set TARGET_DIR=C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga

REM Удаляем старую папку
if exist "%TARGET_DIR%" (
    echo Удаление старой папки...
    rmdir /S /Q "%TARGET_DIR%"
)

REM Копируем новую
echo Копирование файлов в %TARGET_DIR%...
xcopy /E /I /Y "sverchok_nodes" "%TARGET_DIR%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================================
    echo ФАЙЛЫ СКОПИРОВАНЫ!
    echo ======================================================================
    echo.
    echo Теперь нужно добавить категорию в меню:
    echo 1. Откройте Blender
    echo 2. Text Editor -^> New
    echo 3. Скопируйте содержимое файла sverchok_nodes\ADD_TO_MENU.py
    echo 4. Run Script
    echo.
    echo Или добавьте вручную в файлы:
    echo C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\menus\
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
) else (
    echo.
    echo ОШИБКА при копировании файлов!
)

pause

