import flet as ft

import flet.canvas as cv

from PIL import ImageFont

from legacy_grid import RowGridView

font = ImageFont.truetype("fonts/seguibli.ttf", 100)

#0.26

class SiburAppBar(ft.Container):
    def __init__(self, page: ft.Page):
        self.grid = RowGridView((1, 3, 2, 3, 2, 3, 2, 3, 1))
        self.maxFontSize = 34
        super().__init__()
        self.page = page
        self.is_banner = False
        #self.recalc()

    def toggle_banner(self, e: ft.ContainerTapEvent):
        if self.is_banner: self.page.close(self.banner)
        else: self.page.open(self.banner)
        self.is_banner = not self.is_banner

    def calc_size(self):
        w = self.page.width
        if w >= 800:
            return max(
                self.grid.calc_grid(3, w)*.26,
                min(self.page.u.calculateFont(font, self.grid.calc_grid(3, w), "KAPTA"), self.maxFontSize),
                min(self.page.u.calculateFont(font, self.grid.calc_grid(3, w), "API"), self.maxFontSize),
                min(self.page.u.calculateFont(font, self.grid.calc_grid(3, w), "ССЫЛКИ"), self.maxFontSize)
            ) + 45
        else:
            return ((w/3)*.26) + 45

    def recalc(self):
        if self.is_banner:
            self.page.close(self.banner)
            self.is_banner = False
        w = self.page.width
        self.banner = ft.Banner( #менюшка для мобилок
            ft.Container(
                ft.Column([
                    ft.Container(ft.Image("https://i.ibb.co/ky7MyMc/siburok.png", width=w/1.75, height=(w/1.75)*0.26), alignment=ft.alignment.Alignment(0, 0), on_click=lambda e: self.page.go("/")),
                    ft.Container(ft.Text("KAPTA", size=(min(self.page.u.calculateFont(font, w/1.75, "KAPTA"), self.maxFontSize)), font_family="Segoe UI", weight=ft.FontWeight.W_900, italic=True, text_align=ft.TextAlign.CENTER), alignment=ft.alignment.Alignment(0, 0), width=w, on_click=lambda e: self.page.go("/map")),
                    ft.Container(ft.Text("API", size=(min(self.page.u.calculateFont(font, w/1.75, "API"), self.maxFontSize)), font_family="Segoe UI", weight=ft.FontWeight.W_900, italic=True, text_align=ft.TextAlign.CENTER), alignment=ft.alignment.Alignment(0, 0), width=w, on_click=lambda e: self.page.go("/api")),
                    ft.Container(ft.Text("ССЫЛКИ", size=(min(self.page.u.calculateFont(font, w/1.75, "ССЫЛКИ"), self.maxFontSize)), font_family="Segoe UI", weight=ft.FontWeight.W_900, italic=True, text_align=ft.TextAlign.CENTER), alignment=ft.alignment.Alignment(0, 0), width=w, on_click=lambda e: self.page.go("/links")),
                ], ft.MainAxisAlignment.CENTER)
            ), actions=[ft.Container(width=0, height=0)]
        )
        if w >= 800: #бар для пк
            self.content = ft.Column([ft.Row([
                    ft.Container(width=self.grid.calc_grid(1, w)),
                    ft.Container(ft.Image("https://i.ibb.co/ky7MyMc/siburok.png", width=self.grid.calc_grid(3, w), height=self.grid.calc_grid(3, w)*0.26), on_click=lambda e: self.page.go("/")),
                    ft.Container(width=self.grid.calc_grid(2, w)),
                    ft.Container(ft.Text("KAPTA", size=min(self.page.u.calculateFont(font, self.grid.calc_grid(3, w), "KAPTA"), self.maxFontSize), font_family="Segoe UI", weight=ft.FontWeight.W_900, italic=True), width=self.grid.calc_grid(3, w), on_click=lambda e: self.page.go("/map")),
                    ft.Container(width=self.grid.calc_grid(2, w)),
                    ft.Container(ft.Text("API", size=min(self.page.u.calculateFont(font, self.grid.calc_grid(3, w), "API"), self.maxFontSize), font_family="Segoe UI", weight=ft.FontWeight.W_900, italic=True), width=self.grid.calc_grid(3, w), on_click=lambda e: self.page.go("/api")),
                    ft.Container(width=self.grid.calc_grid(2, w)),
                    ft.Container(ft.Text("ССЫЛКИ", size=min(self.page.u.calculateFont(font, self.grid.calc_grid(3, w), "ССЫЛКИ"), self.maxFontSize), font_family="Segoe UI", weight=ft.FontWeight.W_900, italic=True), width=self.grid.calc_grid(3, w), on_click=lambda e: self.page.go("/links")),
                    ft.Container(width=self.grid.calc_grid(1, w))
                ]), 
                ft.Container(bgcolor="white", height=2, width=w)])
        else: #кнопка для мобилок
            self.content = ft.Column([
                ft.Container(ft.Row([
                    ft.Icon(ft.icons.KEYBOARD_ARROW_UP, "#02818a"),
                    ft.Image("https://i.ibb.co/ky7MyMc/siburok.png", width=(w/3), height=(w/3)*0.26),
                    ft.Icon(ft.icons.KEYBOARD_ARROW_UP, "#02818a"),
                ], ft.MainAxisAlignment.SPACE_EVENLY), on_click=self.toggle_banner),
            ft.Container(bgcolor="white", height=2, width=w)], )
        self.update()