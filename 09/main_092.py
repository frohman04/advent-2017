import fileinput
from typing import Dict, List, Tuple
import unittest


class Stack(object):
    def __init__(self):
        self._storage = []

    def push(self, item):
        self._storage += [item]

    def pop(self):
        return self._storage.pop()

    def peek(self):
        return self._storage[-1]

    def __len__(self):
        return len(self._storage)

    def __str__(self):
        return str(self._storage)

    def __repr__(self):
        return repr(self._storage)


def parse(stream: str) -> int:
    stack = Stack()
    total = 0

    for char in stream:
        if len(stack) > 0 and stack.peek() == '!':
            stack.pop()
        elif char == '!':
            stack.push(char)
        elif char in ['{', '<'] and (len(stack) == 0 or stack.peek() != '<'):
            stack.push(char)
        elif char == '>' and stack.peek() == '<':
            stack.pop()
        elif char == '}' and stack.peek() == '{':
            stack.pop()
        elif len(stack) > 0 and stack.peek() == '<':
            total += 1

    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(parse(lines[0]))


class Tests092(unittest.TestCase):
    def test_parse_1(self):
        self.assertEqual(0, parse('{}'))

    def test_parse_2(self):
        self.assertEqual(0, parse('<>'))

    def test_parse_3(self):
        self.assertEqual(1, parse('{<a>}'))

    def test_parse_4(self):
        self.assertEqual(0, parse('{<!a>}'))

    def test_parse_5(self):
        self.assertEqual(4, parse('{<a>,<a>,<a>,<a>}'))

    def test_parse_6(self):
        self.assertEqual(8, parse('{{<ab>},{<ab>},{<ab>},{<ab>}}'))

    def test_parse_7(self):
        self.assertEqual(0, parse('{{<!!>},{<!!>},{<!!>},{<!!>}}'))

    def test_parse_8(self):
        self.assertEqual(17, parse('{{<a!>},{<a!>},{<a!>},{<ab>}}'))
