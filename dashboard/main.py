from typing import List

import curses

NUM_COLORS = 7 # curses has 8, but white is one of them

TABS = ["home", "setup", "peers", "consensus"]

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
        self.stdscr.refresh()

    def run(self):
        c = self.stdscr.getkey()
        while(c != 'q'):
            if(c == 'q'):
                break
            
            self.handle_key(c)

            self.stdscr.refresh()

            c = self.stdscr.getkey()
    
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
            self.stdscr.clear()
            self.curr_tab = TABS[TABS.index(self.curr_tab) - 1]
            self.print_tabs()
            self.stdscr.refresh()

        if(c == 'KEY_RIGHT'):
            self.stdscr.clear()
            index = TABS.index(self.curr_tab)
            if(index + 1 >= len(TABS)):
                self.curr_tab = TABS[0]
            else:
                self.curr_tab = TABS[index + 1]
            self.print_tabs()
            self.stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(Interface.start)


