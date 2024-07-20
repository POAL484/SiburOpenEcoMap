import flet as ft

import legacy_grid

images_links = {
    "deer": "https://i.ibb.co/FYH1Tw9/deer-icon.png",
    "bear": "https://i.ibb.co/Xy70WXf/bear-icon.png",
    "bunny": "https://i.ibb.co/RcZRPdd/bunny-icon.png"
}

def page_map(page: ft.Page):
    hgrid = legacy_grid.RowGridView((1, 8, 1))
    wgrid = legacy_grid.RowGridView((4, 1))
    wgrid1 = legacy_grid.RowGridView((1, 1, 1, 1, 1))
    w = page.width
    h = page.height-(page.controls[0].calc_size())
    map = page.c.SiburMap(page, wgrid.calc_grid(4, w), hgrid.calc_grid(6, h))
    page.add(ft.Row([
        ft.Container(ft.Row([ft.Image(images_links['bunny']), ft.Text(str(map.count['bunny']))]), width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h)),
        ft.Container(ft.Row([ft.Image(images_links['bear']),  ft.Text(str(map.count['bear']))]),  width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h)),
        ft.Container(ft.Row([ft.Image(images_links['deer']),  ft.Text(str(map.count['deer']))]),  width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h)),
        ft.Container(ft.ElevatedButton("Обновить"), width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h)),
        ft.Container(width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h))
    ]))
    page.add(map.comp)