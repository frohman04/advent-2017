from collections import deque
import fileinput
from typing import Dict, List, Set
import unittest


def parse_input(lines: List[str]) -> Dict[int, List[int]]:
    out = {}  # type: Dict[int, List[int]]
    for line in lines:
        parts = line.split('<->')
        source = int(parts[0].strip())
        sinks = [int(x.strip()) for x in parts[1].strip().split(',')]
        out[source] = sinks
    return out


def visit_nodes(edges: Dict[int, List[int]], start: int) -> Set[int]:
    to_visit = deque([start])
    visited = set([start])
    while len(to_visit) > 0:
        node = to_visit.pop()
        for other in edges[node]:
            if other not in visited:
                visited.add(other)
                to_visit.appendleft(other)
    return visited


def count_groups(edges: Dict[int, List[int]]) -> int:
    groups = set([])  # Set[Tuple[]]
    for node in edges.keys():
        groups.add(tuple(sorted(visit_nodes(edges, node))))
    return len(groups)


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(count_groups(parse_input(lines)))


class Tests122(unittest.TestCase):
    def test_parse_input_1(self):
        self.assertDictEqual(
            {
                0: [2],
                1: [1],
                2: [0, 3, 4],
                3: [2, 4],
                4: [2, 3, 6],
                5: [6],
                6: [4, 5]
            },
            parse_input([
                '0 <-> 2',
                '1 <-> 1',
                '2 <-> 0, 3, 4',
                '3 <-> 2, 4',
                '4 <-> 2, 3, 6',
                '5 <-> 6',
                '6 <-> 4, 5'
            ])
        )

    def test_visit_nodes_1(self):
        self.assertEqual(
            set([0, 2, 3, 4, 5, 6]),
            visit_nodes({
                0: [2],
                1: [1],
                2: [0, 3, 4],
                3: [2, 4],
                4: [2, 3, 6],
                5: [6],
                6: [4, 5]
            }, 0)
        )

    def test_visit_nodes_2(self):
        self.assertEqual(
            set([1]),
            visit_nodes({
                0: [2],
                1: [1],
                2: [0, 3, 4],
                3: [2, 4],
                4: [2, 3, 6],
                5: [6],
                6: [4, 5]
            }, 1)
        )

    def test_count_groups_1(self):
        self.assertEqual(
            2,
            count_groups({
                0: [2],
                1: [1],
                2: [0, 3, 4],
                3: [2, 4],
                4: [2, 3, 6],
                5: [6],
                6: [4, 5]
            })
        )
