import pywikibot, os, hashlib

# Загружает изображения из каталога ./Images

# Участник, загрузивший в таблицу спрайтов
user = ""
# Таблица спрайтов (название изначального изображения без Файл:)
sprite_sheet = ""
# Модификация
mod = ""

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


# Функция вычисления SHA1
def file_sha1(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


# Получаем список файлов
file_names = [
    f for f in os.listdir(os.getcwd() + path_prefix) if f.endswith(target_extension)
]

site = pywikibot.Site()
site.login()

for file_name in file_names:
    file_path = os.getcwd() + path_prefix + "\\" + file_name
    image_page = pywikibot.FilePage(site, "Файл:" + file_name)

    print(f"\n=== {file_name} ===")

    # 1. Проверка: файл с таким именем уже существует
    if image_page.exists():
        print("Предупреждение: Файл уже существует на вики")

    # 2. Проверка SHA1 на дубликат
    local_sha1 = file_sha1(file_path)

    duplicates = list(site.allimages(sha1=local_sha1))
    if duplicates:
        print("Пропуск: найден дубликат по SHA1 →", [d.title() for d in duplicates])
        continue

    # 3. Загружаем
    try:
        image_page.text = content
        image_page.upload(file_path, ignore_warnings=True, comment=comment)
        print("Загружено успешно")
    except Exception as e:
        print(f"Ошибка при загрузке: {e}")
