import numpy as np
import random
from time import sleep
from enum import Enum
from asciimatics.screen import Screen

class Direction(Enum):
    """
    Enum for each of the four directions.
    """
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)

WALL_CHARACTER = "█"
QUIT_KEYS = (ord("q"), ord("Q"))
DIRECTION_MAP = {
  ord("a"): Direction.LEFT,
  ord("d"): Direction.RIGHT,
  ord("w"): Direction.UP,
  ord("s"): Direction.DOWN
}

class Snake():
    """
    Represents the main entity of this game, the snake. It moves around and
    attempts to eat fruit while avoiding walls and itself.
    """
    def __init__(self, head, direction, n_parts):
        self.head = head
        self.direction = direction
        self.has_eaten_fruit = False
        self.coordinates = set()
        # self.coordinates.add(tuple(self.head.coords))
        
        # Initialize snake body
        prev_element = self.head
        for _ in range(n_parts):
            prev_coords = np.add(prev_element.coords, Direction.LEFT.value)
            prev_element.prev = SnakeBody(prev_coords)
            prev_element.prev.next_e = prev_element
            
            self.coordinates.add(tuple(prev_coords))
            prev_element = prev_element.prev
        
        self.tail = prev_element
    
    def push(self) -> None:
        """
        Creates a new head in the direction the snake is currently heading.
        """
        new_head_coords = np.add(self.head.coords, self.direction.value)
        new_head = SnakeBody((new_head_coords[0], new_head_coords[1]), self.head)
        self.coordinates.add(tuple(self.head.coords))
        self.head.next_e = new_head
        self.head = new_head
        # self.coordinates.add(tuple(new_head_coords))

    def pop(self) -> None:
        """
        Removes the first element from the snake's tail.
        """
        self.coordinates.remove(tuple(self.tail.coords))
        self.tail = self.tail.next_e
    
    def step(self) -> None:
        """
        Go one square to the currently set direction.
        """
        self.push()
        if not self.has_eaten_fruit:
            self.pop()
        else:
            self.has_eaten_fruit = False
        # tmp_coords = self.head.coords
        # self.head.coords = np.add(self.head.coords, self.direction.value)
        # prev_element = self.head.prev
        # while prev_element is not None:
        #     prev_element.coords = tmp_coords
        #     tmp_coords = prev_element.coords
        #     prev_element = prev_element.prev

class SnakeBody():
    """
    Represents a piece of the snake's body. Each body part contains a reference
    to its previous and next part.
    """
    def __init__(self, coords, prev=None, next_e=None):
        self.coords = coords
        self.prev = prev
        self.next_e = next_e

class Fruit():
    """
    Fruit is a consumable item that the snake actively seeks out in order to
    gain points.
    """
    def __init__(self, coords):
        self.coords = coords
    
    def __repr__(self):
        return "⓿"

class SnakeGame():
    """
    SnakeGame contains all game entities and is primarily responsible for
    coordinating interactions between the entities.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.game_over = False
        self.score = 0
        
        self.vertical_wall = set()
        self.vertical_wall.update((0, y) for y in range(height))
        self.vertical_wall.update((width-1, y) for y in range(height))
        self.horizontal_wall = WALL_CHARACTER * width
        
        self.snake = Snake(
            SnakeBody(np.array((width // 2, height // 2))), Direction.RIGHT, 20
        )
        self.fruit = self.generate_fruit()
    
    def step(self) -> None:
        """
        Advances the game state by one step.
        """
        self.snake.step()
        self.check_collision()
    
    def check_collision(self) -> None:
        """
        Check whether the snake head has collided with something. It is not
        necessary to check for other colliding entities due to the snake head
        being the only thing that moves.
        
        The body parts simply follow the head's previous positions, rendering
        it unnecessary to check for collisions there.
        """
        x, y = self.snake.head.coords
        
        # Check whether the head collided with a wall
        if (x <= 1 or x >= self.width - 1) or (y <= 1 or y >= self.height - 1):
            self.exit_game("Oh no - you've collided with a wall!")
        
        # Check whether the head collided with a fruit
        if self.fruit is not None and self.snake.head.coords == self.fruit.coords:
            self.snake.has_eaten_fruit = True
            self.fruit = self.generate_fruit()
            self.score += 10
        
        # Check whether the head has collided with its body
        if self.snake.head.coords in self.snake.coordinates:
            self.exit_game("Oh no - you've collided with your own body!")
    
    def generate_fruit(self) -> Fruit:
        """
        Generates a new fruit in a random, currently unoccupied location.
        """
        head_set = set()
        head_set.add(tuple(self.snake.head.coords))
        invalid_coordinates = self.snake.coordinates.union(head_set)
        
        while (fruit_coords := (
            random.randint(2, self.width-2), random.randint(2, self.height-2)
        )) not in invalid_coordinates:
            return Fruit(fruit_coords)

    def set_snake_direction(self, direction) -> None:
        """
        Changes the snake's direction. The snake cannot switch to a direction
        opposite of its current direction, e. g. going from left to right is not
        possible.
        
        Args:
            direction, Direction the snake should be facing
        """
        if tuple(-np.array(direction.value)) != self.snake.direction.value:
            self.snake.direction = direction

    def print_to_screen(self, screen) -> None:
        """
        Prints all game entities to the console.
        
        Args:
            screen: Screen, console window
        """
        screen.print_at(self.horizontal_wall, 0, 0)
        screen.print_at(self.horizontal_wall, 0, self.height - 1)
        for wall_coords in self.vertical_wall:
            screen.print_at(WALL_CHARACTER, wall_coords[0], wall_coords[1])
        
        for snake_coord in self.snake.coordinates:
            screen.print_at("█", snake_coord[0], snake_coord[1])
        
        if self.fruit:
            screen.print_at(self.fruit, self.fruit.coords[0], self.fruit.coords[1])

    def exit_game(self, msg) -> None:
        """
        Sets the game_over variable to True, prompting the game loop to exit.
        
        Args:
            msg: str, printed before showing the final score. Should ideally
                 describe why the player lost.
        """
        self.game_over = True
        print(msg)
        print(f"Nice try! You've scored {self.score} points in this session.")

def main(screen) -> None:
    """
    Starts the snake game.
    
    Args:
        screen: Screen, console window
    """
    game = SnakeGame(screen.width, screen.height)
    while not game.game_over:
        screen.clear_buffer(0, 1, 0)
        game.step()
        game.print_to_screen(screen)
        
        # Read input and change direction if possible
        ev = screen.get_key()
        if ev in DIRECTION_MAP:
            game.set_snake_direction(DIRECTION_MAP[ev])
        if ev in QUIT_KEYS:
            return
        
        screen.refresh()
        sleep(0.08)

if __name__ == "__main__":
    Screen.wrapper(main)
