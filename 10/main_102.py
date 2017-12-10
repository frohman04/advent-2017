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


def convert(input: str) -> List[int]:
    return [ord(x) for x in input] + [17, 31, 73, 47, 23]


def hash_round(start: int,
               skip: int,
               lengths: List[int],
               arr: List[int]) -> Tuple[List[int], int, int]:
    curr = start
    for length in lengths:
        arr = rotate(curr, length, arr)
        curr, skip = next_pos(curr, length, skip, arr)

    return arr, curr, skip


def calc_sparse_hash(lengths: List[int]) -> List[int]:
    arr = [x for x in range(256)]

    curr = 0
    skip = 0
    for i in range(64):
        arr, curr, skip = hash_round(curr, skip, lengths, arr)

    return arr


def to_dense_hash(sparse_hash: List[int]) -> List[int]:
    out = []
    for x in range(0, 256, 16):
        total = 0
        for y in range(16):
            total ^= sparse_hash[x + y]
        out += [total]
    return out


def to_hex_str(dense_hash: List[int]) -> str:
    return ''.join(hex(x)[2:].zfill(2) for x in dense_hash)


def hash(input: str) -> str:
    lengths = convert(input)
    sparse_hash = calc_sparse_hash(lengths)
    dense_hash = to_dense_hash(sparse_hash)
    return to_hex_str(dense_hash)


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(hash(lines[0]))


class Tests102(unittest.TestCase):
    def test_convert(self):
        self.assertEqual(
            convert('1,2,3'),
            [49, 44, 50, 44, 51, 17, 31, 73, 47, 23]
        )

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

    def test_hash_round(self):
        self.assertEqual(
            hash_round(0, 0, [3, 4, 1, 5], [0, 1, 2, 3, 4]),
            ([3, 4, 2, 1, 0], 4, 4)
        )

    def test_to_hex_str(self):
        self.assertEqual(
            to_hex_str([64, 7, 255]),
            '4007ff'
        )

    def test_hash_1(self):
        self.assertEqual(
            hash(''),
            'a2582a3a0e66e6e86e3812dcb672a272'
        )

    def test_hash_2(self):
        self.assertEqual(
            hash('AoC 2017'),
            '33efeb34ea91902bb2f59c9920caa6cd'
        )

    def test_hash_3(self):
        self.assertEqual(
            hash('1,2,3'),
            '3efbe78a8d82f29979031a4aa0b16a9d'
        )

    def test_hash_4(self):
        self.assertEqual(
            hash('1,2,4'),
            '63960835bcdc130f0b66d7ff4f6a5a8e'
        )
