import pyxel
import random

# Initialisation des variables
bonhomme_x = 128
bonhomme_y = 128
status = 0
direction = 0
points_de_vie = 10
points_de_victoire = 0
arthropode_liste = []
projectile_liste = []
ft_liste = []

# Charger les ressources
pyxel.init(256, 256)
pyxel.load("3.pyxres")

# Variables pour les écrans
start_screen = True

def generate_positions():
    positions = []
    while len(positions) < 10:
        x, y = random.randint(0, 240), random.randint(0, 240)
        if all((abs(x - px) > 16 and abs(y - py) > 16) for px, py in positions):
            positions.append((x, y))
    return positions

caillou_positions = generate_positions()[:8]
barril_positions = generate_positions()[8:]

def collision_cercle(cx1, cy1, r1, cx2, cy2, r2):
    return ((cx1 - cx2)**2 + (cy1 - cy2)**2) <= (r1 + r2)**2

def projectile_creation(x, y, direction):
    if pyxel.btnp(pyxel.KEY_SPACE) and len(projectile_liste) < 10:
        if direction == 0:
            projectile_liste.append([x + 14, y + 3, direction])
        else:
            projectile_liste.append([x - 4, y + 3, direction])

def projectile_deplacement():
    for projectile in projectile_liste:
        if projectile[2] == 0:
            projectile[0] += 5
        else:
            projectile[0] -= 5
        if projectile[0] < -8 or projectile[0] > 264:
            projectile_liste.remove(projectile)

def ft_creation(x, y):
    if pyxel.btnp(pyxel.KEY_F) and len(ft_liste) < 1:
        ft_liste.append([x + 14, y + 3])

def ft_deplacement():
    for ft in ft_liste:
        ft[0] += 1
        if ft[0] < -8:
            ft_liste.remove(ft)

def bonhomme_deplacement(x, y):
    global direction
    if pyxel.btn(pyxel.KEY_DOWN) and y < 240:
        y += 1.5
    if pyxel.btn(pyxel.KEY_UP) and y > 0:
        y -= 1.5
    if pyxel.btn(pyxel.KEY_LEFT) and x > 0:
        x -= 1.5
        direction = 1
    if pyxel.btn(pyxel.KEY_RIGHT) and x < 240:
        x += 1.5
        direction = 0
    return x, y

def arthropode_creation():
    if pyxel.frame_count % 50 == 0 and len(arthropode_liste) < 5:
        arthropode_liste.append([random.randint(0, 256), random.randint(0, 256)])

def arthropode_suppression():
    global points_de_vie, points_de_victoire
    for arthropode in arthropode_liste[:]:
        arthropode_x, arthropode_y = arthropode
        for projectile in projectile_liste[:]:
            if collision_cercle(arthropode_x, arthropode_y, 7.5, projectile[0], projectile[1], 7.5):
                arthropode_liste.remove(arthropode)
                projectile_liste.remove(projectile)
                points_de_victoire += 1
        if collision_cercle(arthropode_x, arthropode_y, 7.5, bonhomme_x, bonhomme_y, 7.5):
            arthropode_liste.remove(arthropode)
            points_de_vie -= 1

def arthropode_suppressionft():
    for arthropode in arthropode_liste[:]:
        arthropode_x, arthropode_y = arthropode
        for ft in ft_liste[:]:
            if collision_cercle(arthropode_x, arthropode_y, 7.5, ft[0], ft[1], 7.5):
                arthropode_liste.remove(arthropode)

def arthropode_deplacement():
    for arthropode in arthropode_liste[:]:
        arthropode[1] += random.randint(-1, 1)
        arthropode[0] += random.randint(-1, 1)
        if arthropode[1] < 8 or arthropode[1] > 248 or arthropode[0] < 8 or arthropode[0] > 248:
            arthropode_liste.remove(arthropode)

def update():
    global bonhomme_x, bonhomme_y, start_screen
    if start_screen:
        if pyxel.btnp(pyxel.KEY_RETURN):
            start_screen = False
        return

    bonhomme_x, bonhomme_y = bonhomme_deplacement(bonhomme_x, bonhomme_y)

    arthropode_creation()
    arthropode_deplacement()

    projectile_creation(bonhomme_x, bonhomme_y, direction)
    projectile_deplacement()

    ft_creation(bonhomme_x, bonhomme_y)
    ft_deplacement()

    arthropode_suppression()
    arthropode_suppressionft()

def draw():
    global start_screen
    if start_screen:
        pyxel.cls(5)
        pyxel.text(90, 60, "Starship Troopers", pyxel.frame_count % 16)
        pyxel.text(20, 100, "Créateurs: Renan Laugier - Nils Doucet - Arthur Jensen", 7)
        pyxel.text(75, 120, "A Ryangames Production", 7)
        pyxel.text(80, 140, "Fleche pour deplacer", 7)
        pyxel.text(35, 160, "Espace pour Mitraillette; F pour Lance-Flamme", 7)
        pyxel.text(60, 200, "Appuyez sur ENTER pour commencer", 7)
        return

    if points_de_victoire == 25:
        pyxel.cls(5)
        pyxel.text(64, 110, 'Vous avez vaincu les Aliens !', 7)
        pyxel.text(64, 120, 'La Democratie a gagne', 7)
        pyxel.text(64, 130, 'Team Campi', 7)
    elif points_de_vie > 0:
        pyxel.cls(5)
        pyxel.blt(240, 240, 0, 48, 200, 16, 16)
        for (x, y) in caillou_positions:
            pyxel.blt(x, y, 0, 176, 128, 16, 16)
        for (x, y) in barril_positions:
            pyxel.blt(x, y, 0, 176, 112, 16, 16)
        for arthropode in arthropode_liste:
            pyxel.blt(arthropode[0], arthropode[1], 0, 0, 120, -15, 15)
        if direction == 0:
            pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 8, 16, 16)
        else:
            pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 8, -16, 16)
        for projectile in projectile_liste:
            pyxel.blt(projectile[0], projectile[1], 0, 48, 8, 8, 8)
        for ft in ft_liste:
            pyxel.blt(ft[0], ft[1], 0, 128, 32, 16, 16)
    else:
        pyxel.cls(5)
        pyxel.text(64, 110, 'Les Aliens on pris la planète !', 7)
        pyxel.text(64, 120, 'La Democratie a perdu', 7)
    pyxel.text(10, 10, str(points_de_victoire), 6)
    pyxel.text(224, 240, str(points_de_vie), 0)

pyxel.run(update, draw)
