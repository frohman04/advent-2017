import fileinput
import logging
from typing import List
import unittest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def spinlock(rotate: int, iterations: int) -> int:
    zero_loc = 0
    next_val = 0
    length = 1
    curr = 0
    for i in range(iterations):
        if i % 500_000 == 0:
            logging.info('Iteration {}'.format(i))

        curr = (curr + rotate) % length + 1
        if (curr - 1) == zero_loc:
            next_val = i + 1
            logging.info('Iteration {}: Got new value after zero: {}'.format(i, next_val))
        elif curr == zero_loc:
            zero_loc += 1
            logging.info('Iteration {}: Zero value moved to: {}'.format(i, zero_loc))
        length += 1
    return next_val


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(spinlock(int(lines[0]), 50_000_000))


class Tests172(unittest.TestCase):
    def test_0(self):
        self.assertEqual(0, spinlock(3, 0))

    def test_1(self):
        self.assertEqual(1, spinlock(3, 1))

    def test_2(self):
        self.assertEqual(2, spinlock(3, 2))

    def test_3(self):
        self.assertEqual(2, spinlock(3, 3))

    def test_4(self):
        self.assertEqual(2, spinlock(3, 4))

    def test_5(self):
        self.assertEqual(5, spinlock(3, 5))

    def test_6(self):
        self.assertEqual(5, spinlock(3, 6))

    def test_7(self):
        self.assertEqual(5, spinlock(3, 7))

    def test_8(self):
        self.assertEqual(5, spinlock(3, 8))

    def test_9(self):
        self.assertEqual(9, spinlock(3, 9))
