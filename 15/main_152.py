from typing import Generator
import unittest


def gen(init: int, mux: int, div: int) -> Generator[int, None, None]:
    val = init
    while True:
        val = (val * mux) % 2147483647
        if val % div == 0:
            yield val


def gen_a(init: int = 65) -> Generator[int, None, None]:
    return gen(init, 16807, 4)


def gen_b(init: int = 8921) -> Generator[int, None, None]:
    return gen(init, 48271, 8)


def judge(a: int, b: int) -> bool:
    a_bin = a & 65_535
    b_bin = b & 65_535
    return a_bin == b_bin


def score(num_rounds: int, a_init: int = 65, b_init: int = 8921) -> int:
    a = gen_a(a_init)
    b = gen_b(b_init)
    total = 0
    for i in range(num_rounds):
        if judge(next(a), next(b)):
            total += 1
    return total


if __name__ == '__main__':
    print(score(5_000_000, 783, 325))


class Tests152(unittest.TestCase):
    def test_gen_a(self):
        g = gen_a()
        self.assertEqual([1352636452, 1992081072, 530830436, 1980017072, 740335192],
                         [next(g) for _ in range(5)])

    def test_gen_b(self):
        g = gen_b()
        self.assertEqual([1233683848, 862516352, 1159784568, 1616057672, 412269392],
                         [next(g) for _ in range(5)])

    def test_judge_1(self):
        self.assertFalse(judge(1092455, 430625591))

    def test_judge_2(self):
        self.assertFalse(judge(1181022009, 1233683848))

    def test_judge_3(self):
        self.assertTrue(judge(245556042, 1431495498))

    def test_judge_4(self):
        self.assertFalse(judge(1744312007, 137874439))

    def test_judge_5(self):
        self.assertFalse(judge(1352636452, 285222916))

    def test_score_1(self):
        self.assertEqual(1, score(1056))

    def test_score_2(self):
        self.assertEqual(309, score(5_000_000))
