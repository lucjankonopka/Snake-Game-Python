import pygame
from position import Position
from direction import Direction
from game_state import GameState, RUNNING, PAUSED, GAMEOVER

pygame.init()

CUBE_SIZE = 32
CUBES_NUM = 20
WIDTH = CUBE_SIZE * CUBES_NUM
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Snake Game by Lucjan Konopka")
game_speed = 10

GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
SNAKE_COLOR = (43, 110, 51)


pygame.display.update()

snake = [
    Position(-1, 2),
    Position(0, 2),
    Position(1, 2)
]

food = Position(-1, -1)

state = GameState(
    snake=None,
    direction=Direction.RIGHT,
    food=None,
    field_size=CUBES_NUM,
    points=0,
    speed=10
)

actual_score = state.points
actual_direction = state.direction
initial_tail_position = state.snake[0]
end_tail_position = state.snake[0]
initial_foretail_position = state.snake[1]
end_foretail_position = state.snake[1]


def display_pause_screen():
    text_upper = 'Game paused!'
    text_lower = 'Press "space" to continue.'
    pause_upper_text = pygame.font.SysFont(
        'Consolas', 32).render(text_upper, True, BLACK)
    pause_upper_text_rect = pause_upper_text.get_rect(
        center=(WIDTH/2, WIDTH/2 - 20))
    pause_lower_text = pygame.font.SysFont(
        'Consolas', 32).render(text_lower, True, BLACK)
    pause_lower_text_rect = pause_lower_text.get_rect(
        center=(WIDTH/2, WIDTH/2 + 20))
    fill_background(DARK_GRAY)
    screen.blit(pause_upper_text, pause_upper_text_rect)
    screen.blit(pause_lower_text, pause_lower_text_rect)
    pygame.display.update()


def display_game_over():
    text_upper = 'Game Over!'
    text_middle = f'Your score: {state.points}.'
    text_lower = 'Do you want to play again? (y/n)'
    lost_upper_text = pygame.font.SysFont(
        'Consolas', 32).render(text_upper, True, BLACK)
    lost_upper_text_rect = lost_upper_text.get_rect(
        center=(WIDTH/2, WIDTH/2 - 40))
    lost_text_middle = pygame.font.SysFont(
        'Consolas', 32).render(text_middle, True, SNAKE_COLOR)
    lost_text_middle_rect = lost_text_middle.get_rect(
        center=(WIDTH/2, WIDTH/2))
    lost_lower_text = pygame.font.SysFont(
        'Consolas', 32).render(text_lower, True, BLACK)
    lost_lower_text_rect = lost_lower_text.get_rect(
        center=(WIDTH/2, WIDTH/2 + 40))
    fill_background(DARK_GRAY)
    screen.blit(lost_upper_text, lost_upper_text_rect)
    screen.blit(lost_text_middle, lost_text_middle_rect)
    screen.blit(lost_lower_text, lost_lower_text_rect)
    pygame.display.update()


