### Русский язык

Скрипт **`FileOptimize.py`** запускает оптимизацию файлов в текущей директории, выборочно, в зависимости от указанных настроек. В отличии от обычного использования через графический интерфейс, скрипт позволяет запускать несколько процессов оптимизации параллельно. Количество одновременных оптимизаций указывается непосредственно в самом скрипте, как и остальные настройки.

**Осторожно!** Этот скрипт требует обязательного наличия файла конфигурации `FileOptimizer.ini` в домашнем каталоге текущего пользователя (`%userprofile%`). Если устанавливаете FileOptimizer впервые, **обязательно сохраните его конфигурации при первом запуске.** Скрипт **`Install FileOptimizer.bat`** устанавливает **FileOptimizer**, используя [**Windows Package Manager**](https://github.com/microsoft/winget-cli) (winget) и запускает его по завершению установки.

В самом скрипте принудительно включается разрешение на запуск нескольких экземпляров программы и отключается проверка обновлений, так как она вызывает проблемы при параллельном запуске, если установлена не последняя версия, также проверяется наличие файла конфигурации FileOptimizer.

В таблице приведён список параметров, которые можно настроить непосредственно в скрипте:

| Параметр            | Описание                                                                                                                        |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| folder              | Указывает на папку в которой надо оптимизировать файлы. По умолчанию используется абсолютный путь к текущей рабочей директории. |
| prefix              | Указывает на то, файлы с каким префиксом будут оптимизированы.                                                                  |
| extension           | Указывает на то, файлы какого расширения будут оптимизированы.                                                                  |
| file_optimizer_path | Содержит путь к исполняемому файлу FileOptimizer.                                                                              |
| max_parallel        | Указывает число параллельных оптимизаций, запущенных одновременно.                                                              |
| optimization_level  | Указывает уровень оптимизации (целое число от 0 до 9).                                                                          |

### English language

The **`FileOptimize.py`** script runs optimization of files in the current directory, selectively, depending on the specified settings. Unlike the usual GUI usage, the script allows you to run several optimization processes in parallel. The number of simultaneous optimizations is specified directly in the script itself, as well as other settings.

**Attention.** This script requires `FileOptimizer.ini` configuration file in the current user's home directory`(%userprofile%`). If you are installing FileOptimizer for the first time, **be sure to save its configurations the first time you run it.** The **`Install FileOptimizer.bat`** script installs **FileOptimizer** using the [**Windows Package Manager**](https://github.com/microsoft/winget-cli) (winget) and runs it when the installation is complete.

The script itself forcibly enables the permission to run multiple instances of the program and disables checking for updates, as it causes problems when running in parallel if not the latest version is installed, and also checks for the FileOptimizer configuration file.

The table shows a list of parameters that can be configured directly in the script:

| Parameter           | Description                                                                                                                   |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| folder              | Specifies the folder where files should be optimized. By default, the absolute path to the current working directory is used. |
| prefix              | Specifies which prefix files will be optimized.                                                                               |
| extension           | Specifies which extension files will be optimized.                                                                            |
| file_optimizer_path | Contains the path to the FileOptimizer executable file.                                                                      |
| max_parallel        | Specifies the number of parallel optimizations that can be run simultaneously.                                                |
| optimization_level  | Specifies the optimization level (integer from 0 to 9).                                                                       |
