from typing import List

import curses

NUM_COLORS = 7 # curses has 8, but white is one of them

def init_colors():
    for i in range(NUM_COLORS):
        curses.init_pair(i+1, i, curses.COLOR_WHITE)

def print_tabs(stdscr, tab_list: List[str]) -> None:
    column = 2
    row = 10

    for i in range(len(tab_list)):
        tab = tab_list[i]
        stdscr.addstr(column, row, tab, curses.color_pair((i+1) % NUM_COLORS))
        row += len(tab) + 5

def main(stdscr):
    curses.noecho()
    init_colors()
    stdscr.keypad(True)
    # Clear screen
    stdscr.clear()
    
    print_tabs(stdscr, ["setup", "peers", "consensus"])

    stdscr.refresh()
    stdscr.getkey()

if __name__ == "__main__":
    curses.wrapper(main)