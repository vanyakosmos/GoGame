from go.utils import BoardError
from go.matrix import MatrixError
from go.utils import Cell
import random


class Player(object):
    def __init__(self, board, level=0):
        self._matrix = board.matrix
        self._board = board
        self._lvl_id = level

        self.levels = [
            ('Another player', self._none),
            ('AI (#1)', self._move_ai_random),
            ('AI (#2)', self._move_ai_minmax),
            ('AI (#3)', self._move_ai_minmax2),
            # ('AI (#4)', self._move_ai_ko_battle),
            # ('AI (#5)', self._move_ai_castle),
        ]

    @property
    def type(self):
        if 0 > self._lvl_id or self._lvl_id >= len(self.levels):
            return self.levels[0][0]
        return self.levels[self._lvl_id][0]

    def _get_none(self, x, y):
        try:
            return self._board[x, y]
        except MatrixError:
            return None

    def _get_surr(self, x, y):
        coords = (
            (x, y + 1),
            (x, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x - 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
            (x + 1, y - 1),
        )
        return filter(lambda i: bool(i[0]), [
            (self._get_none(a, b), (a, b))
            for a, b in coords])

    def move(self):
        if 0 > self._lvl_id or self._lvl_id >= len(self.levels):
            return self.levels[0][1]()
        return self.levels[self._lvl_id][1]()

    def _none(self):
        pass

    def _move_ai_random(self):
        empties = self._board.get_empty_valid_cells()
        x, y = random.choice(empties)
        self._board.move(x, y)

    def _move_ai_minmax(self):
        empties = self._board.get_empty_valid_cells()
        points = {}

        for x, y in empties:
            surs = list(self._board._get_surrounding(x, y))
            points[(x, y)] = 0
            for e in surs:
                if e[0] != Cell.EMPTY and e[0] != self._board.turn:
                    points[(x, y)] += 1
        x, y = max(points, key=lambda key: points[key])
        self._board.move(x, y)

    def _move_ai_minmax2(self):
        empties = self._board.get_empty_valid_cells()
        points = {}

        for x, y in empties:
            surs = list(self._board._get_surrounding(x, y))
            points[(x, y)] = 0
            for e in surs:
                if e[0] == Cell.EMPTY:
                    points[(x, y)] += -1
                elif e[0] == self._board.turn:
                    points[(x, y)] += 3
                else:  # opponent
                    points[(x, y)] += 3
        x, y = max(points, key=lambda key: points[key])
        print(points[(x, y)])
        self._board.move(x, y)

    def _move_ai_ko_battle(self):
        pass

    def _move_ai_castle(self):
        pass



