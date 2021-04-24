# -*-coding:Utf-8 -*

# minutaria ncurses interface
# basic ncurses interface based on the Python's curses standard library
# Give the user the choice to relaunch the same timer at the end of the first
# automatically launched or to quit the program 

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
    
    mainloop = True
    while mainloop == True:
        # Create a windows dedicated to print timing
        timer_window = curses.newwin(5, 40, 0, 0)
        
        # Initialize the timer and a counter
        timer = minutaria.Timer(hours=TIMER_HOURS,
                                minutes=TIMER_MIN,
                                seconds=TIMER_SEC)
        counter = timer.is_timing_reached()
        
        # Launch the timer and print the remaining time
        while counter == False:
            timer_window.addstr(0, 0, "minutaria", curses.A_STANDOUT)
            timer_window.addstr(2, 0,
                        "Remaining : " + timer._actualized_delta.__str__())
            counter = timer.is_timing_reached()
            timer_window.refresh()

        timer_window.clear()
        timer_window.refresh()

        # Annouce timer's ending by a "Gong !" and 3 flashes
        timer_window.addstr(0, 0, "minutaria", curses.A_STANDOUT)
        timer_window.addstr(2, 0, "GONG !")
        timer_window.refresh()
        for x in range(1, 4):
            curses.flash()
            curses.napms(FLASH_PERIOD)
        
        # Give the user the choice to relaunch the timer or quit
        while True:
            timer_window.addstr(4, 0, "Press r to relaunch or q to quit...")
            timer_window.refresh()
            user_input = timer_window.getch()
            if user_input == ord('r'):
                break
            elif user_input == ord('q'):
                mainloop = False
                break

if __name__ == '__main__':
    curses.wrapper(main)
