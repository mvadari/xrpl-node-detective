import curses

def run(stdscr):
    curses.noecho()
    # Clear screen
    stdscr.clear()

    stdscr.addstr(0, 0, "Hello world",
              curses.A_REVERSE)

    stdscr.refresh()
    stdscr.getkey()

def main():
    curses.wrapper(run)

if __name__ == "__main__":
    main()