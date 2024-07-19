import flet as ft
import flet.map as map

from legacy_v3_grid import *

def page_index(page: ft.Page):

    def res(e: ft.WindowResizeEvent):
        for component in page.controls:
            if isinstance(component, page.c.Graph):
                component.upd()
            if isinstance(component, page.c.SiburAppBar):
                component.recalc()
        print(f"new size: w:{page.width} h:{page.height}")

    page.graph = page.c.Graph(page, [1, 11, 100, 50, 0, 54, 23, 65, 12, 56, 12, 55, 111, 5, 63, 12, 66, 61, 65, 22, 55, 22, 5, 12, 35, 42, 21, 55, 112, 4, 235, 52, 52, 11, 52, 12, 35, 124, 234, 123, 123, 12, 123, 12, 123, 123, 123, 321],
                          (71, 0, 64), (244, 71, 212))

    page.on_resized = res

    #page.add(page.graph)

    '''page.add(map.Map(configuration=map.MapConfiguration(
        initial_center = map.MapLatitudeLongitude(43.413991, 39.953606),
        initial_zoom = 17, on_init=lambda e: print(f"Initialized Map")),
        layers=[
                map.TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    on_image_error=lambda e: print("TileLayer Error"),
                ),], expand=True, ))'''
    
    page.add(page.c.SiburAppBar(page))

    page.add(ft.TextButton("asdasd"))
