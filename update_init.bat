@echo off
echo Обновление __init__.py в Sverchok...
copy /Y "sverchok_nodes\__init__.py" "%APPDATA%\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga\__init__.py"
if %ERRORLEVEL% == 0 (
    echo ✓ Файл успешно обновлен!
) else (
    echo ✗ Ошибка при копировании
    pause
)


