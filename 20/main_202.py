from collections import defaultdict
import datetime
import fileinput
import logging
import re
from typing import Dict, List, Set, Tuple
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
                  self.p[2] + self.v[2])

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


def get_final_orders(particles: Dict[int, Particle]) -> Tuple[List[int], List[int], List[int]]:
    return (
        [i for i, p in sorted(particles.items(), key=lambda x: (x[1].a[0], x[1].v[0]))],
        [i for i, p in sorted(particles.items(), key=lambda x: (x[1].a[1], x[1].v[1]))],
        [i for i, p in sorted(particles.items(), key=lambda x: (x[1].a[2], x[1].v[2]))]
    )


def get_orders(particles: Dict[int, Particle]) -> Tuple[List[int], List[int], List[int]]:
    return (
        [i for i, p in sorted(particles.items(), key=lambda x: x[1].p[0])],
        [i for i, p in sorted(particles.items(), key=lambda x: x[1].p[1])],
        [i for i, p in sorted(particles.items(), key=lambda x: x[1].p[2])]
    )


def is_in_order(particles: Dict[int, Particle],
                final_x_order: List[int],
                final_y_order: List[int],
                final_z_order: List[int]) -> bool:
    x_order, y_order, z_order = get_orders(particles)
    xs = set(x_order)
    ys = set(y_order)
    zs = set(z_order)
    final_x_order = [x for x in final_x_order if x in xs]
    final_y_order = [y for y in final_y_order if y in ys]
    final_z_order = [z for z in final_z_order if z in zs]
    return x_order == final_x_order and y_order == final_y_order and z_order == final_z_order


def flatten(l: List[Set[int]]) -> List[int]:
    return [item for sublist in l for item in sublist]


def find_collisions(particles: Dict[int, Particle]) -> List[int]:
    seen = defaultdict(lambda: set([]))  # type: Dict[Tuple[int, int, int], Set[int]]

    for i, particle in particles.items():
        seen[particle.p].add(i)

    return flatten([parts for pos, parts in seen.items() if len(parts) > 1])


def collide(particles: Dict[int, Particle]) -> int:
    x_order, y_order, z_order = get_final_orders(particles)

    iteration = 0
    start_time = datetime.datetime.now()
    chunk_start_time = start_time
    while not is_in_order(particles, x_order, y_order, z_order):
        for particle in particles.values():
            particle.step()

        collisions = find_collisions(particles)
        if len(collisions) > 0:
            logger.info('Found {} collisions in iteration {}'.format(len(collisions), iteration))
            for i in collisions:
                del particles[i]

        iteration += 1

        if iteration % 1000 == 0:
            next_start_time = datetime.datetime.now()
            logger.info('Iteration {}, {} particles remaining ({} elapsed, {} last chunk)'.format(
                iteration,
                len(particles),
                next_start_time - start_time,
                next_start_time - chunk_start_time
            ))
            chunk_start_time = next_start_time

    return len(particles)


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.rstrip()]
    print(collide(parse(lines)))


class Tests202(unittest.TestCase):
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

    def test_collide(self):
        self.assertEqual(1, collide(
            {
                0: Particle(-6, 0, 0, 3, 0, 0, 0, 0, 0),
                1: Particle(-4, 0, 0, 2, 0, 0, 0, 0, 0),
                2: Particle(-2, 0, 0, 1, 0, 0, 0, 0, 0),
                3: Particle(3, 0, 0, -1, 0, 0, 0, 0, 0)
            }
        ))
