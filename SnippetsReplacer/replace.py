# Настройки
ReorganizationrReplaceList = False

# Открываем файл для чтения
with open("page.wikitext", "r", encoding="utf8") as file:
    # Читаем содержимое файла в строку
    text = file.read()

if ReorganizationrReplaceList:
    # Переменная файла со снипетами с указанием аргументов
    f = open("snippets.txt", encoding="utf8")
    # Указание строки, с которой начинается чтение
    n = 0
    # Очистка файла replacelist.py и задание названия массива
    with open("replacelist.py", "w", encoding="utf8") as stream:
        stream.write("patterns = [" + "\n")
        stream.close()
    # Построковое чтение сниппетов и их запись в файл замен
    for l in f:
        # print(l)
        id = l.replace("\r", "").replace("\n", "")
        n += 1
        if (n % 2) == 1:
            find = id
        else:
            replace = id
            # print(find + replace)
            out = '    ("' + str(find) + '", "' + str(replace) + '"),'
            # print(out)
            with open("replacelist.py", "a", encoding="utf8") as stream:
                stream.write(str(out) + "\n")
                stream.close()
    # Закрытие массива
    with open("replacelist.py", "a", encoding="utf8") as stream:
        stream.write("]")
        stream.close()


# Чтение массива шаблонов для замены
from replacelist import patterns

# Для каждого шаблона в списке
for pattern in patterns:
    # Получаем слово для поиска и слово для замены
    search, replace = pattern
    # Заменяем все вхождения слова для поиска на слово для замены в тексте
    text = text.replace(search, replace)

# Открываем файл для записи
with open("out_page.wikitext", "w", encoding="utf8") as file:
    # Записываем измененный текст в файл
    file.write(text)
