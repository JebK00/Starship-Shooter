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

# Animation du tir
tir_animation = 0
ft_animation = 0
explosions = []

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
            if abs(x - 128) > 15 or abs(y - 128) > 15:  # Empêcher les cailloux/barils de spawn dans un carré de 15x15 autour de x=128, y=128
                positions.append((x, y))
    return positions

caillou_positions = generate_positions()[:8]
barril_positions = generate_positions()[8:]

def collision_cercle(cx1, cy1, r1, cx2, cy2, r2):
    return ((cx1 - cx2)**2 + (cy1 - cy2)**2) <= (r1 + r2)**2

def collision_rectangle(x1, y1, w1, h1, x2, y2, w2, h2):
    return not (x1 > x2 + w2 or x1 + w1 < x2 or y1 > y2 + h2 or y1 + h1 < y2)

def projectile_creation(x, y, direction):
    global tir_animation
    if pyxel.btnp(pyxel.KEY_SPACE or pyxel.GAMEPAD1_BUTTON_X) and len(projectile_liste) < 10:
        if direction == 0:
            projectile_liste.append([x + 14, y + 3, direction, 0])
        else:
            projectile_liste.append([x - 4, y + 3, direction, 0])
        tir_animation = 1

def projectile_deplacement():
    for projectile in projectile_liste[:]:
        if projectile[2] == 0:
            projectile[0] += 5
        else:
            projectile[0] -= 5
        projectile[3] += 1

        for (cx, cy) in caillou_positions + barril_positions:
            if collision_rectangle(projectile[0], projectile[1], 8, 8, cx, cy, 16, 16):
                projectile_liste.remove(projectile)
                break

        if projectile[0] < -8 or projectile[0] > 264:
            projectile_liste.remove(projectile)

def ft_creation(x, y, direction):
    global ft_animation
    if pyxel.btnp(pyxel.KEY_F or pyxel.GAMEPAD1_BUTTON_Y) and len(ft_liste) < 1:
        if direction == 0:
            ft_liste.append([x + 14, y + 3, direction, 0])
        else:
            ft_liste.append([x - 4, y + 3, direction, 0])
        ft_animation = 1

def ft_deplacement():
    for ft in ft_liste[:]:
        if ft[2] == 0:
            ft[0] += 2
        else:
            ft[0] -= 2
        ft[3] += 1

        for (cx, cy) in caillou_positions + barril_positions:
            if collision_rectangle(ft[0], ft[1], 16, 16, cx, cy, 16, 16):
                explosions.append([ft[0], ft[1], 0])
                ft_liste.remove(ft)
                break

        if ft[0] < -16 or ft[0] > 272:
            ft_liste.remove(ft)

def bonhomme_deplacement(x, y):
    global direction
    old_x, old_y = x, y
    if pyxel.btn(pyxel.KEY_DOWN or pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) and y < 240:
        y += 1.5
    if pyxel.btn(pyxel.KEY_UP or pyxel.GAMEPAD1_BUTTON_DPAD_UP) and y > 0:
        y -= 1.5
    if pyxel.btn(pyxel.KEY_LEFT or pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) and x > 0:
        x -= 1.5
        direction = 1
    if pyxel.btn(pyxel.KEY_RIGHT or pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) and x < 240:
        x += 1.5
        direction = 0

    for (cx, cy) in caillou_positions + barril_positions:
        if collision_rectangle(x, y, 16, 16, cx, cy, 16, 16):
            x, y = old_x, old_y
            break

    return x, y

def arthropode_creation():
    while len(arthropode_liste) < 4:
        # Générer une position aléatoire sur les bordures de l'écran
        if random.choice([True, False]):
            x = random.choice([0, 240])
            y = random.randint(0, 240)
        else:
            x = random.randint(0, 240)
            y = random.choice([0, 240])

        if all(not collision_rectangle(x, y, 16, 16, cx, cy, 16, 16) for (cx, cy) in caillou_positions + barril_positions):
            arthropode_liste.append([x, y, random.choice([-1, 1]), random.choice([-1, 1])])

