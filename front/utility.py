

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

if __name__ == "__main__":
    print("\n\n\n\n\n\n\n\n\n")
    print(rgb_to_hex(set_percent_of_colors((71, 0, 64), (244, 71, 212), 0, 100, 50)))