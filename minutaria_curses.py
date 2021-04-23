# -*-coding:Utf-8 -*

# minutaria ncurses interface

import minutaria
import curses # see https://docs.python.org/fr/3.7/howto/curses.html

#Timer choosen duration
TIMER_HOURS = 0
TIMER_MIN = 0
TIMER_SEC = 5

FLASH_PERIOD = 1000 # Duration between flashes at the end of the timer

def main(stdscr):
    # Withdraw cursor visiblity for aesthetic reasons
    curses.curs_set(False)
    while True:
        # Create a windows dedicated to print timing
        timer_windows = curses.newwin(5, 40, 0, 0)
        
        # Initialize the timer and a counter
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
            curses.napms(FLASH_PERIOD)
        
        # Pause before break
        curses.napms(2000)
        break

if __name__ == '__main__':
    curses.wrapper(main)
