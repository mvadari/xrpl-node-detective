from typing import List

import curses

NUM_COLORS = 7 # curses has 8, but white is one of them

def init_colors():
    for i in range(NUM_COLORS):
        curses.init_pair(i+1, i, curses.COLOR_WHITE)

def print_tabs(stdscr, tab_list: List[str], curr_tab) -> None:
    column = 2
    row = 10

    for i in range(len(tab_list)):
        tab = tab_list[i]
        if(tab == curr_tab):
            tab = '**' + tab + '**'
        stdscr.addstr(column, row, tab, curses.color_pair((i+1) % NUM_COLORS))
        row += len(tab) + 5

def main(stdscr):
    curses.noecho()
    init_colors()
    stdscr.keypad(True)
    # Clear screen
    stdscr.clear()
    
    tabs = ["home", "setup", "peers", "consensus"]
    curr_tab = tabs[0]
    print_tabs(stdscr, tabs, curr_tab)
    stdscr.refresh()

    stdscr.keypad(True)
    c = stdscr.getkey()
    while(c != 'q'):
        if(c == 'KEY_LEFT'):
            stdscr.clear()
            curr_tab = tabs[tabs.index(curr_tab) - 1]
            print_tabs(stdscr, tabs, curr_tab)
            stdscr.refresh()

        if(c == 'KEY_RIGHT'):
            stdscr.clear()
            index = tabs.index(curr_tab)
            if(index + 1 >= len(tabs)):
                curr_tab = tabs[0]
            else:
                curr_tab = tabs[index + 1]
            print_tabs(stdscr, tabs, curr_tab)
            stdscr.refresh()


        if(c == 'q'):
            break

        stdscr.refresh()

        c = stdscr.getkey()


if __name__ == "__main__":
    curses.wrapper(main)


