from collections import defaultdict
import fileinput
from typing import Dict, List, Tuple
import unittest


class RawProgram(object):
    def __init__(self, name: str, weight: int, above: List[str]):
        self.name = name
        self.weight = weight
        self.above = above

    def __eq__(self, other):
        return (type(self) == type(other) and
                self.name == other.name and
                self.weight == other.weight and
                self.above == other.above)

    def __repr__(self):
        return 'RawProgram({}, {}, {})'.format(self.name, self.weight, self.above)

    def __str__(self):
        return repr(self)


class Program(object):
    def __init__(self, name: str, weight: int, above: List['Program']):
        self.name = name
        self.weight = weight
        self.above = above

    def __eq__(self, other):
        return (type(self) == type(other) and
                self.name == other.name and
                self.weight == other.weight and
                self.above == other.above)

    def __repr__(self):
        return 'Program({}, {}, {})'.format(self.name, self.weight, self.above)

    def __str__(self):
        return repr(self)

    def to_str(self) -> str:
        return '\n'.join(self._to_str())

    def _flatten(self, l):
        return [item for sublist in l for item in sublist]

    def _to_str(self) -> List[str]:
        lines = [
            'Program({}, {}, ['.format(self.name, self.weight)
        ] + self._flatten([
            s._to_str() for s in self.above
        ]) + [
            '])'
        ]
        return ['  {}'.format(x) for x in lines]


def parse(line: str) -> RawProgram:
    parts = line.split('->')
    name = parts[0].split()[0].strip()
    weight = int(parts[0].split()[1][1:-1].strip())
    if len(parts) > 1:
        above = [x.strip() for x in parts[1].split(',')]
    else:
        above = []
    return RawProgram(name, weight, above)


def parse_all(lines: List[str]) -> Dict[str, RawProgram]:
    programs = {}
    for line in lines:
        program = parse(line)
        programs[program.name] = program
    return programs


def build_tree(programs: Dict[str, RawProgram]) -> Program:
    def find_root() -> RawProgram:
        all_names = set(programs.keys())
        for program in programs.values():
            for name in program.above:
                all_names.remove(name)
        return programs[list(all_names)[0]]

    def transform(name: str) -> Program:
        raw = programs[name]
        return Program(raw.name, raw.weight, [transform(x) for x in raw.above])

    return transform(find_root().name)


def calc_weights(root: Program) -> Program:
    adjusted = [calc_weights(x) for x in root.above]
    return Program(root.name, root.weight + sum([x.weight for x in adjusted]), adjusted)


def find_unbalanced(root: Program) -> Tuple[str, int]:
    answers = [x for x in [find_unbalanced(x) for x in root.above] if x]
    if len(answers) == 1:
        return answers[0]
    elif len(answers) > 1:
        raise Exception('too many answers found: {}'.format(answers))

    weights = defaultdict(lambda: [])
    for node in root.above:
        weights[node.weight] += [node]
    if len(weights) == 2:
        weights = sorted([(len(nodes), weight, nodes) for weight, nodes in weights.items()],
                         key=lambda x: x[0])
        return weights[0][2][0].name, weights[0][1] - weights[1][1]
    elif len(weights) > 2:
        raise Exception('too many distinct weights: {}'.format(len(weights)))


def main(lines: List[str]) -> Tuple[str, int]:
    nodes = parse_all(lines)
    bad_node = find_unbalanced(calc_weights(build_tree(nodes)))
    return bad_node[0], nodes[bad_node[0]].weight - bad_node[1]


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(main(lines))


class Tests072(unittest.TestCase):
    def test_parse_1(self):
        self.assertEqual(RawProgram('foo', 5, []), parse('foo (5)'))

    def test_parse_2(self):
        self.assertEqual(RawProgram('foo', 5, ['bar']), parse('foo (5) -> bar'))

    def test_parse_3(self):
        self.assertEqual(RawProgram('foo', 5, ['bar', 'baz']), parse('foo (5) -> bar, baz'))

    def test_build_tree_1(self):
        self.assertEqual(
            Program('foo', 5, [
                Program('bar', 10, []),
                Program('baz', 15, [
                    Program('snake', 20, [])
                ])
            ]),
            build_tree({
                'foo': RawProgram('foo', 5, ['bar', 'baz']),
                'bar': RawProgram('bar', 10, []),
                'baz': RawProgram('baz', 15, ['snake']),
                'snake': RawProgram('snake', 20, [])
            })
        )

    def test_calc_weights_1(self):
        self.assertEqual(
            Program('tknk', 778, [
                Program('ugml', 251, [
                    Program('gyxo', 61, []),
                    Program('ebii', 61, []),
                    Program('jptl', 61, [])
                ]),
                Program('padx', 243, [
                    Program('pbga', 66, []),
                    Program('havc', 66, []),
                    Program('qoyq', 66, []),
                ]),
                Program('fwft', 243, [
                    Program('ktlj', 57, []),
                    Program('cntj', 57, []),
                    Program('xhth', 57, [])
                ])
            ]),
            calc_weights(
                Program('tknk', 41, [
                    Program('ugml', 68, [
                        Program('gyxo', 61, []),
                        Program('ebii', 61, []),
                        Program('jptl', 61, [])
                    ]),
                    Program('padx', 45, [
                        Program('pbga', 66, []),
                        Program('havc', 66, []),
                        Program('qoyq', 66, []),
                    ]),
                    Program('fwft', 72, [
                        Program('ktlj', 57, []),
                        Program('cntj', 57, []),
                        Program('xhth', 57, [])
                    ])
                ])
            )
        )

    def test_find_unblananced_1(self):
        self.assertEqual(
            ('ugml', 8),
            find_unbalanced(
                Program('tknk', 778, [
                    Program('ugml', 251, [
                        Program('gyxo', 61, []),
                        Program('ebii', 61, []),
                        Program('jptl', 61, [])
                    ]),
                    Program('padx', 243, [
                        Program('pbga', 66, []),
                        Program('havc', 66, []),
                        Program('qoyq', 66, []),
                    ]),
                    Program('fwft', 243, [
                        Program('ktlj', 57, []),
                        Program('cntj', 57, []),
                        Program('xhth', 57, [])
                    ])
                ])
            )
        )

    def test_find_unbalanced_2(self):
        self.assertEqual(
            ('def', 2),
            find_unbalanced(
                Program('abc', 102, [
                    Program('bcd', 52, [
                        Program('def', 27, [
                            Program('fgh', 13, []),
                            Program('ghi', 13, [])
                        ]),
                        Program('efg', 25, [])
                    ]),
                    Program('cde', 50, [])
                ])
            )
        )
