import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120)
        self.x = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        self.x = (self.x + 1) % pyxel.width
        if not self.is_game_over:
            self.elapsed_time = (pyxel.frame_count - self.start_time) // 30
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
            if pyxel.btnp(pyxel.KEY_R):
                self.reset()
    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.x, 0, 8, 8, 9)

    def __init__(self):
        pyxel.init(160, 120, title="Dino Game")
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.start_time = pyxel.frame_count
        self.elapsed_time = 0
        self.is_game_over = False


 

    def draw(self):

        pyxel.cls(0)

        if not self.is_game_over:

            pyxel.text(5, 5, f"Time: {self.elapsed_time} s", 7)

        else:

            pyxel.text(50, 50, "Game Over!", pyxel.frame_count % 16)

            pyxel.text(40, 60, "Press R to Restart", 7)

App()