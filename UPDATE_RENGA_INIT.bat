@echo off
echo ========================================
echo ОБНОВЛЕНИЕ __init__.py ДЛЯ АВТОМАТИЧЕСКОГО МЕНЮ
echo ========================================
echo.

set "SOURCE=%~dp0sverchok_nodes\renga\__init__.py"
set "TARGET=%APPDATA%\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga\__init__.py"

if not exist "%SOURCE%" (
    echo ОШИБКА: Исходный файл не найден!
    echo Путь: %SOURCE%
    pause
    exit /b 1
)

echo Копируем обновленный __init__.py...
echo.
echo Из: %SOURCE%
echo В:  %TARGET%
echo.

REM Проверяем существование целевой папки
for %%F in ("%TARGET%") do set "TARGET_DIR=%%~dpF"
if not exist "%TARGET_DIR%" (
    echo ОШИБКА: Целевая папка не найдена!
    echo Путь: %TARGET_DIR%
    pause
    exit /b 1
)

copy /Y "%SOURCE%" "%TARGET%"
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo УСПЕШНО!
    echo ========================================
    echo.
    echo Файл __init__.py обновлен.
    echo Теперь при каждом запуске Blender категория Renga
    echo будет автоматически добавляться в меню, если её нет.
    echo.
    echo Перезапустите Blender для применения изменений.
    echo.
) else (
    echo.
    echo ОШИБКА: Не удалось скопировать файл!
    echo.
)

pause

