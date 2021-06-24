#!/usr/bin/env python3

"""
libminutaria-cli
================

:Authors:
    Locynaeh
:Version:
    1.0

Command Line Interface (CLI)) based on the libminutaria library.

This script is directly usable in a terminal. Use -h/--help arguments for more
information on how to use the CLI provided.
"""

from datetime import timedelta
from libminutaria import Timer, Preset, logger, get_cli_args, handle_cli_args

if __name__ == '__main__':
    # Default parameters to be use if the script is launched without argument
    # or modified by user input
    TIMER_HOURS = 0  # min 0, max 23
    TIMER_MIN = 0    # min 0, max 59
    TIMER_SEC = 5    # min 0, max 59

    # Printable default duration
    default_duration = timedelta(hours=+TIMER_HOURS,
                                 minutes=+TIMER_MIN,
                                 seconds=+TIMER_SEC)
    DEFAULT = str(default_duration)

    # Launch CLI and get timer values if user input
    args = get_cli_args(DEFAULT)
    timer_values, debug_option = handle_cli_args(args)

    # Initiate logger
    logger = logger(debug_option)

    # Update timer parameters if modified by CLI
    if (timer_values["timer_hours"]
            or timer_values["timer_min"]
            or timer_values["timer_secs"]):
        TIMER_HOURS = timer_values["timer_hours"]
        TIMER_MIN = timer_values["timer_min"]
        TIMER_SEC = timer_values["timer_secs"]

    # Initialize and launch a timer according to parameters
    timer = Timer(hours=TIMER_HOURS, minutes=TIMER_MIN, seconds=TIMER_SEC)

    # Check remaining time along the timer and print it
    counter = timer.is_timing_reached()
    while counter is False:
        print("libminutaria -", "Remaining :", timer.get_timing[:9], end='\r',
              flush=True)
        counter = timer.is_timing_reached()

    # Timer reached 00:00:00
    # Print 3 "GONG !" and some spaces to clear the line
    print("GONG ! " * 3 + ' '*17)

