@echo off
chcp 65001 >nul
echo ======================================================================
echo КОПИРОВАНИЕ ТОЛЬКО ФАЙЛОВ НОД В RENGA
echo ======================================================================
echo.

set SOURCE_DIR=%~dp0sverchok_nodes
set TARGET_DIR=C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga

echo Источник: %SOURCE_DIR%
echo Цель: %TARGET_DIR%
echo.

REM Создаем папку если нет
if not exist "%TARGET_DIR%" (
    mkdir "%TARGET_DIR%"
    echo Создана папка: %TARGET_DIR%
)

REM Удаляем старую папку полностью
if exist "%TARGET_DIR%" (
    echo Удаление старой папки...
    rmdir /S /Q "%TARGET_DIR%"
)

REM Создаем новую папку
mkdir "%TARGET_DIR%"
echo.

echo Копирование ТОЛЬКО файлов нод:
echo.

REM Копируем ТОЛЬКО нужные файлы
copy /Y "%SOURCE_DIR%\__init__.py" "%TARGET_DIR%\" >nul && echo ✓ __init__.py
copy /Y "%SOURCE_DIR%\renga_connect.py" "%TARGET_DIR%\" >nul && echo ✓ renga_connect.py
copy /Y "%SOURCE_DIR%\renga_create_columns.py" "%TARGET_DIR%\" >nul && echo ✓ renga_create_columns.py
copy /Y "%SOURCE_DIR%\renga_get_walls.py" "%TARGET_DIR%\" >nul && echo ✓ renga_get_walls.py
copy /Y "%SOURCE_DIR%\renga_client.py" "%TARGET_DIR%\" >nul && echo ✓ renga_client.py
copy /Y "%SOURCE_DIR%\commands.py" "%TARGET_DIR%\" >nul && echo ✓ commands.py
copy /Y "%SOURCE_DIR%\connection_protocol.py" "%TARGET_DIR%\" >nul && echo ✓ connection_protocol.py

echo.
echo ======================================================================
echo КОПИРОВАНИЕ ЗАВЕРШЕНО!
echo ======================================================================
echo.
echo В папке renga теперь ТОЛЬКО файлы нод:
echo   - __init__.py
echo   - renga_connect.py
echo   - renga_create_columns.py
echo   - renga_get_walls.py
echo   - renga_client.py
echo   - commands.py
echo   - connection_protocol.py
echo.
echo НЕ скопированы (и правильно!):
echo   - ADD_TO_MENU.py (скрипт установки, не нода)
echo   - FORCE_MENU.py (скрипт установки, не нода)
echo   - Все .md файлы (документация)
echo   - Все .txt файлы
echo.
echo Теперь перезапустите Blender - всё должно работать!
echo.
pause

