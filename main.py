import pyxel
import random

bonhomme_x = 51
bonhomme_y = 128
position_caillou_1_x = random.randint(0, 256)
position_caillou_1_y = random.randint(0, 256)
position_caillou_2_x = random.randint(0, 256)
position_caillou_2_y = random.randint(0, 256)
position_caillou_3_x = random.randint(0, 256)
position_caillou_3_y = random.randint(0, 256)
position_caillou_4_x = random.randint(0, 256)
position_caillou_4_y = random.randint(0, 256)
position_caillou_5_x = random.randint(0, 256)
position_caillou_5_y = random.randint(0, 256)
position_caillou_6_x = random.randint(0, 256)
position_caillou_6_y = random.randint(0, 256)
position_caillou_7_x = random.randint(0, 256)
position_caillou_7_y = random.randint(0, 256)
position_caillou_8_x = random.randint(0, 256)
position_caillou_8_y = random.randint(0, 256)
arthropode_liste = []
projectile_liste = []
points_de_vie = 10
points_de_victoire = 0
pyxel.init(256, 256)
pyxel.cls(5)
pyxel.load("3.pyxres")


def collision_cercle_bonhomme(cx1, cy1, r1, cx2, cy2, r2):
    return ((cx1 - cx2)**2) + ((cy1 - cy2)**2) <= (r1 + r2)**2


def collision_cercle_projectile(cx1, cy1, r1, cx2, cy2, r2):
    return ((cx1 - cx2)**2) + ((cy1 - cy2)**2) <= (r1 + r2)**2


def projectile_creation(x, y, projectile_liste):
    if pyxel.btnr(pyxel.KEY_SPACE):
        projectile_liste.append([x + 14, y - 4])
    return projectile_liste


def projectile_deplacement(projectile_liste):
    for projectile in projectile_liste:
        projectile[0] += 1
        if projectile[0] < -8:
            projectile_liste.remove(projectile)
    return projectile_liste


def bonhomme_deplacement(x, y):
    if pyxel.btn(pyxel.KEY_DOWN):
        if y < 256:
            y = y + 1.5
    if pyxel.btn(pyxel.KEY_UP):
        if y > 0:
            y = y - 1.5
    return x, y


def arthropode_creation(arthropode_liste):
    if pyxel.frame_count % 50 == 0:
        if len(arthropode_liste) < 5:
            arthropode_liste.append(
                [random.randint(0, 256),
                 random.randint(0, 256)])
    return arthropode_liste


def arthropode_suppression():
    global bonhomme_x, bonhomme_y, arthropode_liste, points_de_victoire, projectile

    arthropode_enleves = []

    for arthropode in arthropode_liste:

        arthropode_x, arthropode_y = arthropode
        if collision_cercle_projectile(arthropode_x, arthropode_y, 7.5,
                                       projectile[0], projectile[1], 7.5):
            arthropode_enleves.append(arthropode)

    for arthropode in arthropode_enleves:
        points_de_victoire += 1
        arthropode_liste.remove(arthropode)


def arthropode_deplacement(arthropode_liste):
    global points_de_structure
    for arthropode in arthropode_liste:
        arthropode[1] += random.randint(-1, 1)
        arthropode[0] += random.randint(-1, 1)
        if arthropode[1] > 248 and arthropode[1] < 8:
            arthropode_liste.remove(arthropode)
        if arthropode[0] > 248 and arthropode[0] < 8:
            arthropode_liste.remove(arthropode)
    return arthropode_liste


def update():
    global bonhomme_x, bonhomme_y, arthropode_liste, points_de_vie, projectile_liste

    bonhomme_x, bonhomme_y = bonhomme_deplacement(bonhomme_x, bonhomme_y)

    arthropode_liste = arthropode_creation(arthropode_liste)

    arthropode_liste = arthropode_deplacement(arthropode_liste)

    projectile_liste = projectile_creation(bonhomme_x, bonhomme_y,
                                           projectile_liste)

    projectile_liste = projectile_deplacement(projectile_liste)

    arthropode_suppression()


def draw():

    if points_de_victoire == 100:
        pyxel.cls(0)
        pyxel.text(0, 54, 'Vous avez vaincu les Aliens !', 7)
        pyxel.text(0, 64, 'La Démocratie a gagné', 7)
        pyxel.text(0, 74, 'Team Campi', 7)
    else:
        if points_de_vie > 0:
            pyxel.cls(5)
            pyxel.blt(position_caillou_1_x, position_caillou_1_y, 0, 176, 128,
                      16, 16)
            pyxel.blt(position_caillou_2_x, position_caillou_2_y, 0, 192, 128,
                      16, 16)
            pyxel.blt(position_caillou_3_x, position_caillou_3_y, 0, 208, 128,
                      16, 16)
            pyxel.blt(position_caillou_4_x, position_caillou_4_y, 0, 224, 128,
                      32, 16)
            pyxel.blt(position_caillou_5_x, position_caillou_5_y, 0, 176, 128,
                      16, 16)
            pyxel.blt(position_caillou_6_x, position_caillou_6_y, 0, 192, 128,
                      16, 16)
            pyxel.blt(position_caillou_7_x, position_caillou_7_y, 0, 208, 128,
                      16, 16)
            pyxel.blt(position_caillou_8_x, position_caillou_8_y, 0, 224, 128,
                      32, 16)
            for arthropode in arthropode_liste:
                pyxel.blt(arthropode[0], arthropode[1], 0, 0, 120, -15, 15)
            pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 8, 16, 16)
            if pyxel.btnr(pyxel.KEY_SPACE):
                pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 56, 16, 16)

            for tir in projectile_liste:
                pyxel.blt(tir[0], tir[1], 0, 32, 8, 8, 8)
        else:
            pyxel.cls(0)
            pyxel.text(0, 54, 'Les Aliens on pris la planète !', 7)
            pyxel.text(0, 64, 'La Démocratie a perdu', 7)


pyxel.run(update, draw)
