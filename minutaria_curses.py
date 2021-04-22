# -*-coding:Utf-8 -*

# minutaria ncurses interface

import minutaria
import curses # see https://docs.python.org/fr/3.7/howto/curses.html
import time

#Timer choosen duration
TIMER_HOURS = 0
TIMER_MIN = 0
TIMER_SEC = 5

FLASH_PERIOD = 1 # Duration between flashes at the end of the timer

def main(stdscr):
    # Clear screen
    stdscr.clear()
    # Withdraw useless cursor
    curses.curs_set(False)
    while True:
        # Create a windows to print timing
        begin_x = 0; begin_y = 0
        height = 5; width = 40
        timer_windows = curses.newwin(height, width, begin_y, begin_x)
        # Create a windows to welcome user input
        input_window = curses.newwin(5, 50, 5, 0)
        input_window.addstr(0, 0,
                            "Press p to pause, k to stop, r to reset :")
        curses.echo()
        input_window.move(0, 42)
        input_window.refresh()
        user_input = ''
        while user_input not in ('p', 'k', 'r'):
            user_input = input_window.getkey(0, 42)
            input_window.refresh()
            # Initialize a timer and a counter
            timer = minutaria.Timer(hours=TIMER_HOURS,
                                    minutes=TIMER_MIN,
                                    seconds=TIMER_SEC)
            counter = timer.is_timing_reached()
            # Launch the timer and print the remaining time
            while counter == False:
                timer_windows.addstr(0, 0, "minutaria", curses.A_STANDOUT)
                timer_windows.addstr(2, 0,
                            "Remaining : " + timer._actualized_delta.__str__())
                counter = timer.is_timing_reached()
                timer_windows.refresh()

            timer_windows.clear()
            timer_windows.refresh()

            # Annouce timer's ending by a "Gong !" and 3 flashes
            timer_windows.addstr(0, 0, "minutaria", curses.A_STANDOUT)
            timer_windows.addstr(2, 0, "GONG !")
            timer_windows.refresh()
            for x in range(1, 4):
                curses.flash()
                time.sleep(FLASH_PERIOD)
            # Pause before break
            break
        time.sleep(2)
        break

curses.wrapper(main)
