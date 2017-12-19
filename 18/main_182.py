import abc
from concurrent.futures import ThreadPoolExecutor, as_completed
import copy
import fileinput
import logging
from queue import Queue, Empty
import time
from typing import Callable, List, Tuple
import unittest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RegisterFile(object):
    def __init__(self, id: int):
        self._file = {
            'pc': 0
        }
        self._file.update({(chr(i), 0) for i in range(ord('a'), ord('z') + 1)})
        self._file['p'] = id

    def next(self):
        self._file['pc'] += 1

    def jump(self, to: int):
        self._file['pc'] = to

    def pc(self) -> int:
        return self._file['pc']

    def set(self, reg: str, val: int):
        self._file[reg] = val

    def get(self, reg: str) -> int:
        return self._file[reg]

    def __str__(self):
        return 'RegisterFile(pc={}, rf={})'.format(
            self._file['pc'],
            {(key, value) for key, value in self._file.items()
             if key == 'p' or (key != 'pc' and value != 0)})


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


class ValOp(Op):
    def __init__(self, val: int):
        self._val = val

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, self._val)

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return type(self) == type(other) and self._val == other._val


class ValValOp(Op):
    def __init__(self, val1: int, val2: int):
        self._val1 = val1
        self._val2 = val2

    def __repr__(self):
        return '{}({}, {})'.format(type(self).__name__, self._val1, self._val2)

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return type(self) == type(other) and self._val1 == other._val1 and self._val2 == other._val2


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


class SndVal(ValOp):
    def __init__(self, val: int):
        super(SndVal, self).__init__(val)
        self._prog = None  # type: Program

    def set_prog(self, prog: 'Program'):
        self._prog = prog

    def perform(self, rf: RegisterFile):
        self._prog.send(self._val)
        rf.next()


class SndReg(RegOp):
    def __init__(self, reg: str):
        super(SndReg, self).__init__(reg)
        self._prog = None  # type: Program

    def set_prog(self, prog: 'Program'):
        self._prog = prog

    def perform(self, rf: RegisterFile):
        self._prog.send(rf.get(self._reg))
        rf.next()


class RcvReg(RegOp):
    def __init__(self, reg: str):
        super(RcvReg, self).__init__(reg)
        self._prog = None  # type: Program

    def set_prog(self, prog: 'Program'):
        self._prog = prog

    def perform(self, rf: RegisterFile):
        rf.set(self._reg, self._prog.recv())
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


class JgzValVal(ValValOp):
    def perform(self, rf: RegisterFile):
        if self._val1 > 0:
            rf.jump(rf.pc() + self._val2)
        else:
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
    def __init__(self, ops: List[Op], id: int):
        self._id = id
        self._rf = RegisterFile(id)
        self._ops = copy.deepcopy(ops)
        for op in self._ops:
            if type(op) in {SndReg, SndVal, RcvReg}:
                op.set_prog(self)
        self._inbox = Queue()
        self._partner = None  # type: Program

        self._waiting = False
        self._num_sent = 0

        self._is_done = False
        self._stop = False

    def set_partner(self, prog: 'Program'):
        self._partner = prog

    def stop(self):
        self._stop = True

    def execute(self):
        logger.info('{}: {}'.format(self._id, self._rf))
        while 0 <= self._rf.pc() < len(self._ops) and not self._stop:
            next_inst = self._ops[self._rf.pc()]
            logger.info('{} > {}'.format(self._id, next_inst))
            next_inst.perform(self._rf)
            logger.info('{}: {}'.format(self._id, self._rf))
        self._is_done = True

    def send(self, val: int):
        self._num_sent += 1
        self._partner._inbox.put(val)

    def recv(self) -> int:
        if self._inbox.empty():
            self._waiting = True
            next = None
            while next is None and not self._stop:
                try:
                    next = self._inbox.get(block=False)
                except Empty:
                    next = None
                    time.sleep(1)
            self._waiting = False
            return next
        else:
            return self._inbox.get()


