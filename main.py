import pyxel
import random
import time
bonhomme_x = 128
bonhomme_y = 128
status = 0
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
position_barril_1_x = random.randint(0, 256)
position_barril_1_y = random.randint(0, 256)
position_barril_2_x = random.randint(0, 256)
position_barril_2_y = random.randint(0, 256)
arthropode_liste = []
projectile_liste = []
ft_liste = []
points_de_vie = 10
points_de_victoire = 0
pyxel.init(256, 256)
pyxel.cls(5)
pyxel.load("3.pyxres")


def collision_cercle_bonhomme(cx1, cy1, r1, cx2, cy2, r2):
    return ((cx1 - cx2)**2) + ((cy1 - cy2)**2) <= (r1 + r2)**2


def collision_cercle_projectile(cx1, cy1, r1, cx2, cy2, r2):
    return ((cx1 - cx2)**2) + ((cy1 - cy2)**2) <= (r1 + r2)**2

def collision_cercle_projectileft(cx1, cy1, r1, cx2, cy2, r2):
    return ((cx1 - cx2)**2) + ((cy1 - cy2)**2) <= (r1 + r2)**2

def projectile_creation(x, y, projectile_liste, ):
    if pyxel.btnr(pyxel.KEY_SPACE):
        if status==0:
            projectile_liste.append([x + 14, y+3])
    return projectile_liste, 

def projectile_deplacement(projectile_liste, ):
    for projectile in projectile_liste:
        if status==0:
            projectile[0] += 5
            if projectile[0] < -8:
                projectile_liste.remove(projectile)

    return projectile_liste, 

def ft_creation(x, y, ft_liste):
    if pyxel.btnr(pyxel.KEY_F):
        ft_liste.append([x + 14, y+3])
    return ft_liste

def ft_deplacement(ft_liste):
    for ft in ft_liste:
        ft[0] += 1
        if ft[0] < -8:
            ft.remove(ft)
    return ft_liste


def bonhomme_deplacement(x, y):
    if pyxel.btn(pyxel.KEY_DOWN):
        if y < 240:
            y = y + 1.5
    if pyxel.btn(pyxel.KEY_UP):
        if y > 0:
            y = y - 1.5
    if pyxel.btn(pyxel.KEY_LEFT):
        if x > 0:
            x = x - 1.5
    if pyxel.btn(pyxel.KEY_RIGHT):
        if x > 0:
            x = x + 1.5
    return x, y


def arthropode_creation(arthropode_liste):
    if pyxel.frame_count % 50 == 0:
        if len(arthropode_liste) < 5:
            arthropode_liste.append([random.randint(0, 256), random.randint(0, 256)])
    return arthropode_liste


def arthropode_suppression():
    global bonhomme_x, bonhomme_y, arthropode_liste, points_de_victoire, projectile, status, points_de_vie

    arthropode_enleves = []

    for arthropode in arthropode_liste:

        arthropode_x, arthropode_y = arthropode
        for tir_r in projectile_liste:
            if collision_cercle_projectile(arthropode_x, arthropode_y, 7.5, tir_r[0], tir_r[1], 7.5):
                arthropode_enleves.append(arthropode)
                arthropode_liste.remove(arthropode)
                points_de_victoire += 1
        if collision_cercle_bonhomme(arthropode_x, arthropode_y, 7.5, bonhomme_x, bonhomme_y, 7.5):
               arthropode_enleves.append(arthropode)
               arthropode_liste.remove(arthropode)
               points_de_vie -= 1


def arthropode_suppressionft():
    global bonhomme_x, bonhomme_y, arthropode_liste, points_de_victoire, ft

    arthropode_enleves = []

    for arthropode in arthropode_liste:

        arthropode_x, arthropode_y = arthropode
        for tirft in ft_liste:
            if collision_cercle_projectileft(arthropode_x, arthropode_y, 7.5, tirft[0], tirft[1], 7.5):
                arthropode_enleves.append(arthropode)

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
    global bonhomme_x, bonhomme_y, arthropode_liste, points_de_vie, projectile_liste, poin, status, ft_liste

    bonhomme_x, bonhomme_y = bonhomme_deplacement(bonhomme_x, bonhomme_y)

    arthropode_liste = arthropode_creation(arthropode_liste)

    arthropode_liste = arthropode_deplacement(arthropode_liste)

    projectile_liste = projectile_creation(bonhomme_x, bonhomme_y, projectile_liste)

    projectile_liste = projectile_deplacement(projectile_liste)

    ft_liste = ft_creation(bonhomme_x, bonhomme_y, ft_liste)

    ft_liste = ft_deplacement(ft_liste)

    arthropode_suppression()



def draw():
    global status, tir_l, tir_r, projectile
    if points_de_victoire == 25:
        pyxel.cls(0)
        pyxel.text(0, 54, 'Vous avez vaincu les Aliens !', 7)
        pyxel.text(0, 64, 'La Democratie a gagne', 7)
        pyxel.text(0, 74, 'Team Campi', 7)
    else:
        if points_de_vie > 0:
            pyxel.cls(5)
            pyxel.blt(240, 240, 0, 48, 200, 16, 16)
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
            pyxel.blt(position_barril_1_x, position_barril_1_y, 0, 176, 112, 16, 16,)
            pyxel.blt(position_barril_2_x, position_barril_2_y, 0, 192, 112, 16, 16,)
            for arthropode in arthropode_liste:
                pyxel.blt(arthropode[0], arthropode[1], 0, 0, 120, -15, 15)
            if status==0:
                pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 8, 16, 16)
            if status==1:
                    pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 8, -16, 16)
            if pyxel.btnr(pyxel.KEY_RIGHT):
                pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 8, 16, 16)
                if pyxel.btnr(pyxel.KEY_SPACE):
                    pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 56, 16, 16)
                status=0
            if pyxel.btnr(pyxel.KEY_LEFT):
                pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 8, -16, 16)
                if pyxel.btnr(pyxel.KEY_SPACE):
                    pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 56, -16, 16)
                status=1

            for projectile in projectile_liste:
                pyxel.blt(projectile[0], projectile[1], 0, 48, 8, 8, 8)
            
            for tirft in ft_liste:
                    pyxel.blt(tirft[0], tirft[1], 0, 128, 32, 16, 16 )
                    time.sleep(0.1)
                    pyxel.blt(tirft[0], tirft[1], 0, 144, 32, 16, 16 )
                    time.sleep(0.1)
                    pyxel.blt(tirft[0], tirft[1], 0, 160, 32, 16, 16 )
                    time.sleep(0.1)
                    pyxel.blt(tirft[0], tirft[1], 0, 176, 32, 16, 16 )
                    time.sleep(0.1)
                    pyxel.blt(tirft[0], tirft[1], 0, 192, 32, 16, 16 )
                    time.sleep(0.1)
                    pyxel.blt(tirft[0], tirft[1], 0, 208, 32, 16, 16 )
                    time.sleep(0.1)
        else:
            pyxel.cls(0)
            pyxel.text(0, 54, 'Les Aliens on pris la planète !', 7)
            pyxel.text(0, 64, 'La Democratie a perdu', 7)
    pyxel.text(10,10,str(points_de_victoire),6)
    pyxel.text(224,240,str(points_de_vie),0)
  
pyxel.run(update, draw)
