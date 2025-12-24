@echo off
REM Автоматическая установка нод Renga для Sverchok
REM Запустите этот файл двойным кликом

echo ======================================================================
echo АВТОМАТИЧЕСКАЯ УСТАНОВКА НОД RENGA ДЛЯ SVERCHOK
echo ======================================================================
echo.

REM Находим Blender
set BLENDER_PATH=
if exist "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" (
    set BLENDER_PATH=C:\Program Files\Blender Foundation\Blender 5.0\blender.exe
) else if exist "C:\Program Files\Blender Foundation\Blender 4.0\blender.exe" (
    set BLENDER_PATH=C:\Program Files\Blender Foundation\Blender 4.0\blender.exe
) else (
    echo ОШИБКА: Blender не найден в стандартных местах
    echo Укажите путь к Blender вручную в этом файле
    pause
    exit /b 1
)

echo Найден Blender: %BLENDER_PATH%
echo.

REM Запускаем скрипт установки
echo Запуск скрипта установки...
"%BLENDER_PATH%" --background --python install_renga_nodes.py

echo.
echo ======================================================================
echo УСТАНОВКА ЗАВЕРШЕНА!
echo ======================================================================
echo.
echo Теперь:
echo 1. Откройте Blender
echo 2. Перезапустите аддон Sverchok (Edit ^> Preferences ^> Add-ons)
echo 3. Или полностью перезапустите Blender
echo 4. Откройте Sverchok и найдите категорию "Renga" в меню
echo.
pause

