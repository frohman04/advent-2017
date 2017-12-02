import sys
from typing import List
import unittest


def count(nums: List[int]) -> int:
    half = int(len(nums) / 2)
    total = 0
    for i in range(len(nums)):
        if nums[i] == nums[(i + half) % len(nums)]:
            total += nums[i]
    return total


if __name__ == '__main__':
    print(count([int(x) for x in sys.argv[1]]))


class Tests(unittest.TestCase):
    def test_1(self):
        self.assertEqual(6, count([1, 2, 1, 2]))

    def test_2(self):
        self.assertEqual(0, count([1, 2, 2, 1]))

    def test_3(self):
        self.assertEqual(4, count([1, 2, 3, 4, 2, 5]))

    def test_4(self):
        self.assertEqual(12, count([1, 2, 3, 1, 2, 3]))

    def test_5(self):
        self.assertEqual(4, count([1, 2, 1, 3, 1, 4, 1, 5]))
