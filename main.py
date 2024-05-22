import pyxel
import random

def __init__(self):
    pyxel.init(256, 256)
    self.x = 0
    pyxel.run(self.update, self.draw)

def update(self):

    def draw(self):
        pyxel.cls(1)
        pyxel.rect(self.x, 0, 8, 8, 9)

pyxel.run(update, draw)