#! /usr/bin/python3
# -*-coding:Utf-8 -*

from datetime import datetime, timedelta
from sys import exit
import argparse

class Timer:
    """Simple timer printing as HH:MM:SS"""
    def __init__(self, hours = 0, minutes = 0, seconds = 0):
        self._base = datetime.now()
        self._actualization = datetime(self._base.year,
                                       self._base.month,
                                       self._base.day,
                                       self._base.hour,
                                       self._base.minute,
                                       self._base.second,
                                       self._base.microsecond)
        self._delta = timedelta(hours=+hours,
                                minutes=+minutes,
                                seconds=+seconds)
        self._actualized_delta = timedelta(hours=+hours,
                                           minutes=+minutes,
                                           seconds=+seconds)
    def _convert_delta_to_datetime(self):
        """Convert the timedelta object to a datetime object allowing arithmetic
        on it"""
        return self._base + self._delta

    def _rebase_current_time(self):
        """Actualize timing according to current time"""
        self._actualization = datetime.now()
        self._actualized_delta = (self._convert_delta_to_datetime()
                                  - self._actualization)

    def is_timing_reached(self):
        """Return TRUE if timing reached 00:00:00"""
        self._rebase_current_time()
        timing_to_reach = self._convert_delta_to_datetime()
        return self._actualization >= timing_to_reach

    @property
    def get_timing(self):
        """Return the actual remaining time to reach 00:00:00 as a string"""
        return str(self._actualized_delta)

class Preset:
    """A preset timer manager for the Timer class"""
    def __init__(self):
        #Si le fichier des presets n'existe pas, le créer
        pass
    def add_preset(self, name, hours=0, minutes=0, seconds=0):
        #Penser à minifier l'input
        pass
    def get_preset(self, name):
        #Penser à minifier l'input
        #Retour sous la forme {'hours': 0, 'minutes': 1, 'seconds': 30}
        pass
    def delete_preset(self, name):
        #Penser à minifier l'input
        pass
    def rename_preset(self, old_name, new_name):
        # Que l'on modifie le nom ou la durée,
        # supprimer l'ancien et créer un nouveau
        #Penser à minifier l'input
        pass
    def modify_preset_duration(self, name, hours, minutes, seconds):
        # Que l'on modifie le nom ou la durée,
        # supprimer l'ancien et créer un nouveau
        #Penser à minifier l'input
        pass


        """
        try:
            with open('/tmp/fichier', 'w') as fichier:
                # faire un truc avec le fichier
        except EnvironmentError:
            # gérer l'erreur
        """

