@echo off
chcp 65001 >nul
echo ======================================================================
echo УСТАНОВКА НОД RENGA В SVERCHOK
echo ======================================================================
echo.

set SOURCE_DIR=%~dp0sverchok_nodes\renga
set TARGET_DIR=C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga

echo Источник: %SOURCE_DIR%
echo Цель: %TARGET_DIR%
echo.

REM Проверяем наличие исходной папки
if not exist "%SOURCE_DIR%" (
    echo ✗ ОШИБКА: Папка не найдена: %SOURCE_DIR%
    echo.
    echo Создайте папку sverchok_nodes\renga и скопируйте туда файлы нод!
    pause
    exit /b 1
)

REM Удаляем старую папку
if exist "%TARGET_DIR%" (
    echo Удаление старой папки...
    rmdir /S /Q "%TARGET_DIR%"
)

REM Создаем новую папку
mkdir "%TARGET_DIR%"
echo.

echo Копирование файлов нод:
echo.

REM Копируем все файлы из папки renga
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
    echo Теперь:
    echo 1. Перезапустите Blender ПОЛНОСТЬЮ
    echo 2. Откройте Sverchok
    echo 3. Нажмите Add Node или Space
    echo 4. Найдите категорию "Renga" в меню
    echo.
) else (
    echo ✗ ОШИБКА при копировании файлов!
    pause
    exit /b 1
)

pause

