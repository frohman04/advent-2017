import fileinput
import logging
from typing import List, Tuple
import unittest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Enhancement(object):
    def __init__(self, lines: List[List[bool]], rewrite: List[List[bool]]):
        self._rewrite = rewrite

        if len(lines) == 2 and len(lines[0]) == 2 and len(lines[1]) == 2:
            self._size = 2

            self._values = {
                self._to_bin([lines[0][0], lines[0][1], lines[1][0], lines[1][1]]),
                self._to_bin([lines[0][1], lines[1][1], lines[0][0], lines[1][0]]),
                self._to_bin([lines[1][1], lines[1][0], lines[0][1], lines[0][0]]),
                self._to_bin([lines[1][0], lines[0][0], lines[1][1], lines[0][1]])
            }
        elif len(lines) == 3 and len(lines[0]) == 3 and len(lines[1]) == 3 and len(lines[2]) == 3:
            def get_symmetric(pattern: List[bool]) -> List[List[bool]]:
                return [
                    pattern,
                    list(reversed(pattern)),
                    list(reversed(pattern[0:3])) + list(reversed(pattern[3:6])) + list(reversed(pattern[6:9])),
                    pattern[6:9] + pattern[3:6] + pattern[0:3]
                ]

            self._size = 3

            base = [lines[0][0], lines[0][1], lines[0][2],
                    lines[1][0], lines[1][1], lines[1][2],
                    lines[2][0], lines[2][1], lines[2][2]]
            rotate = [lines[0][2], lines[1][2], lines[2][2],
                      lines[0][1], lines[1][1], lines[2][1],
                      lines[0][0], lines[1][0], lines[2][0]]
            self._values = {self._to_bin(x) for x in (get_symmetric(base) + get_symmetric(rotate))}
        else:
            raise ValueError('Bad input.  Must be 2x2 or 3x3, got {}'.format(lines))

    def _to_bin(self, bits: List[bool]) -> int:
        up = 0
        total = 0
        for bit in bits:
            if bit:
                total += pow(2, up)
            up += 1
        return total

    def size(self):
        return self._size

    def try_match(self, lines: List[List[bool]]) -> List[List[bool]]:
        if self._to_bin(flatten(lines)) in self._values:
            return self._rewrite
        else:
            return None


class Enhancements(object):
    def __init__(self, rules: List[Enhancement]):
        self._rules = rules
        self._rules_2 = [x for x in self._rules if x.size() == 2]
        self._rules_3 = [x for x in self._rules if x.size() == 3]

    def apply(self, grid: List[List[bool]]) -> List[List[bool]]:
        if len(grid) % 2 == 0:
            chunk_size = 2
        elif len(grid) % 3 == 0:
            chunk_size = 3
        else:
            raise ValueError('Grid size not a multiple of 2 or 3 ({})'.format(len(grid)))

        src_chunks = self._build_chunks(grid, chunk_size)
        rewrite_chunks = self._rewrite_chunks(src_chunks, chunk_size)
        return self._reassemble(rewrite_chunks)

    def _build_chunks(self, grid: List[List[bool]], chunk_size: int) -> List[List[List[List[bool]]]]:
        chunks = []  # type: List[List[List[List[bool]]]]
        for y in range(0, len(grid), chunk_size):
            row_chunks = []
            for x in range(0, len(grid), chunk_size):
                chunk = []
                for y_offset in range(chunk_size):
                    chunk += [grid[y + y_offset][x:x + chunk_size]]

                row_chunks += [chunk]
            chunks += [row_chunks]
        return chunks

    def _rewrite_chunks(self, chunks: List[List[List[List[bool]]]], chunk_size: int) -> List[List[List[List[bool]]]]:
        out_chunks = []  # type: List[List[List[List[bool]]]]
        for y in range(len(chunks)):
            row_chunks = []
            for x in range(len(chunks)):
                if chunk_size == 2:
                    rules = self._rules_2
                elif chunk_size == 3:
                    rules = self._rules_3
                else:
                    raise ValueError('Unknown chunk size: {}'.format(chunk_size))

                for rule in rules:
                    rewrite = rule.try_match(chunks[y][x])
                    if rewrite is not None:
                        logger.info('Using rewrite:\n{}'.format(to_str(rewrite)))
                        row_chunks += [rewrite]
                        break
                else:
                    raise ValueError('Unable to find matching rule for {}'.format(chunks[y][x]))
            out_chunks += [row_chunks]
        return out_chunks

    def _reassemble(self, chunks: List[List[List[List[bool]]]]) -> List[List[bool]]:
        out = []  # type: List[List[bool]]
        for chunk_y in range(len(chunks)):
            for y_offset in range(len(chunks[0][0])):
                row = []  # type: List[bool]
                for chunk_x in range(len(chunks[chunk_y])):
                    row += chunks[chunk_y][chunk_x][y_offset]
                out += [row]
        return out


def flatten(l):
    return [item for sublist in l for item in sublist]


def parse_pattern(pattern: str) -> List[List[bool]]:
    rows = pattern.split('/')
    return [[x == '#' for x in row] for row in rows]


def parse_single(line: str) -> Enhancement:
    pattern, replacement = line.split(' => ')
    return Enhancement(parse_pattern(pattern), parse_pattern(replacement))


def parse(lines: List[str]) -> Enhancements:
    return Enhancements([parse_single(line) for line in lines])


def to_str(grid: List[List[bool]]) -> str:
    return '\n'.join([''.join(['#' if x else '.' for x in row]) for row in grid])


def main(lines: List[str], iterations: int=5) -> int:
    pattern = parse_pattern('.#./..#/###')
    rules = parse(lines)

    grid = pattern
    logger.info('Starting grid:\n{}'.format(to_str(grid)))
    for i in range(iterations):
        grid = rules.apply(grid)
        logger.info('Iteration {}:\n{}'.format(i + 1, to_str(grid)))

    return len([x for x in flatten(grid) if x])


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.rstrip()]
    print(main(lines))


class Tests211(unittest.TestCase):
    def test(self):
        self.assertEqual(12, main([
            '../.# => ##./#../...',
            '.#./..#/### => #..#/..../..../#..#'
        ], 2))
