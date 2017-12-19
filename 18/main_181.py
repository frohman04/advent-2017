import abc
import fileinput
import logging
import sys
from typing import List
import unittest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RegisterFile(object):
    def __init__(self):
        self._file = {
            'pc': 0,
            'snd': 0
        }
        self._file.update({(chr(i), 0) for i in range(ord('a'), ord('z') + 1)})

    def next(self):
        self._file['pc'] += 1

    def jump(self, to: int):
        self._file['pc'] = to

    def pc(self) -> int:
        return self._file['pc']

    def send(self, val: int):
        self._file['snd'] = val

    def receive(self) -> int:
        return self._file['snd']

    def set(self, reg: str, val: int):
        self._file[reg] = val

    def get(self, reg: str) -> int:
        return self._file[reg]

    def __str__(self):
        return 'RegisterFile(pc={}, snd={}, rf={})'.format(
            self._file['pc'],
            self._file['snd'],
            {(key, value) for key, value in self._file.items()
             if key not in {'pc', 'snd'} and value != 0})


class Op(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def perform(self, rf: RegisterFile):
        pass


class RegOp(Op):
    def __init__(self, reg: str):
        self._reg = reg

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, self._reg)

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return type(self) == type(other) and self._reg == other._reg


class RegValOp(Op):
    def __init__(self, reg: str, val: int):
        self._reg = reg
        self._val = val

    def __repr__(self):
        return '{}({}, {})'.format(type(self).__name__, self._reg, self._val)

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return type(self) == type(other) and self._reg == other._reg and self._val == other._val


class RegRegOp(Op):
    def __init__(self, reg1: str, reg2: str):
        self._reg1 = reg1
        self._reg2 = reg2

    def __repr__(self):
        return '{}({}, {})'.format(type(self).__name__, self._reg1, self._reg1)

    def __eq__(self, other):
        return type(self) == type(other) and self._reg1 == other._reg1 and self._reg2 == other._reg2


class Snd(RegOp):
    def perform(self, rf: RegisterFile):
        rf.send(rf.get(self._reg))
        rf.next()


class Rcv(RegOp):
    def perform(self, rf: RegisterFile):
        if rf.get(self._reg) != 0:
            print(rf.receive())
            sys.exit(0)
        rf.next()


class SetVal(RegValOp):
    def perform(self, rf: RegisterFile):
        rf.set(self._reg, self._val)
        rf.next()


class SetReg(RegRegOp):
    def perform(self, rf: RegisterFile):
        rf.set(self._reg1, rf.get(self._reg2))
        rf.next()


class AddVal(RegValOp):
    def perform(self, rf: RegisterFile):
        rf.set(self._reg, rf.get(self._reg) + self._val)
        rf.next()


class AddReg(RegRegOp):
    def perform(self, rf: RegisterFile):
        rf.set(self._reg1, rf.get(self._reg1) + rf.get(self._reg2))
        rf.next()


class MulVal(RegValOp):
    def perform(self, rf: RegisterFile):
        rf.set(self._reg, rf.get(self._reg) * self._val)
        rf.next()


class MulReg(RegRegOp):
    def perform(self, rf: RegisterFile):
        rf.set(self._reg1, rf.get(self._reg1) * rf.get(self._reg2))
        rf.next()


class ModVal(RegValOp):
    def perform(self, rf: RegisterFile):
        rf.set(self._reg, rf.get(self._reg) % self._val)
        rf.next()


class ModReg(RegRegOp):
    def perform(self, rf: RegisterFile):
        rf.set(self._reg1, rf.get(self._reg1) % rf.get(self._reg2))
        rf.next()


class JgzVal(RegValOp):
    def perform(self, rf: RegisterFile):
        if rf.get(self._reg) > 0:
            rf.jump(rf.pc() + self._val)
        else:
            rf.next()


class JgzReg(RegRegOp):
    def perform(self, rf: RegisterFile):
        if rf.get(self._reg1) > 0:
            rf.jump(rf.pc() + rf.get(self._reg2))
        else:
            rf.next()


class Program(object):
    def __init__(self, inst: List[Op]):
        self._rf = RegisterFile()
        self._inst = inst

    def execute(self):
        logger.info(self._rf)
        while 0 <= self._rf.pc() < len(self._inst):
            next_inst = self._inst[self._rf.pc()]
            logger.info('> {}'.format(next_inst))
            next_inst.perform(self._rf)
            logger.info(self._rf)


def parse_single(line: str) -> Op:
    def build_two_arg(val_ctr, reg_ctr, parts: List[str]) -> Op:
        try:
            int(parts[2])
            is_int = True
        except ValueError:
            is_int = False

        if is_int:
            return val_ctr(parts[1], int(parts[2]))
        else:
            return reg_ctr(parts[1], parts[2])

    parts = line.split()
    if parts[0] == 'snd':
        return Snd(parts[1])
    elif parts[0] == 'rcv':
        return Rcv(parts[1])
    elif parts[0] == 'set':
        return build_two_arg(SetVal, SetReg, parts)
    elif parts[0] == 'add':
        return build_two_arg(AddVal, AddReg, parts)
    elif parts[0] == 'mul':
        return build_two_arg(MulVal, MulReg, parts)
    elif parts[0] == 'mod':
        return build_two_arg(ModVal, ModReg, parts)
    elif parts[0] == 'jgz':
        return build_two_arg(JgzVal, JgzReg, parts)


def parse(lines: List[str]) -> Program:
    return Program([parse_single(x) for x in lines])


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(parse(lines).execute())


class Tests181(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(
            [
                SetVal('a', 1),
                AddVal('a', 2),
                MulReg('a', 'a'),
                ModVal('a', 5),
                Snd('a'),
                SetVal('a', 0),
                Rcv('a'),
                JgzVal('a', -1),
                SetVal('a', 1),
                JgzVal('a', -2)
            ],
            parse([
                'set a 1',
                'add a 2',
                'mul a a',
                'mod a 5',
                'snd a',
                'set a 0',
                'rcv a',
                'jgz a -1',
                'set a 1',
                'jgz a -2'
            ])._inst
        )
