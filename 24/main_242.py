import fileinput
import logging
from typing import Dict, List, Set, Tuple
import unittest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def flatten(l):
    return [item for sublist in l for item in sublist]


def build(pieces: Dict[int, Set[Tuple[int, int]]]) -> Tuple[List[Tuple[int, int]], Tuple[int, int]]:
    def build(bridge: List[Tuple[int, int]],
              connect: int,
              pieces: Dict[int, Set[Tuple[int, int]]],
              used: Set[Tuple[int, int]]) -> Tuple[List[Tuple[int, int]], Tuple[int, int]]:
        next = pieces[connect]
        if all(x in used for x in next):
            length = len(bridge)
            strength = sum(flatten(bridge))
            logger.debug('Found bridge ({}): {}'.format(strength, bridge))
            return bridge, (length, strength)
        else:
            best = None  # type: Tuple[List[Tuple[int, int]], Tuple[int, int]]
            for element in [x for x in next if x not in used]:
                if element[0] == connect:
                    updated_connect = element[1]
                else:
                    updated_connect = element[0]

                result = build(bridge + [element], updated_connect, pieces, set(list(used) + [element]))
                if best is None or best[1] < result[1]:
                    best = result
            return best

    return build([], 0, pieces, set())


def parse(lines: List[str]) -> Dict[int, Set[Tuple[int, int]]]:
    out = {}  # type: Dict[int, Set[Tuple[int, int]]]
    for line in lines:
        end1, end2 = [int(x.strip()) for x in line.split('/')]
        if end1 not in out:
            out[end1] = set()  # type: Set[Tuple[int, int]]
        if end2 not in out:
            out[end2] = set()  # type: Set[Tuple[int, int]]

        out[end1].add((end1, end2))
        out[end2].add((end1, end2))

    return out


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.rstrip()]
    print(build(parse(lines)))


class Tests242(unittest.TestCase):
    def test_parse(self):
        self.assertDictEqual({
            0: {(0, 2), (0, 1)},
            1: {(0, 1), (10, 1)},
            2: {(0, 2), (2, 2), (2, 3)},
            3: {(2, 3), (3, 4), (3, 5)},
            4: {(3, 4)},
            5: {(3, 5)},
            9: {(9, 10)},
            10: {(10, 1), (9, 10)}
        }, parse(['0/2', '2/2', '2/3', '3/4', '3/5', '0/1', '10/1', '9/10']))

    def test_build(self):
        self.assertEqual(([(0, 2), (2, 2), (2, 3), (3, 5)], (4, 19)),
                         build({
                             0: {(0, 2), (0, 1)},
                             1: {(0, 1), (10, 1)},
                             2: {(0, 2), (2, 2), (2, 3)},
                             3: {(2, 3), (3, 4), (3, 5)},
                             4: {(3, 4)},
                             5: {(3, 5)},
                             9: {(9, 10)},
                             10: {(10, 1), (9, 10)}
                         }))
