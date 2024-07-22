import flet as ft

import flet.map as map

import math

import sdevice

#640

images_links = {
    "deer": "https://i.ibb.co/FYH1Tw9/deer-icon.png",
    "bear": "https://i.ibb.co/Xy70WXf/bear-icon.png",
    "bunny": "https://i.ibb.co/RcZRPdd/bunny-icon.png"
}

class Animal(map.Marker):
    def __init__(self, page: ft.Page, dvc: sdevice.Device, handle_hover: callable, handler_click: callable):
        r = math.sqrt((page.width*page.height)/500)
        col = page.cols.BUNNY
        match dvc.pdkClass._class:
            case "bunny": col = page.cols.BUNNY
            case "bear": col = page.cols.BEAR
            case "deer": col = page.cols.DEER
        super().__init__(
            ft.Container(ft.Image(images_links[dvc.pdkClass._class], error_content=ft.Container(shape=ft.BoxShape.CIRCLE, bgcolor=col),
                        ), on_hover=lambda e: handle_hover(e, self), on_click=lambda e: handler_click(e, self)),
            map.MapLatitudeLongitude(dvc.lat, dvc.lon),
            alignment=ft.alignment.Alignment(0, 0),
            width=r,
            height=r
        )
        self.device_tip = page.c.DeviceTip(1, 1, dvc, page)
        self.device_tip.opacity = 0
        self.device_tip.visible = False
        self.device_tip.clicked = False
        self.dvc = dvc