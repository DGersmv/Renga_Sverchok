# Гибридный подход: C# + C++ в одном проекте

## Обзор

Этот документ описывает, как комбинировать C# и C++ в одном проекте Renga плагина для оптимального использования преимуществ обоих языков.

## Архитектура

```
Renga_Grasshopper/
├── RengaGH/                    # C# проект (основной плагин)
│   ├── RengaPlugin.cs          # Главный плагин
│   ├── GeometryHelper.cs       # P/Invoke обертка для C++
│   └── RengaGH.csproj
│
├── RengaGeometry/               # C++ проект (геометрические алгоритмы)
│   ├── GeometryAlgorithms.h    # Заголовочный файл
│   ├── GeometryAlgorithms.cpp  # Реализация
│   └── RengaGeometry.vcxproj    # C++ проект
│
└── Renga_Grasshopper.sln        # Solution с обоими проектами
```

## Способы интеграции

### 1. P/Invoke (Platform Invoke) - Рекомендуется

**Преимущества:**
- ✅ Простая интеграция
- ✅ Не требует изменений в C++ коде
- ✅ Прямой вызов функций
- ✅ Хорошая производительность

**Недостатки:**
- ⚠️ Нужно правильно маршалировать данные
- ⚠️ Управление памятью вручную

**Пример использования:**

```csharp
// В C# коде
var result = GeometryHelper.CalculateComplexGeometry(points, pointCount, 0.1, 0.2);
```

### 2. C++/CLI (Managed C++)

**Преимущества:**
- ✅ Прямой доступ к .NET из C++
- ✅ Удобная работа с управляемой памятью

**Недостатки:**
- ⚠️ Требует C++/CLI компилятор
- ⚠️ Более сложная настройка

### 3. COM интерфейсы

**Преимущества:**
- ✅ Стандартный подход Windows
- ✅ Языковая независимость

**Недостатки:**
- ⚠️ Более сложная настройка
- ⚠️ Overhead от COM

## Настройка проекта

### Шаг 1: Добавить C++ проект в Solution

1. В Visual Studio: `Add → New Project → Visual C++ → Dynamic Library (.dll)`
2. Назвать проект `RengaGeometry`
3. Настроить `x64` платформу

### Шаг 2: Настроить C++ проект

В `RengaGeometry.vcxproj`:
- Configuration Type: `Dynamic Library (.dll)`
- Platform: `x64`
- Character Set: `Unicode`
- C++ Language Standard: `C++17` или выше

### Шаг 3: Добавить зависимости в C# проект

В `RengaGH.csproj` добавить:

```xml
<ItemGroup>
  <ProjectReference Include="..\RengaGeometry\RengaGeometry.vcxproj">
    <ReferenceOutputAssembly>false</ReferenceOutputAssembly>
  </ProjectReference>
</ItemGroup>

<ItemGroup>
  <Content Include="..\RengaGeometry\$(Configuration)\RengaGeometry.dll">
    <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
  </Content>
</ItemGroup>
```

### Шаг 4: Использование в C# коде

```csharp
using RengaPlugin;

// В вашем RengaPlugin.cs
private void CreateComplexGeometry()
{
    var points = new GeometryHelper.Point3D[]
    {
        new GeometryHelper.Point3D { X = 0, Y = 0, Z = 0 },
        new GeometryHelper.Point3D { X = 10, Y = 10, Z = 5 }
    };
    
    var result = GeometryHelper.CalculateComplexGeometry(points, points.Length, 0.1, 0.2);
    
    if (result.Success == 1)
    {
        // Использовать результат
        var width = result.Value1;
        var depth = result.Value2;
        var height = result.Value3;
    }
}
```

## Когда использовать C++ модули

### ✅ Используйте C++ для:

1. **Сложные геометрические алгоритмы**
   - Поиск путей в графах
   - Построение B-spline/NURBS кривых
   - Триангуляция поверхностей
   - Оптимизация сеток

2. **Вычислительно интенсивные операции**
   - Обработка тысяч точек
   - Реальные вычисления в реальном времени
   - Физическое моделирование

3. **Интеграция с нативными библиотеками**
   - Использование существующих C++ библиотек
   - Работа с OpenGL/DirectX
   - Интеграция с другими CAD системами

### ❌ НЕ используйте C++ для:

1. **UI и интерфейсы** - используйте C# (WPF/Windows Forms)
2. **Сетевые операции** - C# лучше подходит
3. **Работа с JSON/XML** - C# удобнее
4. **Стандартные операции Renga API** - C# достаточно

## Примеры использования

### Пример 1: Построение сложной кривой

```csharp
// C# код
public void CreateSplineFromPoints(Renga.Point3D[] controlPoints)
{
    // Конвертация в C++ структуры
    var points = controlPoints.Select(p => new GeometryHelper.Point3D
    {
        X = p.X,
        Y = p.Y,
        Z = p.Z
    }).ToArray();
    
    // Вызов C++ функции
    IntPtr curvePtr = GeometryHelper.CreateComplexCurve(points, points.Length);
    
    try
    {
        // Использование результата
        // ...
    }
    finally
    {
        // Освобождение памяти
        GeometryHelper.FreeMemory(curvePtr);
    }
}
```

### Пример 2: Поиск пути (как в MepCircleConstructor)

```csharp
public int[] FindPath(int startId, int endId)
{
    int maxPathLength = 100;
    int[] path = new int[maxPathLength];
    int actualLength = maxPathLength;
    
    if (GeometryHelper.FindPathBetweenPoints(startId, endId, path, ref actualLength) == 1)
    {
        Array.Resize(ref path, actualLength);
        return path;
    }
    
    return null;
}
```

## Отладка

### Отладка C++ кода из C#

1. Установите точку останова в C++ коде
2. В Visual Studio: `Debug → Attach to Process → Renga.exe`
3. Или запустите C# проект с отладкой - C++ DLL будет загружена автоматически

### Проверка загрузки DLL

```csharp
// Проверка наличия DLL
if (!File.Exists("RengaGeometry.dll"))
{
    throw new FileNotFoundException("RengaGeometry.dll not found");
}
```

## Производительность

### Benchmark пример:

- **C# только**: ~100ms для 1000 точек
- **C++ модуль**: ~10ms для 1000 точек
- **Улучшение**: ~10x для сложных вычислений

## Рекомендации

1. **Начните с C#** - реализуйте основную функциональность
2. **Профилируйте код** - найдите узкие места
3. **Выделите в C++** - только критичные по производительности части
4. **Тестируйте тщательно** - P/Invoke требует внимания к маршалингу

## Полезные ссылки

- [P/Invoke Documentation](https://docs.microsoft.com/en-us/dotnet/standard/native-interop/pinvoke)
- [Marshaling Data with P/Invoke](https://docs.microsoft.com/en-us/dotnet/standard/native-interop/marshalling)
- [Renga C++ Examples](../C++/MepCircleConstructor/)

