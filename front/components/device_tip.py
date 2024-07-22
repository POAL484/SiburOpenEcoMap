import flet as ft

from sdevice import Device

from utility import calcPdkProcent

class ValueWithUnit(ft.Container):
    def __init__(self, val_name: str, val: str, unit: str, val_type: str):
        super().__init__(ft.Row([
            ft.Container(ft.Text(val_name, font_family="Segoe UI")),
            ft.Container(ft.Text(val, font_family="Segoe UI", text_align=ft.TextAlign.CENTER), alignment=ft.alignment.Alignment(0, 0)),
            ft.Container(ft.Text(unit, text_align=ft.TextAlign.END, font_family="Segoe UI", size=10), alignment=ft.alignment.Alignment(1, 0)),
            ft.Container(
                ft.Text(f"{calcPdkProcent(val_type, val_name, float(val))}% от ПДК", font_family="Segoe UI", size=10)
            ) if not calcPdkProcent(val_type, val_name, float(val)) is None else ft.Container(
                ft.Text("Нет ПДК", font_family="Segoe UI", size=10)
            )
        ], ft.MainAxisAlignment.SPACE_BETWEEN))

units_for_live = {
    "temp": "°C",
    "pressure": "Pa",
}
unit_for_live_misc = "ppm (усл. един.)"

units_for_lake = {}
unit_for_lake_misc = "мг/л"

units_for_rain = {}
unit_for_rain_misc = "мг/л"

class DeviceTip(ft.Container):
    def hideMySelf(self, e: ft.ControlEvent):
        self.visible = False
        self.update()

    def __init__(self, width: int, height: int, dvc: Device, page: ft.Page):
        super().__init__(width=width, height=height, bgcolor="#cc555555", border_radius=10, animate_opacity=300, on_animation_end=lambda e: self.hideMySelf(e))
        self.content = ft.Column([

        ], spacing=2, scroll='adaptive')
        self.content.controls.append(ft.ElevatedButton(
            "Подробнее >", on_click=lambda e: page.go(f"/device/{dvc.uid}"),
            bgcolor="#00000000"
        ))
        for paramName in dvc.live.keys():
            if "Speed" in paramName or paramName == "timestamp" or paramName == "timestamp_analises": continue
            self.content.controls.append(
                ValueWithUnit(paramName, dvc.live[paramName], units_for_live[paramName] if paramName in units_for_live.keys() else unit_for_live_misc, 'live')
            )
        self.content.controls.append(
            ft.Container(bgcolor="white", width=width, height=2)
        )
        for paramName in dvc.lake.keys():
            if "Speed" in paramName or paramName == "timestamp" or paramName == "timestamp_analises": continue
            self.content.controls.append(
                ValueWithUnit(paramName, dvc.lake[paramName], units_for_lake[paramName] if paramName in units_for_lake.keys() else unit_for_lake_misc, 'lake')
            )
        self.content.controls.append(
            ft.Container(bgcolor="white", width=width, height=2)
        )
        for paramName in dvc.rain.keys():
            if "Speed" in paramName or paramName == "timestamp" or paramName == "timestamp_analises": continue
            self.content.controls.append(
                ValueWithUnit(paramName, dvc.rain[paramName], units_for_rain[paramName] if paramName in units_for_rain.keys() else unit_for_rain_misc, 'rain')
            )
        self.page = page

    def updateWithNewData(self, dvc: Device):
        self.content = ft.Column([

        ], spacing=2, scroll='adaptive')
        self.content.controls.append(ft.ElevatedButton(
            "Подробнее >", on_click=lambda e: self.page.go(f"/device/{dvc.uid}"),
            bgcolor="#00000000"
        ))
        for paramName in dvc.live.keys():
            if "Speed" in paramName or paramName == "timestamp" or paramName == "timestamp_analises": continue
            self.content.controls.append(
                ValueWithUnit(paramName, dvc.live[paramName], units_for_live[paramName] if paramName in units_for_live.keys() else unit_for_live_misc, 'live')
            )
        self.content.controls.append(
            ft.Container(bgcolor="white", width=self.width, height=2)
        )
        for paramName in dvc.lake.keys():
            if "Speed" in paramName or paramName == "timestamp" or paramName == "timestamp_analises": continue
            self.content.controls.append(
                ValueWithUnit(paramName, dvc.lake[paramName], units_for_lake[paramName] if paramName in units_for_lake.keys() else unit_for_lake_misc, 'lake')
            )
        self.content.controls.append(
            ft.Container(bgcolor="white", width=self.width, height=2)
        )
        for paramName in dvc.rain.keys():
            if "Speed" in paramName or paramName == "timestamp" or paramName == "timestamp_analises": continue
            self.content.controls.append(
                ValueWithUnit(paramName, dvc.rain[paramName], units_for_rain[paramName] if paramName in units_for_rain.keys() else unit_for_rain_misc, 'rain')
            )
        self.update()