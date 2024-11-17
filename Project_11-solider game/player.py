import arcade

from bullet import PlayerBullet
from constants import DIRECTION_RIGHT, DIRECTION_LEFT
from animated import Animated


class Player(Animated):
    def __init__(self, window):
        super().__init__("go_bill/0.gif", 3)
        self.right_textures = []
        self.left_textures = []
        self.direction = DIRECTION_RIGHT
        self.is_walking = False
        self.pain = arcade.load_sound("sounds//pain.wav")
        self.window = window
        self.health = 3
        self.still_right_texture = arcade.load_texture("go_bill/0.gif")
        self.still_left_texture = arcade.load_texture("go_bill/0.gif", flipped_horizontally=True)
        self.is_crawling = False
        self.crawling_right_texture = arcade.load_texture("bill_textures/BillLayingDown.png")
        self.crawling_left_texture = arcade.load_texture("bill_textures/BillLayingDown.png", flipped_horizontally=True)
        for i in range(0, 6):
            self.right_textures.append(arcade.load_texture(f"go_bill/{i}.gif"))
            self.left_textures.append(arcade.load_texture(f"go_bill/{i}.gif", flipped_horizontally=True))

    def update(self):
        super().update()
        if self.direction == DIRECTION_LEFT:
            self.textures = self.left_textures
        else:
            self.textures = self.right_textures
        hit_runmen = arcade.check_for_collision_with_list(self, self.window.runmen)
        for runman in hit_runmen:
            runman.kill()
            self.health -= 1
            arcade.play_sound(self.pain, 0.2)

    def update_animation(self, delta_time):
        if self.is_walking:
            super().update_animation(delta_time)
        else:
            if self.direction == DIRECTION_RIGHT:
                self.texture = self.still_right_texture
            else:
                self.texture = self.still_left_texture
        if self.is_crawling:
            if self.direction == DIRECTION_RIGHT:
                self.texture = self.crawling_right_texture
            else:
                self.texture = self.crawling_left_texture

    def shoot(self):
        if not self.is_crawling:
            top_ = self.top - 10
        else:
            top_ = self.top - 60
        self.window.bullets.append(PlayerBullet(self.center_x, top_, self.direction, self.window))



