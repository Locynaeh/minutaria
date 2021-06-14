#!/usr/bin/env python3

"""
libminutaria ncurses interface
===========================

:Authors:
    Locynaeh
:Version:
    1.0

Basic liblibminutaria ncurses interface based on the Python's curses standard
library.

Give the user  a start/quit command at the beginning and the choice to
relaunch the same timer or quit anytime
Add a configurable flash system at the end of the timer

The TUI is fully usable with CLI arguments thanks to liblibminutaria.
Use -h/--help arguments for more information.

This user interface shall only be use on Unix system as the Windows version
isn't included in the standard library, this script contains a WINDOWS_CHECK
parameter for this purpose.
Nervertheless it should be usable with WSL (not tested).

Functions
---------
main
    A main loop to display a ncurses TUI to a liblibminutaria timer.
"""

import logging
from os import name
import curses  # see https://docs.python.org/fr/3.7/howto/curses.html
from datetime import timedelta
import libminutaria


# Duration between flashes at the end of the timer
FLASH_PERIOD = 1000


def main(stdscr) -> None:
    """ncurses main loop

    Create a dedicated ncurses windows to launch a libminutaria's Timer
    with start/relaunch/quit utility all along.

    First an initial screen displays the initial timing and gives the user
    the launch or quit choice.

    Then, if launch is choosen, then the timer is launched and the user has the
    choice to relaunch (reset the timer and return to the first screen) or
    quit all along.

    Finally, at the end of the timer, a GONG is displayed 3 times with
    configurable flashes. Again the same relaunch/quit choice is given to
    the user.
    """

    # Withdraw cursor visiblity for aesthetic reasons
    curses.curs_set(False)
    # Block I/O calls for the base screen
    stdscr.nodelay(False)

    mainloop = True
    while mainloop:
        # Start or quit command
        stdscr.clear()
        stdscr.addstr(0, 0, "libminutaria", curses.A_STANDOUT)
        stdscr.addstr(2, 0, "Timing : " + str(initial_timing))
        stdscr.addstr(4, 0, "Press any key to launch or q to quit...")
        stdscr.refresh()

        start_action = stdscr.getch()
        if start_action == ord('q'):
            break

        # Clean-up
        stdscr.clear()
        stdscr.refresh()

        # Create a windows dedicated to print timing
        timer_window = curses.newwin(5, 40, 0, 0)
        # Don't block I/O calls for the timer window
        timer_window.nodelay(True)

        # Initialize the timer and a counter
        timer = libminutaria.Timer(hours=TIMER_HOURS,
                                   minutes=TIMER_MIN,
                                   seconds=TIMER_SEC)
        counter = timer.is_timing_reached()

        # Launch the timer and print the remaining time
        while counter is False:
            timer_window.addstr(0, 0, "libminutaria", curses.A_STANDOUT)
            timer_window.addstr(2, 0, "Remaining : " + timer.get_timing[:9])
            timer_window.addstr(4, 0, "Press r to relaunch or q to quit...")
            counter = timer.is_timing_reached()
            # Manage user's choice for the timer loop
            choice = timer_window.getch()
            if choice == ord('q'):
                mainloop = False
                break
            elif choice == ord('r'):
                break
            timer_window.refresh()
        # Manage user's choice for the main loop
        if choice == ord('q'):
            break
        elif choice == ord('r'):
            continue
        else:
            # Annouce timer's ending by a "Gong !" and a flash, 3 times
            timer_window.clear()
            timer_window.refresh()
            timer_window.addstr(0, 0, "libminutaria", curses.A_STANDOUT)
            timer_window.refresh()
            for space in range(1, 4):
                timer_window.addstr(2, 0, "GONG ! " * space)
                timer_window.refresh()
                curses.flash()
                curses.napms(FLASH_PERIOD)

        # Give the user the choice to relaunch the timer or quit
        endloop = True
        while endloop:
            timer_window.addstr(4, 0, "Press r to relaunch or q to quit...")
            timer_window.refresh()
            user_input = timer_window.getch()
            if user_input == ord('r'):
                break
            elif user_input == ord('q'):
                mainloop = False
                break


if __name__ == '__main__':
    # Default parameters to be use if the script is launched without argument
    # or modified by user input
    TIMER_HOURS = 0  # min 0, max 23
    TIMER_MIN = 0    # min 0, max 59
    TIMER_SEC = 5    # min 0, max 59

    # Printable default script duration
    default_duration = timedelta(hours=+TIMER_HOURS,
                                 minutes=+TIMER_MIN,
                                 seconds=+TIMER_SEC)
    DEFAULT = str(default_duration)


    # Launch CLI and get timer values if user input
    args = libminutaria.get_cli_args(DEFAULT)
    timer_values, debug_option = libminutaria.handle_cli_args(args)

    # Initiate logger
    logger = libminutaria.logger(debug_option)

    # Check if not on Windows platform
    WINDOWS_CHECK = True

    if WINDOWS_CHECK:
        try:
            assert("posix" in name), "May not be able to run correctly on "\
                                      "non Posix systems."
        except AssertionError as error:
            print(f"{error}\nThe program was stopped. "
                  "Set WINDOWS_CHECK value to False to disable the check.")
            logger.debug("Exception occurred", exc_info=True)
            exit()

    # Update timer parameters if modified by CLI
    if (timer_values["timer_hours"]
            or timer_values["timer_min"]
            or timer_values["timer_secs"]):
        TIMER_HOURS = timer_values["timer_hours"]
        TIMER_MIN = timer_values["timer_min"]
        TIMER_SEC = timer_values["timer_secs"]

    # Keep a timestamp of the final initial timing choosen after CLI use
    initial_timing = timedelta(hours=TIMER_HOURS,
                               minutes=TIMER_MIN,
                               seconds=TIMER_SEC)

    # Launch the curses main loop in a ncurses wrapper to manage cleaning
    curses.wrapper(main)
