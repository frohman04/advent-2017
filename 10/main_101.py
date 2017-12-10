import fileinput
from typing import Dict, List, Tuple
import unittest


def next_pos(start: int, length: int, skip: int, arr: List[int]) -> Tuple[int, int]:
    next = (start + length + skip) % len(arr)
    return next, skip + 1


def rotate(start: int, length: int, arr: List[int]) -> List[int]:
    if start + length > len(arr):
        rotated = [x for x in reversed(arr[start:len(arr)] + arr[0:(start + length) % len(arr)])]
        arr[start:len(arr)] = rotated[0:len(arr) - start]
        arr[0:(start + length) % len(arr)] = rotated[len(arr) - start:len(rotated)]
    else:
        arr[start:start + length] = reversed(arr[start:start + length])

    return arr


def process(lengths: List[int], arr: List[int] = [x for x in range(256)]) -> int:
    curr = 0
    skip = 0
    for length in lengths:
        arr = rotate(curr, length, arr)
        curr, skip = next_pos(curr, length, skip, arr)

    return arr[0] * arr[1]


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(process([int(x) for x in lines[0].split(',')]))


class Tests101(unittest.TestCase):
    def test_next_pos_1(self):
        self.assertEqual(
            next_pos(0, 3, 0, [0, 1, 2, 3, 4]),
            (3, 1)
        )

    def test_next_pos_2(self):
        self.assertEqual(
            next_pos(3, 4, 1, [0, 1, 2, 3, 4]),
            (3, 2)
        )

    def test_next_pos_3(self):
        self.assertEqual(
            next_pos(3, 1, 2, [0, 1, 2, 3, 4]),
            (1, 3)
        )

    def test_next_pos_4(self):
        self.assertEqual(
            next_pos(1, 5, 3, [0, 1, 2, 3, 4]),
            (4, 4)
        )

    def test_rotate_1(self):
        self.assertEqual(
            rotate(0, 3, [0, 1, 2, 3, 4]),
            [2, 1, 0, 3, 4]
        )

    def test_rotate_2(self):
        self.assertEqual(
            rotate(3, 4, [2, 1, 0, 3, 4]),
            [4, 3, 0, 1, 2]
        )

    def test_rotate_3(self):
        self.assertEqual(
            rotate(3, 1, [4, 3, 0, 1, 2]),
            [4, 3, 0, 1, 2]
        )

    def test_rotate_4(self):
        self.assertEqual(
            rotate(1, 5, [4, 3, 0, 1, 2]),
            [3, 4, 2, 1, 0]
        )

    def test_process(self):
        self.assertEqual(
            process([3, 4, 1, 5], [0, 1, 2, 3, 4]),
            12
        )
