import flet as ft

import flet.map as map

class SiburMap:
    def __init__(self, page: ft.Page, width: int, height: int):
        self.map = map.Map(
            [
                map.TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    on_image_error=lambda e: print("TileLayer Error"),
                    ),
                map.RichAttribution(
                    attributions=[
                        map.TextSourceAttribution(
                            text="OpenStreetMap Contributors",
                            on_click=lambda e: e.page.launch_url(
                                "https://openstreetmap.org/copyright"
                            ),
                        ),
                        map.TextSourceAttribution(
                            text="Sibur",
                            on_click=lambda e: e.page.launch_url("https://sibur.ru"),
                        ),
                    ]
                ),
            ],
            map.MapConfiguration(
                map.MapLatitudeLongitude(62, 95),
                0, 2.9183, map.MapInteractionConfiguration(flags=map.MapInteractiveFlag.ALL)
            ),
            expand=True
        )
        self.devices_layer = map.MarkerLayer([])
        self.count = {"bunny": 0, "bear": 0, "deer": 0}
        for dvc in page.storage.devices:
            self.devices_layer.markers.append(page.c.Animal(page, dvc))
            self.count[dvc.pdkClass._class] += 1
        self.map.layers.append(self.devices_layer)
        #self.map.update()
        self.comp = ft.Container(self.map, width=width, height=height, border_radius=10)