def draw_snake_part(pos):
    position = (pos.x * CUBE_SIZE, pos.y * CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
    pygame.draw.rect(screen, SNAKE_COLOR, position)


def check_snake_tail_actual_movement():
    if initial_tail_position[0] == end_tail_position[0]:
        if (initial_tail_position[1] > end_tail_position[1] and (initial_tail_position[1] != (CUBES_NUM - 1) or end_tail_position[1] != 0)) \
                or (initial_tail_position[1] == 0 and end_tail_position[1] == (CUBES_NUM - 1)):
            return 'up'
        elif (initial_tail_position[1] < end_tail_position[1] and (initial_tail_position[1] != 0 or end_tail_position[1] != (CUBES_NUM - 1))) \
                or (initial_tail_position[1] == (CUBES_NUM - 1) and end_tail_position[1] == 0):
            return 'down'
    if initial_tail_position[1] == end_tail_position[1]:
        if (initial_tail_position[0] > end_tail_position[0] and (initial_tail_position[0] != (CUBES_NUM - 1) or end_tail_position[0] != 0)) \
                or (initial_tail_position[0] == 0 and end_tail_position[0] == (CUBES_NUM - 1)):
            return 'left'
        elif (initial_tail_position[0] < end_tail_position[0] and (initial_tail_position[0] != 0 or end_tail_position[0] != (CUBES_NUM - 1))) \
                or (initial_tail_position[0] == (CUBES_NUM - 1) and end_tail_position[0] == 0):
            return 'right'


def check_snake_foretail_actual_movement():
    if initial_foretail_position[0] == end_foretail_position[0]:
        if (initial_foretail_position[1] > end_foretail_position[1] and (initial_foretail_position[1] != (CUBES_NUM - 1) or end_foretail_position[1] != 0)) \
                or (initial_foretail_position[1] == 0 and end_foretail_position[1] == (CUBES_NUM - 1)):
            return 'up'
        elif (initial_foretail_position[1] < end_foretail_position[1] and (initial_foretail_position[1] != 0 or end_foretail_position[1] != (CUBES_NUM - 1))) \
                or (initial_foretail_position[1] == (CUBES_NUM - 1) and end_foretail_position[1] == 0):
            return 'down'
    if initial_foretail_position[1] == end_foretail_position[1]:
        if (initial_foretail_position[0] > end_foretail_position[0] and (initial_foretail_position[0] != (CUBES_NUM - 1) or end_foretail_position[0] != 0)) \
                or (initial_foretail_position[0] == 0 and end_foretail_position[0] == (CUBES_NUM - 1)):
            return 'left'
        elif (initial_foretail_position[0] < end_foretail_position[0] and (initial_foretail_position[0] != 0 or end_foretail_position[0] != (CUBES_NUM - 1))) \
                or (initial_foretail_position[0] == (CUBES_NUM - 1) and end_foretail_position[0] == 0):
            return 'right'


def draw_snake_tail(pos):
    tail_position = [[pos.x * CUBE_SIZE, pos.y * CUBE_SIZE], [pos.x * CUBE_SIZE, pos.y * CUBE_SIZE],
                     [pos.x * CUBE_SIZE, pos.y * CUBE_SIZE], [pos.x * CUBE_SIZE, pos.y * CUBE_SIZE]]
    # UP
    if (check_snake_tail_actual_movement() == 'up' and check_snake_foretail_actual_movement() == 'up') \
            or (check_snake_foretail_actual_movement() == 'up' and (check_snake_tail_actual_movement() == 'right' or check_snake_tail_actual_movement() == 'left')):
        tail_position[1][0] += CUBE_SIZE - 1
        tail_position[2][0] += 3/4*CUBE_SIZE
        tail_position[2][1] += CUBE_SIZE
        tail_position[3][0] += 1/4*CUBE_SIZE
        tail_position[3][1] += CUBE_SIZE
        # DOWN
    elif (check_snake_tail_actual_movement() == 'down' and check_snake_foretail_actual_movement() == 'down') \
            or (check_snake_foretail_actual_movement() == 'down' and (check_snake_tail_actual_movement() == 'right' or check_snake_tail_actual_movement() == 'left')):
        tail_position[0][1] += CUBE_SIZE
        tail_position[1][0] += 1/4*CUBE_SIZE
        tail_position[2][0] += 3/4*CUBE_SIZE
        tail_position[3][0] += CUBE_SIZE
        tail_position[3][1] += CUBE_SIZE
        # LEFT
    elif check_snake_tail_actual_movement() == 'left' \
            or (check_snake_foretail_actual_movement() == 'left' and (check_snake_tail_actual_movement() == 'up' or check_snake_tail_actual_movement() == 'down')):
        tail_position[1][0] += CUBE_SIZE
        tail_position[1][1] += 1/4*CUBE_SIZE
        tail_position[2][0] += CUBE_SIZE
        tail_position[2][1] += 3/4*CUBE_SIZE
        tail_position[3][1] += CUBE_SIZE
        # RIGHT
    elif check_snake_tail_actual_movement() == 'right' \
            or (check_snake_foretail_actual_movement() == 'right' and (check_snake_tail_actual_movement() == 'up' or check_snake_tail_actual_movement() == 'down')):
        tail_position[0][0] += CUBE_SIZE
        tail_position[1][1] += 1/4*CUBE_SIZE
        tail_position[2][1] += 3/4*CUBE_SIZE
        tail_position[3][0] += CUBE_SIZE
        tail_position[3][1] += CUBE_SIZE
    pygame.draw.polygon(screen, SNAKE_COLOR, tail_position)


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
    radius = 2*CUBE_SIZE / 5
    position = (CUBE_SIZE * (pos.x + 0.5), CUBE_SIZE * (pos.y + 0.5))
    pygame.draw.circle(screen, RED, position, radius)


def draw_snake(snake, actual_direction):
    for part in snake[1:-1]:
        draw_snake_part(part)
    draw_snake_head(snake[-1], actual_direction)
    draw_snake_tail(snake[0])


def fill_background(color):
    screen.fill(color)


def draw_score(actual_score):
    score_text_font = pygame.font.SysFont("Comic Sans MS", 12)
    score_text = score_text_font.render(f"SCORE: {actual_score}", True, BLUE)
    screen.blit(score_text, (10, 10))


def draw(snake, food, actual_score, actual_direction):
    fill_background(GRAY)
    draw_score(actual_score)
    draw_snake(snake, actual_direction)
    draw_food(food)

    pygame.display.update()


draw(snake, food, actual_score, actual_direction)

state.set_initial_position()

clock = pygame.time.Clock()

while True:

    clock.tick(game_speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and state.set_status == "RUNNING":
                state.set_status = "PAUSED"
                print(state.set_status)
                continue
            elif event.key == pygame.K_SPACE and state.set_status == "PAUSED":
                state.set_status = "RUNNING"
                print(state.set_status)
                continue
            elif event.key == pygame.K_n and state.set_status == "GAMEOVER":
                quit()
            if event.key == pygame.K_y and state.set_status == "GAMEOVER":
                state.set_status = "RUNNING"
                state.new_game()
                continue
            elif event.key == pygame.K_q:
                quit()
            elif event.key == pygame.K_UP:
                state.snake_turn(Direction.UP)
            elif event.key == pygame.K_DOWN:
                state.snake_turn(Direction.DOWN)
            elif event.key == pygame.K_LEFT:
                state.snake_turn(Direction.LEFT)
            elif event.key == pygame.K_RIGHT:
                state.snake_turn(Direction.RIGHT)
            actual_direction = state.direction

    if state.set_status == "RUNNING":

        initial_tail_position = state.snake[0]
        initial_foretail_position = state.snake[1]

        state.step()

        end_tail_position = state.snake[0]
        end_foretail_position = state.snake[1]

        draw(state.snake, state.food, state.points, state.direction)

    elif state.set_status == "GAMEOVER":
        display_game_over()

    elif state.set_status == "PAUSED":
        display_pause_screen()
