from collections import defaultdict
import fileinput
import logging
import math
from typing import List, Set, Tuple
import unittest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def infect(grid: Set[Tuple[int, int]], steps: int=10000) -> Tuple[Set[Tuple[int, int]], Tuple[int, int, float], int]:
    num_infected = 0

    curr_x = 0
    curr_y = 0
    dir = math.pi / 2
    for _ in range(steps):
        if (curr_x, curr_y) in grid:
            dir = (dir + 3 * math.pi / 2) % (2 * math.pi)
            grid.remove((curr_x, curr_y))
        else:
            dir = (dir + math.pi / 2) % (2 * math.pi)
            grid.add((curr_x, curr_y))
            num_infected += 1

        curr_x += round(math.cos(dir))
        curr_y -= round(math.sin(dir))

    return grid, (curr_x, curr_y, dir), num_infected


def parse(lines: List[str]) -> Set[Tuple[int, int]]:
    vals = [[x == '#' for x in line] for line in lines]
    center_x = int(len(vals[0]) / 2)
    center_y = int(len(vals) / 2)

    grid = set([])  # type: Set[Tuple[int, int], bool]
    for y in range(len(vals[0])):
        for x in range(len(vals)):
            if vals[y][x]:
                grid.add((x - center_x, y - center_y))

    return grid


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.rstrip()]
    print(infect(parse(lines))[2])


class Tests221(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(
            {
                (1, -1),
                (-1, 0)
            },
            parse([
                '..#',
                '#..',
                '...'
            ])
        )

    def test_infect_1(self):
        self.assertEqual(
            (
                {
                    (0, 0),
                    (1, -1),
                    (-1, 0)
                },
                (-1, 0, math.pi),
                1
            ),
            infect(
                {
                    (1, -1),
                    (-1, 0)
                },
                1
            )
        )

    def test_infect_2(self):
        self.assertEqual(
            (
                {
                    (0, 0),
                    (1, -1)
                },
                (-1, -1, math.pi / 2),
                1
            ),
            infect(
                {
                    (1, -1),
                    (-1, 0)
                },
                2
            )
        )

    def test_infect_6(self):
        self.assertEqual(
            (
                {
                    (0, 0),
                    (1, -1),
                    (-1, 0),
                    (-2, 0),
                    (-2, -1),
                    (-1, -1)
                },
                (-1, -1, math.pi / 2),
                5
            ),
            infect(
                {
                    (1, -1),
                    (-1, 0)
                },
                6
            )
        )

    def test_infect_7(self):
        self.assertEqual(
            (
                {
                    (0, 0),
                    (1, -1),
                    (-1, 0),
                    (-2, 0),
                    (-2, -1)
                },
                (0, -1, 0),
                5
            ),
            infect(
                {
                    (1, -1),
                    (-1, 0)
                },
                7
            )
        )

    def test_infect_70(self):
        self.assertEqual(
            (
                {
                    (0, 0),
                    (-2, 0),
                    (-2, -1),
                    (-1, -2),
                    (0, -1),
                    (0, -3),
                    (1, 1),
                    (1, -4),
                    (2, 1),
                    (2, -4),
                    (3, 0),
                    (3, -3),
                    (4, -1),
                    (4, -2)
                },
                (1, -1, math.pi / 2),
                41
            ),
            infect(
                {
                    (1, -1),
                    (-1, 0)
                },
                70
            )
        )