def minutaria_cli(default_timer):
    parser = argparse.ArgumentParser(prog="minutaria",
                                     description="Execute a given timer from "
                                                 "min 00:00:01 to max 23:59:59."
                                                 " Options -ap and -mpd shall "
                                                 "be used with duration "
                                                 "parameters.",
                                     epilog=f"If no timer is provided, "
                                            f"execute the default: "
                                            f"{default_timer}.")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("-v",
                    "--version",
                    action="version",
                    version="%(prog)s 1.0")
    parser.add_argument("-H",
                        "--hours",
                        type=int,
                        action="store",
                        help="Hour(s) to time")
    parser.add_argument("-M",
                        "--minutes",
                        type=int,
                        action="store",
                        help="Minute(s) to time")
    parser.add_argument("-S",
                        "--seconds",
                        type=int,
                        action="store",
                        help="Second(s) to time")
    group.add_argument("-ap",
                        "--add_preset",
                        action="store",
                        metavar="PRESET_NAME",
                        help="Name of the timer preset to create")
    group.add_argument("-p",
                        "--use_preset",
                        action="store",
                        metavar="PRESET_NAME",
                        help="Name of the timer preset to use")
    group.add_argument("-rp",
                        "--rename_preset",
                        action="store",
                        nargs=2,
                        metavar=("OLD_NAME","NEW_NAME"),
                        help="Names of the timer preset to rename and the new")
    group.add_argument("-mpd",
                        "--modify_preset_duration",
                        action="store",
                        metavar="PRESET_NAME",
                        help="Name of the timer preset to modify")
    group.add_argument("-dp",
                        "--del_preset",
                        action="store",
                        metavar="PRESET_NAME",
                        help="Name of the timer preset to delete")

    args = parser.parse_args()

    # Accepted ranges error management
    if args.hours and args.hours not in range(0, 24):
        print("minutaria: ValueError: argument -H/--hours: invalid choice:"
              f" {args.hours} (choose from 0 to 23)")
        exit()
    if args.minutes and args.minutes not in range(0, 60):
        print(f"minutaria: ValueError: argument -M/--minutes: invalid choice:"
              f" {args.minutes} (choose from 0 to 59)")
        exit()
    if (args.seconds or args.seconds == 0) and args.seconds not in range(1, 60):
        print(f"minutaria: argument -S/--seconds: invalid choice:"
              f" {args.seconds} (choose from 1 to 59)")
        exit()

    # Container for timer values
    timer_values = {
        "timer_hours": None,
        "timer_min": None,
        "timer_secs": None
    }

    # Actualize timing global variables if at list one CLI argument is used
    if args.hours or args.minutes or args.seconds:
        if args.hours == None:
            timer_values["timer_hours"] = 0
        else:
            timer_values["timer_hours"] = args.hours

        if args.minutes == None:
            timer_values["timer_min"] = 0
        else:
            timer_values["timer_min"] = args.minutes

        if args.seconds == None:
            timer_values["timer_secs"] = 0
        else:
            timer_values["timer_secs"] = args.seconds

    # Check whether the user input a timer with the name of the preset to create
    if args.add_preset and (not args.hours
                            and not args.minutes
                            and not args.seconds):
        print(f"minutaria: Error: argument -ap/--add_preset: "
              f"incomplete input: {args.add_preset} (indicate preset name "
              f"and corresponding timer with dedicated parameters)")
        exit()
    elif args.add_preset:
        # Create the corresponding preset and quit
        new_preset = Preset()
        new_preset.add_preset(args.add_preset,
                              timer_values["timer_hours"],
                              timer_values["timer_min"],
                              timer_values["timer_secs"])
        new_preset_duration = timedelta(hours =+ timer_values["timer_hours"],
                                        minutes =+ timer_values["timer_min"],
                                        seconds =+ timer_values["timer_secs"])

        print("New preset added: "
              f"{args.add_preset.capitalize()} - {str(new_preset_duration)}")
        exit()

    # Check whether the user input a timer with the name of the preset to modify
    if args.modify_preset_duration and (not args.hours
                                   and not args.minutes
                                   and not args.seconds):
        print(f"minutaria: Error: argument -mpd/--modify_preset_duration: "
              f"incomplete input: {args.modify_preset_duration} (indicate "
              f"preset name and corresponding timer to modify with dedicated "
              f"parameters)")
        exit()
    elif args.modify_preset_duration:
        # Modify the corresponding preset and quit
        preset_to_modify = Preset()
        preset_to_modify.modify_preset_duration(args.modify_preset_duration,
                                                timer_values["timer_hours"],
                                                timer_values["timer_min"],
                                                timer_values["timer_secs"])
        modified_preset_duration = timedelta(hours =+ timer_values["timer_hours"],
                                             minutes =+ timer_values["timer_min"],
                                             seconds =+ timer_values["timer_secs"])
        print("New preset duration: "
              f"{args.modify_preset_duration.capitalize()}"
              f" - {str(modified_preset_duration)}")
        exit()

    # Check whether the preset to rename is the only user input
    if args.rename_preset and (args.hours or args.minutes or args.seconds):
        print("minutaria: Error: argument -rp/--rename_preset: invalid input: "
              "only indicate the names of the old and the new presets")
        exit()
    elif args.rename_preset:
        # Rename the corresponding preset and quit
        preset_to_rename = Preset()
        preset_to_rename.rename_preset(args.rename_preset[0],
                                       args.rename_preset[1])
        print(f"Preset {args.rename_preset[0].capitalize()} renamed: "
              f"{args.rename_preset[1].capitalize()}")
        exit()

    # Check whether the preset to delete is the only user input
    if args.del_preset and (args.hours or args.minutes or args.seconds):
        print("minutaria: Error: argument -dp/--del_preset: "
              "invalid input: only indicate the name of the preset to delete")
        exit()
    elif args.del_preset:
        # Delete the corresponding preset and quit
        preset_to_delete = Preset()
        preset_to_delete.delete_preset(args.del_preset)
        print(f"Preset deleted: {args.del_preset.capitalize()}")
        exit()

    # Check whether the preset to get and use is the only user input
    if args.use_preset and (args.hours or args.minutes or args.seconds):
        print("minutaria: Error: argument -p/--use_preset: "
              "invalid input: only indicate the name of the preset to use")
        exit()
    elif args.use_preset:
        # Use the corresponding preset
        """
        preset_to_get = Preset()
        preset_to_use = preset_to_get.get_preset(args.use_preset)
        timer_values["timer_hours"] = preset_to_use["hours"]
        timer_values["timer_min"] = preset_to_use["minutes"]
        timer_values["timer_secs"] = preset_to_use["seconds"]
        """

    return timer_values

if __name__ == '__main__':
    # Default parameters to be use if the script is launched without argument
    # or modified by user input
    TIMER_HOURS = 0 # min 0, max 23
    TIMER_MIN = 0   # min 0, max 59
    TIMER_SEC = 5   # min 0, max 59

    #Printable default duration
    default_duration = timedelta(hours =+ TIMER_HOURS,
                                 minutes =+ TIMER_MIN,
                                 seconds =+ TIMER_SEC)
    DEFAULT = str(default_duration)

    # Launch CLI and get timer values if user input
    timer_values = minutaria_cli(DEFAULT)

    if (timer_values["timer_hours"]
        or timer_values["timer_min"]
        or timer_values["timer_secs"]):
            TIMER_HOURS = timer_values["timer_hours"]
            TIMER_MIN = timer_values["timer_min"]
            TIMER_SEC = timer_values["timer_secs"]

    print(timer_values)
    print(TIMER_HOURS, TIMER_MIN, TIMER_SEC, sep=":")

    """timer = Timer(hours = TIMER_HOURS,
                  minutes = TIMER_MIN,
                  seconds = TIMER_SEC)

    counter = timer.is_timing_reached()
    while counter == False:
        print("minutaria -", "Remaining :", timer.get_timing, end='\r',
              flush=True)
        counter = timer.is_timing_reached()

    # Print 3 "GONG !" and some spaces to clear the line
    print("GONG ! " * 3 + ' '*17)"""

    # minutaria: error: argument -H/--hours: invalid choice: 24 (choose from 0 to 23)
    # ValueError: hour must be in 0..23
