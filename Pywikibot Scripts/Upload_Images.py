import pywikibot, os, hashlib

# Загружает изображения из каталога ./Images

# === Настройки ===
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
content = (
    f"==Краткое описание ==\n"
    f"Изображение было получено в результате разбиения таблицы спрайтов [[:Файл:{sprite_sheet}]], "
    f"которая изначально была загружена участником [[Участник:{user}|{user}]].\n\n"
    f"== Лицензирование ==\n{{{{Лицензия/Модификация|{mod}}}}}"
)

valid_ext = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")


# === Логирование ===
def log(message):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")


# === SHA1 локального файла ===
def file_sha1(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


# === 1. Сканируем локальные файлы ===
local_dir = os.getcwd() + path_prefix
file_names = [
    f for f in os.listdir(local_dir)
    if f.lower().endswith(valid_ext)
]

local_sha1_map = {}   # sha1 → [file1, file2]
local_sha1_of = {}    # file → sha1

for file_name in file_names:
    file_path = os.path.join(local_dir, file_name)
    sha1 = file_sha1(file_path)
    local_sha1_of[file_name] = sha1
    local_sha1_map.setdefault(sha1, []).append(file_name)

# === 2. Локальные дубликаты ===
for sha1, files in local_sha1_map.items():
    if len(files) > 1:
        log(f"[Локальные дубликаты] SHA1: {sha1} → {files}")


# === 3. Подключение к вики ===
site = pywikibot.Site()
site.login()


# === 4. Обрабатываем локальные файлы ===
for file_name in file_names:
    sha1 = local_sha1_of[file_name]

    # Пропускаем локальные дубликаты (кроме первого)
    if len(local_sha1_map[sha1]) > 1 and local_sha1_map[sha1][0] != file_name:
        log(f"[Пропуск локального дубликата] {file_name} (SHA1: {sha1})")
        continue

    file_path = os.path.join(local_dir, file_name)
    image_page = pywikibot.FilePage(site, "Файл:" + file_name)

    print(f"\n=== {file_name} ===")

    # Проверка существования файла на вики
    if image_page.exists():
        print("Предупреждение: Файл уже существует на вики")

    # === Проверка дубликата на вики через SHA1 ===
    duplicates = list(site.allimages(sha1=sha1))

    if duplicates:
        duplicate_titles = [d.title() for d in duplicates]
        msg = (
            f"[Дубликат на вики] Локальный файл: {file_name} | Совпадения: {duplicate_titles}"
        )
        print("Пропуск:", msg)
        log(msg)
        continue

    # === Попытка загрузки ===
    try:
        image_page.text = content
        image_page.upload(file_path, ignore_warnings=True, comment=comment)
        print("Загружено успешно")
    except Exception as e:
        msg = f"[Ошибка загрузки] {file_name}: {e}"
        print(msg)
        log(msg)
