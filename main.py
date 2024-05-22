import pyxel
import random
bonhomme_x = 51
bonhomme_y = 128
ennemis_liste = []
pyxel.init(256, 256)
pyxel.cls(5)
pyxel.load("3.pyxres")

def bonhomme_deplacement(x, y)
    if pyxel.btn(pyxel.KEY_DOWN):
        if y < 256:
            y = y + 1.5
    if pyxel.btn(pyxel.KEY_UP):
        if y > 0:
            y = y - 1.5
    return x, y

def update():


def draw():


pyxel.run(update, draw)
