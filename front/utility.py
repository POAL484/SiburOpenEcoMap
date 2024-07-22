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

PDKS = {
    "live": {
        "C4H10": 200,
        "C3H8": 50,
        "LPG": 300,
        "C6H6": 0.3,
        "C6H6O": 0.01
    },
    "lake": {
        "Cl": 350,
        "SO4": 500,
        "NH4": 1.5,
        "NO2": 3.3,
        "NO3": 45,
        "Fe": 0.3,
        "Cu": 1,
        "Zn": 1,
        "Ni": 0.02,
        "Mg": 0.1,
        "-OH": 0.01,
        "petroleum": 0.3
    },
    "rain": {
        "HCO3": 60,
        "SO4": 500,
        "Cl": 350,
        "NO3": 45,
        "Ca": 180,
        "Mg": 50,
        "Na": 200,
        "K": 18
    }
}

def calcPdkProcent(params_type: str, param_name: str, param: float) -> float:
    if params_type == 'live': return
    assert isinstance(param, float), "param is not float"
    if not params_type in PDKS.keys(): return
    if not param_name in PDKS[params_type].keys(): return
    return round((param/PDKS[params_type][param_name])*100, 2)