import flet as ft
import requests as req
import threading as thrd

from pages import *
import components
import utility
import colors
import req_storage

storage = req_storage.Storage()
storage.fetch()
thrd.Thread(target=storage.keep).start()

def main(page: ft.Page):
    def router(e: ft.RouteChangeEvent):
        if len(page.controls) >= 1:
            if page.controls[0].is_banner:
                page.close(page.controls[0].banner)
        page.clean()
        page.scroll = None
        page.add(page.c.SiburAppBar(page))
        page.controls[-1].recalc()
        if e.route.split("/")[1] == "device":
            ROUTES["/device/<>"](page, e.route)
            return
        try:
            ROUTES[e.route](page)
        except KeyError:
            page.go("/404")

    def res(e: ft.WindowResizeEvent):
        for component in page.controls:
            if isinstance(component, page.c.Graph):
                component.upd()
            if isinstance(component, page.c.SiburAppBar):
                component.recalc()
        print(f"new size: w:{page.width} h:{page.height}")

    page.on_resized = res

    page.c = components
    page.u = utility
    page.cols = colors

    page.storage = storage

    page.theme_mode = ft.ThemeMode.DARK

    page.on_route_change = router

    page.go(page.route)

ft.app(main, host="0.0.0.0", port=80, view=None, assets_dir="assets")