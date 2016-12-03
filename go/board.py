from collections import namedtuple
from copy import copy
from enum import Enum

from .matrix import Matrix, MatrixError


class BoardError(Exception):
    pass


class Cell(Enum):
    BLACK = 'black'
    WHITE = 'white'
    EMPTY = 'empty'


class Board(Matrix):

    TURNS = (Cell.BLACK, Cell.WHITE)

    State = namedtuple('State', ['board', 'turn', 'score'])

    def __init__(self, width):
        super(Board, self).__init__(width, width, Cell.EMPTY)

        self._turn = Cell.BLACK

        self._score = {
            Cell.BLACK: 0,
            Cell.WHITE: 0,
        }

        self._history = []
        self._redo = []

    @property
    def turn(self):
        return self._turn

    @property
    def score(self):
        return {
            'black': self._score[Cell.BLACK],
            'white': self._score[Cell.WHITE],
        }

    @property
    def _next_turn(self):
        return self.TURNS[self._turn is Cell.BLACK]

    def move(self, x, y):
        if self[x, y] is not Cell.EMPTY:
            raise BoardError('Cannot move on top of another piece!')

        self._push_history()
        self[x, y] = self._turn

        taken = self._take_pieces(x, y)

        if taken == 0:
            self._check_for_suicide(x, y)

        self._check_for_ko()

        self._flip_turn()
        self._redo = []

    def _check_for_suicide(self, x, y):
        if self.count_liberties(x, y) == 0:
            self._pop_history()
            raise BoardError('Cannot play on location with no liberties!')

    def _check_for_ko(self):
        try:
            if self._matrix == self._history[-2][0]:
                self._pop_history()
                raise BoardError('Cannot make a move that is redundant!')
        except IndexError:
            pass

    def _take_pieces(self, x, y):
        scores = []
        for p, (x1, y1) in self._get_surrounding(x, y):
            if p is self._next_turn and self.count_liberties(x1, y1) == 0:
                score = self._kill_group(x1, y1)
                scores.append(score)
                self._tally(score)
        return sum(scores)

    def _flip_turn(self):
        self._turn = self._next_turn
        return self._turn

    @property
    def _state(self):
        return self.State(self.copy.matrix, self._turn, copy(self._score))

    def _load_state(self, state):
        self._matrix, self._turn, self._score = state

    def _push_history(self):
        self._history.append(self._state)

    def _pop_history(self):
        current_state = self._state
        try:
            self._load_state(self._history.pop())
            return current_state
        except IndexError:
            return None

    def undo(self):
        state = self._pop_history()
        if state:
            self._redo.append(state)
            return state
        else:
            raise BoardError('No moves to undo!')

    def redo(self):
        try:
            self._push_history()
            self._load_state(self._redo.pop())
        except IndexError:
            self._pop_history()
            raise BoardError('No undone moves to redo!')

    def _tally(self, score):
        self._score[self._turn] += score

    def _get_none(self, x, y):
        try:
            return self[x, y]
        except MatrixError:
            return None

    def _get_surrounding(self, x, y):
        coords = (
            (x, y - 1),
            (x + 1, y),
            (x, y + 1),
            (x - 1, y),
        )
        return filter(lambda i: bool(i[0]), [
            (self._get_none(a, b), (a, b))
            for a, b in coords
        ])

    def _get_group(self, x, y, traversed):
        loc = self[x, y]

        locations = [
            (p, (a, b))
            for p, (a, b) in self._get_surrounding(x, y)
            if p is loc and (a, b) not in traversed
        ]

        traversed.add((x, y))

        if locations:
            return traversed.union(*[
                self._get_group(a, b, traversed)
                for _, (a, b) in locations
            ])
        else:
            return traversed

    def get_group(self, x, y):
        if self[x, y] not in self.TURNS:
            raise BoardError('Can only get group for black or white location')

        return self._get_group(x, y, set())

    def _kill_group(self, x, y):
        if self[x, y] not in self.TURNS:
            raise BoardError('Can only kill black or white group')

        group = self.get_group(x, y)
        score = len(group)

        for x1, y1 in group:
            self[x1, y1] = Cell.EMPTY

        return score

    def _get_liberties(self, x, y, traversed):
        loc = self[x, y]

        if loc is Cell.EMPTY:
            return {(x, y)}
        else:
            locations = [
                (p, (a, b))
                for p, (a, b) in self._get_surrounding(x, y)
                if (p is loc or p is Cell.EMPTY) and (a, b) not in traversed
            ]

            traversed.add((x, y))

            if locations:
                return set.union(*[
                    self._get_liberties(a, b, traversed)
                    for _, (a, b) in locations
                ])
            else:
                return set()

    def get_liberties(self, x, y):
        return self._get_liberties(x, y, set())

    def count_liberties(self, x, y):
        return len(self.get_liberties(x, y))
