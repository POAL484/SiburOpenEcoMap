import flet as ft

from PIL import ImageFont

font = ImageFont.truetype("fonts/segoeui.ttf", 100)

class SiburFilterCheckBox(ft.Row):
    def __init__(self, text: str, filter_name: str, ping: callable, checked = False):
        super().__init__([
            ft.Checkbox(text, checked, on_change=lambda e: ping(e, filter_name))
        ])

class DelLine(ft.Container):
    def __init__(self, width: int, height: int):
        super().__init__(
            bgcolor="white", width=width, height=height
        )

class SiburFilter(ft.Container):
    def __init__(self, page: ft.Page, width: int, height: int, filter_changed: callable):

        def ping(e: ft.ControlEvent, filter_name: str):
            match filter_name:
                case "sib":
                    if self.checkboxes['sib'].controls[0].value:
                        if self.checkboxes['!sib'].controls[0].value:
                            self.checkboxes['!sib'].controls[0].value = False
                            self.checkboxes['!sib'].controls[0].update()
                        self.filter['sib'] = 'sib'
                    else:
                        self.filter['sib'] = 'all'
                case "!sib":
                    if self.checkboxes['!sib'].controls[0].value:
                        if self.checkboxes['sib'].controls[0].value:
                            self.checkboxes['sib'].controls[0].value = False
                            self.checkboxes['sib'].controls[0].update()
                        self.filter['sib'] = '!sib'
                    else:
                        self.filter['sib'] = 'all'
                case "class.all" | "class.bunny" | "class.bear" | "class.deer":
                    if filter_name == "class.all":
                        if self.checkboxes['class.bunny'].controls[0].value and self.checkboxes['class.bear'].controls[0].value and self.checkboxes['class.deer'].controls[0].value:
                            self.checkboxes['class.bunny'].controls[0].value = False
                            self.checkboxes['class.bunny'].controls[0].update()
                            self.checkboxes['class.bear'].controls[0].value = False
                            self.checkboxes['class.bear'].controls[0].update()
                            self.checkboxes['class.deer'].controls[0].value = False
                            self.checkboxes['class.deer'].controls[0].update()
                        else:
                            self.checkboxes['class.bunny'].controls[0].value = True
                            self.checkboxes['class.bunny'].controls[0].update()
                            self.checkboxes['class.bear'].controls[0].value = True
                            self.checkboxes['class.bear'].controls[0].update()
                            self.checkboxes['class.deer'].controls[0].value = True
                            self.checkboxes['class.deer'].controls[0].update()
                    if self.checkboxes['class.all'].controls[0].value and ((not self.checkboxes['class.bunny'].controls[0].value) or (not self.checkboxes['class.bear'].controls[0].value) or (not self.checkboxes['class.deer'].controls[0].value)):
                        self.checkboxes['class.all'].controls[0].value = False
                        self.checkboxes['class.all'].controls[0].update()
                    if (not self.checkboxes['class.all'].controls[0].value) and self.checkboxes['class.bunny'].controls[0].value and self.checkboxes['class.bear'].controls[0].value and self.checkboxes['class.deer'].controls[0].value:
                        self.checkboxes['class.all'].controls[0].value = True
                        self.checkboxes['class.all'].controls[0].update()
                    filt = []
                    if self.checkboxes['class.bunny'].controls[0].value: filt.append("bunny")
                    if self.checkboxes['class.bear'].controls[0].value: filt.append("bear")
                    if self.checkboxes['class.deer'].controls[0].value: filt.append("deer")
                    self.filter['class'] = filt
            filter_changed()
                
                

        super().__init__(width=width, height=height)
        self.checkboxes = {
            "sib": SiburFilterCheckBox("СИБУР", 'sib', ping),
            "!sib": SiburFilterCheckBox("Не СИБУР", '!sib', ping),
            "class.all": SiburFilterCheckBox("Все", "class.all", ping, True),
            "class.bunny": SiburFilterCheckBox("Счастливый кролик", "class.bunny", ping, True),
            "class.bear": SiburFilterCheckBox("Грустный медведь", "class.bear", ping, True),
            "class.deer": SiburFilterCheckBox("Больной олень", "class.deer", ping, True)
        }
        self.page = page
        self.content = ft.Container(ft.Column([
            ft.Text("Фильтры", size=page.u.calculateFont(font, self.width/1.5, "Фильтры"), font_family="Segoe UI", text_align=ft.TextAlign.CENTER),
            self.checkboxes['sib'],
            self.checkboxes['!sib'],
            DelLine(width, 2),
            self.checkboxes['class.all'],
            self.checkboxes['class.bunny'],
            self.checkboxes['class.bear'],
            self.checkboxes['class.deer']
        ], ft.MainAxisAlignment.START, ft.CrossAxisAlignment.CENTER), opacity=1)
        self.bgcolor = "#343434"
        #self.opacity = .1
        self.border_radius=10
        self.filter = {"sib": "all", "class": ["bunny", "bear", "deer"]}