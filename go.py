#!/usr/bin/env python3

import argparse
import sys

from tkinter import Tk
from go.board import Board
from go.view import View


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', type=int, default=7, help='size of board')

    args = parser.parse_args()

    if args.size < 7 or args.size > 19:
        sys.stdout.write('Board size must be between 7 and 19!\n')
        sys.exit(0)

    root = Tk()
    root.title("GO. THE GAME")
    root.lift()
    root.attributes("-topmost", True)
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))

    board = Board(args.size)
    View(root, board)
    root.mainloop()

if __name__ == '__main__':
    main()