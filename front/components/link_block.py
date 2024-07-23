import flet as ft

class SiburLinkBlock(ft.OutlinedButton):
    def __init__(self, page: ft.Page, name: str, desc: str, link: str, width: int):
        super().__init__(
            content=ft.Column([
                ft.Text(name, size=30, style=ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT)),
                ft.Text(desc, style=ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT))
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(10)),
            on_click=lambda e: page.launch_url(link),
            width=width
        )