import flet as ft

from PIL import ImageFont

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

DEER_IMG = "https://i.ibb.co/PFLMFhh/deer-icon-white.png"
BEAR_IMG = "https://i.ibb.co/N9mjH5T/bear-icon-white.png"
BUNNY_IMG = "https://i.ibb.co/QbqTCcw/bunny-icon-white.png"

pomidor = ImageFont.truetype("fonts/seguibl.ttf", 100)

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
    grid3 = legacy_grid.RowGridView((1, 1, 1))
    grid2 = legacy_grid.RowGridView((1, 1))
    page.add(
        ft.ElevatedButton(content=ft.Text("Инструкция", size=hgrid.calc_grid(.6, h)), on_click=lambda e: page.open(
            ft.AlertDialog(content=page.c.SiburBlock(
                page, ft.Text("Инструкция", size=min(page.u.calculateFont(pomidor, (page.width-50)/1.3, "Инструкция"), 58)),
                ft.Container(
                    ft.Column([
                        ft.Text(spans=[
                            ft.TextSpan("Экологическая карта", ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT)),
                            ft.TextSpan(" позволяет отобразить результаты мониторинга окружающей среды, предоставляя оценку ee благополучия для человека")
                        ]),
                        ft.Text(spans=[
                            ft.TextSpan("Каждая круглая метка - это "),
                            ft.TextSpan("устройство \"СИБУРок\"", ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT))
                        ]),
                        ft.Column([
                            ft.Text(spans=[ft.TextSpan("Оно анализирует среду по следующим параметрам:", ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT))]),
                            ft.Row([
                                ft.Container(ft.Text("Прямые параметры: параметры, которые получают с датчиков. Обновляются раз в 1 минуту. Измеряеют: температуру, влажность, различные токсичные газы"), width=grid2.calc_grid(1, grid3.calc_grid(2, w-50))),
                                ft.Text("Лабораторные параметры: параметры, которые являются результатами анализов в лаборатории. Устройства автоматически отбирают пробы осадков и, по условию близости, и пробы из водоемов. Отобранные пробы доставляются в лабораторию по средством беспилотных систем. Обновляются раз в несколько дней.", width=grid2.calc_grid(1, grid3.calc_grid(2, w-50)))
                            ])
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Column([
                            ft.Row([
                                ft.Image(BUNNY_IMG, width=55, height=55),
                                ft.Text(spans=[
                                    ft.TextSpan("\"Счастливый кролики\"", ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT)),
                                    ft.TextSpan(" ставиться сибурку, если каждый егo параметр не превышает "),
                                    ft.TextSpan("80% от нормы", ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT))
                                ])
                            ]),
                            ft.Row([
                                ft.Image(BEAR_IMG, width=55, height=55),
                                ft.Text(spans=[
                                    ft.TextSpan("\"Грустный медведь\"", ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT)),
                                    ft.TextSpan(" ставиться сибурку, если каждый его параметр "),
                                    ft.TextSpan("не превышает норму", ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT))
                                ])
                            ]),
                            ft.Row([
                                ft.Image(DEER_IMG, width=55, height=55),
                                ft.Text(spans=[
                                    ft.TextSpan("\"Больной олень\"", ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT)),
                                    ft.TextSpan(" ставиться сибурку, если хотя бы один его параметр "),
                                    ft.TextSpan("превышает норму", ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT))
                                ])
                            ])
                        ])
                    ])
                ),
                ft.Container(ft.Image("https://i.ibb.co/NYBpcQ6/eco-Map-Banner.png", width=((h-50)/1.15)/2, height=((h-50)/1.15), border_radius=10)),
                w-50, h-50, False
            ))
        ))
    )

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
    grid2 = legacy_grid.RowGridView((1, 1))
    page.add(
        ft.ElevatedButton(content=ft.Text("Инструкция", size=hgrid.calc_grid(.6, h)), on_click=lambda e: page.open(
            ft.AlertDialog(content=page.c.SiburColumnBlock(
                page, ft.Text("Инструкция", size=min(page.u.calculateFont(pomidor, (page.width-50)/1.3, "Инструкция"), 58)),
                ft.Container(
                    ft.Column([
                        ft.Text(spans=[
                            ft.TextSpan("Экологическая карта", ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT)),
                            ft.TextSpan(" позволяет отобразить результаты мониторинга окружающей среды, предоставляя оценку ee благополучия для человека")
                        ]),
                        ft.Text(spans=[
                            ft.TextSpan("Каждая круглая метка - это "),
                            ft.TextSpan("устройство \"СИБУРок\"", ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT))
                        ]),
                        ft.Text(spans=[ft.TextSpan("Оно анализирует среду по следующим параметрам:", ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT))]),
                        ft.Container(ft.Text("Прямые параметры: параметры, которые получают с датчиков. Обновляются раз в 1 минуту. Измеряеют: температуру, влажность, различные токсичные газы"), ),
                        ft.Text("Лабораторные параметры: параметры, которые являются результатами анализов в лаборатории. Устройства автоматически отбирают пробы осадков и, по условию близости, и пробы из водоемов. Отобранные пробы доставляются в лабораторию по средством беспилотных систем. Обновляются раз в несколько дней."),
                        ft.Row([
                                ft.Image(BUNNY_IMG, width=45, height=45),
                                ft.Column([
                                    ft.Text("\"Счастливый кролики\"", style=ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT), size=page.u.calculateFont(pomidor, w-50-50-50, "ставиться сибурку, если каждый")),
                                    ft.Text("ставиться сибурку, если каждый", size=page.u.calculateFont(pomidor, w-50-50-50, "ставиться сибурку, если каждый")),
                                    ft.Text("егo параметр не превышает", size=page.u.calculateFont(pomidor, w-50-50-50, "ставиться сибурку, если каждый")),
                                    ft.Text("80% от нормы", style=ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT), size=page.u.calculateFont(pomidor, w-50-50-50, "ставиться сибурку, если каждый"))
                                ])
                            ]),
                            ft.Row([
                                ft.Image(BEAR_IMG, width=45, height=45),
                                ft.Column([
                                    ft.Text("\"Грустный медведь\"", style=ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT), size=page.u.calculateFont(pomidor, w-50-50-50, "ставиться сибурку, если")),
                                    ft.Text("ставиться сибурку, если", size=page.u.calculateFont(pomidor, w-50-50-50, "ставиться сибурку, если")),
                                    ft.Text("каждый его параметр", size=page.u.calculateFont(pomidor, w-50-50-50, "ставиться сибурку, если")),
                                    ft.Text("не превышает норму", style=ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT), size=page.u.calculateFont(pomidor, w-50-50-50, "ставиться сибурку, если"))
                                ])
                            ]),
                            ft.Row([
                                ft.Image(DEER_IMG, width=45, height=45),
                                ft.Column([
                                    ft.Text("\"Больной олень\"", style=ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT), size=page.u.calculateFont(pomidor, w-50-50-50, "хотя бы один его параметр")),
                                    ft.Text("ставиться сибурку, если", size=page.u.calculateFont(pomidor, w-50-50-50, "хотя бы один его параметр")),
                                    ft.Text("хотя бы один его параметр", size=page.u.calculateFont(pomidor, w-50-50-50, "хотя бы один его параметр")),
                                    ft.Text("превышает норму", style=ft.TextStyle(color=page.cols.SIBURBLOCK_ACCENT), size=page.u.calculateFont(pomidor, w-50-50-50, "хотя бы один его параметр"))
                                ])
                            ])
                        ])
                    
                ),
                ft.Container(ft.Image("https://i.ibb.co/NYBpcQ6/eco-Map-Banner.png", width=((h-50)/1.15)/2, height=((h-50)/1.15), border_radius=10)),
                w-50, h-50, False
            ))
        ))
    )