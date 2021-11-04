import time
from typing import List, Optional

import curses
from dashboard.init import check_if_synced, title

from dashboard.config import generate_config_screen
from dashboard.peers import get_formatted_peers
from dashboard.unl import unl_screen

from dashboard.init import connect

NUM_COLORS = 256 # curses has 8, but white is one of them

TABS = ["home", "peers", "config", "unl"]

def init_colors():
    for i in range(NUM_COLORS):
        curses.init_pair(i+1, i, curses.COLOR_WHITE)

def alternate_init_colors():
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1) 

class Interface:
    @classmethod
    def start(cls, stdscr):
        interface = cls(stdscr)
        return interface.run()

    def __init__(self, stdscr) -> None:
        # Create curses screen
        stdscr.keypad(True)
        curses.use_default_colors()
        curses.noecho()
        stdscr.refresh()
        self.original_scr = stdscr

        # Get screen width/height
        self.height, self.width = stdscr.getmaxyx()

        # Create a curses pad (pad size is height + 10)
        mypad_height = 32767
        
        self.pos = 0
        self.max_rows = 32767
        self.stdscr = curses.newpad(mypad_height, self.width)
        self.stdscr.scrollok(1)
        alternate_init_colors()
        self.stdscr.keypad(True)

        # Clear screen
        self.stdscr.clear()
        
        # How often to poll for new input
        self.stdscr.timeout(100)

        # State for time-based events
        self.last_sync_check = 0
        self.sync_status = "unchecked"
        
        # print tabs
        self.curr_tab = TABS[0]
        self.print_tabs()
        self.print_current_tab()
        self.refresh()

    #Allows us to use a Pad as if it were a Window by always maintaining the same height and width
    #Call this instead of self.stdscr.refresh()
    def refresh(self):
        height, width = self.original_scr.getmaxyx()
        self.stdscr.refresh(self.pos + 2, 0, 0, 0, height - 1, width - 1)
        
    def run(self):
        n = 0
        while True:
            #Timeout in __init__ ensures that this is non-blocking
            try:
                c = self.stdscr.getkey()
            except:
                c = "NO_INPUT"
            
            self.stdscr.clear()
            if(c == 'q'):
                break
            
            self.handle_key(c)

            self.check_for_time_events()

            self.print_tabs()
            self.print_current_tab()
            self.refresh()

    
    def check_for_time_events(self):
        if(not(self.is_synced()) and self.last_sync_check + 10 < time.time()):
            self.sync_status = check_if_synced()
            self.last_sync_check = time.time()

    def is_synced(self):
        return (self.sync_status == "proposing") or (self.sync_status == "full") or (self.sync_status == "validating")

    def print_current_tab(self):
        if self.curr_tab == "config":
            generate_config_screen(self.stdscr)
        elif(self.curr_tab == "peers"):
            print_section("peers", get_formatted_peers(), self.stdscr, 5, 10)
        elif self.curr_tab == "unl":
            unl_screen(self.stdscr)
        elif(self.curr_tab == "home"):
            formatted = []
            formatted.extend(title)
            row, column = print_section("", formatted, self.stdscr, 5, 10, 3)
            #TODO: Add more specific messages based on the status, rather than just displaying the status
            print_section("", [f"Current sync status: {self.sync_status}"], self.stdscr, row, column)
    
    def print_tabs(self) -> None:
        row = 2
        column = 10
        tab_lens = []

        for i in range(len(TABS)):
            tab = TABS[i]
            if(tab == self.curr_tab):
                tab = f"*{tab.upper()}*"
            else:
                tab = f" {tab} "
            tab_box = f"|{tab}|"
            self.stdscr.addstr(row, column, tab_box, curses.color_pair(7))
            self.stdscr.addstr(row+1, column, "-"*len(tab_box), curses.color_pair(7))
            column += len(tab_box) + 5
    
    def handle_key(self, c: str) -> None:
        #TODO: Investigate why vertical scrolling is not updating
        if c == 'KEY_DOWN' and self.pos < self.original_scr.getyx()[0] - self.original_scr.getmaxyx()[0] - 1:
            self.pos += 1
        elif c == 'KEY_UP' and self.pos > 0:
            self.pos -= 1

        if(c == 'KEY_LEFT'):
            self.curr_tab = TABS[TABS.index(self.curr_tab) - 1]

        if(c == 'KEY_RIGHT'):
            index = TABS.index(self.curr_tab)
            if(index + 1 >= len(TABS)):
                self.curr_tab = TABS[0]
            else:
                self.curr_tab = TABS[index + 1]


def print_section(section_name: str, return_lines: List[str], stdscr, row: int, column: int, color_pair_param: Optional[int] = None):
    if section_name != "":
        stdscr.addstr(row, column, f"***{section_name.upper()}***", curses.color_pair(3))
        row += 2

    for line in return_lines:
        color_pair = 4
        if "Error" in line:
            color_pair = 2
        stdscr.addstr(row, column, line, curses.color_pair(color_pair_param or color_pair))
        row += 1
    row += 1
    return (row, column)

if __name__ == "__main__":
    curses.wrapper(Interface.start)

