@echo off
echo ========================================
echo ИСПРАВЛЕНИЕ ОШИБКИ RNA_ADD
echo ========================================
echo.
echo Заменяем все вхождения RNA_ADD на ADD в файлах Sverchok...
echo.

set "SVERCHOK_PATH=%APPDATA%\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master"

if not exist "%SVERCHOK_PATH%" (
    echo ОШИБКА: Папка Sverchok не найдена!
    echo Путь: %SVERCHOK_PATH%
    pause
    exit /b 1
)

echo Найдена папка Sverchok: %SVERCHOK_PATH%
echo.

REM Используем PowerShell для замены
powershell -Command "(Get-Content '%SVERCHOK_PATH%\ui\nodeview_space_menu.py') -replace 'RNA_ADD', 'ADD' | Set-Content '%SVERCHOK_PATH%\ui\nodeview_space_menu.py'"
if %errorlevel% equ 0 (
    echo [OK] nodeview_space_menu.py исправлен
) else (
    echo [ОШИБКА] Не удалось исправить nodeview_space_menu.py
)

powershell -Command "(Get-Content '%SVERCHOK_PATH%\ui\nodeview_rclick_menu.py') -replace 'RNA_ADD', 'ADD' | Set-Content '%SVERCHOK_PATH%\ui\nodeview_rclick_menu.py'"
if %errorlevel% equ 0 (
    echo [OK] nodeview_rclick_menu.py исправлен
) else (
    echo [ОШИБКА] Не удалось исправить nodeview_rclick_menu.py
)

powershell -Command "(Get-Content '%SVERCHOK_PATH%\nodes\logic\evolver.py') -replace 'RNA_ADD', 'ADD' | Set-Content '%SVERCHOK_PATH%\nodes\logic\evolver.py'"
if %errorlevel% equ 0 (
    echo [OK] evolver.py исправлен
) else (
    echo [ОШИБКА] Не удалось исправить evolver.py
)

echo.
echo ========================================
echo ПРОВЕРКА
echo ========================================
echo.

findstr /S /I "RNA_ADD" "%SVERCHOK_PATH%\*.py" >nul 2>&1
if %errorlevel% equ 0 (
    echo [ВНИМАНИЕ] Найдены оставшиеся вхождения RNA_ADD:
    findstr /S /I "RNA_ADD" "%SVERCHOK_PATH%\*.py"
) else (
    echo [OK] Все вхождения RNA_ADD заменены на ADD!
)

echo.
echo ========================================
echo ГОТОВО!
echo ========================================
echo.
echo Теперь перезапустите Blender и проверьте, что ошибка исчезла.
echo.
pause

