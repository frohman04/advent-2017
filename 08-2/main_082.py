from collections import defaultdict
import fileinput
from typing import Dict, List, Tuple
import unittest


class Condition(object):
    lt = lambda a, b: a < b
    lte = lambda a, b: a <= b
    eq = lambda a, b: a == b
    ne = lambda a, b: a != b
    gte = lambda a, b: a >= b
    gt = lambda a, b: a > b

    def __init__(self, register: str, op: str, amt: int):
        self._register = register
        self._amt = amt

        if op == '<':
            self._op = self.__class__.lt
        elif op == '<=':
            self._op = self.__class__.lte
        elif op == '==':
            self._op = self.__class__.eq
        elif op == '!=':
            self._op = self.__class__.ne
        elif op == '>=':
            self._op = self.__class__.gte
        elif op == '>':
            self._op = self.__class__.gt
        else:
            raise Exception('Unknown op: {}'.format(op))

    def evaluate(self, registers: Dict[str, int]) -> bool:
        return self._op(registers[self._register], self._amt)

    def __eq__(self, other):
        return (type(self) == type(other) and
                self._register == other._register and
                self._amt == other._amt and
                self._op == other._op)


class Command(object):
    inc = lambda a, b: a + b
    dec = lambda a, b: a - b

    def __init__(self, register: str, op: str, amt: int, cond: Condition):
        self._register = register
        self._amt = amt

        if op == 'inc':
            self._op = self.__class__.inc
        elif op == 'dec':
            self._op = self.__class__.dec
        else:
            raise Exception('Unsupported op: {}'.format(op))

        self._cond = cond

    def apply(self, registers: Dict[str, int]) -> Dict[str, int]:
        if self._cond.evaluate(registers):
            registers[self._register] = self._op(registers[self._register], self._amt)
        return registers

    def __eq__(self, other):
        return (type(self) == type(other) and
                self._register == other._register and
                self._amt == other._amt and
                self._op == other._op and
                self._cond == other._cond)


def parse_line(line: str) -> Command:
    parts = line.split('if')

    cond_parts = parts[1].split()
    cond = Condition(cond_parts[0], cond_parts[1], int(cond_parts[2]))

    cmd_parts = parts[0].split()
    cmd = Command(cmd_parts[0], cmd_parts[1], int(cmd_parts[2]), cond)

    return cmd


def parse(lines: List[str]) -> List[Command]:
    return [parse_line(line) for line in lines]


def execute(cmds: List[Command]) -> Tuple[Dict[str, int], int]:
    registers = defaultdict(lambda: 0)  # type: Dict[str, int]

    max_val = 0
    for cmd in cmds:
        registers = cmd.apply(registers)
        max_val = max(max_val, max(registers.values()))

    return registers, max_val


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(execute(parse(lines))[1])


class Tests082(unittest.TestCase):
    def test_parse_line_1(self):
        self.assertEqual(
            Command('a', 'inc', 5, Condition('b', '<', 3)),
            parse_line('a inc 5 if b < 3')
        )

    def test_condition_evaluate_lt(self):
        self.assertEqual(
            True,
            Condition('a', '<', 3).evaluate({'a': 2})
        )

    def test_condition_evaluate_lte(self):
        self.assertEqual(
            True,
            Condition('a', '<=', 3).evaluate({'a': 3})
        )

    def test_condition_evaluate_eq(self):
        self.assertEqual(
            True,
            Condition('a', '==', 3).evaluate({'a': 3})
        )

    def test_condition_evaluate_ne(self):
        self.assertEqual(
            True,
            Condition('a', '!=', 3).evaluate({'a': 2})
        )

    def test_condition_evaluate_gte(self):
        self.assertEqual(
            True,
            Condition('a', '>=', 3).evaluate({'a': 3})
        )

    def test_condition_evaluate_gt(self):
        self.assertEqual(
            True,
            Condition('a', '>', 3).evaluate({'a': 4})
        )

    def test_command_apply_new_register(self):
        self.assertEqual(
            {'a': 4},
            dict(Command('a', 'inc', 4, Condition('a', '==', 0)).apply(defaultdict(lambda: 0)))
        )

    def test_command_apply_skip(self):
        self.assertEqual(
            {'a': 4},
            Command('a', 'inc', 1, Condition('a', '<', 3)).apply({'a': 4})
        )

    def test_command_apply_inc(self):
        self.assertEqual(
            {'a': 4},
            Command('a', 'inc', 1, Condition('a', '==', 3)).apply({'a': 3})
        )

    def test_command_apply_dec(self):
        self.assertEqual(
            {'a': 2},
            Command('a', 'dec', 1, Condition('a', '==', 3)).apply({'a': 3})
        )

    def test_execute_1(self):
        self.assertEqual(
            (
                {
                    'a': 1,
                    'c': -10
                },
                10
            ),
            execute([
                Command('b', 'inc', 5, Condition('a', '>', 1)),
                Command('a', 'inc', 1, Condition('b', '<', 5)),
                Command('c', 'dec', -10, Condition('a', '>=', 1)),
                Command('c', 'inc', -20, Condition('c', '==', 10))
            ])
        )
