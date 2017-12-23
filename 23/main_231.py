import abc
import fileinput
import logging
from typing import Callable, List, Union
import unittest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RegisterFile(object):
    def __init__(self):
        self._file = {
            'pc': 0,
            'count': 0
        }
        self._file.update({(chr(i), 0) for i in range(ord('a'), ord('z') + 1)})

    def next(self):
        self._file['pc'] += 1

    def jump(self, to: int):
        self._file['pc'] = to

    def pc(self) -> int:
        return self._file['pc']

    def set(self, reg: str, val: int):
        self._file[reg] = val

    def get(self, reg: Union[str, int]) -> int:
        if type(reg) == int:
            return reg
        else:
            return self._file[reg]

    def count(self):
        self._file['count'] += 1

    def get_count(self) -> int:
        return self._file['count']

    def __str__(self):
        return 'RegisterFile(pc={}, count={}, rf={})'.format(
            self._file['pc'],
            self._file['count'],
            {(key, value) for key, value in self._file.items()
             if key not in {'pc', 'count'} and value != 0})


class Op(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def perform(self, rf: RegisterFile):
        pass


class RegRegOp(Op):
    def __init__(self, reg1: Union[str, int], reg2: Union[str, int]):
        self._reg1 = reg1
        self._reg2 = reg2

    def __repr__(self):
        return '{}({}, {})'.format(type(self).__name__, self._reg1, self._reg2)

    def __eq__(self, other):
        return type(self) == type(other) and self._reg1 == other._reg1 and self._reg2 == other._reg2


class Set(RegRegOp):
    def perform(self, rf: RegisterFile):
        rf.set(self._reg1, rf.get(self._reg2))
        rf.next()


class Sub(RegRegOp):
    def perform(self, rf: RegisterFile):
        rf.set(self._reg1, rf.get(self._reg1) - rf.get(self._reg2))
        rf.next()


class Mul(RegRegOp):
    def perform(self, rf: RegisterFile):
        rf.set(self._reg1, rf.get(self._reg1) * rf.get(self._reg2))
        rf.next()

        rf.count()


class Jnz(RegRegOp):
    def perform(self, rf: RegisterFile):
        if rf.get(self._reg1) != 0:
            rf.jump(rf.pc() + rf.get(self._reg2))
        else:
            rf.next()


class Program(object):
    def __init__(self, inst: List[Op]):
        self._rf = RegisterFile()
        self._inst = inst

    def execute(self) -> int:
        logger.info(self._rf)
        while 0 <= self._rf.pc() < len(self._inst):
            next_inst = self._inst[self._rf.pc()]
            logger.info('> {}'.format(next_inst))
            next_inst.perform(self._rf)
            logger.info(self._rf)

        return self._rf.get_count()


def parse_single(line: str) -> Op:
    def build_two_arg(ctr: Callable[[Union[str, int], Union[str, int]], Op],
                      parts: List[str]) -> Op:
        try:
            int(parts[1])
            is_int_1 = True
        except ValueError:
            is_int_1 = False

        try:
            int(parts[2])
            is_int_2 = True
        except ValueError:
            is_int_2 = False

        if is_int_1 and is_int_2:
            return ctr(int(parts[1]), int(parts[2]))
        elif is_int_2:
            return ctr(parts[1], int(parts[2]))
        elif is_int_1:
            return ctr(int(parts[1]), parts[2])
        else:
            return ctr(parts[1], parts[2])

    parts = line.split()
    if parts[0] == 'set':
        return build_two_arg(Set, parts)
    elif parts[0] == 'sub':
        return build_two_arg(Sub, parts)
    elif parts[0] == 'mul':
        return build_two_arg(Mul, parts)
    elif parts[0] == 'jnz':
        return build_two_arg(Jnz, parts)


def parse(lines: List[str]) -> Program:
    return Program([parse_single(x) for x in lines])


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(parse(lines).execute())


class Tests231(unittest.TestCase):
    pass
