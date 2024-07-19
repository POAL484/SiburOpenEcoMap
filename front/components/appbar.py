import flet as ft

from PIL import ImageFont

from legacy_grid import RowGridView

font = ImageFont.truetype("fonts/seguibli.ttf", 100)

#0.26

class SiburAppBar(ft.Container):
    def __init__(self, page: ft.Page):
        grid = RowGridView((1, 3, 2, 3, 2, 3, 2, 3, 1))
        w = page.width
        maxFontSize = 34
        super().__init__(
            ft.Row([
                ft.Container(width=grid.calc_grid(1, w)),
                ft.Container(ft.Image("https://i.ibb.co/ky7MyMc/siburok.png", width=grid.calc_grid(3, w), height=grid.calc_grid(3, w)*0.26), on_click=lambda e: print(e)),
                ft.Container(width=grid.calc_grid(2, w)),
                ft.Container(ft.Text("KAPTA", size=min(page.u.calculateFont(font, grid.calc_grid(3, w), "KAPTA"), maxFontSize), font_family="Segoe UI", weight=ft.FontWeight.W_900, italic=True), width=grid.calc_grid(3, w)),
                ft.Container(width=grid.calc_grid(2, w)),
                ft.Container(ft.Text("КАРТЫ СИБУРА", size=min(page.u.calculateFont(font, grid.calc_grid(3, w), "КАРТЫ СИБУРА"), maxFontSize), font_family="Segoe UI", weight=ft.FontWeight.W_900, italic=True), width=grid.calc_grid(3, w)),
                ft.Container(width=grid.calc_grid(2, w)),
                ft.Container(ft.Text("API", size=min(page.u.calculateFont(font, grid.calc_grid(3, w), "API"), maxFontSize), font_family="Segoe UI", weight=ft.FontWeight.W_900, italic=True), width=grid.calc_grid(3, w)),
                ft.Container(width=grid.calc_grid(1, w))
            ]), 
        )