import curses

from init import connect

def run(stdscr):
    curses.noecho()
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    # Clear screen
    stdscr.clear()

    connect(stdscr)

    stdscr.refresh()
    stdscr.getkey()

def main():
    curses.wrapper(run)

if __name__ == "__main__":
    main()