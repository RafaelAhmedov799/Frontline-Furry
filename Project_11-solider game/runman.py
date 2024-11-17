import arcade

from constants import DIRECTION_RIGHT, DIRECTION_LEFT
from animated import Animated


class Runman(Animated):
    def __init__(self, center_x, center_y, window):
        super().__init__("runman/frame-01.gif", 3)
        self.right_textures = []
        self.left_textures = []
        self.direction = DIRECTION_RIGHT
        self.is_walking = False
        self.center_x = center_x
        self.center_y = center_y
        self.window = window
        self.coin = arcade.load_sound("sounds//coin.wav")
        for i in range(1, 10):
            self.left_textures.append(arcade.load_texture(f"runman/frame-0{i}.gif"))
            self.right_textures.append(arcade.load_texture(f"runman/frame-0{i}.gif", flipped_horizontally=True))

    def update(self):
        super().update()
        if self.direction == DIRECTION_LEFT:
            self.textures = self.left_textures
            self.change_x = -1
        else:
            self.textures = self.right_textures
            self.change_x = 1
        hit = arcade.check_for_collision_with_list(self, self.window.bullets)
        if hit:
            self.kill()
            arcade.play_sound(self.coin, 0.8)
        if self.center_x > self.window.player.center_x:
            self.direction = DIRECTION_LEFT
        else:
            self.direction = DIRECTION_RIGHT
