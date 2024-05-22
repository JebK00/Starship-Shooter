import pyxel
import random

#initialise
vitesse = 1,5
bonhomme_x = 128
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
aleatoire =0
aleatoire2 =0

def collision_cercle(cx1, cy1, r1, cx2, cy2, r2):
    return ((cx1 - cx2) ** 2) + ((cy1 - cy2) ** 2) <= (r1 + r2) ** 2

def projectile_creation(x, y, projectile_liste):
    if pyxel.btnr(pyxel.KEY_SPACE):
        projectile_liste.append([x+4, y-4])
        vitesse = 0,5
    else :
        vitesse = 1,5
    return projectile_liste

def projectile_deplacement(projectile_liste):
    for projectile in projectile_liste:
        projectile[1] -= 1
        if  projectile[1]<-8:
            projectile_liste.remove(projectile)
    return projectile_liste

def bonhomme_deplacement(x, y):
    if pyxel.btn(pyxel.KEY_DOWN):
        if y < 256:
            y = y + vitesse
    if pyxel.btn(pyxel.KEY_UP):
        if y > 0:
            y = y - vitesse
    return x, y

def arthropode_creation(arthropode_liste):
    if pyxel.frame_count % 50 == 0:
        if len(arthropode_liste)<5:
            arthropode_liste.append([random.randint(0, 256), 0])
    return arthropode_liste

def arthropode_suppression():
    global bonhomme_x, bonhomme_y, arthropode_liste, points_de_victoire

    arthropode_enleves = []

    for ennemi in arthropode_liste:

        ennemi_x, ennemi_y = ennemi
        if collision_cercle(ennemi_x, ennemi_y, 7.5, bonhomme_x, bonhomme_y, 7.5):
            arthropode_enleves.append(ennemi)

    for ennemi in arthropode_enleves:
        points_de_victoire += 1
        arthropode_liste.remove(ennemi)


def arthropode_deplacement(arthropode_liste):
    global points_de_structure
    for ennemi in arthropode_liste:
        ennemi[1] += 1
        if ennemi[1] > 256:
            arthropode_liste.remove(ennemi)
    return arthropode_liste

def update():
    global bonhomme_x, bonhomme_y, arthropode_liste, points_de_vie, projectile_liste, vitesse
    bonhomme_x, bonhomme_y = bonhomme_deplacement(bonhomme_x, bonhomme_y)
    arthropode_liste = arthropode_creation(arthropode_liste)
    arthropode_liste = arthropode_deplacement(arthropode_liste)
    projectile_liste = projectile_creation(bonhomme_x, bonhomme_y, projectile_liste)
    projectile_liste = projectile_deplacement(projectile_liste)
    arthropode_suppression()

    aleatoire = random.randint(0,1)
    aleatoire2 = random.randint(0,1)
    if aleatoire == 0:
        if aleatoire2 ==0:
            arthropode_x+=1
        else:
            arthropode_x-=1
def draw():


    if points_de_victoire == 100:
        pyxel.cls(0)
        pyxel.text(0, 54, 'Vous avez vaincu les Aliens !', 7)
        pyxel.text(0, 64, 'La Démocratie a gagné', 7)
        pyxel.text(0, 74, 'Team Campi', 7)
    else:
        if points_de_vie>0:
            pyxel.cls(5)
            pyxel.blt(position_caillou_1_x, position_caillou_1_y, 0, 176, 128, 16, 16)
            pyxel.blt(position_caillou_2_x, position_caillou_2_y, 0, 192, 128, 16, 16)
            pyxel.blt(position_caillou_3_x, position_caillou_3_y, 0, 208, 128, 16, 16)
            pyxel.blt(position_caillou_4_x, position_caillou_4_y, 0, 224, 128, 32, 16)
            pyxel.blt(position_caillou_5_x, position_caillou_5_y, 0, 176, 128, 16, 16)
            pyxel.blt(position_caillou_6_x, position_caillou_6_y, 0, 192, 128, 16, 16)
            pyxel.blt(position_caillou_7_x, position_caillou_7_y, 0, 208, 128, 16, 16)
            pyxel.blt(position_caillou_8_x, position_caillou_8_y, 0, 224, 128, 32, 16)
            for arthropode in arthropode_liste:
                pyxel.blt(arthropode[0], arthropode[1], 0, 0, 120, -15, 15)
            pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 8, 16, 15)
        else:
            pyxel.cls(0)
            pyxel.text(0, 54, 'Les Aliens on pris la planète !', 7)
            pyxel.text(0, 64, 'La Démocratie a perdu', 7)



pyxel.run(update, draw)
