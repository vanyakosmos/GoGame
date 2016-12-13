#!/usr/bin/env python3

import argparse
import sys

from tkinter import Tk
from go.board import Board
from go.view import View
from go.player import Player


__author__ = "Bachynin Ivan"
__copyright__ = "Copyright 2016"
__version__ = "1.1"

MIN = 7
MAX = 19


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', type=int, default=7, help='size of board')
    parser.add_argument('-b', '--bot', type=int, default=3, help='bot level')

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
    ai = Player(board, level=args.bot)
    View(root, board, ai)
    root.mainloop()

if __name__ == '__main__':
    main()
