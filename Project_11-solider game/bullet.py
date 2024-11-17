import arcade

from constants import DIRECTION_RIGHT


class Bullet(arcade.Sprite):
    def __init__(self, file_name, scale, window):
        super().__init__(file_name, scale)
        self.window = window
        self.pain = arcade.load_sound("sounds//pain.wav")

    def update(self):
        super().update()
        if arcade.check_for_collision(self, self.window.player):
            self.window.player.health -= 1
            self.kill()
            arcade.play_sound(self.pain, 0.3)


class PlayerBullet(Bullet):
    def __init__(self, center_x, top, direction, window):
        super().__init__("bullet.png", 0.05, window)
        self.center_x = center_x+40*(1 if direction == DIRECTION_RIGHT else -1)
        self.top = top
        self.direction = direction
        if self.direction == DIRECTION_RIGHT:
            self.change_x = 5
        else:
            self.change_x = -5


class SniperBullet(Bullet):
    def __init__(self, center_x, center_y, change_x, change_y, window):
        super().__init__("bullet.png", 0.05, window)
        self.center_x = center_x+30*change_x
        self.center_y = center_y+30*change_y
        self.change_x = change_x
        self.change_y = change_y

