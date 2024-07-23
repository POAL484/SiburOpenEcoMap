import flet as ft

import legacy_grid

class SiburBlock(ft.Container):
    def __init__(self,
                 page: ft.Page,
                 title: ft.Text,
                 _content2: ft.Container,
                 _content1: ft.Container,
                 width: int, height: int,
                 order: bool = True):
        super().__init__(width=width, height=height)
        self.page = page
        wgrid = legacy_grid.RowGridView((2, 1))
        _content2.width = wgrid.calc_grid(2, width)
        _content1.width = wgrid.calc_grid(1, width)
        self.content = ft.Column([
            title,
            ft.Row([
                _content2, _content1 if order else _content1, _content2
            ], vertical_alignment=ft.CrossAxisAlignment.START)
        ], ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

class SiburColumnBlock(ft.Container):
    def __init__(self,
                 page: ft.Page,
                 title: ft.Text,
                 _content2: ft.Container,
                 _content1: ft.Container,
                 width: int, height: int,
                 order: bool = True):
        super().__init__(width=width, height=height)
        self.page = page
        self.content = ft.Column([
            title,
            
        ] + [_content2, _content1] if order else [_content1, _content2], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll='adaptive')