@echo off
chcp 65001 >nul
echo ======================================================================
echo ПОЛНОЕ ИСПРАВЛЕНИЕ УСТАНОВКИ НОД RENGA
echo ======================================================================
echo.

set SOURCE_DIR=%~dp0sverchok_nodes\renga
set TARGET_DIR=C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga

echo 1. Удаление старой папки...
if exist "%TARGET_DIR%" (
    rmdir /S /Q "%TARGET_DIR%"
)

echo 2. Создание новой папки...
mkdir "%TARGET_DIR%"

echo 3. Копирование ТОЛЬКО файлов нод (без README.md):
copy /Y "%SOURCE_DIR%\__init__.py" "%TARGET_DIR%\" >nul && echo   ✓ __init__.py
copy /Y "%SOURCE_DIR%\renga_connect.py" "%TARGET_DIR%\" >nul && echo   ✓ renga_connect.py
copy /Y "%SOURCE_DIR%\renga_create_columns.py" "%TARGET_DIR%\" >nul && echo   ✓ renga_create_columns.py
copy /Y "%SOURCE_DIR%\renga_get_walls.py" "%TARGET_DIR%\" >nul && echo   ✓ renga_get_walls.py
copy /Y "%SOURCE_DIR%\renga_client.py" "%TARGET_DIR%\" >nul && echo   ✓ renga_client.py
copy /Y "%SOURCE_DIR%\commands.py" "%TARGET_DIR%\" >nul && echo   ✓ commands.py
copy /Y "%SOURCE_DIR%\connection_protocol.py" "%TARGET_DIR%\" >nul && echo   ✓ connection_protocol.py

echo.
echo 4. Удаление кэша...
if exist "%TARGET_DIR%\__pycache__" (
    rmdir /S /Q "%TARGET_DIR%\__pycache__"
    echo   ✓ Кэш удален
)

echo.
echo ======================================================================
echo УСТАНОВКА ЗАВЕРШЕНА!
echo ======================================================================
echo.
echo Теперь:
echo 1. Полностью перезапустите Blender
echo 2. Подождите 10 секунд после загрузки
echo 3. Запустите скрипт CHECK_AND_FIX.py в Blender (Text Editor)
echo 4. Или проверьте меню Sverchok - категория "Renga" должна быть там
echo.
pause

