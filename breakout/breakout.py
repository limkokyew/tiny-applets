import numpy as np
from math import cos, sin, degrees, radians, atan2
from time import sleep
from enum import Enum
from asciimatics.screen import Screen
from pynput.keyboard import Key, KeyCode, Listener

class Direction(Enum):
    NONE = 0
    LEFT = -1
    RIGHT = 1
    
QUIT_KEYS = (KeyCode.from_char("q"), KeyCode.from_char("Q"))
DIRECTION_MAP = {
  KeyCode.from_char("a"): Direction.LEFT,
  KeyCode.from_char("d"): Direction.RIGHT,
}
HELD_KEY = None

class Paddle():
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.screen_width = (width * 6) - 1
        self.direction = Direction.NONE
        self.char_display = "▬" * width
    
    def move(self):
        new_value = self.x + self.direction.value
        if not(new_value < 1 or new_value + self.width > self.screen_width):
            self.x = new_value

    def __repr__(self):
        return self.char_display

class Ball():
    def __init__(self, x, y, distance_per_step=1, angle=90):
        self.x = x
        self.y = y
        self.distance_per_step = distance_per_step
        self.angle = angle
        self.char_display = "●"
    
    def get_next_step(self):
        # Reduce vertical speed in order to keep horizontal and vertical speed
        # somewhat consistent
        new_x = self.x + self.distance_per_step * cos(radians(self.angle))
        new_y = self.y + self.distance_per_step * 0.4 * sin(radians(self.angle))
        return new_x, new_y
    
    def move(self):
        self.x, self.y = self.get_next_step()
        if (self.y < 0):
            self.angle = 90
    
    def __repr__(self):
        return self.char_display

class Brick():
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.char_display = "■" * width
    
    def __repr__(self):
        return self.char_display

class BreakoutGame():
    def __init__(self, width, height, n_bricks_col=8):
        self.paddle = Paddle(x=(width // 2) - 2, y=height - 5, width=width // 6)
        self.ball = Ball(x=width // 2, y=10)
        
        # Vertical walls to the left and right
        # self.walls = 
        
        self.bricks = []
        brick_width = width // n_bricks_col
        for y in range(5):
            for x in range(0, width, brick_width+1):
                self.bricks.append(Brick(x, y, brick_width))
    
    def step(self):
        self.paddle.move()
        
        next_x, next_y = self.ball.get_next_step()
        if ((next_x >= self.paddle.x and next_x <= self.paddle.x + self.paddle.width) and
           (next_y >= self.paddle.y and next_y <= self.paddle.y + 1)):
           # Calculate the angle between ball and paddle as if the center of the
           # paddle is lower than it actually is - this ensures that resulting
           # angles do not change too much even with tiny changes
           self.ball.angle = degrees(atan2(
               self.ball.y - (self.paddle.y + 5),
               self.ball.x - (self.paddle.x + (self.paddle.width // 2))
           ))
        self.ball.move()
    
    def print_to_screen(self, screen):
        screen.print_at(self.paddle, self.paddle.x, self.paddle.y)
        for brick in self.bricks:
            screen.print_at(brick, brick.x, brick.y)
        screen.print_at(self.ball, int(round(self.ball.x)), int(round(self.ball.y)))

def on_press(key):
    global HELD_KEY
    HELD_KEY = key

def on_release(key):
    global HELD_KEY
    HELD_KEY = None

def main(screen):
    game = BreakoutGame(screen.width, screen.height)
    listener = Listener(
        on_press=on_press,
        on_release=on_release
    )
    listener.start()
    while True:
        screen.clear_buffer(1, 1, 0)
        
        # screen.print_at(game.paddle, game.paddle.x, screen.height - 5)
        game.step()
        game.print_to_screen(screen)
        
        # While key inputs are being handled by pynput already, we still need
        # to call get_key() in order to prevent inputs being written to the
        # console once the game ends
        screen.get_key()
        if HELD_KEY in DIRECTION_MAP:
            game.paddle.direction = DIRECTION_MAP[HELD_KEY]
        elif HELD_KEY in QUIT_KEYS:
            return
        else:
            game.paddle.direction = Direction.NONE
        
        screen.refresh()
        sleep(0.02)

if __name__ == "__main__":
    Screen.wrapper(main)
