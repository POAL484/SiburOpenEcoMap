import flet as ft
#import flet.canvas as cv

"""class Graph(cv.Canvas):
    def __init__(self, page: ft.Page, values: list, ):
        super().__init__()
        for val in values:
            self.shapes.append(cv.Rect(

            ))
        self.shapes = [cv.Rect(100, 100, 200, 200, 10, ft.Paint("#ff01d0"))]
        """

class Graph(ft.Column):
    def __init__(self, page: ft.Page, values: list, color_1: tuple, color_2: tuple):
        super().__init__()
        self.clr1 = color_1
        self.clr2 = color_2
        self.vals = values
        self.r = ft.Row()
        self.controls = [self.r]
        self.c = ft.Container()
        self.r.controls = [self.c, ]
        self.c.bgcolor = "#484848"
        self.c.border_radius = 5
        self.c.padding = 5
        graph_width = min(page.width, 1000)
        self._height = 250
        self.max_value = max(values)
        pilars = []
        for value in values:
            transp = ft.Container(height=self._height-((value/self.max_value)*self._height), bgcolor="#00000000", border_radius=(graph_width/(len(values)*2))//2.5, width=graph_width/(len(values)*2))
            pillar_tip = ft.canvas.Canvas([
                    ft.canvas.Rect((-(10+(10*len(str(value))))//2)+((graph_width/(len(values)*2))//2), -10, 10+(10*len(str(value))), 20, 5, ft.Paint('black')),
                    ft.canvas.Text((graph_width/(len(values)*2))//2, 0, str(value), alignment=ft.alignment.center, style=ft.TextStyle(14)),
                    ], visible=False, height=0, width=0
                )
            cont = ft.Container(height=((value/self.max_value)*self._height), bgcolor=page.u.rgb_to_hex(page.u.set_percent_of_colors(color_1, color_2, 0, self.max_value, value)),
                             border_radius=(graph_width/(len(values)*2))//2.5,
                             width=graph_width/(len(values)*2),
                             on_hover=self.column_hover)
            cont.value = value
            cont.tip = pillar_tip
            cont.transp = transp
            pilars.append(ft.Column([
                transp,
                ft.Stack([cont,
                pillar_tip,]),
                ]))
        self.c.content = ft.Row(pilars, alignment=ft.MainAxisAlignment.SPACE_EVENLY, width=100)
        self.c.width = graph_width
        self.r.controls.append(ft.Column([
            ft.Container(height=self.c.padding*2),
            ft.Text(str(self.max_value), size=16),
            ft.Container(height=(self._height-(self.c.padding*2)-16-16-16-(self.c.padding))//2),
            ft.Text(str(self.max_value//2) if self.max_value % 2 == 0 else str(self.max_value/2), size=16),
            ft.Container(height=(self._height-(self.c.padding*2)-16-16-16-(self.c.padding))//2),
            ft.Text("0", size=16),
            ft.Container(height=self.c.padding)
            ]))
        self.r.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
    def column_hover(self, e: ft.HoverEvent):
        e.control.tip.visible = e.data
        #if e.data:
        #    e.control.transp.height = self._height-((e.control.value/self.max_value)*self._height)
        #else:
        #    e.control.transp.height = self._height-((e.control.value/self.max_value)*self._height)
        e.control.tip.update()
        #e.control.transp.update()

    def upd(self):
        self.r = ft.Row()
        self.controls = [self.r]
        self.c = ft.Container()
        self.r.controls = [self.c, ]
        self.c.bgcolor = "#484848"
        self.c.border_radius = 5
        self.c.padding = 5
        graph_width = min(self.page.width, 1200) - 100
        self._height = 250
        self.max_value = max(self.vals)
        pilars = []
        for value in self.vals:
            transp = ft.Container(height=self._height-((value/self.max_value)*self._height), bgcolor="#00000000", border_radius=(graph_width/(len(self.vals)*2))//2.5, width=graph_width/(len(self.vals)*2))
            pillar_tip = ft.canvas.Canvas([
                    ft.canvas.Rect((-(10+(10*len(str(value))))//2)+((graph_width/(len(self.vals)*2))//2), -10, 10+(10*len(str(value))), 20, 5, ft.Paint('black')),
                    ft.canvas.Text((graph_width/(len(self.vals)*2))//2, 0, str(value), alignment=ft.alignment.center, style=ft.TextStyle(14)),
                    ], visible=False, height=0, width=0
                )
            cont = ft.Container(height=((value/self.max_value)*self._height), bgcolor=self.page.u.rgb_to_hex(self.page.u.set_percent_of_colors(self.clr1, self.clr2, 0, self.max_value, value)),
                             border_radius=(graph_width/(len(self.vals)*2))//2.5,
                             width=graph_width/(len(self.vals)*2),
                             on_hover=self.column_hover)
            cont.value = value
            cont.tip = pillar_tip
            cont.transp = transp
            pilars.append(ft.Column([
                transp,
                ft.Stack([cont,
                pillar_tip,]),
                ]))
        self.c.content = ft.Row(pilars, alignment=ft.MainAxisAlignment.SPACE_EVENLY, width=100)
        self.c.width = graph_width
        self.r.controls.append(ft.Column([
            ft.Container(height=self.c.padding*2),
            ft.Text(str(self.max_value), size=16),
            ft.Container(height=(self._height-(self.c.padding*2)-16-16-16-(self.c.padding))//2),
            ft.Text(str(self.max_value//2) if self.max_value % 2 == 0 else str(self.max_value/2), size=16),
            ft.Container(height=(self._height-(self.c.padding*2)-16-16-16-(self.c.padding))//2),
            ft.Text("0", size=16),
            ft.Container(height=self.c.padding)
            ]))
        self.r.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.update()