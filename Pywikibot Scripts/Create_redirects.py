import pywikibot, json

# Создает перенаправления из файла ./Redirects.json в заданном пространстве имён.
# Файл Redirects.json Представляет собой словарь вида «"Страница": "Цель перенаправления"» в формате JSON.

summary = "Перенаправление для предмета из прошлой версии"
namespace = "Файл:"

site = pywikibot.Site()
site.login()

with open("Redirects.json", "r", encoding="utf8") as raw_redirects:
    # Преобразование строк JSON в объект Python
    redirects = json.load(raw_redirects)

for item in redirects:
    # title: заголовок новой страницы.
    title = f"{namespace}{item}"
    redirectTarget = f"{namespace}{redirects[item]}"
    # summary: краткое описание изменений.
    page = pywikibot.Page(site, title)
    targetPage = pywikibot.Page(site, redirectTarget)
    # Проверка на существование страницы
    if page.exists():
        print(f"❌ Перенаправление не создано. Страница '{title}' уже существует.")
    else:
        # Предотвращение разорванных перенаправлений
        if targetPage.exists():
            # Предотвращение двойных перенаправлений
            if targetPage.isRedirectPage():
                print(
                    f"🔁 Страница '{redirectTarget}' является перенаправлением. Будет создано перенаправление по цели перенаправления."
                )
                redirectTargetGet = targetPage.getRedirectTarget()
                # content: содержимое новой страницы.
                content = f"#перенаправление [[{redirectTargetGet.title()}]]"
            else:
                # content: содержимое новой страницы.
                content = f"#перенаправление [[{redirectTarget}]]"
            page.text = content
            # Создание страницы
            page.save(summary=summary, bot=True)
        else:
            print(
                f"❌ Перенаправление {title} не создано. Целевая страница {redirectTarget} не существует."
            )
