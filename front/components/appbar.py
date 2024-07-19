import flet as ft

from PIL import ImageFont

from legacy_grid import RowGridView

font = ImageFont.truetype("fonts/seguibli.ttf", 100)

#0.26

class SiburAppBar(ft.Container):
    def __init__(self, page: ft.Page):
        self.grid = RowGridView((1, 3, 2, 3, 2, 3, 2, 3, 1))
        self.page = page
        w = page.width
        self.maxFontSize = 34
        super().__init__(
            ft.Column([ft.Row([
                ft.Container(width=self.grid.calc_grid(1, w)),
                ft.Container(ft.Image("https://i.ibb.co/ky7MyMc/siburok.png", width=self.grid.calc_grid(3, w), height=self.grid.calc_grid(3, w)*0.26), on_click=lambda e: print(e)),
                ft.Container(width=self.grid.calc_grid(2, w)),
                ft.Container(ft.Text("KAPTA", size=min(page.u.calculateFont(font, self.grid.calc_grid(3, w), "KAPTA"), self.maxFontSize), font_family="Segoe UI", weight=ft.FontWeight.W_900, italic=True), width=self.grid.calc_grid(3, w)),
                ft.Container(width=self.grid.calc_grid(2, w)),
                ft.Container(ft.Text("ЗАВОДЫ СИБУРА", size=min(page.u.calculateFont(font, self.grid.calc_grid(3, w), "ЗАВОДЫ СИБУРА"), self.maxFontSize), font_family="Segoe UI", weight=ft.FontWeight.W_900, italic=True), width=self.grid.calc_grid(3, w)),
                ft.Container(width=self.grid.calc_grid(2, w)),
                ft.Container(ft.Text("API", size=min(page.u.calculateFont(font, self.grid.calc_grid(3, w), "API"), self.maxFontSize), font_family="Segoe UI", weight=ft.FontWeight.W_900, italic=True), width=self.grid.calc_grid(3, w)),
                ft.Container(width=self.grid.calc_grid(1, w))
            ]), 
            ft.Container(bgcolor="white", height=2, width=w)]), 
        )

    def recalc(self):
        w = self.page.width
        self.content = ft.Column([ft.Row([
                ft.Container(width=self.grid.calc_grid(1, w)),
                ft.Container(ft.Image("https://i.ibb.co/ky7MyMc/siburok.png", width=self.grid.calc_grid(3, w), height=self.grid.calc_grid(3, w)*0.26), on_click=lambda e: print(e)),
                ft.Container(width=self.grid.calc_grid(2, w)),
                ft.Container(ft.Text("KAPTA", size=min(self.page.u.calculateFont(font, self.grid.calc_grid(3, w), "KAPTA"), self.maxFontSize), font_family="Segoe UI", weight=ft.FontWeight.W_900, italic=True), width=self.grid.calc_grid(3, w)),
                ft.Container(width=self.grid.calc_grid(2, w)),
                ft.Container(ft.Text("ЗАВОДЫ СИБУРА", size=min(self.page.u.calculateFont(font, self.grid.calc_grid(3, w), "ЗАВОДЫ СИБУРА"), self.maxFontSize), font_family="Segoe UI", weight=ft.FontWeight.W_900, italic=True), width=self.grid.calc_grid(3, w)),
                ft.Container(width=self.grid.calc_grid(2, w)),
                ft.Container(ft.Text("API", size=min(self.page.u.calculateFont(font, self.grid.calc_grid(3, w), "API"), self.maxFontSize), font_family="Segoe UI", weight=ft.FontWeight.W_900, italic=True), width=self.grid.calc_grid(3, w)),
                ft.Container(width=self.grid.calc_grid(1, w))
            ]), 
            ft.Container(bgcolor="white", height=2, width=w)])
        self.update()