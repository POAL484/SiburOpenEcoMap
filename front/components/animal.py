import flet as ft

import flet.map as map

import math

import device

#640

class Animal(map.CircleMarker):
    def __init__(self, page: ft.Page, dvc: device.Device):
        r = math.sqrt((page.width*page.height)/640)
        col = page.cols.BUNNY
        match dvc.pdkClass._class:
            case "bunny": col = page.coles.BUNNY
            case "bear": col = page.coles.BEAR
            case "deer": col = page.coles.DEER
        super().__init__(radius=r,
                         color="white",
                         border_color=col,
                         border_stroke_width=1,
                         coordinates=map.MapLatitudeLongitude(dvc.lat, dvc.lon),
                         )