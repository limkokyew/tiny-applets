import numpy as np
from time import sleep
from enum import Enum
from asciimatics.screen import Screen

class Direction(Enum):
    LEFT = {"key": "a", "offset": (-1, 0)}
    RIGHT = {"key": "d", "offset": (1, 0)}
    UP = {"key": "w", "offset": (0, -1)}
    DOWN = {"key": "s", "offset": (0, 1)}
    
QUIT_KEYS = (ord("q"), ord("Q"))
DIRECTION_MAP = {
  ord("a"): Direction.LEFT,
  ord("d"): Direction.RIGHT,
  ord("w"): Direction.UP,
  ord("s"): Direction.DOWN
}

class Snake():
    def __init__(self, head, direction, n_parts):
        self.head = head
        self.direction = direction
        self.coordinates = set()
        self.coordinates.add(tuple(self.head.coords))
        
        # Initialize snake body
        prev_element = self.head
        for _ in range(n_parts):
            prev_coords = np.add(prev_element.coords, Direction.LEFT.value["offset"])
            prev_element.prev = SnakeBody(prev_coords)
            prev_element.prev.next_e = prev_element
            
            self.coordinates.add(tuple(prev_coords))
            prev_element = prev_element.prev
        
        self.tail = prev_element
    
    def push(self):
        """
        Creates a new head in the direction the snake is currently heading.
        """
        new_head_coords = np.add(self.head.coords, self.direction.value["offset"])
        new_head = SnakeBody((new_head_coords[0], new_head_coords[1]), self.head)
        self.head.next_e = new_head
        self.head = new_head
        self.coordinates.add(tuple(new_head_coords))

    def pop(self):
        """
        Removes the first element from the snake's tail.
        """
        self.coordinates.remove(tuple(self.tail.coords))
        self.tail = self.tail.next_e
    
    def step(self):
        """
        Go one square to the currently set direction.
        """
        self.push()
        self.pop()
        # tmp_coords = self.head.coords
        # self.head.coords = np.add(self.head.coords, self.direction.value["offset"])
        # prev_element = self.head.prev
        # while prev_element is not None:
        #     prev_element.coords = tmp_coords
        #     tmp_coords = prev_element.coords
        #     prev_element = prev_element.prev

class SnakeBody():
    def __init__(self, coords, prev=None, next_e=None):
        self.coords = coords
        self.prev = prev
        self.next_e = next_e

def initialize_game(width, height):
    """
    Initializes the snake game for a window of the specified width and height.
    
    Args:
        width: int, width of console
        height: int, height of console
    """
    wall_coords = set()
    wall_coords.update((x, 0) for x in range(width))
    wall_coords.update((x, height-1) for x in range(width))
    wall_coords.update((0, y) for y in range(height))
    wall_coords.update((width-1, y) for y in range(height))
    
    snake = Snake(
        SnakeBody(np.array((width // 2, height // 2))), Direction.RIGHT, 3
    )
    
    return snake, wall_coords

def main(screen):
    snake, wall_coords = initialize_game(screen.width, screen.height)
    while True:
        for wall_coord in wall_coords:
            screen.print_at("█", wall_coord[0], wall_coord[1])
        for snake_coord in snake.coordinates:
            screen.print_at("■", snake_coord[0], snake_coord[1])
        snake.step()
        ev = screen.get_key()
        if ev in DIRECTION_MAP:
            snake.direction = DIRECTION_MAP[ev]
        if ev in QUIT_KEYS:
            return
        screen.refresh()
        screen.clear_buffer(0, 1, 0)
        sleep(0.1)

if __name__ == "__main__":
    Screen.wrapper(main)
