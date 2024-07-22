import flet as ft

from PIL import ImageFont

font = ImageFont.truetype("fonts/seguibl.ttf", 100)

def page_404(page: ft.Page):

    page.add(ft.Text("Ошибка 404: Страница не найдена!", size=page.u.calculateFont(font, page.width/1.1, "Ошибка 404: Страница не найдена"), weight=ft.FontWeight.W_900, font_family="Segoe UI"))
    page.add(ft.ElevatedButton("Ha главную", on_click=lambda e: page.go("/")))