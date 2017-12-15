from typing import Generator
import unittest


def gen(init: int, mux: int) -> Generator[int, None, None]:
    val = init
    while True:
        val = (val * mux) % 2147483647
        yield val


def gen_a(init: int = 65) -> Generator[int, None, None]:
    return gen(init, 16807)


def gen_b(init: int = 8921  ) -> Generator[int, None, None]:
    return gen(init, 48271)


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
    print(score(40_000_000, 783, 325))


class Tests151(unittest.TestCase):
    def test_gen_a(self):
        g = gen_a()
        self.assertEqual([1092455, 1181022009, 245556042, 1744312007, 1352636452],
                         [next(g) for _ in range(5)])

    def test_gen_b(self):
        g = gen_b()
        self.assertEqual([430625591, 1233683848, 1431495498, 137874439, 285222916],
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
        self.assertEqual(1, score(5))

    def test_score_2(self):
        self.assertEqual(588, score(40_000_000))
