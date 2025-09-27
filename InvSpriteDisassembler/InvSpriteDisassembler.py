from slpp import slpp
from PIL import Image
import re, json, os

# Открытие спрайта
with open("./WikiSprite.lua", "r", encoding="utf8") as file:
    # Читаем содержимое файла в строку
    wiki_sprite_raw = file.read()
# Исключение названия массива
wiki_sprite_raw = wiki_sprite_raw.replace("return", "")
# Преобразование мета-таблицы LUA в словарь Python
wiki_sprite = slpp.decode(wiki_sprite_raw)

# Название мода в переменную
mod_name = wiki_sprite["настройки"]["имя"]
# Выяснения названия изображения спрайта из настроек спрайта, если они не указаны, задаётся стандартное
image = wiki_sprite["настройки"].get("изобр", mod_name + "CSS.png").replace(" ", "_")
# Размер клетки
size = wiki_sprite["настройки"]["разм"]
# Открытие картинки
im = Image.open(image)
# Проверка, анимированно ли изображение
if im.is_animated:
    print("Внимание!!!\nИзображение анимированно")
# Вычисление количества элементов в строке спрайта
item_format = wiki_sprite["настройки"]["формат"] / wiki_sprite["настройки"]["разм"]
# Псевдонимы
aliases_list = "return {\n"
# Содержимое для Модуль:Инвентарный слот/Англоязычные названия/<Мод>
enNamesModule = f"-- Англоязычные названия для блоков и предметов, отображаемых в Инвентарном слоте.\n\n-- Простые обозначения, не требующие автоматической генерации\nlocal enNames = {{\n"

# Таблица проверки результатов
sprite_table = '{| class="wikitable invslot-plain"\n|-\n!Название\n!Изобр.\n!Слот\n!Спрайт\n!Изобр. спрайт\n|-'
# Словарик для создания перенаправлений, если размер изображения 16
redirects_list = {}
# Словарик для создания перенаправлений, если размер изображения 32
redirects_list_32 = {}

# Папка, в которую будут сохранены результаты выполнения скрипта
target_path = f"{os.getcwd()}\\{mod_name}"

if not os.path.isdir(target_path):
    os.makedirs(target_path)


# Проверка и добавление англоязычного названия в псевдоним в случае если оно указано для названий с запрещёнными символами
def get_en_name(pattern):
    if wiki_sprite["IDы"][pattern].get("en") != None:
        en_name = ', english = "' + wiki_sprite["IDы"][pattern]["en"] + '"'
    return en_name


# Создание псевдонима для запрещённых символов
def aliases_fix_proc(pattern, pattern_fix):
    aliases_fix = (
        '	["'
        + pattern
        + '"] = { title = "'
        + pattern
        + '", name = "'
        + pattern_fix
        + '"'
        + get_en_name(pattern)
        + " },\n"
    )
    return aliases_fix


# Сжатие изображений предметов с пиксельной репликацией
def compress_neighbor_pixels(region):
    # Проверка на пиксельную репликацию
    for x in range(0, size, 2):
        for y in range(0, size, 2):
            pixel_box = (x, y, x + 1, y + 1)
            pixel_box2 = (x + 1, y, x + 2, y + 1)
            pixel_box3 = (x, y + 1, x + 1, y + 2)
            pixel_box4 = (x + 1, y + 1, x + 2, y + 2)
            pixel_region = region.crop(pixel_box)
            pixel_region2 = region.crop(pixel_box2)
            pixel_region3 = region.crop(pixel_box3)
            pixel_region4 = region.crop(pixel_box4)
            if (
                pixel_region.histogram() == pixel_region2.histogram()
                and pixel_region.histogram() == pixel_region3.histogram()
                and pixel_region.histogram() == pixel_region4.histogram()
            ):
                result = False
            else:
                result = True
                break
        if result:
            break
    # Если изображение невозможно сжать попиксельно
    if result:
        im_result = Image.new("RGBA", (int(size), int(size)), (255, 0, 0, 0))
        im_result.paste(region)
    # Если изображение можно сжать попиксельно
    else:
        im_result = Image.new("RGBA", (int(size / 2), int(size / 2)), (255, 0, 0, 0))
        for x in range(int(size / 2)):
            for y in range(int(size / 2)):
                pixel_box = (x * 2, y * 2, x * 2 + 1, y * 2 + 1)
                pixel_region = region.crop(pixel_box)
                pixel_box2 = (x, y)
                im_result.paste(pixel_region, pixel_box2)
    return im_result


