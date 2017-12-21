import fileinput
import logging
import re
from typing import Dict, List
import unittest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Particle(object):
    def __init__(self,
                 p_x: int, p_y: int, p_z: int,
                 v_x: int, v_y: int, v_z: int,
                 a_x: int, a_y: int, a_z: int):
        self.p = (p_x, p_y, p_z)
        self.v = (v_x, v_y, v_z)
        self.a = (a_x, a_y, a_z)

    def step(self):
        self.v = (self.v[0] + self.a[0],
                  self.v[1] + self.a[1],
                  self.v[2] + self.a[2])
        self.p = (self.p[0] + self.v[0],
                  self.p[1] + self.v[1],
                  self.p[2] + self.p[2])

    def __str__(self):
        return 'p=<{}, {}, {}>, v=<{}, {}, {}>, a=<{}, {}, {}>'.format(*self.p, *self.v, *self.a)

    def __repr__(self):
        return 'Particle({}, {}, {}, {}, {}, {}, {}, {}, {})'.format(*self.p, *self.v, *self.a)

    def __eq__(self, other):
        return (type(self) == type(other) and
                self.p == other.p and
                self.v == other.v and
                self.a == other.a)


def parse(lines: List[str]) -> Dict[int, Particle]:
    r = re.compile(r'p=<([^,]+),([^,]+),([^,]+)>, '
                   r'v=<([^,]+),([^,]+),([^,]+)>, '
                   r'a=<([^,]+),([^,]+),([^,]+)>')

    i = 0
    parsed = {}  # type: Dict[int, Particle]
    for line in lines:
        p = Particle(*[int(x) for x in r.match(line).groups()])
        parsed[i] = p
        i += 1
    return parsed


def find_min(particles: Dict[int, Particle]) -> int:
    return min((sum(abs(x) for x in p.a), i) for i, p in particles.items())[1]


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.rstrip()]
    print(find_min(parse(lines)))


class Tests201(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(
            {
                0: Particle(3, 0, 0, 2, 0, 0, -1, 0, 0),
                1: Particle(4, 0, 0, 0, 0, 0, -2, 0, 0)
            },
            parse(['p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>',
                   'p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>']))

    def test_step_1(self):
        p = Particle(3, 0, 0, 2, 0, 0, -1, 0, 0)
        self.assertEqual(Particle(3, 0, 0, 2, 0, 0, -1, 0, 0), p)
        p.step()
        self.assertEqual(Particle(4, 0, 0, 1, 0, 0, -1, 0, 0), p)
        p.step()
        self.assertEqual(Particle(4, 0, 0, 0, 0, 0, -1, 0, 0), p)
        p.step()
        self.assertEqual(Particle(3, 0, 0, -1, 0, 0, -1, 0, 0), p)

    def test_step_2(self):
        p = Particle(4, 0, 0, 0, 0, 0, -2, 0, 0)
        self.assertEqual(Particle(4, 0, 0, 0, 0, 0, -2, 0, 0), p)
        p.step()
        self.assertEqual(Particle(2, 0, 0, -2, 0, 0, -2, 0, 0), p)
        p.step()
        self.assertEqual(Particle(-2, 0, 0, -4, 0, 0, -2, 0, 0), p)
        p.step()
        self.assertEqual(Particle(-8, 0, 0, -6, 0, 0, -2, 0, 0), p)

    def test_find_min(self):
        self.assertEqual(0, find_min({
            0: Particle(3, 0, 0, 2, 0, 0, -1, 0, 0),
            1: Particle(4, 0, 0, 0, 0, 0, -2, 0, 0)
        }))
