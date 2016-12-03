from tkinter import *

from go.board import BoardError, Cell
from go.matrix import Matrix


class View(Matrix):
    TILE_SIZE = 3

    TYPE = {Cell.BLACK: {'bg': '#111111', 'relief': RAISED},
            Cell.WHITE: {'bg': '#eeeeee', 'relief': RAISED},
            Cell.EMPTY: {'bg': '#aaaaaa', 'relief': SUNKEN}}

    TURN = {Cell.BLACK: {'bg': '#111111', 'fg': 'white', 'text': 'black\'s turn'},
            Cell.WHITE: {'bg': '#eeeeee', 'fg': 'black', 'text': 'white\'s turn'}}

    def __init__(self, root, board):
        super(View, self).__init__(board.width,
                                   board.height)
        self._board = board

        self._game_grid = Frame(root, padx=10, pady=10)
        self._game_grid.pack()

        self._err = Label(root)
        self._err.pack()

        self._turn = Label(root, width=30, relief=SOLID,
                           padx=5, pady=5,
                           **View.TURN[self._board.turn])
        self._turn.pack()

        self._score = Label(root, text=self.score,
                            padx=10, pady=10)
        self._score.pack()

        self._matrix = [[Label(self._game_grid)
                         for _ in range(self.height)]
                        for _ in range(self.width)]

        self._redraw()

    def _callback(self, _, x, y):
        try:
            self._board.move(x, y)
            self._err.config(text="")
            self._turn.config(**View.TURN[self._board.turn])
            self._score.config(text=self.score)
            self._redraw()
        except BoardError as be:
            self._err.config(text=str(be))

    def _redraw(self):
        for y, row in enumerate(self._matrix):
            for x, element in enumerate(row):
                b = element
                b.config(bd=1,
                         width=self.TILE_SIZE*2, height=self.TILE_SIZE,
                         **View.TYPE[self._board[x + 1, y + 1]])
                b.grid(row=y, column=x)
                b.bind("<Button-1>", lambda event, i=x+1, j=y+1: self._callback(event, i, j))

    @property
    def score(self):
        return "Black: {black:4d}\t\t\t\tWhite: {white:4d}".format(**self._board.score)
