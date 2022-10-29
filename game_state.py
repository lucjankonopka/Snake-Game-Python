from direction import Direction
from position import Position
from random import randint

INITIAL_SNAKE = [
    Position(2, 3),
    Position(3, 3),
    Position(4, 3)
]
INITIAL_DIRECTION = Direction.RIGHT
INITIAL_POINTS = 0
INITIAL_SPEED=10
RUNNING, PAUSED, GAMEOVER = "RUNNING", "PAUSED", "GAMEOVER"

class GameState:
    def __init__(self, snake=None, direction=INITIAL_DIRECTION, food=None, field_size=20, points=INITIAL_POINTS, speed=INITIAL_SPEED, set_status=RUNNING):
        if snake is None:
            snake = INITIAL_SNAKE[:]

        self.snake = snake
        self.direction = direction
        self.field_size = field_size
        self.points = points
        self.speed = speed
        self.set_status = set_status

        if food == None:
            self.set_new_random_food_position()
        else:
            self.food = food

    def set_initial_position(self):
        self.snake = INITIAL_SNAKE[:]
        self.direction = INITIAL_DIRECTION
        self.set_new_random_food_position()
        self.points = INITIAL_POINTS
        self.speed = INITIAL_SPEED

    def new_game(self):
        set_status = RUNNING
        self.set_initial_position()
        return set_status


    def next_head(self, direction):
        pos = self.snake[-1]
        if direction == Direction.UP:
            return Position(pos.x, (pos.y - 1) % self.field_size)
        elif direction == Direction.DOWN:
            return Position(pos.x, (pos.y + 1) % self.field_size)
        elif direction == Direction.RIGHT:
            return Position((pos.x + 1) % self.field_size, pos.y)
        elif direction == Direction.LEFT:
            return Position((pos.x - 1) % self.field_size, pos.y)

    def set_new_random_food_position(self):
        self.food = Position(
            randint(0, self.field_size - 1),
            randint(1, self.field_size - 1)
        )
        if self.food in self.snake:
            self.set_new_random_food_position()

    def can_snake_turn(self, direction):
        new_head = self.next_head(direction)
        return new_head != self.snake[-2]

    def snake_turn(self, direction):
        if self.can_snake_turn(direction):
            self.direction = direction

    def step(self):
        new_head = self.next_head(self.direction)

        collision = new_head in self.snake
        if collision:
            self.set_status = GAMEOVER
            return 

        self.snake.append(new_head)
        if new_head == self.food:
            self.set_new_random_food_position()
            self.points += 1
            self.speed += 1/2
        else:
            self.snake = self.snake[1:]

