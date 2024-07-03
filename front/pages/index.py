import flet as ft

def page_index(page: ft.Page):

    def res(e: ft.WindowResizeEvent):
        for component in page.controls:
            if isinstance(component, page.c.Graph):
                component.upd()

    page.graph = page.c.Graph(page, [1, 11, 100, 50, 0, 54, 23, 65, 12, 56, 12, 55, 111, 5, 63, 12, 66, 61, 65, 22, 55, 22, 5, 12, 35, 42, 21, 55, 112, 4, 235, 52, 52, 11, 52, 12, 35, 124, 234, 123, 123, 12, 123, 12, 123, 123, 123, 321],
                          (71, 0, 64), (244, 71, 212))

    page.on_resized = res

    page.add(page.graph)
    page.add(ft.TextButton("asdasd"))
