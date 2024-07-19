import flet as ft

def page_404(page: ft.Page):

    page.add(ft.Text("Ошибка 404: Страница не найдена!", size=page.height/5, weight=ft.FontWeight.W_900, font_family="Segoe UI"))
    page.add(ft.ElevatedButton("Ha главную", on_click=lambda e: page.go("/")))