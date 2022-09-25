import pygame
from position import Position
from direction import Direction
from game_state import GameState
import random

pygame.init()

CUBE_SIZE = 32
CUBES_NUM = 20
WIDTH = CUBE_SIZE * CUBES_NUM
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Snake Game by Lucjan Konopka")

GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
SNAKE_COLOR = (0, 153, 51)


pygame.display.update()

snake = [
    Position(2, 2),
    Position(3, 2),
    Position(4, 2)
]

food = Position(19, 19)

state = GameState(
    snake=None,
    direction=Direction.RIGHT,
    food=None,
    field_size=CUBES_NUM,
    points=0
)

actual_score = state.points
actual_direction = state.direction


def draw_snake_part(pos):
    position = (pos.x * CUBE_SIZE, pos.y * CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
    pygame.draw.rect(screen, SNAKE_COLOR, position)


def draw_snake_head(pos, actual_direction):
    head_position = (pos.x * CUBE_SIZE, pos.y *
                     CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
    eye_radius = CUBE_SIZE/4
    pupil_radius = CUBE_SIZE/8
    pupil_shift = CUBE_SIZE/8
    eye_position = [pos.x * CUBE_SIZE + CUBE_SIZE /
                    4, pos.y * CUBE_SIZE + CUBE_SIZE/2]
    pupil_position = eye_position[:]
    if actual_direction == Direction.UP:
        b1, b2, b3, b4 = (10, 10, -1, -1)
        pupil_position[1] -= pupil_shift
    elif actual_direction == Direction.DOWN:
        b1, b2, b3, b4 = (-1, -1, 10, 10)
        pupil_position[1] += pupil_shift
    elif actual_direction == Direction.LEFT:
        b1, b2, b3, b4 = (10, -1, 10, -1)
        pupil_position[0] -= pupil_shift
    elif actual_direction == Direction.RIGHT:
        b1, b2, b3, b4 = (-1, 10, -1, 10)
        pupil_position[0] += pupil_shift
    pygame.draw.rect(screen, SNAKE_COLOR, head_position, 0, -1, b1, b2, b3, b4)
    pygame.draw.circle(screen, WHITE, eye_position, eye_radius)
    pygame.draw.circle(
        screen, WHITE, (eye_position[0] + CUBE_SIZE/2, eye_position[1]), eye_radius)
    pygame.draw.circle(screen, BLACK, pupil_position, pupil_radius)
    pygame.draw.circle(
        screen, BLACK, (pupil_position[0] + CUBE_SIZE/2, pupil_position[1]), pupil_radius)


def draw_food(pos):
    radius = CUBE_SIZE / 2
    position = (CUBE_SIZE * (pos.x + 0.5), CUBE_SIZE * (pos.y + 0.5))
    pygame.draw.circle(screen, RED, position, radius)


def draw_snake(snake, actual_direction):
    for part in snake[:-1]:
        draw_snake_part(part)
    draw_snake_head(snake[-1], actual_direction)


def fill_background():
    screen.fill(GRAY)


def draw_score(actual_score):
    # position = (0, 0, WIDTH, CUBE_SIZE)
    # pygame.draw.rect(screen, DARK_GRAY, position)
    score_text_font = pygame.font.SysFont("Comic Sans MS", 12)
    score_text = score_text_font.render(f"SCORE: {actual_score}", True, BLUE)
    # score_text_rect = score_text.get_rect(center=(WIDTH/2, CUBE_SIZE/2))
    screen.blit(score_text, (10, 10))


def draw(snake, food, actual_score):
    fill_background()
    draw_score(actual_score)
    draw_snake(snake, actual_direction)
    draw_food(food)

    pygame.display.update()


draw(snake, food, actual_score)

state.set_initial_position()

clock = pygame.time.Clock()

while True:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                state.snake_turn(Direction.UP)
            elif event.key == pygame.K_DOWN:
                state.snake_turn(Direction.DOWN)
            elif event.key == pygame.K_LEFT:
                state.snake_turn(Direction.LEFT)
            elif event.key == pygame.K_RIGHT:
                state.snake_turn(Direction.RIGHT)

            actual_direction = state.direction

    state.step()
    draw(state.snake, state.food, state.points)
