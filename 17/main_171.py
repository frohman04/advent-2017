import fileinput
from typing import List, Tuple
import unittest


def spinlock(rotate: int, iterations: int) -> Tuple[List[int], int]:
    buffer = [0]
    curr = 0
    for i in range(iterations):
        for _ in range(rotate):
            curr = (curr + 1) % len(buffer)

        curr += 1
        buffer.insert(curr, i + 1)
    return buffer, curr


def get_next(data: Tuple[List[int], int]) -> int:
    return data[0][data[1] + 1]


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(get_next(spinlock(int(lines[0]), 2017)))


class Tests171(unittest.TestCase):
    def test_0(self):
        self.assertEqual(([0], 0),
                         spinlock(3, 0))

    def test_1(self):
        self.assertEqual(([0, 1], 1),
                         spinlock(3, 1))

    def test_2(self):
        self.assertEqual(([0, 2, 1], 1),
                         spinlock(3, 2))

    def test_3(self):
        self.assertEqual(([0, 2, 3, 1], 2),
                         spinlock(3, 3))

    def test_4(self):
        self.assertEqual(([0, 2, 4, 3, 1], 2),
                         spinlock(3, 4))

    def test_5(self):
        self.assertEqual(([0, 5, 2, 4, 3, 1], 1),
                         spinlock(3, 5))

    def test_6(self):
        self.assertEqual(([0, 5, 2, 4, 3, 6, 1], 5),
                         spinlock(3, 6))

    def test_7(self):
        self.assertEqual(([0, 5, 7, 2, 4, 3, 6, 1], 2),
                         spinlock(3, 7))

    def test_8(self):
        self.assertEqual(([0, 5, 7, 2, 4, 3, 8, 6, 1], 6),
                         spinlock(3, 8))

    def test_9(self):
        self.assertEqual(([0, 9, 5, 7, 2, 4, 3, 8, 6, 1], 1),
                         spinlock(3, 9))
