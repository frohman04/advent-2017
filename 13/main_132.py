import fileinput
from typing import Dict, List
import unittest


class Firewall(object):
    def __init__(self, depth: int, range: int):
        self._depth = depth
        self._range = range
        self._pos = 0
        self._step = 1

    def step(self) -> int:
        if self._pos == self._range - 1 and self._step == 1:
            self._step = -1
        elif self._pos == 0 and self._step == -1:
            self._step = 1
        self._pos += self._step
        return self._pos

    @property
    def depth(self) -> int:
        return self._depth

    @property
    def range(self) -> int:
        return self._range

    @property
    def pos(self) -> int:
        return self._pos

    @property
    def severity(self) -> int:
        return self._depth * self._range

    def __str__(self) -> str:
        return '{:>2}: {}'.format(
            self._depth,
            ''.join(['[{}]'.format('S' if i == self._pos else ' ') for i in range(self._range)]))

    def __repr__(self) -> str:
        return 'Firewall(depth={}, range={})(pos={})'.format(self._depth, self._range, self._pos)

    def __eq__(self, other) -> bool:
        return (type(self) == type(other) and
                self._depth == other._depth and
                self._range == other._range and
                self._pos == other._pos and
                self._step == other._step)


def parse(lines: List[str]) -> List[Firewall]:
    out = []  # type: List[Firewall]
    for line in lines:
        parts = [x.strip() for x in line.split(':')]
        out += [Firewall(int(parts[0]), int(parts[1]))]
    return out


def simulate(firewalls: List[Firewall]) -> int:
    firewalls = dict((f.depth, f) for f in firewalls)

    for f in firewalls.values():
        for _ in range(f.depth):
            f.step()

    def is_safe(firewalls: Dict[int, Firewall]) -> bool:
        return all([f.pos != 0 for f in firewalls.values()])

    delay = 0
    while not is_safe(firewalls):
        for f in firewalls.values():
            f.step()
        delay += 1

    return delay


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(simulate(parse(lines)))


class Tests132(unittest.TestCase):
    def test_firewall_step(self):
        f = Firewall(0, 3)
        self.assertEqual(0, f.pos)
        for i in [1, 2, 1, 0, 1]:
            self.assertEqual(i, f.step())
            self.assertEqual(i, f.pos)

    def test_firewall_severity(self):
        self.assertEqual(24, Firewall(6, 4).severity)

    def test_parse(self):
        self.assertEqual([Firewall(2, 4), Firewall(3, 5)], parse(['2: 4', '3: 5']))

    def test_simulate(self):
        self.assertEqual(10, simulate([Firewall(0, 3),
                                       Firewall(1, 2),
                                       Firewall(4, 4),
                                       Firewall(6, 4)]))
