# Позволяет анимировать инвентарные иконки предметов и жидкостей.
# Требует файлы предметов с анимацией, разложенной вниз, и файлов
# mcmeta, содержащих время отображения каждого кадра.

from PIL import Image
import os, json

# Получение списка изображений с расширением .png в текущем каталоге
filtered_files = [
    file_name for file_name in os.listdir(os.getcwd()) if file_name.endswith(".png")
]

# Перечисление всех изображений с расширением .png
for i in filtered_files:
    frames = []  # Объявление массива для хранения фреймов
    im = Image.open("./" + i)  # Открытие изображения
    framescount = (im.height) // (im.width)  # Подсчёт фреймов
    procframe = 0  # Сброс значения для нового файла
    for procframe in range(1, framescount + 1):  # Сохранение каждого фрейма в массив
        box = (0, (procframe - 1) * (im.width), (im.width), procframe * (im.width))
        region = im.crop(box)
        frames.append(region)
    # Определение скорости анимации
    if os.path.exists(f"{i}.mcmeta"):
        with open(f"{i}.mcmeta", "r", encoding="utf-8") as mcMetaFile:
            mcMetaData = json.load(mcMetaFile)
            frameTime = mcMetaData["animation"]["frametime"] * 50
        # Сохранение анимированного изображения
        frames[0].save(
            f".//{i.replace(".png", ".webp")}",
            save_all=True,
            append_images=frames[1:],  # Срез который игнорирует первый кадр.
            duration=frameTime,
            optimization=True,
            loop=0,
            lossless=True,
        )
    else:
        print(f"❌ Файл «{i}.mcmeta» не найден. Анимация для «{i}» не будет создана.")
