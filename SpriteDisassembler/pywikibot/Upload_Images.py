import pywikibot, os

# Загружает изображения из каталога ./Images

# Участник, загрузивший в таблицу спрайтов
user=""
# Таблица спрайтов (название изначального изображения без Файл:)
sprite_sheet=""
# Модификация
mod=""

# Указание расширений для изображений
target_extension = ".png"
# Каталог с изображениями.
path_prefix = "\\Images"
# Комментарий к загружаемому изображению
comment = "Это изображение загружено с помощью Pywikibot"
# Содержание страницы файла
content = str(
    f"==Краткое описание ==\nИзображение было получено в результате разбиения таблицы спрайтов [[:Файл:{sprite_sheet}]], которая изначально была загружена участником [[Участник:{user}|{user}]].\n\n== Лицензирование ==\n{{{{Лицензия/Модификация|{mod}}}}}"
)
# Генерация списка изображений
file_names = os.listdir(os.getcwd() + path_prefix)
# Фильтрация имён по заданному расширению
filtered_file_names = [
    file_name for file_name in file_names if file_name.endswith(target_extension)
]

site = pywikibot.Site()
site.login()
# Перечисление файлов
for file_name in filtered_file_names:
    file_path = os.getcwd() + path_prefix + "\\" + file_name
    image_page = pywikibot.FilePage(site, "Файл:" + file_name)
    image_page.text = content
    image_page.upload(file_path, ignore_warnings=True, comment=comment)
