from PIL.ImageFont import FreeTypeFont

def rgb_to_hex(color: iter):
    s = "#"
    for comp in color:
        s += str(hex(round(comp)))[2:]
    return s

def set_percent_of_colors(color_1: tuple, color_2: tuple, min_: float, max_: float, val: float):
    assert len(color_1) == len(color_2)
    col = []
    percent = val / (max_ - min_)
    for i in range(len(color_1)):
        col.append( max(color_1[i], color_2[i]) - (abs(color_1[i]-color_2[i])*percent) )
    return col

def calculateFont(font: FreeTypeFont, target_width: float, text: str):
    prop_width = font.getlength(text)
    prop_height = font.size
    return (target_width*prop_height)/prop_width