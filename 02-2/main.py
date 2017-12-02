import fileinput
import itertools
from typing import List
import unittest


def checksum(data: List[List[int]]) -> int:
    running_sum = 0
    for line in data:
        for first, second in itertools.permutations(line, 2):
            if int(first / second) == (first / second):
                running_sum += int(first / second)
                break
    return running_sum


def parse(data_str: List[str]) -> List[List[int]]:
    data = []  # type: List[List[int]]
    for line in data_str:
        data += [[int(x) for x in line.split()]]
    return data


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line]
    print(checksum(parse(lines)))


class Tests(unittest.TestCase):
    def test_1(self):
        self.assertEqual(9, checksum(parse(['5 9 2 8', '9 4 7 3', '3 8 6 5'])))
