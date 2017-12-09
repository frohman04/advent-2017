import fileinput
from typing import Dict, List
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


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(build_tree(parse_all(lines)).name)


class Tests071(unittest.TestCase):
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
