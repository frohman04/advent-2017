import enum
import fileinput
from typing import Generator, Tuple
import unittest


def coords() -> Generator[Tuple[int, Tuple[int, int]], None, None]:
    class Direction(enum.Enum):
        UP = 1
        LEFT = 2
        DOWN = 3
        RIGHT = 4

        def next(self):
            return Direction((self.value % len(Direction)) + 1)

    idx = 1
    direction = Direction.RIGHT
    side_len = 1
    curr_len = 0
    num_sides = 0
    curr_x = 0
    curr_y = 0
    while True:
        yield (idx, (curr_x, curr_y))

        idx += 1
        if direction == Direction.LEFT:
            curr_x -= 1
        elif direction == Direction.UP:
            curr_y += 1
        elif direction == Direction.RIGHT:
            curr_x += 1
        elif direction == Direction.DOWN:
            curr_y -= 1

        curr_len += 1
        if curr_len == side_len:
            curr_len = 0
            num_sides += 1
            if num_sides == 2:
                num_sides = 0
                side_len += 1
            direction = direction.next()


def neighbor_sum() -> Generator[Tuple[int, int], None, None]:
    """
    Calculate the sum of all neighbors of the cell.

    :return: the neighbor sum
    """
    cache = {}
    for curr_coords in coords():
        if curr_coords[0] == 1:
            total = 1
        else:
            total = 0
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    if not (x == 0 and y == 0):
                        key = (x + curr_coords[1][0], y + curr_coords[1][1])
                        if key in cache:
                            total += cache[key]
        cache[curr_coords[1]] = total
        yield (curr_coords[0], total)


def first_larger(num: int) -> int:
    for idx, total in neighbor_sum():
        if total > num:
            return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(first_larger(int(lines[0])))


class Tests032(unittest.TestCase):
    def test_coords(self):
        cs = coords()
        self.assertEqual([
            (1, (0, 0)),
            (2, (1, 0)),
            (3, (1, 1)),
            (4, (0, 1)),
            (5, (-1, 1)),
            (6, (-1, 0)),
            (7, (-1, -1)),
            (8, (0, -1)),
            (9, (1, -1)),
            (10, (2, -1)),
            (11, (2, 0)),
            (12, (2, 1)),
            (13, (2, 2)),
            (14, (1, 2)),
            (15, (0, 2)),
            (16, (-1, 2)),
            (17, (-2, 2)),
            (18, (-2, 1)),
            (19, (-2, 0)),
            (20, (-2, -1)),
            (21, (-2, -2)),
            (22, (-1, -2)),
            (23, (0, -2)),
            (24, (1, -2)),
            (25, (2, -2))
        ], [next(cs) for _ in range(25)])

    def test_neighbor_sum(self):
        ns = neighbor_sum()
        self.assertEqual(
            [x for x in zip(range(1, 24),
                            [1, 1, 2, 4, 5, 10, 11, 23, 25, 26,
                             54, 57, 59, 122, 133, 142, 147, 304, 330, 351,
                             362, 747, 806])],
            [next(ns) for _ in range(23)])
