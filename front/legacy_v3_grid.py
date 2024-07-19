import flet as ft

class SGridElement(ft.Container):
    def __init__(self, content: ft.Control, xsize: int, ysize: int):
        super().__init__(content=content)
        self.xsize = xsize
        self.ysize = ysize

class SGridNewLine: pass

class SGridPackedElement:
    def __init__(self, c: SGridElement, start_x: int, end_x: int, start_y: int, end_y: int):
        self.c = c
        self.start_x = start_x
        self.end_x = end_x
        self.start_y = start_y
        self.end_y = end_y

class SGrid(ft.Container):

    def packAll(self, elements: list) -> tuple:
        cursor = {'x': 0, 'y': 0}
        matrix = {}
        maxes = {'x': -1, 'y': -1}
        packed = []
        for el in elements:
            assert isinstance(el, SGridElement) or isinstance(el, SGridNewLine), f"All elements should be SGridElement or SGridNewLine, element type {type(el)} found"
            if isinstance(el, SGridNewLine):
                if cursor['x'] > maxes['x']: maxes['x'] = cursor['x']
                cursor['x'] = 0
                cursor['y'] += 1
            else:
                packed.append(SGridPackedElement(
                    el, cursor['x'], cursor['x']+el.xsize-1, cursor['y'], cursor['y']+el.ysize-1
                ))
                for xsized in range(el.xsize):
                    for ysized in range(el.ysize):
                        matrix[cursor['x']+xsized, cursor['y']+ysized] = 'X'
                cursor['x'] += el.xsize
            try:
                while matrix[cursor['x'], cursor['y']] == "X":
                    cursor['x'] += 1
            except KeyError: pass
        maxes['y'] = cursor['y'] + 1
        return (maxes, packed)
    
    
    def columnCheck(self, packedElements: list, start_x: int, end_x: int, start_y: int, end_y: int) -> tuple:
        pck = self.getInZone(packedElements, start_x, end_x, start_y, end_y)
        ys = []
        for ycheck in range(int(start_y+.5), int(end_y-1.5)):
            s = True
            for el in pck:
                #print(ycheck, ycheck+.5, el.start_y, el.end_y)
                if ( ycheck+.5 > el.start_y and ycheck+.5 < el.end_y ):
                    s = False
            if s: ys.append(ycheck+.5)
        return (len(ys) != 0, ys)

    def getInZone(self, packedElements: list, start_x: int, end_x: int, start_y: int, end_y: int):
        pck = []
        for el in packedElements:
            if el.start_x > start_x and el.end_x < end_x and el.start_y > start_y and el.end_y < end_y:
                pck.append(el)
        return pck
    
    def rowCheck(self, packedElements: list, start_x: int, end_x: int, start_y: int, end_y: int) -> tuple:
        pck = self.getInZone(packedElements, start_x, end_x, start_y, end_y)
        xs = []
        for xcheck in range(int(start_x+.5), int(end_x-1.5)):
            s = True
            for el in pck:
                #print(xcheck, xcheck+.5, el.start_x, el.end_x)
                if ( xcheck+.5 > el.start_x and xcheck+.5 < el.end_x ):
                    s = False
            if s: xs.append(xcheck+.5)
        return (len(xs) != 0, xs)

    def reRow(self, start_x: int, end_x: int, start_y: int, end_y: int, debug_history: str):
        state, myRow = self.rowCheck(self.packed, start_x, end_x, start_y, end_y)
        if not state:
            el = self.getInZone(self.packed, start_x, end_x, start_y, end_y)[0].c
            print(f"Found object: {start_x}, {end_x}, {start_y}, {end_y}\n\n")
            el.width = ((end_x-start_x)/self.maxes['x'])*self.w
            el.height = ((end_y-start_y)/self.maxes['y'])*self.h
            return el
        debug_history += f"row {start_x} {end_x} {start_y} {end_y} {myRow} "
        print(debug_history)
        #print("__row", myRow)
        grow = ft.Row(spacing=0)
        grow.controls.append(self.reColumn(start_x, myRow[0], start_y, end_y, debug_history))
        print(self.reColumn(start_x, myRow[0], start_y, end_y, debug_history))
        for col in myRow[1:]:
            grow.controls.append(self.reColumn(myRow[myRow.index(col)-1], col, start_y, end_y, debug_history))
        print(f"\n{myRow[-1]}\n")
        grow.controls.append(self.reColumn(myRow[-1], end_x, start_y, end_y, debug_history))
        return grow

    def reColumn(self, start_x: int, end_x: int, start_y: int, end_y: int, debug_history: str):
        state, myColumn = self.columnCheck(self.packed, start_x, end_x, start_y, end_y)
        if not state:
            el = self.getInZone(self.packed, start_x, end_x, start_y, end_y)[0].c
            print(f"Found object: {start_x}, {end_x}, {start_y}, {end_y}\n\n")
            el.width = ((el.xsize)/self.maxes['x'])*self.w
            el.height = ((el.ysize)/self.maxes['y'])*self.h
            return el
        debug_history += f"column {start_x} {end_x} {start_y} {end_y} {myColumn} "
        print(debug_history)
        #print("__column", myColumn)
        gcol = ft.Column(spacing=0)
        gcol.controls.append(self.reRow(start_x, end_x, start_y, myColumn[0], debug_history))
        print(self.reRow(start_x, end_x, start_y, myColumn[0], debug_history))
        for row in myColumn[1:]:
            gcol.controls.append(self.reRow(start_x, end_x, myColumn[myColumn.index(row)-1], row, debug_history))
        gcol.controls.append(self.reRow(start_x, end_x, myColumn[-1], end_y, debug_history))
        return gcol

    def __init__(self, elements: list, width: int | None = None, height: int | None = None):
        self.maxes, self.packed = self.packAll(elements)
        
        self.w = width
        self.h = height

        print(self.rowCheck(self.packed, -.5, self.maxes['x']+.5, -.5, self.maxes['y']+.5))

        if self.columnCheck(self.packed, -.5, self.maxes['x']+.5, -.5, self.maxes['y']+.5)[0]:
            cont = self.reColumn(-.5, self.maxes['x']+.5, -.5, self.maxes['y']+.5, '')
        elif self.rowCheck(self.packed, -.5, self.maxes['x']+.5, -.5, self.maxes['y']+.5)[0]:
            cont = self.reRow(-.5,self.maxes['x']+.5, -.5, self.maxes['y']+.5, '')
        else:
            raise Exception("Failed to column or row check")
        
        super().__init__(cont)