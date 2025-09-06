# Конвертирует текстовые файлы в словарь json.
# Каждая нечётная строка - ключ, следующая за ней (чётная) - значение

import json

# Пути к файлам
txtFilePath = "Redirects.txt"
jsonFilePath = "Redirects.json"


def file_to_json(txtFilePath):
    result = {}
    with open(txtFilePath, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i in range(0, len(lines) - 1, 2):
            key = lines[i].strip()
            value = lines[i + 1].strip()
            result[key] = value
    return result


json_dict = file_to_json(txtFilePath)

# Сохранение в JSON-файл
with open(jsonFilePath, "w", encoding="utf-8") as json_file:
    json.dump(json_dict, json_file, ensure_ascii=False, indent=4)
