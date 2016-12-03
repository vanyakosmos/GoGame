from copy import copy


class MatrixError(Exception):
    pass


class Matrix(object):
    def __init__(self, width, height, empty=None):
        self.width = width
        self.height = height
        self._empty = empty

        self._reset()

    def _reset(self):
        self._matrix = [
            [self._empty for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def _check_index(self, x, y):
        if (
            x < 1 or
            x > self.width or
            y < 1 or
            y > self.height
        ):
            raise MatrixError('Index is not within array dimensions {w}x{h}'.format(
                x=x, y=y, w=self.width, h=self.height
            ))

    @staticmethod
    def _zero_index(x, y):
        return x - 1, y - 1

    def __getitem__(self, i):
        self._check_index(*i)
        x, y = self._zero_index(*i)
        return self._matrix[y][x]

    def __setitem__(self, i, value):
        self._check_index(*i)
        x, y = self._zero_index(*i)
        self._matrix[y][x] = value

    def __eq__(self, other):
        return self._matrix == other.matrix

    @property
    def matrix(self):
        return self._matrix

    @property
    def copy(self):
        new = copy(self)
        new._matrix = [copy(row) for row in self._matrix]
        return new
