#!/usr/bin/env python3

import argparse
import sys

from tkinter import Tk
from go.board import Board
from go.view import View
from go.player import Player


__author__ = "Bachynin Ivan"
__copyright__ = "Copyright 2016"
__version__ = "1.2"

MIN = 3
MAX = 19


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', type=int, default=7, help='size of board')

    args = parser.parse_args()

    if args.size < MIN or args.size > MAX:
        sys.stdout.write('Size must be in range [{MIN}..{MAX}]\n'.format(MIN=MIN, MAX=MAX))
        sys.exit(0)

    root = Tk()
    root.title("GO. THE GAME")
    root.lift()
    root.attributes("-topmost", True)
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))

    board = Board(args.size)
    p1 = Player(board, level=0)
    p2 = Player(board, level=4)
    View(root, board, p1, p2)
    root.mainloop()

if __name__ == '__main__':
    main()