# Перечисление спрайта
for pattern in wiki_sprite["IDы"]:
    # Исключение заглушки Неизвестно из генерации
    if pattern != "Неизвестно":
        # Определение позиции спрайта
        x_sprite = (int(wiki_sprite["IDы"][pattern]["поз"]) - 1) % item_format
        y_sprite = (int(wiki_sprite["IDы"][pattern]["поз"]) - 1) // item_format
        x = x_sprite * size
        y = y_sprite * size
        box = (x, y, x + size, y + size)
        # Получение иконки со спрайта
        region = im.crop(box)
        # Проверка наличия плохих символов
        if ":" in pattern or "/" in pattern:
            if ":" in pattern:
                pattern_fix = pattern.replace(":", "-")
                # Название файла
                img_name = "Grid " + pattern_fix + " (" + mod_name + ").png"
                # Запись псевдонима
                aliases_list = aliases_list + aliases_fix_proc(pattern, pattern_fix)
                # название предмета для таблицы
                tem_name = pattern_fix
            if "/" in pattern:
                pattern_fix = pattern.replace("/", "-")
                # Название файла
                img_name = "Grid " + pattern_fix + " (" + mod_name + ").png"
                # Запись псевдонима
                aliases_list = aliases_list + aliases_fix_proc(pattern, pattern_fix)
                # Название предмета для таблицы
                item_name = pattern_fix
        else:
            # Название файла
            img_name = "Grid " + pattern + " (" + mod_name + ").png"
            # Запись псевдонима для англоязычного названия, если оно есть
            if wiki_sprite["IDы"][pattern].get("en") != None:
                enNamesModule = (
                    enNamesModule
                    + f'	["{pattern}"] = "{wiki_sprite["IDы"][pattern]["en"]}",\n'
                )
            # Название предмета для таблицы
            item_name = pattern
        compress_neighbor_pixels(region).save(f"{target_path}\\{img_name}")
        # Генерация названий для обычных спрайтов
        sprite_name = f"Спрайт-{mod_name.replace(" ", "-")} {pattern.lower().replace(" ", "-")}.png"

        # Дополнение словаря изображений если размер 16
        if compress_neighbor_pixels(region).size[0] == 16:
            redirects_list.update({sprite_name: img_name})
        else:
            redirects_list_32.update({sprite_name: img_name})

        # Таблица проверки результатов
        sprite_table = (
            f"{sprite_table}\n!{pattern}\n|[[Файл:{img_name}|Grid]]\n|"
            + "{{Слот|"
            + mod_name
            + ":"
            + pattern
            + "}}\n|[[:Файл:"
            + f"{sprite_name}|СпрайтФайл]]\n|[[Файл:{sprite_name}|32px]]\n|-"
        )

# Сохранение словарика перенаправлений
# 16
with open(f"{target_path}\\Redirects.json", "w", encoding="utf-8") as dictionary:
    json.dump(redirects_list, dictionary, ensure_ascii=False)
# 32
with open(f"{target_path}\\Redirects32.json", "w", encoding="utf-8") as dictionary32:
    json.dump(redirects_list_32, dictionary32, ensure_ascii=False)

# Сохранение таблицы
with open(
    f"{target_path}\\Table.mediawiki", "w", encoding="utf-8"
) as sprite_table_file:
    sprite_table_file.write(re.sub(r"\|-$", "|}", sprite_table))

# Сохранение псевдонимов
with open(f"{target_path}\\Aliases.lua", "w", encoding="utf-8") as aliases_file:
    aliases_file.write(re.sub(",\n$", "\n", aliases_list + f"}}"))

# Сохранение англоязычных названий и подключение названий, определённых через шаблон {{Англ}}

with open(f"{target_path}\\EnNames.lua", "w", encoding="utf-8") as enNames_file:
    enNames_file.write(
        re.sub(",\n$", "\n", enNamesModule)
        + f'}}\n\n-- Импорт названий, определённых через шаблон {{{{Англ}}}}\nlocal queryLimit = 500\nlocal queryOffset = 0\nlocal queryCount = 0\nrepeat\n		local queryResults = mw.ext.bucket("en_name")\n		.select("ru", "en")\n		.where{{"mod", "{mod_name}"}}\n		.limit(queryLimit)\n		.offset(queryOffset)\n		.run()\n	if queryResults then\n		queryCount = #queryResults\n		for _, result in ipairs(queryResults) do\n			enNames[result.ru] = result.en\n		end\n		queryOffset = queryOffset + queryLimit\n	else\n		error("[[Модуль:Инвентарный слот/Англоязычные названия/{mod_name}]]: Ошибка запроса Bucket")\n		break\n	end\nuntil queryCount < queryLimit\n\nreturn enNames'
    )
