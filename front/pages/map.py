import flet as ft

import legacy_grid

from components.animal import Animal

images_links = {
    "deer": "https://i.ibb.co/FYH1Tw9/deer-icon.png",
    "bear": "https://i.ibb.co/Xy70WXf/bear-icon.png",
    "bunny": "https://i.ibb.co/RcZRPdd/bunny-icon.png"
}

SIBUR_UIDS = {
    "Тобольск": "ed5973d8-b0de-49d5-941c-c1fd35897902",
    "Воронеж": "9af81ccb-5dab-4cde-8fdf-dd64254e3142",
    "Дзержинск": "852f88c2-85c3-4e00-a31c-56fc938dd210",
    "Казань": "3016db26-26e0-4441-85a9-9b1e0e2212b2",
    "Томск": "eb01fd24-6b8e-4eec-b03c-477a2b13aacd"
}

def page_map(page: ft.Page):
    if page.width < 800:
        mobile_version(page)
        return

    def filter_changed():
        map.refilter(filter_.filter)
        stck.controls = [stck.controls[0],]
        stck.controls += map.tips
        stck.update()

    def handle_hover(e: ft.HoverEvent, an: Animal):
        if an.device_tip.clicked: return
        hideAllTips(an.device_tip)
        if e.data == "true": an.device_tip.visible = True
        an.device_tip.update()
        an.device_tip.opacity = 1 if e.data == "true" else 0
        an.device_tip.update()

    def handle_click(e: ft.ControlEvent, an: Animal):
        if an.device_tip.clicked:
            an.device_tip.opacity = 0
            an.device_tip.clicked = False
            an.device_tip.update()
        else:
            hideAllTips()
            an.device_tip.visible = True
            an.device_tip.opacity = 1
            an.device_tip.clicked = True
            an.device_tip.update()

    def hideAllTips(not_update = None):
        for tip in map.tips:
            if tip == not_update: continue
            tip.clicked = False
            tip.visible = False
            tip.opacity = 0
            tip.update()

    hgrid = legacy_grid.RowGridView((1, 8, 1))
    wgrid = legacy_grid.RowGridView((4, 1))
    wgrid1 = legacy_grid.RowGridView((1, 1, 1, 1, 1))
    w = page.width - 20
    h = page.height-(page.controls[0].calc_size())
    map = page.c.SiburMap(page, wgrid.calc_grid(4, w), hgrid.calc_grid(8, h), handle_hover, handle_click)
    filter_ = page.c.SiburFilter(page, wgrid.calc_grid(1, w), hgrid.calc_grid(8, h), filter_changed)
    page.add(ft.Row([
        ft.Container(ft.Row([ft.Image(images_links['bunny'], width=hgrid.calc_grid(1, h)/1.4, height=hgrid.calc_grid(1, h)/1.4), ft.Text(str(map.count['bunny']), size=hgrid.calc_grid(1, h)/1.8)]), width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h)),
        ft.Container(ft.Row([ft.Image(images_links['bear'], width=hgrid.calc_grid(1, h)/1.4, height=hgrid.calc_grid(1, h)/1.4),  ft.Text(str(map.count['bear']), size=hgrid.calc_grid(1, h)/1.8)]),  width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h)),
        ft.Container(ft.Row([ft.Image(images_links['deer'], width=hgrid.calc_grid(1, h)/1.4, height=hgrid.calc_grid(1, h)/1.4),  ft.Text(str(map.count['deer']), size=hgrid.calc_grid(1, h)/1.8)]),  width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h)),
        ft.Container(ft.IconButton(ft.icons.UPDATE, on_click=lambda e :filter_changed()), width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h)),
        ft.Container(width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h))
    ]))
    stck = ft.Stack([map.comp] + map.tips)
    page.add(ft.Row([
        stck, filter_
    ]))

def mobile_version(page: ft.Page):
    def filter_changed():
        map.refilter(filter_.filter)

    def handle_hover(e: ft.HoverEvent, an: Animal): pass

    def handle_click(e: ft.ControlEvent, an: Animal):
        page.open(page.c.DeviceTipMobile(page, an.dvc).page1)

    wgrid2 = legacy_grid.RowGridView((8,))
    hgrid = legacy_grid.RowGridView((1, 8, 1))
    wgrid1 = legacy_grid.RowGridView((1, 1, 1, 1))
    w = page.width - 20
    h = page.height-(page.controls[0].calc_size())
    map = page.c.SiburMap(page, w, hgrid.calc_grid(8, h), handle_hover, handle_click)
    filter_ = page.c.SiburFilterMobile(page, wgrid2.calc_grid(5, w), hgrid.calc_grid(8, h), filter_changed)
    page.add(ft.Row([
        ft.Container(ft.Row([ft.Image(images_links['bunny'], width=hgrid.calc_grid(1, h)/1.75, height=hgrid.calc_grid(1, h)/1.75), ft.Text(str(map.count['bunny']), size=hgrid.calc_grid(1, h)/1.8)]), width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h)),
        ft.Container(ft.Row([ft.Image(images_links['bear'], width=hgrid.calc_grid(1, h)/1.75, height=hgrid.calc_grid(1, h)/1.75),  ft.Text(str(map.count['bear']), size=hgrid.calc_grid(1, h)/1.8)]),  width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h)),
        ft.Container(ft.Row([ft.Image(images_links['deer'], width=hgrid.calc_grid(1, h)/1.75, height=hgrid.calc_grid(1, h)/1.75),  ft.Text(str(map.count['deer']), size=hgrid.calc_grid(1, h)/1.8)]),  width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h)),
        ft.Container(ft.IconButton(ft.icons.UPDATE, on_click=lambda e: map.refilter(filter_.filter)), width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h)),
    ]))
    page.add(ft.Stack([map.comp, filter_.closed, filter_.opened], alignment=ft.Alignment(1, 1)))