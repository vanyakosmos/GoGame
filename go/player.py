from go.matrix import MatrixError
from go.utils import Cell
import random

scores = []


class Player(object):
    def __init__(self, board, level=0):
        self._matrix = board.matrix
        self._board = board
        self._lvl_id = level

        self.levels = [
            ('Another player', self._none),
            ('AI (#1)', self._move_ai_random),
            ('AI (#2)', self._move_ai_heuristic),
            ('AI (#3)', self._move_ai_heuristic2),
            ('AI (#4)', self._move_ai_min_max_1),
            ('AI (#5)', self._move_ai_min_max_2),
        ]

    @property
    def type(self):
        if 0 > self._lvl_id or self._lvl_id >= len(self.levels):
            return self.levels[0][0]
        return self.levels[self._lvl_id][0]

    def move(self, x, y):
        if self._lvl_id == 0:
            return self._none(x, y)
        if self._lvl_id < 1 or len(self.levels) <= self._lvl_id:
            return self.levels[0][1]()
        return self.levels[self._lvl_id][1]()

    def _none(self, x, y):
        self._board.move(x, y)

    def _move_ai_random(self):
        empties = self._board.get_empty_valid_cells()
        x, y = random.choice(empties)
        self._board.move(x, y)

    def _move_ai_heuristic(self):
        empties = self._board.get_empty_valid_cells()
        points = {}

        for x, y in empties:
            surs = list(self._get_surr(x, y))
            points[(x, y)] = 0
            for e in surs:
                if e[0] != Cell.EMPTY and e[0] != self._board.turn:
                    points[(x, y)] += 1
        x, y = max(points, key=lambda key: points[key])
        self._board.move(x, y)

    def _move_ai_heuristic2(self):
        empties = self._board.get_empty_valid_cells()
        points = {}

        for x, y in empties:
            surs = list(self._get_surr(x, y))
            points[(x, y)] = 0
            for e in surs:
                if e[0] == Cell.EMPTY:
                    points[(x, y)] += -1
                elif e[0] == self._board.turn:
                    points[(x, y)] += 1
                else:  # opponent
                    points[(x, y)] += 2
        x, y = max(points, key=lambda key: points[key])
        print(points[(x, y)])
        self._board.move(x, y)

    def _move_ai_min_max_1(self):
        self._move_ai_min_max(2)

    def _move_ai_min_max_2(self):
        self._move_ai_min_max(4)

    def _move_ai_min_max(self, level):
        global scores
        scores = [None] * (level+1)

        empties = self._board.get_empty_valid_cells()
        current_turn = self._board.turn
        points = []
        for x, y in empties:
            self._board.move(x, y)
            new_empties = self._board.get_empty_valid_cells()

            # res = self._min_max_recursive(level-1, False, new_empties, current_turn)
            res = self._min_max_alpha(level-1, False, new_empties, current_turn)

            points.append((res, x, y))
            self._board.undo()

            # print('{turn} >> score: {scr}  > ({x}, {y})'.format(turn=current_turn, scr=res, x=x, y=y))

        res, x, y = max(points, key=lambda a: a[0])
        x, y = self._rnd_point_from_max_seq(points, res)
        print("{turn} >> ({x}, {y})  max score: {scr}\n".format(x=x, y=y, scr=res, turn=current_turn))
        self._board.move(x, y)

    def _min_max_recursive(self, level, use_max, empties, turn):
        if level == 0 or len(empties) == 0:
            return self._evaluate_coolness(turn)
        points = []

        for x, y in empties:
            self._board.move(x, y)
            new_empties = self._board.get_empty_valid_cells()

            points.append(self._min_max_recursive(level - 1, not use_max, new_empties, turn))
            self._board.undo()

        return max(points) if use_max else min(points)

    def _min_max_alpha(self, level, use_max, empties, turn):
        if level == 0 or len(empties) == 0:
            return self._evaluate_coolness(turn)
        points = []

        for x, y in empties:
            # print(scores)
            self._board.move(x, y)
            new_empties = self._board.get_empty_valid_cells()

            res = self._min_max_alpha(level - 1, not use_max, new_empties, turn)
            self._board.undo()

            if scores[level] is not None and \
                    (use_max and res <= scores[level] or
                     not use_max and res >= scores[level]):
                # print("braked")
                break

            points.append(res)

        if scores[level] is not None:
            points.append(scores[level])
        scores[level] = max(points) if use_max else min(points)
        return scores[level]

    def _evaluate_coolness(self, turn):
        b, w = self._board.score[Cell.BLACK], self._board.score[Cell.WHITE]
        return b - w if turn == Cell.BLACK else w - b

    @staticmethod
    def _rnd_point_from_max_seq(seq, max_score):
        out = []
        for score, x, y in seq:
            if score == max_score:
                out.append((x, y))
        return random.choice(out)

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
            # (x - 1, y + 1),
            # (x - 1, y - 1),
            (x + 1, y),
            # (x + 1, y + 1),
            # (x + 1, y - 1),
        )
        return filter(lambda i: bool(i[0]), [
            (self._get_none(a, b), (a, b))
            for a, b in coords])
