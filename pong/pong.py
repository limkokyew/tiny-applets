import random
import numpy as np
from math import cos, sin, degrees, radians, atan2
from time import sleep
from enum import Enum
from asciimatics.screen import Screen
from pynput.keyboard import Key, KeyCode, Listener

class Direction(Enum):
    NONE = 0
    UP = -1
    DOWN = 1

QUIT_KEYS = (KeyCode.from_char("q"), KeyCode.from_char("Q"))
DIRECTION_MAP = {
  KeyCode.from_char("w"): Direction.UP,
  KeyCode.from_char("s"): Direction.DOWN,
}
HELD_KEY = None

class Paddle():
    def __init__(self, x, y, height, screen_height):
        self.x = x
        self.y = y
        self.height = height
        self.screen_height = screen_height
        self.direction = Direction.NONE
        self.char_display = "|"
    
    def move(self):
        new_value = self.y + self.direction.value
        if not (new_value < 0 or new_value + self.height > self.screen_height):
            self.y = new_value

    def __repr__(self):
        return self.char_display

class Ball():
    def __init__(self, x, y, distance_per_step=1, angle=90):
        self.x = x
        self.y = y
        self.distance_per_step = distance_per_step
        self.angle = angle
        self.direction = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
        self.char_display = "●"
    
    def get_next_step(self):
        # Reduce vertical speed in order to keep horizontal and vertical speed
        # somewhat consistent
        new_x = self.x + self.direction[0]
        new_y = self.y + 0.6 * self.direction[1]
        # new_x = self.x + self.distance_per_step * cos(radians(self.angle))
        # new_y = self.y + self.distance_per_step * 0.4 * sin(radians(self.angle))
        return new_x, new_y
    
    def move(self):
        self.x, self.y = self.get_next_step()
    
    def __repr__(self):
        return self.char_display

class PongGame():
    def __init__(self, width, height, n_bricks_col=8):
        self.paddle = Paddle(x=1, y=1, height=height//3, screen_height=height)
        self.ball = Ball(x=width//2, y=height//2, angle=random.randint(0, 360))
        # self.boundaries
        self.screen_width = width
        self.screen_height = height
    
    def step(self):
        self.paddle.move()
        
        next_x, next_y = self.ball.get_next_step()
        if next_x <= self.paddle.x and next_y >= self.paddle.y and next_y <= self.paddle.y + self.paddle.height:
            normal_vector = np.array([1, 0])
            new_direction = -self.ball.direction
            new_direction = (2 * np.dot(normal_vector, new_direction)) * normal_vector - new_direction
            self.ball.direction = new_direction
        
        elif (next_y < 0 or next_y > self.screen_height):
            if next_y < 0:
                normal_vector = np.array([0, 1])
            else:
                normal_vector = np.array([0, -1])
            new_direction = -self.ball.direction
            new_direction = (2 * np.dot(normal_vector, new_direction)) * normal_vector - new_direction
            self.ball.direction = new_direction
            
        self.ball.move()
    
    def print_to_screen(self, screen):
        for y in range(self.paddle.height):
            screen.print_at(self.paddle, self.paddle.x, self.paddle.y + y)
        screen.print_at(self.ball, int(round(self.ball.x)), int(round(self.ball.y)))

def on_press(key):
    global HELD_KEY
    HELD_KEY = key

def on_release(key):
    global HELD_KEY
    HELD_KEY = None

def main(screen):
    game = PongGame(screen.width, screen.height)
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
