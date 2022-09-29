from game_state import RUNNING, GameState
from direction import Direction
from position import Position
import unittest


class GameStateTest(unittest.TestCase):

    def test_movement_right(self):
        state = GameState(
            snake=[
                Position(2, 3),
                Position(2, 4),
                Position(2, 5)
            ],
            direction=Direction.RIGHT,
            food=Position(7, 7),
            field_size=20
        )

        state.step()

        expected_state = [
            Position(2, 4),
            Position(2, 5),
            Position(3, 5)
        ]

        self.assertEqual(expected_state, state.snake)

    def test_movement_left(self):
        state = GameState(
            snake=[
                Position(2, 3),
                Position(2, 4),
                Position(2, 5)
            ],
            direction=Direction.LEFT,
            food=Position(7, 7),
            field_size=20
        )

        state.step()

        expected_state = [
            Position(2, 4),
            Position(2, 5),
            Position(1, 5)
        ]

        self.assertEqual(expected_state, state.snake)

    def test_movement_up(self):
        state = GameState(
            snake=[
                Position(1, 3),
                Position(2, 3),
                Position(3, 3)
            ],
            direction=Direction.UP,
            food=Position(7, 7),
            field_size=20
        )

        state.step()

        expected_state = [
            Position(2, 3),
            Position(3, 3),
            Position(3, 2)
        ]

        self.assertEqual(expected_state, state.snake)

    def test_movement_down(self):
        state = GameState(
            snake=[
                Position(1, 3),
                Position(2, 3),
                Position(3, 3)
            ],
            direction=Direction.DOWN,
            food=Position(7, 7),
            field_size=20
        )

        state.step()

        expected_state = [
            Position(2, 3),
            Position(3, 3),
            Position(3, 4)
        ]

        self.assertEqual(expected_state, state.snake)

    def test_upper_border(self):
        state = GameState(
            snake=[
                Position(3, 2),
                Position(3, 1),
                Position(3, 0)
            ],
            direction=Direction.UP,
            food=Position(7, 7),
            field_size=20
        )

        state.step()

        expected_state = [
            Position(3, 1),
            Position(3, 0),
            Position(3, 19)
        ]

        self.assertEqual(expected_state, state.snake)

    def test_lower_border(self):
        state = GameState(
            snake=[
                Position(3, 17),
                Position(3, 18),
                Position(3, 19)
            ],
            direction=Direction.DOWN,
            food=Position(7, 7),
            field_size=20
        )

        state.step()

        expected_state = [
            Position(3, 18),
            Position(3, 19),
            Position(3, 0)
        ]

        self.assertEqual(expected_state, state.snake)

    def test_right_border(self):
        state = GameState(
            snake=[
                Position(17, 2),
                Position(18, 2),
                Position(19, 2)
            ],
            direction=Direction.RIGHT,
            food=Position(7, 7),
            field_size=20
        )

        state.step()

        expected_state = [
            Position(18, 2),
            Position(19, 2),
            Position(0, 2)
        ]

        self.assertEqual(expected_state, state.snake)

    def test_left_border(self):
        state = GameState(
            snake=[
                Position(2, 2),
                Position(1, 2),
                Position(0, 2)
            ],
            direction=Direction.LEFT,
            food=Position(7, 7),
            field_size=20
        )

        state.step()

        expected_state = [
            Position(1, 2),
            Position(0, 2),
            Position(19, 2)
        ]

        self.assertEqual(expected_state, state.snake)

    def test_food_eaten(self):
        state = GameState(
            snake=[
                Position(2, 2),
                Position(2, 3),
                Position(2, 4)
            ],
            direction=Direction.DOWN,
            food=Position(2, 5),
            field_size=20,
            points=0
        )

        state.step()

        expected_state = [
            Position(2, 2),
            Position(2, 3),
            Position(2, 4),
            Position(2, 5)
        ]
        expected_points = 1

        self.assertEqual(expected_state, state.snake)
        self.assertFalse(state.food in state.snake)
        self.assertEqual(expected_points, state.points)


    def test_snake_death(self):
        state = GameState(
            snake=[
                Position(1, 2),
                Position(2, 2),
                Position(3, 2),
                Position(3, 3),
                Position(2, 3)
            ],
            direction=Direction.UP,
            food=Position(3, 1),
            field_size=25,
            set_status=RUNNING
        )

        state.step()

        from game_state import GAMEOVER
        self.assertEqual(GAMEOVER, state.set_status)
        self.assertFalse(state.food in state.snake)


    def test_snake_turn(self):
        state = GameState(
            snake=[
                Position(1, 2),
                Position(2, 2),
                Position(3, 2),
                Position(3, 3),
                Position(2, 3)
            ],
            direction=Direction.UP,
            food=Position(3, 1),
            field_size=25
        )

        state.snake_turn(Direction.LEFT)
        self.assertEqual(Direction.LEFT, state.direction)
        state.snake_turn(Direction.UP)
        self.assertEqual(Direction.UP, state.direction)
        state.snake_turn(Direction.DOWN)
        self.assertEqual(Direction.DOWN, state.direction)
        state.snake_turn(Direction.RIGHT)
        self.assertEqual(Direction.DOWN, state.direction)


    def test_can_snake_turn(self):
        state = GameState(
            snake=[
                Position(1, 2),
                Position(2, 2),
                Position(3, 2),
                Position(3, 3),
                Position(2, 3)
            ],
            direction=Direction.UP,
            food=Position(3, 1),
            field_size=25
        )

        self.assertTrue(state.can_snake_turn(Direction.LEFT))
        self.assertFalse(state.can_snake_turn(Direction.RIGHT))
        self.assertTrue(state.can_snake_turn(Direction.UP))
        self.assertTrue(state.can_snake_turn(Direction.DOWN))
        