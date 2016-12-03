import os


def bold(v, color=0):
    return '\033[{};1m{}\033[0m'.format(color, v)


def clear():
    os.system('clear')


class _GetChar:
    def __call__(self):
        import sys
        import tty
        import termios

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        ch = None
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch


getch = _GetChar()
