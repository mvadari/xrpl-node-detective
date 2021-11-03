from typing import List

import curses

from dashboard.config import generate_config_screen
from dashboard.peers import get_formatted_peers
from dashboard.validations import validation_screen

NUM_COLORS = 7 # curses has 8, but white is one of them

TABS = ["home", "setup", "peers", "consensus", "config", "validation"]

def init_colors():
    for i in range(NUM_COLORS):
        curses.init_pair(i+1, i, curses.COLOR_WHITE)

class Interface:
    @classmethod
    def start(cls, stdscr):
        interface = cls(stdscr)
        return interface.run()

    def __init__(self, stdscr) -> None:
        self.stdscr = stdscr
        curses.noecho()
        init_colors()
        self.stdscr.keypad(True)
        # Clear screen
        self.stdscr.clear()
        
        # print tabs
        self.curr_tab = TABS[0]
        self.print_tabs()
        self.print_current_tab()
        self.stdscr.refresh()

    def run(self):
        c = self.stdscr.getkey()
        while(c != 'q'):
            self.stdscr.clear()
            if(c == 'q'):
                break
            
            self.handle_key(c)

            self.print_tabs()
            self.print_current_tab()
            self.stdscr.refresh()

            c = self.stdscr.getkey()
    
    def print_current_tab(self):
        if self.curr_tab == "config":
            generate_config_screen(self.stdscr)
        elif self.curr_tab == "peers":
            formatted = get_formatted_peers()
            print_section("peers", formatted, self.stdscr, 5, 10)
        elif self.curr_tab == "validation":
            validation_screen(self.stdscr)
    
    def print_tabs(self) -> None:
        column = 2
        row = 10

        for i in range(len(TABS)):
            tab = TABS[i]
            if(tab == self.curr_tab):
                tab = '**' + tab + '**'
            self.stdscr.addstr(column, row, tab, curses.color_pair((i+1) % NUM_COLORS))
            row += len(tab) + 5
    
    def handle_key(self, c: str) -> None:
        if(c == 'KEY_LEFT'):
            self.curr_tab = TABS[TABS.index(self.curr_tab) - 1]

        if(c == 'KEY_RIGHT'):
            index = TABS.index(self.curr_tab)
            if(index + 1 >= len(TABS)):
                self.curr_tab = TABS[0]
            else:
                self.curr_tab = TABS[index + 1]


def print_section(section_name: str, return_lines: List[str], stdscr, row: int, column: int):
    stdscr.addstr(row, column, f"***{section_name.upper()}***", curses.color_pair(1))
    row += 2

    for line in return_lines:
        color_pair = 1
        if "Error" in line:
            color_pair = 2
        stdscr.addstr(row, column, line, curses.color_pair(color_pair))
        row += 1
    row += 1
    return (row, column)

if __name__ == "__main__":
    curses.wrapper(Interface.start)


