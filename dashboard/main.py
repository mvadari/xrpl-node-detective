from typing import List

import curses

def print_tabs(stdscr, tab_list: List[str]) -> None:
    column = 2
    row = 10

    for tab in tab_list:
        stdscr.addstr(column, row, tab, curses.A_REVERSE)
        row += len(tab) + 5

def main(stdscr):
    curses.noecho()
    stdscr.keypad(True)
    # Clear screen
    stdscr.clear()
    
    print_tabs(stdscr, ["setup", "peers", "consensus"])

    stdscr.refresh()
    stdscr.getkey()

if __name__ == "__main__":
    curses.wrapper(main)