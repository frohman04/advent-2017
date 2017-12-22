from collections import defaultdict
from enum import Enum
import fileinput
import logging
import math
from typing import Dict, List, Tuple
import unittest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class State(Enum):
    CLEAN = 1
    WEAKENED = 2
    INFECTED = 3
    FLAGGED = 4


def infect(grid: Dict[Tuple[int, int], State], steps: int=10000000) -> Tuple[Dict[Tuple[int, int], State], Tuple[int, int, float], int]:
    num_infected = 0

    curr_x = 0
    curr_y = 0
    dir = math.pi / 2
    for i in range(steps):
        if (i + 1) % 100_000 == 0:
            logger.info('Iteration {}'.format(i + 1))

        curr = grid[(curr_x, curr_y)]
        if curr == State.CLEAN:
            dir = (dir + math.pi / 2) % (2 * math.pi)
            grid[(curr_x, curr_y)] = State.WEAKENED
        elif curr == State.WEAKENED:
            dir = dir
            grid[(curr_x, curr_y)] = State.INFECTED
            num_infected += 1
        elif curr == State.INFECTED:
            dir = (dir + 3 * math.pi / 2) % (2 * math.pi)
            grid[(curr_x, curr_y)] = State.FLAGGED
        elif curr == State.FLAGGED:
            dir = (dir + math.pi) % (2 * math.pi)
            del grid[(curr_x, curr_y)]
        else:
            raise ValueError('Unknown state at {}: {}'.format((curr_x, curr_y),
                                                              grid[(curr_x, curr_y)]))

        curr_x += round(math.cos(dir))
        curr_y -= round(math.sin(dir))

    return grid, (curr_x, curr_y, dir), num_infected


def parse(lines: List[str]) -> Dict[Tuple[int, int], State]:
    vals = [[x == '#' for x in line] for line in lines]
    center_x = int(len(vals[0]) / 2)
    center_y = int(len(vals) / 2)

    grid = defaultdict(lambda: State.CLEAN)  # type: Dict[Tuple[int, int], State]
    for y in range(len(vals[0])):
        for x in range(len(vals)):
            if vals[y][x]:
                grid[(x - center_x, y - center_y)] = State.INFECTED

    return grid


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.rstrip()]
    print(infect(parse(lines))[2])


class Tests222(unittest.TestCase):
    def setUp(self):
        grid = defaultdict(lambda: State.CLEAN)
        grid[(1, -1)] = State.INFECTED
        grid[(-1, 0)] = State.INFECTED
        self.grid = grid

    def test_parse(self):
        self.assertEqual(
            {
                (1, -1): State.INFECTED,
                (-1, 0): State.INFECTED
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
                    (0, 0): State.WEAKENED,
                    (1, -1): State.INFECTED,
                    (-1, 0): State.INFECTED
                },
                (-1, 0, math.pi),
                0
            ),
            infect(self.grid, 1)
        )

    def test_infect_2(self):
        self.assertEqual(
            (
                {
                    (0, 0): State.WEAKENED,
                    (-1, 0): State.FLAGGED,
                    (1, -1): State.INFECTED
                },
                (-1, -1, math.pi / 2),
                0
            ),
            infect(self.grid, 2)
        )

    def test_infect_5(self):
        self.assertEqual(
            (
                {
                    (0, 0): State.WEAKENED,
                    (1, -1): State.INFECTED,
                    (-1, 0): State.FLAGGED,
                    (-2, 0): State.WEAKENED,
                    (-2, -1): State.WEAKENED,
                    (-1, -1): State.WEAKENED
                },
                (-1, 0, 0),
                0
            ),
            infect(self.grid, 5)
        )

    def test_infect_6(self):
        self.assertEqual(
            (
                {
                    (0, 0): State.WEAKENED,
                    (1, -1): State.INFECTED,
                    (-2, 0): State.WEAKENED,
                    (-2, -1): State.WEAKENED,
                    (-1, -1): State.WEAKENED
                },
                (-2, 0, math.pi),
                0
            ),
            infect(self.grid, 6)
        )

    def test_infect_7(self):
        self.assertEqual(
            (
                {
                    (0, 0): State.WEAKENED,
                    (1, -1): State.INFECTED,
                    (-2, 0): State.INFECTED,
                    (-2, -1): State.WEAKENED,
                    (-1, -1): State.WEAKENED
                },
                (-3, 0, math.pi),
                1
            ),
            infect(self.grid, 7)
        )

    def test_infect_100(self):
        self.assertEqual(26, infect(self.grid, 100)[2])

    # def test_infect_10000000(self):
    #     self.assertEqual(2511944, infect(self.grid, 10000000)[2])
