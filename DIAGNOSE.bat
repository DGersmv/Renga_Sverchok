@echo off
chcp 65001 >nul
echo ======================================================================
echo ДИАГНОСТИКА УСТАНОВКИ НОД RENGA
echo ======================================================================
echo.

set RENGA_DIR=C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga

echo 1. ПРОВЕРКА ФАЙЛОВ В ПАПКЕ RENGA:
echo.
if exist "%RENGA_DIR%" (
    echo ✓ Папка найдена: %RENGA_DIR%
    echo.
    echo Файлы в папке:
    dir /B "%RENGA_DIR%"
    echo.
) else (
    echo ✗ Папка НЕ найдена: %RENGA_DIR%
    echo.
    echo Скопируйте папку renga в:
    echo %RENGA_DIR%
    pause
    exit /b 1
)

echo.
echo 2. ПРОВЕРКА СОДЕРЖИМОГО __init__.py:
echo.
if exist "%RENGA_DIR%\__init__.py" (
    echo ✓ __init__.py найден
    findstr /C:"_add_category_to_menu" "%RENGA_DIR%\__init__.py" >nul
    if %ERRORLEVEL% EQU 0 (
        echo ✓ Функция автоматического добавления в меню найдена
    ) else (
        echo ✗ Функция автоматического добавления в меню НЕ найдена!
        echo   Нужно обновить __init__.py
    )
) else (
    echo ✗ __init__.py НЕ найден!
)

echo.
echo 3. ПРОВЕРКА МЕНЮ:
echo.
set MENUS_DIR=C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\menus

if exist "%MENUS_DIR%" (
    echo ✓ Папка меню найдена
    echo.
    for %%F in (full_by_data_type.yaml full_by_operations.yaml) do (
        set FILE_PATH=%MENUS_DIR%\%%F
        if exist "!FILE_PATH!" (
            echo Проверка %%F:
            findstr /C:"Renga:" "!FILE_PATH!" >nul
            if !ERRORLEVEL! EQU 0 (
                echo   ✓ Категория Renga найдена
            ) else (
                echo   ✗ Категория Renga НЕ найдена
            )
        ) else (
            echo   ⚠ Файл %%F не найден
        )
    )
) else (
    echo ✗ Папка меню не найдена: %MENUS_DIR%
)

echo.
echo ======================================================================
echo ДИАГНОСТИКА ЗАВЕРШЕНА
echo ======================================================================
echo.
echo Если файлы есть, но ноды не работают:
echo 1. Проверьте консоль Blender на ошибки
echo 2. Удалите __pycache__ в папке renga
echo 3. Полностью перезапустите Blender
echo.
pause

