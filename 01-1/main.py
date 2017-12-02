import sys
from typing import List
import unittest


def count(nums: List[int]) -> int:
    nums = nums + [nums[0]]
    total = 0
    for i in range(len(nums) - 1):
        if nums[i] == nums[i + 1]:
            total += nums[i]
    return total


if __name__ == '__main__':
    print(count([int(x) for x in sys.argv[1]]))


class Tests(unittest.TestCase):
    def test_1(self):
        self.assertEqual(3, count([1, 1, 2, 2]))

    def test_2(self):
        self.assertEqual(4, count([1, 1, 1, 1]))

    def test_3(self):
        self.assertEqual(0, count([1, 2, 3, 4]))

    def test_4(self):
        self.assertEqual(9, count([9, 1, 2, 1, 2, 1, 2, 9]))
