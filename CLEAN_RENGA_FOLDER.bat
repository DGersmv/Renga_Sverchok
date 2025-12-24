@echo off
chcp 65001 >nul
echo ======================================================================
echo ОЧИСТКА ПАПКИ RENGA ОТ ЛИШНИХ ФАЙЛОВ
echo ======================================================================
echo.
echo Sverchok пытается импортировать ВСЕ .py файлы как ноды!
echo В папке renga должны быть ТОЛЬКО файлы нод!
echo.

set RENGA_DIR=C:\Users\DGer\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga

echo Удаление лишних файлов из %RENGA_DIR%...
echo.

REM Удаляем файлы, которые НЕ являются нодами
del /Q "%RENGA_DIR%\ADD_TO_MENU.py" 2>nul && echo ✓ Удален ADD_TO_MENU.py
del /Q "%RENGA_DIR%\FORCE_MENU.py" 2>nul && echo ✓ Удален FORCE_MENU.py
del /Q "%RENGA_DIR%\INSTALL.txt" 2>nul && echo ✓ Удален INSTALL.txt
del /Q "%RENGA_DIR%\INSTALLATION.md" 2>nul && echo ✓ Удален INSTALLATION.md
del /Q "%RENGA_DIR%\INSTALL_FIX.md" 2>nul && echo ✓ Удален INSTALL_FIX.md
del /Q "%RENGA_DIR%\MENU_FIX_GUIDE.md" 2>nul && echo ✓ Удален MENU_FIX_GUIDE.md
del /Q "%RENGA_DIR%\MENU_REGISTRATION.md" 2>nul && echo ✓ Удален MENU_REGISTRATION.md
del /Q "%RENGA_DIR%\QUICK_FIX.md" 2>nul && echo ✓ Удален QUICK_FIX.md
del /Q "%RENGA_DIR%\README.md" 2>nul && echo ✓ Удален README.md
del /Q "%RENGA_DIR%\TROUBLESHOOTING.md" 2>nul && echo ✓ Удален TROUBLESHOOTING.md
del /Q "%RENGA_DIR%\VERIFICATION.md" 2>nul && echo ✓ Удален VERIFICATION.md

echo.
echo ======================================================================
echo ОЧИСТКА ЗАВЕРШЕНА!
echo ======================================================================
echo.
echo В папке renga теперь только файлы нод:
echo   - __init__.py
echo   - renga_connect.py
echo   - renga_create_columns.py
echo   - renga_get_walls.py
echo   - renga_client.py
echo   - commands.py
echo   - connection_protocol.py
echo.
echo Теперь перезапустите Blender - Sverchok должен загрузиться!
echo.
pause

