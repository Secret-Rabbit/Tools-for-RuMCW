import pywikibot, os, hashlib

# Загружает изображения из каталога ./Images

# Участник, загрузивший в таблицу спрайтов
user = ""
# Таблица спрайтов (название изначального изображения без Файл:)
sprite_sheet = ""
# Модификация
mod = ""

# Файл для логирования ошибок и предупреждений
log_file = "upload_log.txt"
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

# Функция для логирования сообщений
def log(message):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")

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

    # Проверка существования
    if image_page.exists():
        print("Предупреждение: Файл уже существует на вики")

    # Проверка SHA1
    local_sha1 = file_sha1(file_path)
    duplicates = list(site.allimages(sha1=local_sha1))

    if duplicates:
        duplicate_titles = [d.title() for d in duplicates]

        msg = (
            f"[Дубликат] Локальный файл: {file_name} | SHA1: {local_sha1} | "
            f"Совпадения на вики: {duplicate_titles}"
        )

        print("Пропуск:", msg)
        log(msg)
        continue

    # Попытка загрузки
    try:
        image_page.text = content
        image_page.upload(file_path, ignore_warnings=True, comment=comment)
        print("Загружено успешно")
    except Exception as e:
        msg = f"Ошибка загрузки {file_name}: {e}"
        print(msg)
        log(msg)
