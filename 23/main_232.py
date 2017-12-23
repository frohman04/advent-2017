import logging
import unittest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run(debug: bool) -> int:
    b = 84
    c = b
    h = 0
    if debug:
        b = (b * 100) + 100_000
        c = b + 17_000
    for _ in range(b, c + 1, 17):
        for d in range(2, int(_ / 2)):
            if int(_ / d) == _ / d:
                h += 1
                break
    return h


if __name__ == '__main__':
    print(run(True))


class Tests232(unittest.TestCase):
    def test_run_no_debug(self):
        self.assertEqual(1, run(False))
