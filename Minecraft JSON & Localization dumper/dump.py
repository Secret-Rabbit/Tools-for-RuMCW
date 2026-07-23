import json, requests, os, logging
from pathlib import Path

# Параметры
# Options

# Корневая папка дампов (по умолчанию текущая папка)
# Root folder for dumps (default is the current folder)
ROOT_FOLDER = Path(os.getcwd())
# Папка для хранения манифестов лаунчера
# Folder for storing launcher manifests
MANIFESTS_FOLDER = "dumps"
# Папка для хранения манифеста версии и локализаций
# Folder for storing version manifest and localizations
LOCALIZATIONS_FOLDER = "localizations"
# Файл для логов
# Log file
LOG_FILE_NAME = "app.log"
# Язык локализации
# Localization language
LANG = "ru_ru"

# Названия столбцов таблицы по порядку
# Names of table columns in order
TRANSLATION_KEY = "Ключ перевода"
EN_LANG_NAME = "Англоязычное название"
LOCALIZED_NAME = "Русскоязычное название"
VOID_PLACEHOLDER = "{{Нет}}"

# Токен и ИД чата для уведомлений в Телеграм
# Telegram bot token and chat ID for notifications
DISABLE_NOTIFICATIONS = True
TELEGRAM_BOT_TOKEN = "Your_Telegram_Bot_Token"
TELEGRAM_CHAT_ID = "Your_Telegram_Chat_ID"

URL = "https://piston-meta.mojang.com/mc/game/version_manifest.json"

# Allow list
# Разрешающий список
FAVORITE_KEYS = {
    "^biome\\.",
    "^block\\.",
    "^dataPack\\.",
    "^effect\\.",
    "^gamerule\\.",
    "^subtitles\\.",
    "advancements\\.",
    "container\\.",
    "enchantment\\.minecraft\\.",
    "entity\\.minecraft\\.",
    "filled_map\\.",
    "flat_world_preset\\.",
    "gameMode\\.",
    "generator\\.",
    "item\\.minecraft\\.",
    "jukebox_song\\.",
    "painting\\.minecraft\\.",
    "trim_pattern",
}
    # Restricted list
    # Запрещающий список
UNWANTED_KEYS = {
    "^advancements\\.empty",
    "^advancements\\.progress$",
    "^advancements\\.sad_label$",
    "^advancements\\.toast\\.",
    "^block\\.minecraft\\.beacon\\.",
    "^block\\.minecraft\\.bed/\\.",
    "^block\\.minecraft\\.bed\\.",
    "^block\\.minecraft\\.player_head\\.named$",
    "^block\\.minecraft\\.set_spawn$",
    "^block\\.minecraft\\.spawn\\.not_valid$",
    "^block\\.minecraft\\.spawner\\.",
    "^block\\.minecraft\\.tnt\\.disabled$",
    "^container\\.beehive\\.bees$",
    "^container\\.beehive\\.honey$",
    "^container\\.enchant\\.$",
    "^container\\.enchant\\.clue$",
    "^container\\.enchant\\.lapis\\.",
    "^container\\.enchant\\.level\\.",
    "^container\\.isLocked$",
    "^container\\.repair\\.cost$",
    "^container\\.repair\\.expensive$",
    "^container\\.shulkerBox\\.",
    "^container\\.spectatorCantOpen$",
    "^container\\.upgrade\\.error_tooltip$",
    "^container\\.upgrade\\.missing_template_tooltip$",
    "^dataPack.title$",
    "^dataPack.validation.",
    "^effect\\.duration\\.infinite$",
    "^effect\\.none$",
    "^entity\\.minecraft\\.falling_block_type$",
    "^filled_map\\.id$",
    "^filled_map\\.level$",
    "^filled_map\\.locked$",
    "^filled_map\\.scale$",
    "^flat_world_preset.unknown$",
    "^gameMode\\.changed$",
    "^item.minecraft\\.crossbow\\.projectile.",
    "^item\\.minecraft\\.bundle\\.",
    "^item\\.minecraft\\.crossbow\\.projectile$",
    "^item\\.minecraft\\.debug_stick\\.",
    "^item\\.minecraft\\.firework_rocket\\.",
    "^item\\.minecraft\\.firework_rocket\\.flight$",
    "^item\\.minecraft\\.smithing_template\\.",
    "^selectWorld\\.gameMode\\.adventure\\.",
    "^selectWorld\\.gameMode\\.creative\\.",
    "^selectWorld\\.gameMode\\.hardcore\\.",
    "^selectWorld\\.gameMode\\.spectator\\.",
    "^selectWorld\\.gameMode\\.survival\\.",
}

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=f"{ROOT_FOLDER}\\{LOG_FILE_NAME}",
    encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)

