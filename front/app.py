import flet as ft
import requests as req

from pages import *
import components
import utility
import colors

def main(page: ft.Page):
    def router(e: ft.RouteChangeEvent):
        page.clean()
        page.add(page.c.SiburAppBar(page))
        page.controls[-1].recalc()
        try:
            ROUTES[e.route](page)
        except KeyError:
            page.go("/404")

    page.c = components
    page.u = utility
    page.cols = colors

    page.on_route_change = router

    page.go("/")

ft.app(main, port=80, view=None)