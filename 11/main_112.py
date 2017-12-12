import fileinput
from typing import List, Tuple
import unittest


N = (0, 1, -1)
NE = (1, 0, -1)
SE = (1, -1, 0)
S = (0, -1, 1)
SW = (-1, 0, 1)
NW = (-1, 1, 0)


def move(curr: Tuple[int, int, int], amt: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return curr[0] + amt[0], curr[1] + amt[1], curr[2] + amt[2]


def get_coords(path: List[str]) -> List[Tuple[int, int, int]]:
    coords = [(0, 0, 0)]
    for step in path:
        if step == 'n':
            coords += [move(coords[-1], N)]
        elif step == 'ne':
            coords += [move(coords[-1], NE)]
        elif step == 'se':
            coords += [move(coords[-1], SE)]
        elif step == 's':
            coords += [move(coords[-1], S)]
        elif step == 'sw':
            coords += [move(coords[-1], SW)]
        elif step == 'nw':
            coords += [move(coords[-1], NW)]
        else:
            raise Exception('Unknown direction: {}'.format(step))
    return coords


def flatten(l: List[Tuple[int, int, int]]) -> List[int]:
    return [item for sublist in l for item in sublist]


def num_steps(path: List[str]) -> int:
    return max(abs(x) for x in flatten(get_coords(path)))


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(num_steps(lines[0].split(',')))


class Tests112(unittest.TestCase):
    def test_move_1(self):
        self.assertEqual(
            (2, 2, 3),
            move((1, 2, 3), (1, 0, 0))
        )

    def test_move_2(self):
        self.assertEqual(
            (1, 3, 3),
            move((1, 2, 3), (0, 1, 0))
        )

    def test_move_3(self):
        self.assertEqual(
            (1, 2, 4),
            move((1, 2, 3), (0, 0, 1))
        )

    def test_num_steps_1(self):
        self.assertEqual(
            3,
            num_steps(['ne', 'ne', 'ne'])
        )

    def test_num_steps_2(self):
        self.assertEqual(
            0,
            num_steps(['ne', 'ne', 'sw', 'sw'])
        )

    def test_num_steps_3(self):
        self.assertEqual(
            2,
            num_steps(['ne', 'ne', 's', 's'])
        )

    def test_num_steps_4(self):
        self.assertEqual(
            3,
            num_steps(['se', 'sw', 'se', 'sw', 'sw'])
        )
