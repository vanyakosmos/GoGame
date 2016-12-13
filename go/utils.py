from enum import Enum


class BoardError(Exception):
    pass


class Cell(Enum):
    BLACK = 'black'
    WHITE = 'white'
    EMPTY = 'empty'
