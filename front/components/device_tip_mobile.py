import flet as ft

from utility import calcPdkProcent
from sdevice import Device

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

class DeviceTipMobile():
    def selfClose(self, cur_page: int):
        self.page.close(self.__getattribute__(f"page{cur_page}"))

    def closeAndGo(self, cur_page: int):
        self.page.close(self.__getattribute__(f"page{cur_page}"))
        self.page.go(f"/device/{self.dvc.uid}")

    def toPage(self, from_page: int, to_page: int):
        self.page.close(self.__getattribute__(f"page{from_page}"))
        self.page.open(self.__getattribute__(f"page{to_page}"))

    def __init__(self, page: ft.Page, dvc: Device):
        self.page1 = ft.AlertDialog()
        self.page1.content = ft.Column([])
        self.page1.title = ft.Text("Последние данные c датчиков")
        self.page2 = ft.AlertDialog()
        self.page2.content = ft.Column([])
        self.page2.title = ft.Text("Последнее исследование воды из водоема")
        self.page3 = ft.AlertDialog()
        self.page3.content = ft.Column([])
        self.page3.title = ft.Text("Последнее исследование воды из осадков")
        for paramName in dvc.live.keys():
            if "Speed" in paramName or paramName == "timestamp" or paramName == "timestamp_analises": continue
            self.page1.content.controls.append(
                ValueWithUnit(paramName, dvc.live[paramName], units_for_live[paramName] if paramName in units_for_live.keys() else unit_for_live_misc, 'live')
            )
        for paramName in dvc.lake.keys():
            if "Speed" in paramName or paramName == "timestamp" or paramName == "timestamp_analises": continue
            self.page2.content.controls.append(
                ValueWithUnit(paramName, dvc.lake[paramName], units_for_lake[paramName] if paramName in units_for_lake.keys() else unit_for_lake_misc, 'lake')
            )
        for paramName in dvc.rain.keys():
            if "Speed" in paramName or paramName == "timestamp" or paramName == "timestamp_analises": continue
            self.page3.content.controls.append(
                ValueWithUnit(paramName, dvc.rain[paramName], units_for_rain[paramName] if paramName in units_for_rain.keys() else unit_for_rain_misc, 'rain')
            )
        self.page1.actions=[
            ft.TextButton(">", on_click=lambda e: self.toPage(1, 2)),
            ft.TextButton("Подробнее", on_click=lambda e: self.closeAndGo(1)),
            ft.TextButton("Закрть", on_click=lambda e: self.selfClose(1))
        ]
        self.page2.actions=[
            ft.TextButton("<", on_click=lambda e: self.toPage(2, 1)),
            ft.TextButton(">", on_click=lambda e: self.toPage(2, 3)),
            ft.TextButton("Подробнее", on_click=lambda e: self.closeAndGo(2)),
            ft.TextButton("Закрть", on_click=lambda e: self.selfClose(2))
        ]
        self.page3.actions=[
            ft.TextButton("<", on_click=lambda e: self.toPage(3, 2)),
            ft.TextButton("Подробнее", on_click=lambda e: self.closeAndGo(3)),
            ft.TextButton("Закрть", on_click=lambda e: self.selfClose(3))
        ]
        self.page = page
        self.dvc = dvc