def check_folder(target):
    if not os.path.isdir(target):
        os.makedirs(target)


def get_full_path(folder):
    full_path = f"{ROOT_FOLDER}\\{folder}"
    check_folder(full_path)
    return full_path


def update_manifest():
    version_manifest = requests.get(URL, timeout=10)
    version_manifest_json = version_manifest.json()
    snap = version_manifest_json["latest"]["snapshot"]
    if not DISABLE_NOTIFICATIONS:
        telegram_notify(snap)
    for i in version_manifest_json["versions"]:
        if i["id"] == snap:
            client_url = i["url"]
    snap_folder_path = f"{get_full_path(LOCALIZATIONS_FOLDER)}\\{snap}"
    check_folder(snap_folder_path)
    if (
        not os.path.isfile(f"{snap_folder_path}\\{LANG}-table.mediawiki")
        or not os.path.isfile(f"{snap_folder_path}\\{LANG}.json")
        or not os.path.isfile(f"{snap_folder_path}\\en_us.json")
        or not os.path.isfile(f"{snap_folder_path}\\{snap}.json")
    ):
        get_localization(client_url, LANG)
        logging.info(f"New snapshot detected: {snap}")
    else:
        logging.info(f"Snapshot {snap} localization file already exists")
    check_folder(get_full_path(MANIFESTS_FOLDER))
    with open(
        f"{(get_full_path(MANIFESTS_FOLDER))}\\{file_name}.json", "w", encoding="utf-8"
    ) as manifest_file:
        json.dump(version_manifest_json, manifest_file, ensure_ascii=False)


