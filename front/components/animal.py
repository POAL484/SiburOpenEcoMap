import flet as ft

import flet.map as map

import math

import sdevice

#640

images_links = {
    "deer": ",https://i.ibb.co/FYH1Tw9/deer-icon.png",
    "bear": ",https://i.ibb.co/Xy70WXf/bear-icon.png",
    "bunny": ",https://i.ibb.co/RcZRPdd/bunny-icon.png"
}

class Animal(map.Marker):
    def __init__(self, page: ft.Page, dvc: sdevice.Device):
        r = math.sqrt((page.width*page.height)/500)
        col = page.cols.BUNNY
        match dvc.pdkClass._class:
            case "bunny": col = page.cols.BUNNY
            case "bear": col = page.cols.BEAR
            case "deer": col = page.cols.DEER
        super().__init__(
            ft.Image(images_links[dvc.pdkClass._class], error_content=ft.Container(shape=ft.BoxShape.CIRCLE, bgcolor=col),),
            map.MapLatitudeLongitude(dvc.lat, dvc.lon),
            alignment=ft.alignment.Alignment(0, 0),
            width=r,
            height=r
        )