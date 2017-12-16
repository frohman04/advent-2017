import abc
import fileinput
import logging
from typing import List
import unittest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Operation(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def perform(self, init: str) -> str:
        pass


class Spin(Operation):
    def __init__(self, amt: int):
        self._amt = amt

    def __repr__(self):
        return 'Spin({})'.format(self._amt)

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return (type(self) == type(other) and
                self._amt == other._amt)

    def perform(self, init: str):
        return init[-self._amt:] + init[:-self._amt]


def exchange(init: str, idx_1: int, idx_2: int) -> str:
    return (init[:idx_1] +
            init[idx_2] +
            init[idx_1 + 1:idx_2] +
            init[idx_1] +
            init[idx_2 + 1:])


class Exchange(Operation):
    def __init__(self, pos_1: int, pos_2: int):
        if pos_1 <= pos_2:
            self._pos_1 = pos_1
            self._pos_2 = pos_2
        else:
            self._pos_1 = pos_2
            self._pos_2 = pos_1

    def __repr__(self):
        return 'Exchange({}, {})'.format(self._pos_1, self._pos_2)

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return (type(self) == type(other) and
                self._pos_1 == other._pos_1 and
                self._pos_2 == other._pos_2)

    def perform(self, init: str):
        return exchange(init, self._pos_1, self._pos_2)


class Partner(Operation):
    def __init__(self, name_1: str, name_2: str):
        self._name_1 = name_1
        self._name_2 = name_2

    def __repr__(self):
        return 'Parnter({}, {})'.format(self._name_1, self._name_2)

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return (type(self) == type(other) and
                self._name_1 == other._name_1 and
                self._name_2 == other._name_2)

    def perform(self, init: str):
        idx_1 = init.index(self._name_1)
        idx_2 = init.index(self._name_2)
        if idx_2 <= idx_1:
            temp = idx_1
            idx_1 = idx_2
            idx_2 = temp
        return exchange(init, idx_1, idx_2)


def parse_single(raw_op: str) -> Operation:
    if raw_op.startswith('s'):
         return Spin(int(raw_op[1:]))
    elif raw_op.startswith('x'):
        data = raw_op[1:].split('/')
        if len(data) != 2:
            raise Exception('Wrong number of arguments (got {})'.format(data))
        return Exchange(int(data[0]), int(data[1]))
    elif raw_op.startswith('p'):
        data = raw_op[1:].split('/')
        if len(data) != 2:
            raise Exception('Wrong number of arguments (got {})'.format(data))
        return Partner(data[0], data[1])
    else:
        raise Exception('Unknown op: {}'.format(raw_op))


def parse(raw_ops: str) -> List[Operation]:
    return [parse_single(x) for x in raw_ops.split(',')]


def execute(ops: List[Operation], init: str='abcdefghijklmnop') -> str:
    curr = init
    for op in ops:
        curr = op.perform(curr)
    return curr


def execute_all(ops: List[Operation], init: str='abcdefghijklmnop') -> str:
    curr = init
    period = 0
    values = [init]
    is_first = True
    while init != curr or is_first:
        curr = execute(ops, curr)

        period += 1
        values += [curr]
        is_first = False

    logger.info('Found loop after {} iterations'.format(period))
    return values[1_000_000_000 % period]


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(execute_all(parse(lines[0])))


class Tests162(unittest.TestCase):
    def test_parse_s(self):
        self.assertEqual(Spin(5), parse_single('s5'))

    def test_parse_e(self):
        self.assertEqual(Exchange(3, 21), parse_single('x3/21'))

    def test_parse_p(self):
        self.assertEqual(Partner('a', 'b'), parse_single('pa/b'))

    def test_parse(self):
        self.assertEqual([Spin(5), Exchange(3, 21), Partner('a', 'b')],
                         parse('s5,x3/21,pa/b'))

    def test_spin(self):
        self.assertEqual('eabcd', Spin(1).perform('abcde'))

    def test_exchange(self):
        self.assertEqual('eabdc', Exchange(3, 4).perform('eabcd'))

    def test_partner(self):
        self.assertEqual('baedc', Partner('e', 'b').perform('eabdc'))

    def test_execute(self):
        self.assertEqual('baedc', execute([Spin(1), Exchange(3, 4), Partner('e', 'b')], 'abcde'))