def arthropode_suppression():
    global points_de_vie, points_de_victoire
    for arthropode in arthropode_liste[:]:
        arthropode_x, arthropode_y = arthropode[:2]
        for projectile in projectile_liste[:]:
            if collision_cercle(arthropode_x, arthropode_y, 7.5, projectile[0], projectile[1], 7.5):
                arthropode_liste.remove(arthropode)
                projectile_liste.remove(projectile)
                points_de_victoire += 1
        if collision_cercle(arthropode_x, arthropode_y, 7.5, bonhomme_x, bonhomme_y, 7.5):
            arthropode_liste.remove(arthropode)
            points_de_vie -= 1
        for ft in ft_liste[:]:
            if collision_cercle(arthropode_x, arthropode_y, 7.5, ft[0], ft[1], 7.5):
                arthropode_liste.remove(arthropode)
                explosions.append([arthropode_x, arthropode_y, 0])
                ft_liste.remove(ft)
                break

def arthropode_deplacement():
    for arthropode in arthropode_liste:
        arthropode_x, arthropode_y = arthropode[:2]
        if collision_cercle(arthropode_x, arthropode_y, 50, bonhomme_x, bonhomme_y, 0):
            dx = bonhomme_x - arthropode_x
            dy = bonhomme_y - arthropode_y
            distance = (dx**2 + dy**2)**0.5
            arthropode[0] += dx / distance * 1.25
            arthropode[1] += dy / distance * 1.25
        else:
            arthropode[0] += arthropode[2] * 1
            arthropode[1] += arthropode[3] * 1
            if arthropode[0] < 0 or arthropode[0] > 240:
                arthropode[2] *= -1
            if arthropode[1] < 0 or arthropode[1] > 240:
                arthropode[3] *= -1

        for (cx, cy) in caillou_positions + barril_positions:
            if collision_rectangle(arthropode[0], arthropode[1], 16, 16, cx, cy, 16, 16):
                arthropode[0] -= arthropode[2] * 1.5
                arthropode[1] -= arthropode[3] * 1.5
                arthropode[2] *= -1
                arthropode[3] *= -1

def update():
    global bonhomme_x, bonhomme_y, tir_animation, ft_animation, points_de_vie, points_de_victoire, start_screen

    if start_screen:
        if pyxel.btnp(pyxel.KEY_RETURN or pyxel.GAMEPAD1_BUTTON_A):
            start_screen = False
        return

    bonhomme_x, bonhomme_y = bonhomme_deplacement(bonhomme_x, bonhomme_y)
    projectile_creation(bonhomme_x, bonhomme_y, direction)
    projectile_deplacement()
    ft_creation(bonhomme_x, bonhomme_y, direction)
    ft_deplacement()
    arthropode_creation()
    arthropode_deplacement()
    arthropode_suppression()

    if tir_animation > 0:
        tir_animation += 1
        if tir_animation > 5:
            tir_animation = 0

    if ft_animation > 0:
        ft_animation += 1
        if ft_animation > 5:
            ft_animation = 0

    for explosion in explosions[:]:
        explosion[2] += 1
        if explosion[2] > 5:
            explosions.remove(explosion)

