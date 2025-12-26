# Скрипт для копирования нод Renga в Sverchok
# Автоматически копирует папку renga в правильное место

$sverchokPath = "$env:APPDATA\Blender Foundation\Blender\5.0\scripts\addons\sverchok-master\nodes\renga"
$sourcePath = "renga"

Write-Host "=== Копирование нод Renga в Sverchok ===" -ForegroundColor Green
Write-Host ""

# Проверка исходной папки
if (-not (Test-Path $sourcePath)) {
    Write-Host "ОШИБКА: Папка $sourcePath не найдена!" -ForegroundColor Red
    Write-Host "Убедитесь, что вы находитесь в корне проекта Renga_Sverchok" -ForegroundColor Yellow
    exit 1
}

# Проверка наличия __init__.py
if (-not (Test-Path "$sourcePath\__init__.py")) {
    Write-Host "ОШИБКА: Файл $sourcePath\__init__.py не найден!" -ForegroundColor Red
    exit 1
}

# Проверка целевой папки
$sverchokNodesPath = Split-Path $sverchokPath -Parent
if (-not (Test-Path $sverchokNodesPath)) {
    Write-Host "ОШИБКА: Папка Sverchok не найдена: $sverchokNodesPath" -ForegroundColor Red
    Write-Host "Убедитесь, что Sverchok установлен в Blender 5.0" -ForegroundColor Yellow
    exit 1
}

Write-Host "Исходная папка: $sourcePath" -ForegroundColor Cyan
Write-Host "Целевая папка: $sverchokPath" -ForegroundColor Cyan
Write-Host ""

# Удаление старой папки (если есть)
if (Test-Path $sverchokPath) {
    Write-Host "Удаление старой папки..." -ForegroundColor Yellow
    Remove-Item -Path $sverchokPath -Recurse -Force
}

# Удаление __pycache__ из исходной папки
if (Test-Path "$sourcePath\__pycache__") {
    Write-Host "Удаление __pycache__ из исходной папки..." -ForegroundColor Yellow
    Remove-Item -Path "$sourcePath\__pycache__" -Recurse -Force
}

# Копирование
Write-Host "Копирование файлов..." -ForegroundColor Yellow
try {
    Copy-Item -Path "$sourcePath\*" -Destination $sverchokPath -Recurse -Force
    Write-Host "✓ Файлы успешно скопированы!" -ForegroundColor Green
} catch {
    Write-Host "ОШИБКА при копировании: $_" -ForegroundColor Red
    exit 1
}

# Проверка результата
if (Test-Path "$sverchokPath\__init__.py") {
    Write-Host "✓ Файл __init__.py найден в целевой папке" -ForegroundColor Green
} else {
    Write-Host "ОШИБКА: Файл __init__.py не найден после копирования!" -ForegroundColor Red
    exit 1
}

# Проверка функции register
$initContent = Get-Content "$sverchokPath\__init__.py" -Raw
if ($initContent -match "def register\(\):") {
    Write-Host "✓ Функция register() найдена в __init__.py" -ForegroundColor Green
} else {
    Write-Host "ПРЕДУПРЕЖДЕНИЕ: Функция register() не найдена!" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== ГОТОВО ===" -ForegroundColor Green
Write-Host ""
Write-Host "Следующие шаги:" -ForegroundColor Cyan
Write-Host "1. Закройте Blender полностью (если открыт)" -ForegroundColor White
Write-Host "2. Запустите Blender" -ForegroundColor White
Write-Host "3. Откройте консоль: Window > Toggle System Console" -ForegroundColor White
Write-Host "4. Перезагрузите аддон Sverchok: Edit > Preferences > Add-ons" -ForegroundColor White
Write-Host "5. Проверьте консоль на сообщения 'Renga nodes: Registered ...'" -ForegroundColor White
Write-Host "6. Ноды должны появиться в категории 'Renga' в меню Sverchok" -ForegroundColor White



