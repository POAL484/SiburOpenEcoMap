import flet as ft

import legacy_grid

def page_links(page: ft.Page):
    if page.width > 800:
        mgrid = legacy_grid.RowGridView((1, 3, 1, 3, 1))
        page.add(
            ft.Row([
                page.c.SiburLinkBlock(
                    page,
                    "Телеграм бот",
                    "Телеграм бот, который используется сотрудниками лабораторий для ввода результатов анализов. В данный момент действия для простых пользователей находятся в разработке",
                    "https://t.me/SiburOpenEcoMapBot",
                    mgrid.calc_grid(3, page.width-10)
                ),
                page.c.SiburLinkBlock(
                    page,
                    "GitHub Repo",
                    "Репозиторий со всем исходным кодом на GitHub, всключая сервер, телеграм бот, цифровую платформу для мониторинга и код для роботизировнных установок",
                    "https://github.com/POAL484/SiburOpenEcoMap",
                    mgrid.calc_grid(3, page.width-10)
                )
            ], ft.MainAxisAlignment.SPACE_EVENLY)
        )
        page.add(
            ft.Row([
                page.c.SiburLinkBlock(
                    page,
                    "СИБУР",
                    "Компания «ПАО «СИБУР Холдинг» явлюяется заказчиком и партнером проект Открытой Экологической Карты СИБУР",
                    "https://sibur.ru",
                    mgrid.calc_grid(3, page.width-10)
                ),
                page.c.SiburLinkBlock(
                    page,
                    "Проектный сайт",
                    "Сайт в архиве больших вызовов, где можно больше узнать о проекте",
                    "https://clck.ru/9TFat",
                    mgrid.calc_grid(3, page.width-10)
                )
            ], ft.MainAxisAlignment.SPACE_EVENLY)
        )
        page.add(
            ft.Row([
                page.c.SiburLinkBlock(
                    page,
                    "Кокурс «Большие Вызовы»",
                    "Данных проект был разработан в рамках проектной научно-технической смены «Большие вызовы» в образовательном центре «Сириус»",
                    "https://konkurs.sochisirius.ru",
                    mgrid.calc_grid(3, page.width-10)
                ),
                page.c.SiburLinkBlock(
                    page,
                    "ОЦ «Сириус»",
                    "Данных проект был разработан в рамках проектной научно-технической смены «Большие вызовы» в образовательном центре «Сириус»",
                    "https://sochisirius.ru",
                    mgrid.calc_grid(3, page.width-10)
                )
            ], ft.MainAxisAlignment.SPACE_EVENLY)
        )
    else:
        page.scroll = ft.ScrollMode.HIDDEN
        page.add(
            ft.Column([
                page.c.SiburLinkBlock(
                    page,
                    "Телеграм бот",
                    "Телеграм бот, который используется сотрудниками лабораторий для ввода результатов анализов. В данный момент действия для простых пользователей находятся в разработке",
                    "https://t.me/SiburOpenEcoMapBot",
                    page.width
                ),
                page.c.SiburLinkBlock(
                    page,
                    "GitHub Repo",
                    "Репозиторий со всем исходным кодом на GitHub, всключая сервер, телеграм бот, цифровую платформу для мониторинга и код для роботизировнных установок",
                    "https://github.com/POAL484/SiburOpenEcoMap",
                    page.width
                ),
                page.c.SiburLinkBlock(
                    page,
                    "СИБУР",
                    "Компания «ПАО «СИБУР Холдинг» явлюяется заказчиком и партнером проект Открытой Экологической Карты СИБУР",
                    "https://sibur.ru",
                    page.width
                ),
                page.c.SiburLinkBlock(
                    page,
                    "Проектный сайт",
                    "Сайт в архиве больших вызовов, где можно больше узнать о проекте",
                    "https://clck.ru/9TFat",
                    page.width
                ),
                page.c.SiburLinkBlock(
                    page,
                    "Кокурс «Большие Вызовы»",
                    "Данных проект был разработан в рамках проектной научно-технической смены «Большие вызовы» в образовательном центре «Сириус»",
                    "https://konkurs.sochisirius.ru",
                    page.width
                ),
                page.c.SiburLinkBlock(
                    page,
                    "ОЦ «Сириус»",
                    "Данных проект был разработан в рамках проектной научно-технической смены «Большие вызовы» в образовательном центре «Сириус»",
                    "https://sochisirius.ru",
                    page.width
                )], horizontal_alignment=ft.CrossAxisAlignment.CENTER))