## Русский
**Minecraft JSON & Localization dumper** — утилита для сохранения новейших версий манифеста лаунчера и релизного манифеста сборок (со сборки 22w42a при каждом выходе новой сборки обновляются все манифесты версий, а в них обновляется параметр `assetIndex`, благодаря чему все сборки получают новейшую локализацию, что не позволяет в последствии отследить историю изменений), а также локализации для определённого языка, включая создание таблицы для Minecraft Wiki. Поддерживаются уведомления с помощью бота Telegram.

### Требования
- Python 3.7 и выше с зависимостями:
  - notifiers (требуется только в том случае, если уведомления в Telegram включены)
  - requests

### Параметры
Для настройки папок сохранения, логирования, а также заголовков таблицы отредактируйте файл `dump.py`:
| Переменная | Описание |
| - | - |
| `ROOT_FOLDER` | Корневая папка дампов, в ней создаются папки для манифестов и локализаций, а также хранится файл логов (по умолчанию текущая папка).|
| `MANIFESTS_FOLDER` | Папка для сохранения манифестов лаунчера. В ней манифесты сохраняются с датой и временем обновления файла в названии. Например, `Thu, 16 Jul 2026 14-43-09 GMT.json`.
| `LOCALIZATIONS_FOLDER` | Папка для хранения манифеста версии и локализаций. Папки в ней названы как новейшая предварительная сборка в лаунчере. Например, папка `26.3-snapshot-4` будет содержать манифест версии `26.3-snapshot-4.json`, MediaWiki таблицу локализации `ru_ru-table.mediawiki`, а также `en_us.json`, `ru_ru.json`.
| `LOG_FILE_NAME` | Название файла логов. Предполагается что файл имеет расширение `.log` для правильного отображения в редакторах кода.
| `LANG` | Код локализации в игре. Доступные коды можно узнать на Minecraft Wiki в статье [язык](https://minecraft.wiki/w/Language#Languages) |
| `TRANSLATION_KEY` | Отвечает за название первого столбца таблицы, который содержит ключи перевода |
| `EN_LANG_NAME` | Отвечает за название второго столбца таблицы, который содержит англоязычные названия |
| `LOCALIZED_NAME` | Отвечает за название третьего столбца таблицы, который содержит локализованное название |
| `VOID_PLACEHOLDER` | Отвечает за содержимое ячейки, в том случае, если локализованное название отсутствует |
| `FAVORITE_KEYS` | Разрешающий список с использованием регулярных выражений. Обычно синхронизирован с [BuildTable.py](https://github.com/Secret-Rabbit/Tools-for-RuMCW/blob/main/MCJSONLocalizationTableGenerator/BuildTable.py). |
| `UNWANTED_KEYS` | Запрещающий список с использованием регулярных выражений. Обычно синхронизирован с [BuildTable.py](https://github.com/Secret-Rabbit/Tools-for-RuMCW/blob/main/MCJSONLocalizationTableGenerator/BuildTable.py). |
| `DISABLE_NOTIFICATIONS` | Если `true`, то уведомления не будут присылаться, также библиотека `notifiers` не требуется. |
| `TELEGRAM_BOT_TOKEN` | Токен для уведомлений в Телеграм, не используется, если уведомления выключены |
| `TELEGRAM_CHAT_ID` | ИД чата для уведомлений в Телеграм, не используется, если уведомления выключены |

## English  
> [!NOTE]
> This text can be partially translated by machine translation or AI.

**Minecraft JSON & Localization dumper** — a utility for saving the latest versions of the launcher manifest and the release manifest of builds (starting from build 22w42a, every new build updates all version manifests, and the `assetIndex` parameter inside them is updated as well, causing all builds to receive the newest localization, which makes it impossible to track the history of changes afterward), as well as localization for a specific language, including generating a table for Minecraft Wiki. Telegram bot notifications are supported.

### Requirements
- Python 3.7 or higher with dependencies:  
  - notifiers (required only if Telegram notifications are enabled)  
  - requests

### Parameters
To configure dump folders, logging, and table headers, edit the `dump.py` file:

| Variable | Description |
| - | - |
| `ROOT_FOLDER` | The root folder for dumps. It contains subfolders for manifests and localizations, as well as the log file (default is the current folder). |
| `MANIFESTS_FOLDER` | Folder for saving launcher manifests. Manifests are saved with the date and time of the file update in the filename. For example: `Thu, 16 Jul 2026 14-43-09 GMT.json`. |
| `LOCALIZATIONS_FOLDER` | Folder for storing the version manifest and localizations. Subfolders are named after the latest snapshot in the launcher. For example, the folder `26.3-snapshot-4` will contain the version manifest `26.3-snapshot-4.json`, the MediaWiki localization table `ru_ru-table.mediawiki`, as well as `en_us.json`, `ru_ru.json`. |
| `LOG_FILE_NAME` | The name of the log file. It is assumed that the file has a `.log` extension for correct display in code editors. |
| `LANG` | The localization code used in the game. Available codes can be found on Minecraft Wiki in the [language](https://minecraft.wiki/w/Language#Languages) article. |
| `TRANSLATION_KEY` | Defines the name of the first column of the table, which contains translation keys. |
| `EN_LANG_NAME` | Defines the name of the second column of the table, which contains English names. |
| `LOCALIZED_NAME` | Defines the name of the third column of the table, which contains localized names. |
| `VOID_PLACEHOLDER` | Defines the content of a cell when a localized name is missing. |
| `FAVORITE_KEYS` | Allowlist using regular expressions. Usually synchronized with [BuildTable.py](https://github.com/Secret-Rabbit/Tools-for-RuMCW/blob/main/MCJSONLocalizationTableGenerator/BuildTable.py). |
| `UNWANTED_KEYS` | Denylist using regular expressions. Usually synchronized with [BuildTable.py](https://github.com/Secret-Rabbit/Tools-for-RuMCW/blob/main/MCJSONLocalizationTableGenerator/BuildTable.py). |
| `DISABLE_NOTIFICATIONS` | If `true`, notifications will not be sent, and the `notifiers` library is not required. |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token for notifications; not used if notifications are disabled. |
| `TELEGRAM_CHAT_ID` | Telegram chat ID for notifications; not used if notifications are disabled. |