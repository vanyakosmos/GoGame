from tkinter import *

from go.board import BoardError, Cell
from go.matrix import Matrix
from time import sleep


class View(Matrix):
    TILE_SIZE = 2

    TYPE = {Cell.BLACK: {'bg': '#111111', 'relief': RAISED},
            Cell.WHITE: {'bg': '#eeeeee', 'relief': RAISED},
            Cell.EMPTY: {'bg': '#aaaaaa', 'relief': SUNKEN}}

    TURN = {Cell.BLACK: {'bg': '#111111', 'fg': 'white', 'text': 'black\'s turn'},
            Cell.WHITE: {'bg': '#eeeeee', 'fg': 'black', 'text': 'white\'s turn'}}

    def __init__(self, root, board, p1, p2):
        super(View, self).__init__(board.width,
                                   board.height)
        self._board = board
        self._p1 = p1
        self._p2 = p2

        self._game_grid = Frame(root, padx=10, pady=10)
        self._game_grid.pack()

        self._err = Label(root, fg='#aa0000')
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

        if p1._lvl_id != 0 and p2._lvl_id != 0:
            button = Button(root, text="Start bot battle", command=self._start_bot_battle)
            button.pack()

        self._redraw()

    def _start_bot_battle(self):
        while True:
            try:
                self._player_turn(1, 1)
                self._determine_winner()
            except BoardError:
                break

    def _callback(self, _, x, y):
        try:
            self._player_turn(x, y)
            self._determine_winner()
        except BoardError:
            pass

    def _player_turn(self, x, y):
        try:
            if self._board.turn == Cell.BLACK:
                self._p1.move(x, y)
            else:
                self._p2.move(x, y)
            self._err.config(text="")
            self._turn.config(**View.TURN[self._board.turn])
            self._score.config(text=self.score)
            self._redraw()
        except BoardError as be:
            self._err.config(text=str(be))
            raise be

    def _determine_winner(self):
        if self._board.game_end():
            self._err.config(text="")
            self._turn.config(bg="#f44242", fg='white')
            if self._board.score[Cell.BLACK] > self._board.score[Cell.WHITE]:
                self._turn.config(text="Player 1 (black) wins!")
            elif self._board.score[Cell.BLACK] < self._board.score[Cell.WHITE]:
                self._turn.config(text="Player 2 (white) wins!")
            else:
                self._turn.config(text="Draw!")
            self._redraw(bind=False)
            raise BoardError('fin')

    def _redraw(self, bind=True):
        for y, row in enumerate(self._matrix):
            for x, element in enumerate(row):
                b = element
                b.config(bd=1,
                         width=self.TILE_SIZE*2, height=self.TILE_SIZE,
                         **View.TYPE[self._board[x + 1, y + 1]])
                b.grid(row=y, column=x)

                b.unbind("<Button-1>")
                if bind:
                    b.bind("<Button-1>", lambda event, i=x+1, j=y+1: self._callback(event, i, j))

    @property
    def score(self):
        return "Black: {:4d}\t\t\t\tWhite: {:4d}".format(self._board.score[Cell.BLACK], self._board.score[Cell.WHITE])
