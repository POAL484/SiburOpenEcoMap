import flet as ft

def generateEmpty(hor_size: int, vert_size: int):
    return SGridElement(ft.Container(), hor_size, vert_size)

class SGridElement(ft.Container):
    def __init__(self, control: ft.Control, hor_size: int, vert_size: int):
        super().__init__(
            control, margin=0
        )
        self.hor_size = hor_size
        self.vert_size = vert_size

class SGridNewLine: pass
class SGridAutoHeight: pass
class SGridAutoWidth: pass

class _SGridElementReady:
    def __init__(self, control: SGridElement, hor_size: int, vert_size: int, xsize: int, ysize: int):
        self.control = control
        self.hor_size = hor_size
        self.vert_size = vert_size
        self.xsize = xsize
        self.ysize = ysize

class SGrid(ft.Container):
    #def _find_free_in_matrix(self, matrix: dict)

    def __init__(self, width: int|SGridAutoWidth, height: int|SGridAutoHeight, elements: list):
        super().__init__()
        for el in elements:
            assert isinstance(el, SGridElement) or isinstance(el, SGridNewLine), f"All elements in SGrid must be SGridElement or SGridNewLine, found element type {type(el)}"
        matrix = {}
        x = 0
        y = 0
        for el in elements:
            if isinstance(el, SGridNewLine):
                x = 0
                y += 1
            else:
                for x1 in range(el.hor_size):
                    for y1 in range(el.vert_size):
                        matrix[x+x1, y+y1] = el
                x += el.hor_size
            try:
                while isinstance(matrix[x, y], SGridElement):
                    x += 1
            except KeyError: pass
        self.matrix = matrix
        print(matrix)
        self.x_max, self.y_max = 0, 0
        for xy in matrix.keys():
            print(xy, matrix[xy].content.bgcolor)
            if xy[0]+1 > self.x_max: self.x_max = xy[0]+1
            if xy[1]+1 > self.y_max: self.y_max = xy[1]+1
        rw = []
        self.ah = isinstance(height, SGridAutoHeight)
        self.aw = isinstance(width, SGridAutoWidth)
        self.h = height if not self.ah else 10
        self.w = width if not self.aw else 10
        print(self.x_max, self.y_max)
        for x in range(self.x_max):
            rw.append([])
            for y in range(self.y_max):
                try: self.matrix[x, y]
                except KeyError:
                    rw[y].append(_SGridElementReady(generateEmpty(1, 1), 1, 1, (1/self.x_max)*self.w, (1/self.y_max)*self.h))
                    continue
                print(matrix[x, y].content.bgcolor)
                el = self.matrix[x, y]
                s = True
                try:
                    if rw[x-1][y].control == el:
                        s = False
                except IndexError: pass
                try:
                    if rw[x][y-1].control == el:
                        s = False
                except IndexError: pass
                if s:
                    rw[x].append(_SGridElementReady(el, el.hor_size, el.vert_size, (el.hor_size/self.x_max)*self.w, (el.vert_size/self.y_max)*self.h))
        print("meow")
        for elc in rw:
            print("[]")
            for el in elc:
                print(el.control.content.bgcolor)
        gr = ft.Row(spacing=0)
        for elColumn in rw:
            col = ft.Column(spacing=0)
            for el in elColumn:
                if isinstance(el.control, SGrid):
                    if el.control.ah:
                        el.control.h = el.ysize
                    if el.control.aw:
                        el.control.w = el.xsize
                    if el.control.ah or el.control.aw:
                        el.control.recalc()
                el.control.width = el.xsize
                el.control.height = el.ysize
                col.controls.append(el.control)
            gr.controls.append(col)
        self.content = gr
        print(rw)

    def recalc(self):
        rw = []
        for x in range(self.x_max):
            rw.append([])
            for y in range(self.y_max):
                try: self.matrix[x, y]
                except KeyError:
                    rw[y].append(_SGridElementReady(generateEmpty(1, 1), 1, 1, (1/self.x_max)*self.w, (1/self.y_max)*self.h))
                    continue
                print(self.matrix[x, y].content.bgcolor)
                el = self.matrix[x, y]
                s = True
                try:
                    if rw[x-1][y].control == el:
                        s = False
                except IndexError: pass
                try:
                    if rw[x][y-1].control == el:
                        s = False
                except IndexError: pass
                if s:
                    rw[x].append(_SGridElementReady(el, el.hor_size, el.vert_size, (el.hor_size/self.x_max)*self.w, (el.vert_size/self.y_max)*self.h))
        print("meow")
        for elc in rw:
            print("[]")
            for el in elc:
                print(el.control.content.bgcolor)
        for x in range(self.x_max):
            rw.append([])
            for y in range(self.y_max):
                try: self.matrix[x, y]
                except KeyError:
                    rw[y].append(_SGridElementReady(generateEmpty(1, 1), 1, 1, (1/self.x_max)*self.w, (1/self.y_max)*self.h))
                    continue
                print(self.matrix[x, y].content.bgcolor)
                el = self.matrix[x, y]
                s = True
                try:
                    if rw[x-1][y].control == el:
                        s = False
                except IndexError: pass
                try:
                    if rw[x][y-1].control == el:
                        s = False
                except IndexError: pass
                if s:
                    rw[x].append(_SGridElementReady(el, el.hor_size, el.vert_size, (el.hor_size/self.x_max)*self.w, (el.vert_size/self.y_max)*self.h))
        print("meow")
        for elc in rw:
            print("[]")
            for el in elc:
                print(el.control.content.bgcolor)
        gr = ft.Row(spacing=0)
        for elColumn in rw:
            col = ft.Column(spacing=0)
            for el in elColumn:
                el.control.width = el.xsize
                el.control.height = el.ysize
                col.controls.append(el.control)
            gr.controls.append(col)
        self.content = gr
        self.content = gr
        self.update()