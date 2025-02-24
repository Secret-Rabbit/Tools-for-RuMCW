import pywikibot, json

# Создает страницу вики с перенаправлениями из файла ./Redirects.json.

site = pywikibot.Site()
site.login()

with open("Redirects.json", "r", encoding="utf8") as raw_redirects:
    # Преобразование строк JSON в объект Python
    redirects = json.load(raw_redirects)

for item in redirects:
    # title: заголовок новой страницы.
    title = f"Файл:{item}"
    # content: содержимое новой страницы.
    content = f"#перенаправление [[Файл:{redirects[item]}]]"
    # summary: краткое описание изменений.
    summary = "Перенаправление для спрайта предмета"
    page = pywikibot.Page(site, title)
    page.text = content
    # Создание страницы
    page.save(summary=summary)
