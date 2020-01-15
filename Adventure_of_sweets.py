import pyxel
from random import randint


class App:

 ###################
 ##Initial setting##
 ###################

    def __init__(self):

        pyxel.init(96, 150, caption="Adventure of sweets", fps=15, scale=5)
        pyxel.load("../assets/gannbaru.pyxel")
        pyxel.image(1).load(0, 0, "../assets/abcd.png")

        self.first()

        pyxel.run(self.update, self.draw)

    def first(self):
        self.hp = 3
        self.score = 0
        self.player_x = 40
        self.player_y = 15
        self.t_l = 0
        self.t_r = 0
        self.frame_x = 14
        self.frame_y = 48
        self.sweets_num = 0
        self.floor = [(0, 500, (100 + 60 * i), randint(0, 6), True, True)
                      for i in range(4)]

        self.draw_C_select = False
        self.is_OP = True
        self.player_is_alive = True
        self.player_is_invincible = True
        self.numeber_count = True
        self.is_game_over = False

 ############
 ###updata###
 ############

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R):
            self.score = 0
            self.first()

        if self.hp == 0:
            self.is_game_over = True

        if self.is_OP:
            if pyxel.btn(pyxel.constants.KEY_S):
                self.draw_C()
                self.is_OP = False
                self.draw_C_select = True
            return

        if self.draw_C_select:
            self.Chara_S()
            if pyxel.btn(pyxel.constants.KEY_A):
                self.draw()
                self.draw_C_select = False
            return

        if self.is_game_over:
            if pyxel.btn(pyxel.constants.KEY_Q):
                pyxel.quit()
            if pyxel.btn(pyxel.constants.KEY_R):
                self.first()
            return

        self.update_player()

        for i, v in enumerate(self.floor):
            self.floor[i] = self.update_floor_check(*v)

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            self.t_l = self.t_l + 1
        if self.t_l == 1:
            self.player_x = max(self.player_x - 32, 8)
            self.t_l = 0
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            self.t_r = self.t_r + 1
        if self.t_r == 1:
            self.player_x = min(self.player_x + 32, pyxel.width - 24)
            self.t_r = 0

    def update_floor_check(self, x, x_one, y, num, is_active, is_active_two):
        #x, x_one, y
        x_one = 500
        if num == 0:
            x = 32
        if 1 <= num <= 3:
            if num == 1:
                x = 0
            if num == 2:
                x = 32
            if num == 3:
                x = 64
        if 4 <= num <= 6:
            if num == 4:
                x = 0
                x_one = 32
            if num == 5:
                x = 32
                x_one = 64
            if num == 6:
                x = 0
                x_one = 64

        # stage_checker
        if self.player_is_invincible:
            if is_active:
                if (
                    self.player_x + 16 >= x
                    and self.player_x <= x + 32
                    and self.player_y + 16 >= y
                    and self.player_y <= y + 16
                ):
                    is_active = False
                    self.player_is_invincible = False
                    self.hp = self.hp - 1

            if is_active_two:
                if (
                    self.player_x + 16 >= x_one
                    and self.player_x <= x_one + 32
                    and self.player_y + 16 >= y
                    and self.player_y <= y + 16
                ):
                    is_active_two = False
                    self.player_is_invincible = False
                    self.hp = self.hp - 1
            else:
                y -= 0

        y -= 4

        if y < -16:
            y += 240
            is_active = True
            is_active_two = True
            self.numeber_count = True
            num = randint(0, 6)

        return (x, x_one, y, num, is_active, is_active_two)

    def Chara_S(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            self.frame_x = max(self.frame_x - 25, 14)

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            self.frame_x = min(self.frame_x + 25, 64)

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
            self.frame_y = min(self.frame_y + 20, 68)

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):
            self.frame_y = max(self.frame_y - 20, 48)

        if (self.frame_x == 14 and self.frame_y == 48):
            self.sweets_num = 0

        if (self.frame_x == 39 and self.frame_y == 48):
            self.sweets_num = 1

        if (self.frame_x == 64 and self.frame_y == 48):
            self.sweets_num = 2

        if (self.frame_x == 14 and self.frame_y == 68):
            self.sweets_num = 3

        if (self.frame_x == 39 and self.frame_y == 68):
            self.sweets_num = 4

        if (self.frame_x == 64 and self.frame_y == 68):
            self.sweets_num = 5

