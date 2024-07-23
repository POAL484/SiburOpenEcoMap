import flet as ft
import flet.map as map

import legacy_grid

from PIL import ImageFont

fontBlack = ImageFont.truetype("fonts/seguibl.ttf", 100)
fontBlackItalic = ImageFont.truetype("fonts/seguibli.ttf", 100)
fontDef = ImageFont.truetype("fonts/segoeui.ttf", 100)

DEER_IMG = "https://i.ibb.co/PFLMFhh/deer-icon-white.png"
BEAR_IMG = "https://i.ibb.co/N9mjH5T/bear-icon-white.png"
BUNNY_IMG = "https://i.ibb.co/QbqTCcw/bunny-icon-white.png"

def page_index(page: ft.Page):

    h = page.height - page.controls[0].calc_size() - 50

    welcomegrid = legacy_grid.RowGridView((2, 1, 2))
    page.add(ft.Container(ft.Column([
        ft.Text(spans=[
            ft.TextSpan("Открытая экологическая карта "),
            ft.TextSpan("СИБУР", ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT))
        ], size=page.u.calculateFont(fontBlack, page.width/1.1, "Открытая экологическая карта СИБУР"), font_family="Segoe UI", text_align=ft.TextAlign.CENTER),
        ft.Text(spans=[
            ft.TextSpan("Мы проводим "),
            ft.TextSpan("экологический мониторинг", ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT))
        ], size=page.u.calculateFont(fontDef, page.width/1.5, "Мы проводим экологический мониторинг"), font_family="Segoe UI", text_align=ft.TextAlign.CENTER)
    ], ft.MainAxisAlignment.SPACE_EVENLY, ft.CrossAxisAlignment.CENTER), height=welcomegrid.calc_grid(2, h), alignment=ft.Alignment(0, 0)))
    page.add(ft.Container(
        ft.Text(spans=[
            ft.TextSpan("Прямо сейчас", ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT)),
            ft.TextSpan(" в России:")
        ], size=page.u.calculateFont(fontDef, page.width/2, "Прямо сейчас в России:"), font_family="Segoe UI", text_align=ft.TextAlign.CENTER)
    , height=welcomegrid.calc_grid(1, h), alignment=ft.Alignment(0, 0)))
    half3 = legacy_grid.RowGridView((1, 1, 1.125))
    if page.width > 800:
        page.add(ft.Container(
            ft.Column([
                ft.Row([
                    ft.Row([
                        ft.Image(BUNNY_IMG, width=half3.calc_grid(1, half3.calc_grid(1, page.width)), height=half3.calc_grid(1, half3.calc_grid(1, page.width))),
                        ft.Text(page.storage.count['bunny'], font_family="Segoe UI", size=page.u.calculateFont(fontDef, half3.calc_grid(2, half3.calc_grid(1, page.width)), f"{page.storage.count['bunny']}{page.storage.count['bunny']} СЧАСТЛИВЫХ")*2),
                        ft.Column([
                            ft.Text("Счастливых", font_family="Segoe UI", size=page.u.calculateFont(fontDef, half3.calc_grid(2, half3.calc_grid(1, page.width)), f"{page.storage.count['bunny']}{page.storage.count['bunny']} Счастливых")),
                            ft.Text("Кроликов", font_family="Segoe UI", size=page.u.calculateFont(fontDef, half3.calc_grid(2, half3.calc_grid(1, page.width)), f"{page.storage.count['bunny']}{page.storage.count['bunny']} Счастливых"))
                        ])
                    ]),
                    ft.Row([
                        ft.Image(BEAR_IMG, width=half3.calc_grid(1, half3.calc_grid(1, page.width)), height=half3.calc_grid(1, half3.calc_grid(1, page.width))),
                        ft.Text(page.storage.count['bear'], font_family="Segoe UI", size=page.u.calculateFont(fontDef, half3.calc_grid(2, half3.calc_grid(1, page.width)), f"{page.storage.count['bear']}{page.storage.count['bear']} ГРУСТНЫХ")*2),
                        ft.Column([
                            ft.Text("Грустных", font_family="Segoe UI", size=page.u.calculateFont(fontDef, half3.calc_grid(2, half3.calc_grid(1, page.width)), f"{page.storage.count['bear']}{page.storage.count['bear']} Грустных")),
                            ft.Text("Медведей", font_family="Segoe UI", size=page.u.calculateFont(fontDef, half3.calc_grid(2, half3.calc_grid(1, page.width)), f"{page.storage.count['bear']}{page.storage.count['bear']} Грустных"))
                        ])
                    ]),
                    ft.Row([
                        ft.Image(DEER_IMG, width=half3.calc_grid(1, half3.calc_grid(1, page.width)), height=half3.calc_grid(1, half3.calc_grid(1, page.width))),
                        ft.Text(page.storage.count['deer'], font_family="Segoe UI", size=page.u.calculateFont(fontDef, half3.calc_grid(2, half3.calc_grid(1, page.width)), f"{page.storage.count['deer']}{page.storage.count['deer']} БОЛЬНЫХ")*2),
                        ft.Column([
                            ft.Text("Больных", font_family="Segoe UI", size=page.u.calculateFont(fontDef, half3.calc_grid(2, half3.calc_grid(1, page.width)), f"{page.storage.count['deer']}{page.storage.count['deer']} Больных")),
                            ft.Text("Оленей", font_family="Segoe UI", size=page.u.calculateFont(fontDef, half3.calc_grid(2, half3.calc_grid(1, page.width)), f"{page.storage.count['deer']}{page.storage.count['deer']} Больных"))
                        ])
                    ])
                ]),
                ft.Container(
                    ft.ElevatedButton(content=ft.Text("Подробнее на карте >", size=page.u.calculateFont(fontDef, half3.calc_grid(.8, page.width), "Подробнее на карте >"), style=ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT)), width=half3.calc_grid(1, page.width), on_click=lambda e: page.go("/map")), alignment=ft.Alignment(1, 0)
                )
            ])
        ))
    else:
        grid6 = legacy_grid.RowGridView((6,))
        page.add(ft.Container(
            ft.Column([
                ft.Column([
                    ft.Row([
                        ft.Image(BUNNY_IMG, width=half3.calc_grid(1, half3.calc_grid(1, page.width)), height=half3.calc_grid(1, half3.calc_grid(1, page.width))),
                        #ft.Text(page.storage.count['bunny'], font_family="Segoe UI", size=page.u.calculateFont(fontDef, half3.calc_grid(2, half3.calc_grid(1, page.width)), f"{page.storage.count['bunny']} СЧАСТЛИВЫХ КРОЛИКОВ")),
                        #ft.Column([
                            ft.Text(f"{page.storage.count['bunny']} Счастливых кроликов", font_family="Segoe UI", size=page.u.calculateFont(fontDef, grid6.calc_grid(4.5, page.width), f"{page.storage.count['bunny']} Счастливых кроликов")),
                            #ft.Text("КРОЛИКОВ", font_family="Segoe UI", size=page.u.calculateFont(fontDef, half3.calc_grid(2, half3.calc_grid(1, page.width)), f"{page.storage.count['bunny']}{page.storage.count['bunny']} СЧАСТЛИВЫХ"))
                        #])
                    ]),
                    ft.Row([
                        ft.Image(BEAR_IMG, width=half3.calc_grid(1, half3.calc_grid(1, page.width)), height=half3.calc_grid(1, half3.calc_grid(1, page.width))),
                        #ft.Text(page.storage.count['bear'], font_family="Segoe UI", size=page.u.calculateFont(fontDef, half3.calc_grid(2, half3.calc_grid(1, page.width)), f"{page.storage.count['bear']}{page.storage.count['bear']} ГРУСТНЫХ")*2),
                        #ft.Column([
                            ft.Text(f"{page.storage.count['bear']} Грустных медведей", font_family="Segoe UI", size=page.u.calculateFont(fontDef, grid6.calc_grid(4.5, page.width), f"{page.storage.count['bear']} Грустных медведей")),
                            #ft.Text("МЕДВЕДЕЙ", font_family="Segoe UI", size=page.u.calculateFont(fontDef, half3.calc_grid(2, half3.calc_grid(1, page.width)), f"{page.storage.count['bear']}{page.storage.count['bear']} МЕДВЕДЕЙ"))
                        #])
                    ]),
                    ft.Row([
                        ft.Image(DEER_IMG, width=half3.calc_grid(1, half3.calc_grid(1, page.width)), height=half3.calc_grid(1, half3.calc_grid(1, page.width))),
                        #ft.Text(page.storage.count['deer'], font_family="Segoe UI", size=page.u.calculateFont(fontDef, half3.calc_grid(2, half3.calc_grid(1, page.width)), f"{page.storage.count['deer']}{page.storage.count['deer']} БОЛЬНЫХ")*2),
                        #ft.Column([
                            ft.Text(f"{page.storage.count['deer']} Больных оленей",  font_family="Segoe UI",  size=page.u.calculateFont(fontDef, grid6.calc_grid(4.5, page.width), f"{page.storage.count['deer']} Больных оленей")),
                            #ft.Text("ОЛЕНЕЙ", font_family="Segoe UI", size=page.u.calculateFont(fontDef, half3.calc_grid(2, half3.calc_grid(1, page.width)), f"{page.storage.count['deer']}{page.storage.count['deer']} БОЛЬНЫХ"))
                        #])
                    ])
                ]),
                ft.Container(
                    ft.ElevatedButton(content=ft.Text("Подробнее на карте >", size=page.u.calculateFont(fontDef, half3.calc_grid(.8, page.width), "Подробнее на карте >"), style=ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT)), width=half3.calc_grid(1, page.width), on_click=lambda e: page.go("/map")), alignment=ft.Alignment(1, 0)
                )
            ])
        ))