import random
import numpy as np
from math import cos, sin, degrees, radians, atan2
from time import sleep
from enum import Enum
from asciimatics.screen import Screen
from pynput.keyboard import Key, KeyCode, Listener

class Direction(Enum):
    """
    Contains all directions the player can use to move their paddle.
    """
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
    def __init__(self, x, y, height, screen_height, normal_vector):
        self.x = x
        self.y = y
        self.height = height
        self.screen_height = screen_height
        self.normal_vector = normal_vector
        self.direction = Direction.NONE
        self.char_display = "|"
    
    def move(self):
        """
        Moves the paddle one pixel in its current direction.
        """
        new_value = self.y + self.direction.value
        if not (new_value < 0 or new_value + self.height > self.screen_height):
            self.y = new_value
    
    def point_in_boundary(self, x, y):
        """
        Checks whether a specified point xy is located inside the paddle's
        bounding box. If yes, returns True, otherwise False.
        
        Args:
            x: int, x-coordinate
            y: int, y-coordinate
        
        Returns:
            True if point is inside bounding box, False otherwise.
        """
        return (x >= self.x - 0.5
                    and x <= self.x + 0.5
                    and y >= self.y
                    and y <= self.y + self.height)

    def __repr__(self):
        return self.char_display

class Ball():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
        self.char_display = "●"
    
    def get_next_step(self):
        """
        Returns the new ball coordinates if it were to move without actually
        changing anything.
        
        Returns:
            tuple, next x and y coordinates
        """
        # Reduce vertical speed in order to keep horizontal and vertical speed
        # somewhat consistent
        new_x = self.x + self.direction[0]
        new_y = self.y + 0.6 * self.direction[1]
        return new_x, new_y
    
    def move(self):
        """
        Moves the ball along its current direction.
        """
        self.x, self.y = self.get_next_step()
    
    def reflect(self, vec):
        """
        Changes the ball's direction, reflecting it using the specified vector.
        
        Args:
            vec: np.array, used to determine new direction
        """
        new_direction = -self.direction
        new_direction = (2 * np.dot(vec, new_direction)) * vec - new_direction
        self.direction = new_direction
    
    def __repr__(self):
        return self.char_display

class PongGame():
    def __init__(self, width, height, n_bricks_col=8):
        self.paddle = Paddle(
            x=1,
            y=1,
            height=height//3,
            screen_height=height,
            normal_vector=np.array([1, 0])
        )
        self.cpu_paddle = Paddle(
            x=width-1,
            y=height-1-(height//3),
            height=height//3,
            screen_height=height,
            normal_vector=np.array([-1, 0])
        )
        self.ball = Ball(x=width//2, y=height//2)
        
        # self.boundaries
        self.screen_width = width
        self.screen_height = height
    
    def step(self):
        """
        Performs a game step, i. e.:
         - Updates positions of all entities
         - Checks for collision
         - If ball lands in either player's goal, increase score for opposing
           player and spawn a new ball
        """
        self.paddle.move()
        self.cpu_paddle.move()
        next_x, next_y = self.ball.get_next_step()
        
        # TODO: Probably could be done better ...
        hit_paddle = False
        for paddle in [self.paddle, self.cpu_paddle]:
            if not hit_paddle and paddle.point_in_boundary(next_x, next_y):
                self.ball.reflect(paddle.normal_vector)
                hit_paddle = True
        
        if not hit_paddle and (next_y < 0 or next_y > self.screen_height):
            if next_y < 0:
                self.ball.reflect(np.array([0, 1]))
            else:
                self.ball.reflect(np.array([0, -1]))
        
        self.ball.move()
    
    def print_to_screen(self, screen):
        """
        Prints all game entities to the console.
        
        Args:
            screen: asciimatics.Screen, used to print characters
        """
        for y in range(self.paddle.height):
            screen.print_at(self.paddle, self.paddle.x, self.paddle.y + y)
            screen.print_at(self.cpu_paddle, self.cpu_paddle.x, self.cpu_paddle.y + y)
        screen.print_at(self.ball, int(round(self.ball.x)), int(round(self.ball.y)))

def on_press(key):
    """
    Performs actions that should be done when user presses any key.
    
    Args:
        key: automatically passed by pynput, represents the key being pressed
    """
    global HELD_KEY
    HELD_KEY = key

def on_release(key):
    """
    Performs actions that should be done when user releases any key.
    
    Args:
        key: automatically passed by pynput, represents the key being released
    """
    global HELD_KEY
    HELD_KEY = None

def main(screen):
    """
    Main game loop, periodically executes a new game step.
    
    Args:
        screen: asciimatics.Screen, used to render characters onto the console
    """
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