def draw():

    if start_screen:
        pyxel.cls(5)
        pyxel.text(90, 60, "Starship Shooter", pyxel.frame_count % 16)
        pyxel.text(20, 100, "Créateurs: Renan Laugier - Nils Doucet - Arthur Jensen", 7)
        pyxel.text(75, 120, "A Ryangames Production", 7)
        pyxel.text(80, 140, "Fleche pour deplacer", 7)
        pyxel.text(35, 160, "Espace pour Mitraillette; F pour Lance-Roquette", 7)
        pyxel.text(60, 200, "Appuyez sur ENTER pour commencer", 7)
        return

    if points_de_victoire == 25:
        pyxel.cls(5)
        pyxel.text(64, 110, 'Vous avez vaincu les Aliens !', 7)
        pyxel.text(64, 120, 'La Democratie a gagne', 7)
        pyxel.text(64, 130, 'Team Campi', 7)
    elif points_de_vie > 0:
        pyxel.cls(5)
        for (x, y) in caillou_positions:
            pyxel.blt(x, y, 0, 176, 128, 16, 16)
        for (x, y) in barril_positions:
            pyxel.blt(x, y, 0, 176, 112, 16, 16)
        for arthropode in arthropode_liste:
            pyxel.blt(arthropode[0], arthropode[1], 0, 0, 120, -16, 16)

        # Animation du tir
        if tir_animation > 0 and tir_animation <= 5:
            if direction == 0:
                pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 56  , 16, 16)  # Tir à droite
                if tir_animation==1:
                    pyxel.blt(bonhomme_x + 16, bonhomme_y + 3, 0, 32, 16, 8, 8)
                if tir_animation==2:
                    pyxel.blt(bonhomme_x + 16, bonhomme_y + 3, 0, 40, 16, 8, 8)
                if tir_animation==3:
                    pyxel.blt(bonhomme_x + 16, bonhomme_y + 3, 0, 48, 16, 8, 8)
                if tir_animation==4:
                    pyxel.blt(bonhomme_x + 16, bonhomme_y + 3, 0, 56, 16, 8, 8)
                if tir_animation==5:
                    pyxel.blt(bonhomme_x + 16, bonhomme_y + 3, 0, 64, 16, 8, 8)
            else:
                pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 56, -16, 16)  # Tir à gauche
                if tir_animation==1:
                    pyxel.blt(bonhomme_x - 8, bonhomme_y + 3, 0, 32, 16, -8, 8)
                if tir_animation==2:
                    pyxel.blt(bonhomme_x - 8, bonhomme_y + 3, 0, 40, 16, -8, 8)
                if tir_animation==3:
                    pyxel.blt(bonhomme_x - 8, bonhomme_y + 3, 0, 48, 16, -8, 8)
                if tir_animation==4:
                    pyxel.blt(bonhomme_x - 8, bonhomme_y + 3, 0, 56, 16, -8, 8)
                if tir_animation==5:
                    pyxel.blt(bonhomme_x - 8, bonhomme_y + 3, 0, 64, 16, -8, 8)
        else:
            if direction == 0:
                pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 8, 16, 16)
            else:
                pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 8, -16, 16)

        for projectile in projectile_liste:
            if projectile[3] < 3:
                pyxel.blt(projectile[0], projectile[1], 0, 32, 8, 8, 8)
            elif projectile[3] < 6:
                pyxel.blt(projectile[0], projectile[1], 0, 40, 8, 8, 8)
            else:
                pyxel.blt(projectile[0], projectile[1], 0, 48, 8, 8, 8)

        for ft in ft_liste:
            if ft_animation > 0 and ft_animation <= 5:
                if direction == 0:
                    pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 56  , 16, 16)  # Tir à droite
                    if ft_animation==1:
                        pyxel.blt(bonhomme_x + 16, bonhomme_y + 3, 0, 32, 16, 8, 8)
                    if ft_animation==2:
                        pyxel.blt(bonhomme_x + 16, bonhomme_y + 3, 0, 40, 16, 8, 8)
                    if ft_animation==3:
                        pyxel.blt(bonhomme_x + 16, bonhomme_y + 3, 0, 48, 16, 8, 8)
                    if ft_animation==4:
                        pyxel.blt(bonhomme_x + 16, bonhomme_y + 3, 0, 56, 16, 8, 8)
                    if ft_animation==5:
                        pyxel.blt(bonhomme_x + 16, bonhomme_y + 3, 0, 64, 16, 8, 8)
                else:
                    pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 56, -16, 16)  # Tir à gauche
                    if ft_animation==1:
                        pyxel.blt(bonhomme_x - 8, bonhomme_y + 3, 0, 32, 16, -8, 8)
                    if ft_animation==2:
                        pyxel.blt(bonhomme_x - 8, bonhomme_y + 3, 0, 40, 16, -8, 8)
                    if ft_animation==3:
                        pyxel.blt(bonhomme_x - 8, bonhomme_y + 3, 0, 48, 16, -8, 8)
                    if ft_animation==4:
                        pyxel.blt(bonhomme_x - 8, bonhomme_y + 3, 0, 56, 16, -8, 8)
                    if ft_animation==5:
                        pyxel.blt(bonhomme_x - 8, bonhomme_y + 3, 0, 64, 16, -8, 8)
            else:
                if ft[2] == 0:
                    pyxel.blt(ft[0], ft[1], 0, 128, 32, 16, 16)  # ft à droite
                else:
                    pyxel.blt(ft[0], ft[1], 0, 128, 48, 16, 16)  # ft à gauche
            if direction==0:
                if ft[3] < 3:
                    pyxel.blt(ft[0]-8, ft[1]-4, 0, 40, 56, 8, 16)
                elif ft[3] < 6:
                    pyxel.blt(ft[0], ft[1]-4, 0, 48, 56, 16, 16)
                else:
                    pyxel.blt(ft[0], ft[1]-4, 0, 64, 56, 16, 16)
            if direction==1:
                if ft[3] < 3:
                    pyxel.blt(ft[0], ft[1]-4, 0, 40, 56, -8, 16)
                elif ft[3] < 6:
                    pyxel.blt(ft[0], ft[1]-4, 0, 48, 56, -16, 16)
                else:
                    pyxel.blt(ft[0], ft[1]-4, 0, 64, 56, -16, 16)


        for explosion in explosions:
            pyxel.blt(explosion[0], explosion[1], 0, 128, 32, 16, 16)
            pyxel.blt(explosion[0], explosion[1], 0, 144, 32, 16, 16)
            pyxel.blt(explosion[0], explosion[1], 0, 160, 32, 16, 16)
            pyxel.blt(explosion[0], explosion[1], 0, 176, 32, 16, 16)
            pyxel.blt(explosion[0], explosion[1], 0, 192, 32, 16, 16)
            pyxel.blt(explosion[0], explosion[1], 0, 208, 32, 16, 16)
            pyxel.blt(explosion[0], explosion[1], 0, 224, 32, 16, 16)
            pyxel.blt(explosion[0], explosion[1], 0, 240, 32, 16, 16)
            pyxel.blt(explosion[0], explosion[1], 0, 128, 32, 16, 16)

        if points_de_victoire>=0 and points_de_victoire<8:
            pyxel.blt(16, 10, 0, 32, 184, 16, 16)
            pyxel.text(10, 10, str(points_de_victoire), 6)
        if points_de_victoire>=8 and points_de_victoire<16:
            pyxel.blt(16, 10, 0, 32, 200, 16, 16)
            pyxel.text(10, 10, str(points_de_victoire), 6)
        if points_de_victoire>=16 and points_de_victoire<25:
            pyxel.blt(16, 10, 0, 32, 216, 16, 16)        
            pyxel.text(10, 10, str(points_de_victoire), 6)
        if points_de_vie>6:
            pyxel.blt(240, 240, 0, 48, 216, 16, 16)
            pyxel.text(224, 240, str(points_de_vie), 0)
        if points_de_vie>3 and points_de_vie<=6:
            pyxel.blt(240, 240, 0, 48, 200, 16, 16)
            pyxel.text(224, 240, str(points_de_vie), 0)
        if points_de_vie>0 and points_de_vie<=3:
            pyxel.blt(240, 240, 0, 48, 184, 16, 16)
            pyxel.text(224, 240, str(points_de_vie), 0)
    else:
        pyxel.cls(5)
        pyxel.text(64, 110, 'Les Aliens ont pris la planète !', 7)
        pyxel.text(64, 120, 'La Democratie a perdu', 7)
        pyxel.text(64, 130, 'Appuyez sur R pour recommencer', 7)

pyxel.run(update, draw)
