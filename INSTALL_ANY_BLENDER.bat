@echo off
chcp 65001 >nul
echo ======================================================================
echo УСТАНОВКА НОД RENGA В ЛЮБОЙ BLENDER
echo ======================================================================
echo.

set SOURCE_DIR=%~dp0sverchok_nodes\renga
set BLENDER_VERSION=5.0

REM Проверяем наличие исходной папки
if not exist "%SOURCE_DIR%" (
    echo ✗ ОШИБКА: Папка не найдена: %SOURCE_DIR%
    echo.
    echo Убедитесь, что папка sverchok_nodes\renga существует!
    pause
    exit /b 1
)

echo Поиск папки Sverchok...
echo.

REM Пробуем найти папку Sverchok для разных версий Blender
set FOUND=0
for %%V in (5.0 5 4.0 4 3.6 3.5) do (
    set TARGET_DIR=%APPDATA%\Blender Foundation\Blender\%%V\scripts\addons\sverchok-master\nodes\renga
    if exist "%APPDATA%\Blender Foundation\Blender\%%V\scripts\addons\sverchok-master\nodes" (
        echo ✓ Найдена папка Sverchok для Blender %%V
        set FOUND=1
        set BLENDER_VERSION=%%V
        goto :install
    )
)

if %FOUND% EQU 0 (
    echo ✗ ОШИБКА: Sverchok не найден!
    echo.
    echo Установите аддон Sverchok в Blender сначала.
    echo Или укажите путь вручную в этом скрипте.
    pause
    exit /b 1
)

:install
set TARGET_DIR=%APPDATA%\Blender Foundation\Blender\%BLENDER_VERSION%\scripts\addons\sverchok-master\nodes\renga

echo.
echo Источник: %SOURCE_DIR%
echo Цель: %TARGET_DIR%
echo.

REM Удаляем старую папку
if exist "%TARGET_DIR%" (
    echo Удаление старой папки...
    rmdir /S /Q "%TARGET_DIR%"
)

REM Создаем новую папку
mkdir "%TARGET_DIR%"
echo.

echo Копирование файлов нод:
xcopy /E /I /Y "%SOURCE_DIR%\*" "%TARGET_DIR%\" >nul

if %ERRORLEVEL% EQU 0 (
    echo ✓ Файлы скопированы успешно!
    echo.
    echo Скопированы файлы:
    dir /B "%TARGET_DIR%"
    echo.
    echo ======================================================================
    echo УСТАНОВКА ЗАВЕРШЕНА!
    echo ======================================================================
    echo.
    echo Теперь нужно добавить категорию в меню:
    echo 1. Откройте Blender
    echo 2. Text Editor -^> New
    echo 3. Скопируйте содержимое файла ADD_TO_MENU.py из корня проекта
    echo 4. Run Script
    echo.
    echo Или добавьте вручную в файлы:
    echo %APPDATA%\Blender Foundation\Blender\%BLENDER_VERSION%\scripts\addons\sverchok-master\menus\
    echo.
    echo Добавьте в full_by_data_type.yaml и full_by_operations.yaml:
    echo.
    echo - Renga:
    echo     - icon_name: PLUGIN
    echo     - extra_menu: ConnectionPartialMenu
    echo     - SvRengaConnectNode
    echo     - SvRengaCreateColumnsNode
    echo     - SvRengaGetWallsNode
    echo.
    echo После этого перезапустите Blender!
    echo.
) else (
    echo ✗ ОШИБКА при копировании файлов!
)

pause

