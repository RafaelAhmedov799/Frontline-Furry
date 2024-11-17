import arcade
from bullet import *
import time


class Sniper(arcade.Sprite):
    def __init__(self, center_x, center_y, window):
        super().__init__("sniper//sniper_forward.png")
        self.left_straight = arcade.load_texture("sniper//sniper_forward.png")
        self.right_straight = arcade.load_texture("sniper//sniper_forward.png", flipped_horizontally=True)
        self.left_down = arcade.load_texture("sniper//sniper_angle.png")
        self.right_down = arcade.load_texture("sniper//sniper_angle.png", flipped_horizontally=True)
        self.sniper_shoot = arcade.load_sound("sounds//enemy_shot.wav")
        self.last_shoot_time = time.time()
        self.coin = arcade.load_sound("sounds//coin.wav")
        self.center_x = center_x
        self.center_y = center_y
        self.window = window

    def update(self):
        super().update()
        bullets = arcade.check_for_collision_with_list(self, self.window.bullets)
        for bullet in bullets:
            bullet.kill()
            arcade.play_sound(self.coin, 0.8)
        if len(bullets) > 0:
            self.kill()
        if self.center_x > self.window.player.center_x:
            if self.center_y > self.window.player.center_y:
                self.texture = self.left_down
                dx = -2
                dy = -2
            else:
                self.texture = self.left_straight
                dx = -2
                dy = 0
        else:
            if self.center_y > self.window.player.center_y:
                self.texture = self.right_down
                dx = 2
                dy = -2
            else:
                self.texture = self.right_straight
                dx = 2
                dy = 0
        if time.time() - self.last_shoot_time > 2:
            self.window.bullets.append(SniperBullet(self.center_x, self.center_y, dx, dy, self.window))
            arcade.play_sound(self.sniper_shoot, 0.4)
            self.last_shoot_time = time.time()


