import os

os.system('')


def rgb(red=None, green=None, blue=None, bg=False):
    if (bg == False and red != None and green != None and blue != None):
        return f'\u001b[38;2;{red};{green};{blue}m'
    elif (bg == True and red != None and green != None and blue != None):
        return f'\u001b[48;2;{red};{green};{blue}m'
    elif (red == None and green == None and blue == None):
        return '\u001b[0m'


def text(str):
    g0 = rgb()
    g2 = rgb(0, 100, 0, True) + "" + rgb(100, 255, 100)

    print(f"{g2}{str}{g0}")
