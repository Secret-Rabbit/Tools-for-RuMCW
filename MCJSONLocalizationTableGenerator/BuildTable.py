from zipfile import ZipFile
import requests, os, json, re

# The version of the game. If left empty, the last snapshot will be used
# Версия игры. Если оставить пустым, будет использоваться последний снапшот
mc_ver = "1.21.3"
# In-Game Locale Code
# Код локализации в игре
lang = "ru_ru"

# Названия столбцов таблицы по порядку
# Names of table columns in order
translate_key = "Ключ перевода"
en_lang_name = "Англоязычное название"
localized_name = "Русскоязычное название"
void_placeholder = "{{Нет}}"

# Allow list
# Разрешающий список
favorites_keys = {
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
unwanted_keys = {
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

# Getting links to JSON versions list
# Получение ссылок на JSON версий
version_manifest = requests.get(
    "https://piston-meta.mojang.com/mc/game/version_manifest.json"
).json()
# Checking if the version is specified. If no version is specified, the latest snapshot will be used
# Проверка указания версии. Если версия не задана, то будет использоваться последний снапшот
if mc_ver == "":
    mc_ver = version_manifest["latest"]["snapshot"]
for i in version_manifest["versions"]:
    if i["id"] == mc_ver:
        # Reading a version-related JSON file and then converting JSON strings into a Python object
        # Чтение связанного с версией JSON-файла с последующим преобразованием строк JSON в объект Python
        ver_json = requests.get(i["url"]).json()
        # Downloading the client of target version
        # Скачивание клиента целевой версии
        client_jar_raw = requests.get(ver_json["downloads"]["client"]["url"])
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
        # Удаление архива client.zip
        # Remove client.zip archive
        os.remove("client.zip")
        # Чтение JSON активов целевой версии с последующим преобразованием строк JSON в объект Python
        # Reading assets JSON of target version and then converting the JSON strings into a Python object
        asset_index = requests.get(ver_json["assetIndex"]["url"]).json()
        # Получение хеша json-файла локализации для заданного языка
        # Get hash of localization json file for specified language
        hash_lang = asset_index["objects"][f"minecraft/lang/{lang}.json"]["hash"]
        # Чтение JSON-файла локализации целевой версии с последующим преобразованием строк JSON в объект Python
        # Reading target version localization JSON file and then converting the JSON strings into a Python object
        other_lang = requests.get(
            f"https://resources.download.minecraft.net/{hash_lang[:2]}/{hash_lang}"
        ).json()


with open(
    lang + "-" + mc_ver + ".mediawiki", "w", encoding="utf8"
) as localization_table:
    # Запись шапки таблицы в файл
    # Write table header to file
    localization_table.write(
        '{|class="wikitable sortable"'
        + f"\n!{translate_key}\n!{en_lang_name}\n!{localized_name}"
    )
    # Перечисление англоязычных ИД`ы
    # Listing of English-language IDs
    for i in en_us:
        # Сброс срабатывания фильтра плохих ключей
        # Reset bad key filter triggering
        ex_key = 0
        # Перечисление плохих ключей
        # Listing bad keys
        for u in unwanted_keys:
            # Проверка ключа на несоответствие
            # Checking key for inconsistency
            if bool(re.search(u, i)):
                # Вызов срабатывания фильтра плохих ключей
                # Triggering bad key filter
                ex_key = 1
        # Перечисление избранных ключей
        # Listing your favorite keys
        for f in favorites_keys:
            # Проверка срабатывания фильтра ключей и проверка на избранность
            # Checking the activation of key filter and checking for favorites
            if ex_key == 0 and bool(re.search(f, i)):
                # Проверка на то, является ли строка описанием, субтитрами, названием песен, информацией не нужной в ссылках
                # Checking whether the string is a description, subtitles, song title, or information not needed in the links
                if (
                    bool(re.search("\\.desc", i))
                    or bool(re.search("subtitles\\.", i))
                    or bool(re.search("\\.info", i))
                    or bool(re.search("jukebox_song\\.", i))
                ):
                    # Запись в файл отформатированных строк без ссылок
                    # Writing formatted strings to a file without links
                    localization_table.write(
                        f"\n|-\n|{i}\n|{en_us[i]}\n|{other_lang.setdefault(i, void_placeholder)}"
                    )
                else:
                    # Обработка пустых строк
                    # Processing of empty lines
                    if other_lang.setdefault(i, void_placeholder) == void_placeholder:
                        # Запись в файл отформатированных строк таблицы
                        # Writing formatted table rows
                        localization_table.write(
                            f"\n|-\n|{i}\n|[[:en:{en_us[i]}|{en_us[i]}"
                            + "]]\n|"
                            + void_placeholder
                        )
                    else:
                        # Запись в файл отформатированных строк таблицы
                        # Writing formatted table rows to a file
                        localization_table.write(
                            f"\n|-\n|{i}\n|[[:en:{en_us[i]}|{en_us[i]}]]\n|[[{other_lang[i]}]]"
                        )
    localization_table.write("\n|}")
    localization_table.close
