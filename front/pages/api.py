import flet as ft

import legacy_grid

from PIL import ImageFont

pomidor = ImageFont.truetype("fonts/segoeui.ttf", 100)

BEAR_IMG = "https://i.ibb.co/N9mjH5T/bear-icon-white.png"

def page_api(page: ft.Page):
    grid3 = legacy_grid.RowGridView((1, 1, 1))
    page.add(ft.Row([
        ft.Image(BEAR_IMG, width=min(grid3.calc_grid(1, page.width-5), 250), height=min(grid3.calc_grid(1, page.width-5), 250)),
        ft.Image(BEAR_IMG, width=min(grid3.calc_grid(1, page.width-5), 250), height=min(grid3.calc_grid(1, page.width-5), 250)),
        ft.Image(BEAR_IMG, width=min(grid3.calc_grid(1, page.width-5), 250), height=min(grid3.calc_grid(1, page.width-5), 250)),
    ], spacing=0))
    page.add(ft.Text("Даже медведи грустят по этому поводу", size=page.u.calculateFont(pomidor, page.width/1.2, "Даже медведи грустят по этому поводу"), font_family="Segoe UI", weight=ft.FontWeight.BOLD))
    page.add(ft.Text(spans=[
        ft.TextSpan("К сожалению, раздел с описанием API для разработчиков сейчас находиться в разработке, но вы все еще можете использовать наш API! Для знакомства с ним можете использовать "),
        ft.TextSpan("заметки в исходном код на GitHub", ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT, decoration=ft.TextDecoration.UNDERLINE), url="https://github.com/POAL484/SiburOpenEcoMap/blob/master/back/app.py")
    ]))
