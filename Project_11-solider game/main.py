import time

import arcade

from coords import COORDS
from sniper_coords import SNIPER_COORDS
from player import *
from bullet import *
from sniper import *
from runman import *
from runmen_coords import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Shooter Game"


class Platform(arcade.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__("line.png")
        self.center_y = center_y
        self.center_x = center_x


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bgs = []
        for i in range(1,16):
            self.bgs.append(arcade.load_texture(f"background/Map{i}.png"))
        self.level_i = 0
        self.player = Player(self)
        self.platforms = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.snipers = arcade.SpriteList()
        self.shoot_s = arcade.load_sound("sounds//shoot.wav")
        self.jump_s = arcade.load_sound("sounds//jump.wav")
        self.main_s = arcade.load_sound("sounds//main_theme.mp3")
        self.pain = arcade.load_sound("sounds//pain.wav")
        self.coin = arcade.load_sound("sounds//coin.wav")
        self.sniper_shoot = arcade.load_sound("sounds//enemy_shot.wav")
        self.runmen = arcade.SpriteList()
        self.coords = ""
        self.runmen_engines = []
        self.last_level_time = None
        self.setup()
        self.engine = arcade.PhysicsEnginePlatformer(self.player, self.platforms, 0.5)
        self.to_be_continued_texture = arcade.load_texture("endgame.png")
        self.game = True
        self.game_over_texture = arcade.load_texture("game_over.jpg")
        self.heart_texture = arcade.load_texture("6-pixel-heart-4.png")
        self.time = 0

    def setup(self):
        arcade.play_sound(self.main_s, 0.2, looping=True)
        self.player.center_x = 150
        self.player.bottom = 50
        for i in range(9):
            self.platforms.append(Platform(100*i, 50))
        self.append_platforms(COORDS[self.level_i])
        for sniper in SNIPER_COORDS[self.level_i]:
            self.snipers.append(Sniper(sniper[0], sniper[1], self))
        self.append_runmen(self.level_i)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bgs[self.level_i])
        self.player.draw()
        #self.platforms.draw()
        self.bullets.draw()
        self.snipers.draw()
        self.runmen.draw()
        #arcade.draw_text(self.coords, SCREEN_WIDTH/2, 0, arcade.color.BLACK, anchor_x="center", anchor_y="bottom")
        if self.player.health <= 0:
            arcade.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT, self.game_over_texture)
        for i in range(self.player.health):
            arcade.draw_texture_rectangle(25+334*0.1*i, SCREEN_HEIGHT-20, 334*0.1, 334*0.1, self.heart_texture)
        if self.last_level_time != None and time.time() - self.last_level_time > 3:
            arcade.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT, self.to_be_continued_texture)

    def switch_platforms(self, current, next):
        for i in range(len(COORDS[current])):
            self.platforms.pop()
        self.append_platforms(COORDS[next])

    def append_platforms(self, platforms):
        for platform in platforms:
            self.platforms.append(Platform(platform[0], platform[1]))

    def switch_right(self):
        if self.level_i == len(self.bgs) - 1:
            self.player.right = SCREEN_WIDTH
            return
        self.switch_platforms(self.level_i, self.level_i+1)
        self.switch_snipers_and_runmen(self.level_i + 1)
        self.level_i += 1
        self.player.left = 0
        if self.level_i == len(self.bgs) - 1:
            self.last_level_time = time.time()

    def switch_left(self):
        if self.level_i == 0:
            self.player.left = 0
            return
        self.switch_platforms(self.level_i, self.level_i-1)
        self.switch_snipers_and_runmen(self.level_i - 1)
        self.level_i -= 1
        self.player.right = SCREEN_WIDTH

    def switch_snipers_and_runmen(self, next):
        self.snipers.clear()
        self.runmen.clear()
        for sniper_coords in SNIPER_COORDS[next]:
            self.snipers.append(Sniper(sniper_coords[0], sniper_coords[1], self))
        self.append_runmen(next)

    def append_runmen(self, next):
        for runman_coords in RUNMEN_COORDS[next]:
            runman = Runman(runman_coords[0], runman_coords[1], self)
            self.runmen.append(runman)
            self.runmen_engines.append(arcade.PhysicsEnginePlatformer(runman, self.platforms, 0.5))

    def update(self, delta_time):
        if self.game:
                self.player.update()
                self.player.update_animation(delta_time)
                self.engine.update()
                self.bullets.update()
                self.snipers.update()
                self.runmen.update()
                self.runmen.update_animation(delta_time)
                for engine in self.runmen_engines:
                    engine.update()
                if self.player.left > SCREEN_WIDTH:
                    self.switch_right()
                if self.player.left < 0:
                    self.switch_left()
                if self.player.health <= 0:
                    self.game = False
                if self.last_level_time != None and time.time() - self.last_level_time > 3:
                    self.game = False

    def on_key_press(self, symbol: int, modifiers: int):
        if self.game:
            if symbol == arcade.key.LEFT:
                self.player.direction = DIRECTION_LEFT
                if not self.player.is_crawling:
                    self.player.change_x = -1
                    self.player.is_walking = True
            if symbol == arcade.key.RIGHT:
                self.player.direction = DIRECTION_RIGHT
                if not self.player.is_crawling:
                    self.player.change_x = 1
                    self.player.is_walking = True
            if symbol == arcade.key.UP:
                if self.engine.can_jump():
                    self.engine.jump(10)
                    arcade.play_sound(self.jump_s, 0.8)
            if symbol == arcade.key.DOWN:
                self.player.is_crawling = True
                self.player.change_x = 0
            if symbol == arcade.key.SPACE:
                self.player.shoot()
                arcade.play_sound(self.shoot_s, 0.8)

    def on_key_release(self, symbol: int, modifiers: int):
        if self.game:
            if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
                self.player.change_x = 0
                self.player.is_walking = False
            if symbol == arcade.key.DOWN:
                self.player.is_crawling = False

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.coords = f"{x}, {y}"


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()