def get_localization(url, lang):
    from zipfile import ZipFile
    import re
    # Reading a version-related JSON file and then converting JSON strings into a Python object
    # Чтение связанного с версией JSON-файла с последующим преобразованием строк JSON в объект Python
    ver_json = requests.get(url, timeout=10).json()
    localization_full_path = f"{get_full_path(LOCALIZATIONS_FOLDER)}\\{ver_json['id']}"
    with open(
        f"{localization_full_path}\\{ver_json['id']}.json", "w", encoding="utf-8"
    ) as version_manifest:
        json.dump(ver_json, version_manifest, ensure_ascii=False)
    logging.info("Save last snapshot manifest")
    check_folder(localization_full_path)
    # Downloading the client of target version
    # Скачивание клиента целевой версии
    client_jar_raw = requests.get(ver_json["downloads"]["client"]["url"], timeout=10)
    # Saving a version archive named client.zip
    # Сохранение архива версии с названием client.zip
    with open("client.zip", "wb") as file:
        file.write(client_jar_raw.content)
        # Открытие архива client.zip
        # Opening the client.zip archive
    with ZipFile("client.zip", "r") as jar_file:
        # Открытие файла en_us.json
        # Opening en_us.json file
        with jar_file.open("assets/minecraft/lang/en_us.json", "r") as en_data:
            # Преобразование строк JSON в объект Python
            # Converting JSON strings to a Python object
            en_us = json.load(en_data)
        with open(
            f"{localization_full_path}\\en_us.json", "w", encoding="utf-8"
        ) as en_file:
            json.dump(en_us, en_file, ensure_ascii=False)
        logging.info(
            "Localization file en_us.json has been successfully extracted from the client archive"
        )
    # Удаление архива client.zip
    # Remove client.zip archive
    os.remove("client.zip")
    # Чтение JSON активов целевой версии с последующим преобразованием строк JSON в объект Python
    # Reading assets JSON of target version and then converting the JSON strings into a Python object
    asset_index = requests.get(ver_json["assetIndex"]["url"], timeout=10).json()
    # Получение хеша json-файла локализации для заданного языка
    # Get hash of localization json file for specified language
    hash_lang = asset_index["objects"][f"minecraft/lang/{lang}.json"]["hash"]
    # Чтение JSON-файла локализации целевой версии с последующим преобразованием строк JSON в объект Python
    # Reading target version localization JSON file and then converting the JSON strings into a Python object
    other_lang = requests.get(
        f"https://resources.download.minecraft.net/{hash_lang[:2]}/{hash_lang}",
        timeout=10,
    ).json()
    with open(
        f"{localization_full_path}\\{lang}.json", "w", encoding="utf-8"
    ) as lang_file:
        json.dump(other_lang, lang_file, ensure_ascii=False)
    logging.info(
        f"Localization file {lang}.json has been successfully downloaded from the assets"
    )

    output_text = ""

    # Шапка таблицы
    output_text += (
        '{|class="wikitable sortable"'
        + f"\n!{TRANSLATION_KEY}\n!{EN_LANG_NAME}\n!{LOCALIZED_NAME}"
    )

    # Перечисление англоязычных ИД`ов
    for i in en_us:
        ex_key = 0

        # Проверка плохих ключей
        for u in UNWANTED_KEYS:
            if bool(re.search(u, i)):
                ex_key = 1

        # Проверка избранных ключей
        for f in FAVORITE_KEYS:
            if ex_key == 0 and bool(re.search(f, i)):

                # Проверка на описание/субтитры/песни/инфо
                if (
                    bool(re.search(r"\.desc", i))
                    or bool(re.search(r"subtitles\.", i))
                    or bool(re.search(r"\.info", i))
                    or bool(re.search(r"jukebox_song\.", i))
                ):
                    output_text += f"\n|-\n|{i}\n|{en_us[i]}\n|{other_lang.setdefault(i, VOID_PLACEHOLDER)}"

                else:
                    # Пустые строки
                    if other_lang.setdefault(i, VOID_PLACEHOLDER) == VOID_PLACEHOLDER:
                        output_text += f"\n|-\n|{i}\n|[[:en:{en_us[i]}|{en_us[i]}]]\n|{VOID_PLACEHOLDER}"
                    else:
                        output_text += f"\n|-\n|{i}\n|[[:en:{en_us[i]}|{en_us[i]}]]\n|[[{other_lang[i]}]]"

    # Закрытие таблицы
    output_text += "\n|}"

    # Запись в файл
    with open(
        f"{localization_full_path}\\{lang}-table.mediawiki",
        "w",
        encoding="utf8",
    ) as localization_table:
        localization_table.write(output_text)
    logging.info(
        f"Localization table {lang}-table.mediawiki has been successfully created"
    )
    return output_text

def telegram_notify(snap):
    from notifiers import get_notifier
    telegram = get_notifier("telegram")
    telegram.notify(message=f"New version released: {snap}", token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID)

def main():
    try:
        r = requests.head(URL, timeout=10)
        last_modified = r.headers.get("Last-Modified")
        global file_name
        file_name = last_modified.replace(":", "-")
        if not os.path.isfile(f"{get_full_path(MANIFESTS_FOLDER)}\\{file_name}.json"):
            logging.info("New update manifest detected. Downloading...")
            update_manifest()
        else:
            logging.info("Updates not detected")

    except Exception as e:
        logging.error(e)
    except Warning as w:
        logging.warning(w)


if __name__ == "__main__":
    main()