#        print(self.sweets_num)

  ##########
  ###draw###
  ##########

    def draw(self):
        if self.is_OP:
            self.draw_OP()
            return

        if self.draw_C_select:
            self.draw_C()
            return

        if self.is_game_over:
            self.draw_crash_screen()
            return

        pyxel.cls(12)

        if not self.is_game_over:
            if (pyxel.frame_count % 12) == 0:
                self.score += 10

        # draw player
        if self.player_is_invincible:
            if self.sweets_num == 0:
                pyxel.blt(self.player_x, self.player_y, 0, 16, 16, 16, 16, 12)

            if self.sweets_num == 1:
                pyxel.blt(self.player_x, self.player_y, 0, 0, 16, 16, 16, 12)

            if self.sweets_num == 2:
                pyxel.blt(self.player_x, self.player_y, 0, 16, 0, 16, 16, 12)

            if self.sweets_num == 3:
                pyxel.blt(self.player_x, self.player_y, 0, 0, 0, 16, 16, 6)

            if self.sweets_num == 4:
                pyxel.blt(self.player_x, self.player_y, 0, 32, 16, 16, 16, 12)

            if self.sweets_num == 5:
                pyxel.blt(self.player_x, self.player_y, 0, 32, 0, 16, 16, 12)

        else:
            t = pyxel.frame_count
            t = 0
            i = 0
            i = i + i
            while t > 100:
                while t > t + 20:
                    pyxel.blt(self.player_x, self.player_y, 0, 0, 0, 16, 16, 6)
                while t > t + 20:
                    pyxel.blt(self.player_x, self.player_y, 0, 32, 48, 16, 16)

            self.player_is_invincible = True

        # draw stage
        for x, x_one, y, num, is_active, is_active_two in self.floor:
            #            print(num)
            if num == 0:
                pyxel.blt(32, y, 0, 0, 48, 32, 16, 12)

            if 1 <= num <= 3:
                if num == 1:
                    pyxel.blt(0, y, 0, 0, 48, 32, 16, 12)

                if num == 2:
                    pyxel.blt(32, y, 0, 0, 48, 32, 16, 12)

                if num == 3:
                    pyxel.blt(64, y, 0, 0, 48, 32, 16, 12)

            elif 4 <= num <= 6:

                if num == 4:
                    pyxel.blt(0, y, 0, 0, 48, 32, 16, 12)
                    pyxel.blt(32, y, 0, 0, 48, 32, 16, 12)

                if num == 5:
                    pyxel.blt(32, y, 0, 0, 48, 32, 16, 12)
                    pyxel.blt(64, y, 0, 0, 48, 32, 16, 12)

                if num == 6:
                    pyxel.blt(0, y, 0, 0, 48, 32, 16, 12)
                    pyxel.blt(64, y, 0, 0, 48, 32, 16, 12)

        # draw HP
        for i in range(self.hp):
            pyxel.blt(2, i * 16, 0, 0, 64, 16, 16, 12,)

        # draw score
        s = "SCORE {:>4}".format(self.score)
        pyxel.text(51, 4, s, 1)
        pyxel.text(50, 4, s, 7)

    def draw_crash_screen(self):
        pyxel.cls(3)
        pyxel.text(32, 50, "R: restart", 6)
        pyxel.text(32, 60, "Q: quit", 8)
        pyxel.text(25, 70, "SCORE:", 9)
        pyxel.text(55, 70, str(self.score), 7)

    def draw_OP(self):
        pyxel.cls(5)
        pyxel.text(33, 90, "S: START", 1)
        pyxel.text(32, 90, "S: START", 7)
        pyxel.blt(5, 0, 1, 0, 0, 90, 100, 1)

    def draw_C(self):
        pyxel.cls(4)
        pyxel.rectb(self.frame_x, self.frame_y, self.frame_x +
                    17, self.frame_y+18, pyxel.frame_count & 10)
        pyxel.text(25, 30, "SELECT SWEETS", 1)
        pyxel.text(24, 30, "SELECT SWEETS", 7)
        pyxel.text(33, 90, "A: START", 1)
        pyxel.text(32, 90, "A: START", 7)
        pyxel.blt(15, 50, 0, 16, 16, 16, 16, 12)  # sweets_num=0
        pyxel.blt(40, 50, 0, 0, 16, 16, 16, 12)  # sweeets_num=1
        pyxel.blt(65, 50, 0, 16, 0, 16, 16, 12)  # sweets_num=2
        pyxel.blt(15, 70, 0, 0, 0, 16, 16, 6)  # sweets_num=3
        pyxel.blt(40, 70, 0, 32, 16, 16, 16, 12)  # sweets_num=4
        pyxel.blt(65, 70, 0, 32, 0, 16, 16, 12)  # sweets_num=5
        if self.sweets_num == 0:
            pyxel.text(26, 120, "STICK CANDY", 1)
            pyxel.text(25, 120, "STICK CANDY", 7)
        if self.sweets_num == 1:
            pyxel.text(25, 120, "RICE CRACKER", 1)
            pyxel.text(24, 120, "RICE CRACKER", 7)
        if self.sweets_num == 2:
            pyxel.text(30, 120, "ICE CREAM", 1)
            pyxel.text(29, 120, "ICE CREAM", 7)
        if self.sweets_num == 3:
            pyxel.text(30, 120, "ICE CANDY", 1)
            pyxel.text(29, 120, "ICE CANDY", 7)
        if self.sweets_num == 4:
            pyxel.text(38, 120, "CANDY", 1)
            pyxel.text(37, 120, "CANDY", 7)
        if self.sweets_num == 5:
            pyxel.text(30, 120, "SOFT CREAM", 1)
            pyxel.text(29, 120, "SOFT CREAM", 7)


App()
