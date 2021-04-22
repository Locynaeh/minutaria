# -*-coding:Utf-8 -*

# minutaria ncurses interface

import minutaria
import curses # see https://docs.python.org/fr/3.7/howto/curses.html
import time

TIMER_HOURS = 0
TIMER_MIN = 0
TIMER_SEC = 5
FLASH_PERIOD = 1

def main(stdscr):
    # Clear screen
    stdscr.clear()
    # Withdraw useless cursor
    curses.curs_set(False)
    while True:
        # Create a windows to print timing
        begin_x = 0; begin_y = 0
        height = 5; width = 40
        win = curses.newwin(height, width, begin_y, begin_x)
        # Initialize a timer and a counter
        timer = minutaria.Timer(hours=TIMER_HOURS,
                                minutes=TIMER_MIN,
                                seconds=TIMER_SEC)
        counter = timer.is_timing_reached()
        # Launch the timer and print the remaining time
        while counter == False:
            win.addstr(0, 0, "Remaining : " + timer._actualized_delta.__str__())
            counter = timer.is_timing_reached()
            win.noutrefresh()
            curses.doupdate()

        stdscr.clear()
        stdscr.refresh()

        # Annouce timer's ending by a "Gong !" and 3 flashes
        print("GONG !")
        for x in range(1, 4):
            curses.flash()
            time.sleep(FLASH_PERIOD)
        # Pause before break
        time.sleep(3)
        break

curses.wrapper(main)