def parse_single(line: str) -> Op:
    def build_one_arg(val_ctr: Callable[[str, int], Op],
                      reg_ctr: Callable[[str, str], Op],
                      parts: List[str]) -> Op:
        try:
            int(parts[1])
            is_int = True
        except ValueError:
            is_int = False

        if is_int:
            return val_ctr(int(parts[1]))
        else:
            return reg_ctr(parts[1])

    def build_two_arg(val_val_ctr: Callable[[int, int], Op],
                      val_ctr: Callable[[str, int], Op],
                      reg_ctr: Callable[[str, str], Op],
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
            return val_val_ctr(int(parts[1]), int(parts[2]))
        elif is_int_2:
            return val_ctr(parts[1], int(parts[2]))
        else:
            return reg_ctr(parts[1], parts[2])

    parts = line.split()
    if parts[0] == 'snd':
        return build_one_arg(SndVal, SndReg, parts)
    elif parts[0] == 'rcv':
        return RcvReg(parts[1])
    elif parts[0] == 'set':
        return build_two_arg(None, SetVal, SetReg, parts)
    elif parts[0] == 'add':
        return build_two_arg(None, AddVal, AddReg, parts)
    elif parts[0] == 'mul':
        return build_two_arg(None, MulVal, MulReg, parts)
    elif parts[0] == 'mod':
        return build_two_arg(None, ModVal, ModReg, parts)
    elif parts[0] == 'jgz':
        return build_two_arg(JgzValVal, JgzVal, JgzReg, parts)


def parse(lines: List[str]) -> Tuple[Program, Program]:
    ops = [parse_single(x) for x in lines]
    return Program(ops, 0), Program(ops, 1)


class Watchdog(object):
    def __init__(self, prog0: Program, prog1: Program):
        self._prog0 = prog0
        self._prog1 = prog1
        self._stop = False

    def stop(self):
        self._stop = True

    def run(self):
        while not self._stop and not (((self._prog0._waiting and
                                        self._prog0._inbox.empty()) or
                                       self._prog0._is_done) and
                                      ((self._prog1._waiting and
                                        self._prog1._inbox.empty()) or
                                       self._prog1._is_done)):
            logger.info('\n\t'.join(['',
                                     'wd: 0: waiting = {}'.format(self._prog0._waiting),
                                     'wd: 0: empty = {}'.format(self._prog0._inbox.empty()),
                                     'wd: 0: done = {}'.format(self._prog0._is_done),
                                     'wd: 1: waiting = {}'.format(self._prog1._waiting),
                                     'wd: 1: empty = {}'.format(self._prog1._inbox.empty()),
                                     'wd: 1: done = {}'.format(self._prog1._is_done)]))
            time.sleep(1)
        logger.warn('Watchdog triggered!')


def run(prog0: Program, prog1: Program) -> Tuple[int, int]:
    prog0.set_partner(prog1)
    prog1.set_partner(prog0)
    watchdog = Watchdog(prog0, prog1)
    with ThreadPoolExecutor(max_workers=5) as pool:
        watchdog_future = pool.submit(watchdog.run)
        prog0_future = pool.submit(prog0.execute)
        prog1_future = pool.submit(prog1.execute)

        for future in as_completed([watchdog_future, prog0_future, prog1_future]):
            if future == watchdog_future:
                logger.info('Watchdog killing deadlocked programs')
                prog0.stop()
                prog1.stop()
                prog0_future.cancel()
                prog1_future.cancel()
            elif future == prog1_future:
                logger.info('Program 1 halted')
                prog0.stop()
                watchdog.stop()
                prog0_future.cancel()
                watchdog_future.cancel()
            else:
                logger.info('Program 0 halted')
    return prog0._num_sent, prog1._num_sent


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(run(*parse(lines)))


class Tests182(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(
            [
                SetVal('a', 1),
                AddVal('a', 2),
                MulReg('a', 'a'),
                ModVal('a', 5),
                SndReg('a'),
                SetVal('a', 0),
                RcvReg('a'),
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
            ])[0]._ops
        )
