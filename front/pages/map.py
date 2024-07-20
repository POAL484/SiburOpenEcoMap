import flet as ft

import legacy_grid

images_links = {
    "deer": "https://i.ibb.co/FYH1Tw9/deer-icon.png",
    "bear": "https://i.ibb.co/Xy70WXf/bear-icon.png",
    "bunny": "https://i.ibb.co/RcZRPdd/bunny-icon.png"
}

def page_map(page: ft.Page):

    def filter_changed():
        print(filter_.filter)

    hgrid = legacy_grid.RowGridView((1, 8, 1))
    wgrid = legacy_grid.RowGridView((4, 1))
    wgrid1 = legacy_grid.RowGridView((1, 1, 1, 1, 1))
    w = page.width - 20
    h = page.height-(page.controls[0].calc_size())
    map = page.c.SiburMap(page, wgrid.calc_grid(4, w), hgrid.calc_grid(8, h))
    filter_ = page.c.SiburFilter(page, wgrid.calc_grid(1, w), hgrid.calc_grid(8, h), filter_changed)
    page.add(ft.Row([
        ft.Container(ft.Row([ft.Image(images_links['bunny'], width=hgrid.calc_grid(1, h)/1.4, height=hgrid.calc_grid(1, h)/1.4), ft.Text(str(map.count['bunny']), size=hgrid.calc_grid(1, h)/1.8)]), width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h)),
        ft.Container(ft.Row([ft.Image(images_links['bear'], width=hgrid.calc_grid(1, h)/1.4, height=hgrid.calc_grid(1, h)/1.4),  ft.Text(str(map.count['bear']), size=hgrid.calc_grid(1, h)/1.8)]),  width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h)),
        ft.Container(ft.Row([ft.Image(images_links['deer'], width=hgrid.calc_grid(1, h)/1.4, height=hgrid.calc_grid(1, h)/1.4),  ft.Text(str(map.count['deer']), size=hgrid.calc_grid(1, h)/1.8)]),  width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h)),
        ft.Container(ft.IconButton(ft.icons.UPDATE), width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h)),
        ft.Container(width=wgrid1.calc_grid(1, w), height=hgrid.calc_grid(1, h))
    ]))
    page.add(ft.Row([
        map.comp, filter_
    ]))