from enum import Enum
import logging
from typing import List
import unittest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Direction(Enum):
    LEFT = 1
    RIGHT = 2


class State(object):
    def __init__(self, name):
        self._name = name
        self._edges = []  # type: List['Edge']

    def add_edge(self, edge: 'Edge'):
        self._edges += [edge]

    def get_edge(self, value: int) -> 'Edge':
        selected = [x for x in self._edges if x.value == value]
        if len(selected) != 1:
            raise ValueError('Must be only one edge found for query value {}, got {}'.format(
                value, selected))
        return selected[0]

    def __repr__(self):
        return 'Node({})'.format(self._name)

    def __str__(self):
        return 'Node({}, edges={})'.format(self._name, self._edges)


class Edge(object):
    def __init__(self, value: int, write: int, dir: Direction, next: State):
        self.value = value
        self.write = write
        self.dir = dir
        self.next = next

    def __repr__(self):
        return 'Edge({}, {}, {}, {})'.format(self.value, self.write, self.dir, self.next)

    def __str__(self):
        return repr(self)


class Machine(object):
    def __init__(self, start_state: State):
        self._left = []  # type: List[int]
        self._right = []  # type: List[int]
        self._current = 0
        self._state = start_state

    def step(self):
        edge = self._state.get_edge(self._current)
        if edge.dir == Direction.LEFT:
            self._right.append(edge.write)
            if len(self._left) > 0:
                self._current = self._left.pop()
            else:
                self._current = 0
        elif edge.dir == Direction.RIGHT:
            self._left.append(edge.write)
            if len(self._right) > 0:
                self._current = self._right.pop()
            else:
                self._current = 0
        else:
            raise ValueError('Unknown direction: {}'.format(edge.dir))

        self._state = edge.next

    def num_ones(self) -> 1:
        return len([x for x in (self._left + self._right + [self._current]) if x == 1])


def run(machine: Machine, iterations: int) -> int:
    for _ in range(iterations):
        if (_ + 1) % 1_000_000 == 0:
            logger.info('Iteration {} of {}'.format(_ + 1, iterations))
        machine.step()
    return machine.num_ones()


if __name__ == '__main__':
    a = State('a')
    b = State('b')
    c = State('c')
    d = State('d')
    e = State('e')
    f = State('f')
    a.add_edge(Edge(0, 1, Direction.RIGHT, b))
    a.add_edge(Edge(1, 0, Direction.LEFT, c))
    b.add_edge(Edge(0, 1, Direction.LEFT, a))
    b.add_edge(Edge(1, 1, Direction.RIGHT, c))
    c.add_edge(Edge(0, 1, Direction.RIGHT, a))
    c.add_edge(Edge(1, 0, Direction.LEFT, d))
    d.add_edge(Edge(0, 1, Direction.LEFT, e))
    d.add_edge(Edge(1, 1, Direction.LEFT, c))
    e.add_edge(Edge(0, 1, Direction.RIGHT, f))
    e.add_edge(Edge(1, 1, Direction.RIGHT, a))
    f.add_edge(Edge(0, 1, Direction.RIGHT, a))
    f.add_edge(Edge(1, 1, Direction.RIGHT, e))
    print(run(Machine(a), 12_134_527))


class Tests251(unittest.TestCase):
    def test(self):
        a = State('a')
        b = State('b')
        a.add_edge(Edge(0, 1, Direction.RIGHT, b))
        a.add_edge(Edge(1, 0, Direction.LEFT, b))
        b.add_edge(Edge(0, 1, Direction.LEFT, a))
        b.add_edge(Edge(1, 1, Direction.RIGHT, a))
        self.assertEqual(3, run(Machine(a), 6))
