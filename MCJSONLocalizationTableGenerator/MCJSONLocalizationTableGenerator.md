## Русский

**MC Localization Table Generator** позволяет сгенерировать таблицу MediaWiki для не англоязычной локализации ванильного Minecraft версии 18w02a и выше.

Для указания версии и изменения языка, а также настройки таблицы отредактируйте файл `BuildTable.py`:
| Переменная | Описание |
| - | - |
| `mc_ver` | Версия игры как в лаунчере. Если оставить пустым, будет использоваться последний снапшот |
| `lang` | Код локализации в игре. Доступные коды можно узнать на Minecraft Wiki в статье [язык](https://minecraft.wiki/w/Language#Languages) |
| `translate_key` | Отвечает за название первого столбца таблицы, который содержит ключи перевода |
| `en_lang_name` | Отвечает за название второго столбца таблицы, который содержит англоязычные названия |
| `localized_name` | Отвечает за название третьего столбца таблицы, который содержит локализованное название |
| `void_placeholder` | Отвечает за содержимое ячейки, в том случае, если локализованное название отсутствует |
| `favorites_keys` | Разрешающий список с использованием регулярных выражений |
| `unwanted_keys` | Запрещающий список с использованием регулярных выражений |

После запуска создаётся файл с названием `<версия_игры>-<код_локализации>.mediawiki `, содержащий сортируемую таблицу следующего вида:
| Ключ перевода | Англоязычное название | Русскоязычное название |
| - | - | - |
| ... | ... | ... |

Формат вывода предполагает создание ссылок для значений всех ключей перевода, не являющихся описанием.

## English

**MC LocalizationTable Generator** allows you to generate a MediaWiki table for non-English localization of vanilla Minecraft version 18w02a and higher.

To specify the version and change the language, as well as the table settings, edit the file `BuildTable.py `:
| Variable | Description |
| - | - |
| `mc_ver` | The version of the game is like in the launcher. If left blank, the last snapshot will be used |
| `lang` | The localization code in the game. The available codes can be found on the Minecraft Wiki in the article [language](https://minecraft.wiki/w/Language#Languages) |
| `translate_key` | Responsible for the name of the first column of the table, which contains the translation keys |
| `en_lang_name` | Responsible for the name of the second column of the table, which contains English-language names |
| `localized_name` | Responsible for the name of the third column of the table, which contains the localized name |
| `void_placeholder` | Responsible for the contents of the cell, if there is no localized name |
| `favorites_keys` | Allow list using regular expressions |
| `unwanted_keys` | Restricted list using regular expressions |

After launch, a file is created with the name `<game_version>-<localization_code>.mediawiki ` containing a sortable table of the following type:
| Translation key | English-language name | localized name |
| - | - | - |
| ... | ... | ... |

The output format assumes the creation of links for the values of all translation keys that are not a description.
