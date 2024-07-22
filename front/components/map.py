import flet as ft

import flet.map as map

SIBUR_UIDS = {
    "Тобольск": "ed5973d8-b0de-49d5-941c-c1fd35897902",
    "Воронеж": "9af81ccb-5dab-4cde-8fdf-dd64254e3142",
    "Дзержинск": "852f88c2-85c3-4e00-a31c-56fc938dd210",
    "Казань": "3016db26-26e0-4441-85a9-9b1e0e2212b2",
    "Томск": "eb01fd24-6b8e-4eec-b03c-477a2b13aacd"
}

class SiburMap:
    def __init__(self, page: ft.Page, width: int, height: int, handle_hover: callable, handle_click: callable):
        self.handle_hover = handle_hover
        self.handle_click = handle_click
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
            self.devices_layer.markers.append(page.c.Animal(page, dvc, handle_hover, handle_click))
            self.count[dvc.pdkClass._class] += 1
        self.map.layers.append(self.devices_layer)
        #self.map.update()
        self.comp = ft.Container(self.map, width=width, height=height, border_radius=10)
        self.page = page
        self.tips = []
        for an in self.devices_layer.markers:
            an.device_tip.width = width//4
            an.device_tip.height = height
            self.tips.append(an.device_tip)

    def refilter(self, filter: str):
        dvcs = []
        for dvc in self.page.storage.devices:
            dvcs.append(self.page.c.Animal(self.page, dvc, self.handle_hover, self.handle_click))
            if filter['sib'] == "sib":
                if not dvc.uid in SIBUR_UIDS.values():
                    dvcs.pop()
                    continue
            if filter['sib'] == "!sib":
                if dvc.uid in SIBUR_UIDS.values():
                    dvcs.pop()
                    continue
            if not dvc.pdkClass._class in filter['class']:
                dvcs.pop()
                continue
        self.devices_layer.markers = dvcs
        for an in self.devices_layer.markers:
            an.device_tip.updateWithNewData(an.dvc)
        self.map.update()