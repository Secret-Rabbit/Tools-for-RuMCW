target_extension = ".png"
framerate = 40

from PIL import Image
import os

file_names = os.listdir(os.getcwd())


def filter_files_by_extension(file_names, target_extension):
    """
    Функция фильтрует список названий файлов по заданному расширению.

    :param file_names: Список названий файлов
    :param target_extension: Желаемое расширение (например, ".txt" или ".jpg")
    :return: Отфильтрованный список файлов в виде массива
    """
    filtered_files = [
        file_name for file_name in file_names if file_name.endswith(target_extension)
    ]
    return filtered_files


# Фильтр, отбрасывавший все файлы, не совпадающие с заданным расширением.
filtered_files = filter_files_by_extension(file_names, target_extension)

for i in filtered_files:
    frames = []  # Объявление массива для хранения фреймов
    # Генерация названия конечного файла
    imggifname = i.replace(target_extension, ".webp")
    im = Image.open("./" + i)  # Открытие изображения
    framescount = (im.height) // (im.width)  # Подсчёт фреймов
    procframe = 0  # Сброс значения для нового файла
    for procframe in range(1, framescount + 1):  # Сохранение каждого фрейма в массив
        box = (0, (procframe - 1) * (im.width), (im.width), procframe * (im.width))
        region = im.crop(box)
        frames.append(region)
    # Сохранение анимированного изображения
    frames[0].save(
        "./" + imggifname,
        save_all=True,
        append_images=frames[1:],  # Срез который игнорирует первый кадр.
        duration=200,
        optimization=True,
        loop=0,
        lossless=True,
    )
