import flet as ft

import legacy_grid

from PIL import ImageFont

pomidor = ImageFont.truetype("fonts/segoeui.ttf", 100)

DEER_IMG = "https://i.ibb.co/PFLMFhh/deer-icon-white.png"
BEAR_IMG = "https://i.ibb.co/N9mjH5T/bear-icon-white.png"
BUNNY_IMG = "https://i.ibb.co/QbqTCcw/bunny-icon-white.png"

def page_device_uid(page: ft.Page, route: str):
    grid3 = legacy_grid.RowGridView((1, 1, 1))
    page.add(ft.Row([
        ft.Image(BUNNY_IMG, width=min(grid3.calc_grid(1, page.width-5), 250), height=min(grid3.calc_grid(1, page.width-5), 250)),
        ft.Image(BEAR_IMG, width=min(grid3.calc_grid(1, page.width-5), 250), height=min(grid3.calc_grid(1, page.width-5), 250)),
        ft.Image(DEER_IMG, width=min(grid3.calc_grid(1, page.width-5), 250), height=min(grid3.calc_grid(1, page.width-5), 250)),
    ], spacing=0))
    page.add(ft.Text("Вот это да!", size=page.u.calculateFont(pomidor, page.width/1.8, "Вот это да!"), font_family="Segoe UI", weight=ft.FontWeight.BOLD))
    page.add(ft.Text(
        "Кажется, вы попали в раздел, который еще находиться в разработке! Ниже вы можете перейти на другие страницы:"
    ))
    page.add(ft.Row([
        ft.ElevatedButton("Главная >", on_click=lambda e: page.go("/")),
        ft.ElevatedButton("Карта >", on_click=lambda e: page.go("/map"))
    ]))
