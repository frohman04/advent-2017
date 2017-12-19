import fileinput
import logging
from typing import List
import unittest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_start(first_line: str) -> int:
    return first_line.index('|')


def traverse(cells: List[str], start_x: int, start_y: int) -> str:
    logger.info('Starting at ({}, {})'.format(start_x, start_y))

    curr_x = start_x
    curr_y = start_y
    delta_x = 0
    delta_y = 1

    found = ''

    curr_cell = cells[curr_y][curr_x]
    while curr_cell != ' ':
        if curr_cell == '+':
            if delta_x == 0:
                delta_y = 0
                if curr_x + 1 < len(cells[curr_y]) and cells[curr_y][curr_x + 1] != ' ':
                    logger.info('Turning right at ({}, {})'.format(curr_x, curr_y))
                    delta_x = 1
                else:
                    logger.info('Turning left at ({}, {})'.format(curr_x, curr_y))
                    delta_x = -1
            else:
                delta_x = 0
                if curr_y + 1 < len(cells) and curr_x < len(cells[curr_y + 1]) and cells[curr_y + 1][curr_x] != ' ':
                    logger.info('Turning up at ({}, {})'.format(curr_x, curr_y))
                    delta_y = 1
                else:
                    logger.info('Turning down at ({}, {})'.format(curr_x, curr_y))
                    delta_y = -1
        elif 'A' <= curr_cell <= 'Z':
            logger.info('Found "{}" at ({}, {})'.format(curr_cell, curr_x, curr_y))
            found += curr_cell

        curr_x += delta_x
        curr_y += delta_y
        curr_cell = cells[curr_y][curr_x]

    return found


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.rstrip()]
    print(traverse(lines, find_start(lines[0]), 0))


class Tests191(unittest.TestCase):
    input = '''
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
'''.strip('\n').split('\n')

    def test_find_first(self):
        self.assertEqual(5, find_start(Tests191.input[0]))

    def test_traverse(self):
        self.assertEqual('ABCDEF', traverse(Tests191.input, 5, 0))
