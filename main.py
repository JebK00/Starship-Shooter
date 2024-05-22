import pyxel
import random
bonhomme_x = 51
bonhomme_y = 128
ennemis_liste = []
points_de_vie = 10
points_de_victoire = 0
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
    global bonhomme_x, bonhomme_y, ennemis_liste, points_de_vie
    bonhomme_x, bonhomme_y = bonhomme_deplacement(bonhomme_x, bonhomme_y)
    ennemis_liste = ennemis_creation(ennemis_liste)
    ennemis_liste = ennemis_deplacement(ennemis_liste)
    ennemis_suppression()

def draw():
 if 

pyxel.run(update, draw)
