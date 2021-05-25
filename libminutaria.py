#! /usr/bin/python3
# -*-coding:Utf-8 -*

# libminutaria
# Provide a library allowing to create timers, presets managed by a JSON file
# and an integrable CLI to manage both.

from datetime import datetime, timedelta
from sys import exit
import argparse
import json

class Timer:
    """
    Simple timer printing as HH:MM:SS.
    Allow to launch a given timer, check remaining time before 00:00:00, check
    wether timing is reached and get the current timing allong the process.
    """
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
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
        """
        Convert the timedelta object to a datetime object allowing arithmetic
        on it
        """
        return self._base + self._delta

    def _rebase_current_time(self):
        """Actualize timing according to current time"""
        self._actualization = datetime.now()
        self._actualized_delta = (self._convert_delta_to_datetime()
                                  - self._actualization)

    def is_timing_reached(self) -> bool:
        """Return TRUE if timing reached 00:00:00"""
        self._rebase_current_time()
        timing_to_reach = self._convert_delta_to_datetime()
        return self._actualization >= timing_to_reach

    @property
    def get_timing(self) -> str:
        """Return the actual remaining time to reach 00:00:00 as a string"""
        return str(self._actualized_delta)

class Preset:
    """A preset timer manager for the Timer class"""
    def __init__(self):
        # If the preset file doesn't exist, create it
        try:
            with open('preset.json', 'r') as preset_file_read:
                pass
        except FileNotFoundError:
            with open('preset.json', 'w') as preset_file_write:
                json.dump([], preset_file_write, indent=4)
    def add(self, name: str, hours: int = 0, minutes: int = 0, seconds: int = 0):
        """
        Check wether the choosen name does exist, if not create the preset and
        write it in the preset.json file and return the json object added as a
        dict, if yes raise an exception.
        """
        # Create a data set to be inclued, preset name is lowercased
        # Check wether the name already exist
        try:
            self.get(name)
        except ValueError:
            self.preset_name = name.lower()
            self.hours = hours
            self.min = minutes
            self.secs = seconds
            # Prepare the set in a dict to be added as a json object
            preset_dict_to_append = {"name": self.preset_name,
                                     "duration": {"hours": self.hours,
                                                  "min": self.min,
                                                  "secs": self.secs
                                                  }
                                     }
            # Open the json preset file to add the new preset
            with open('preset.json', 'r') as preset_file_read:
                # Load json presets to be modified
                json_data = json.load(preset_file_read)
                with open('preset.json', 'w') as preset_file_write:
                    # Append the new json object
                    json_data.append(preset_dict_to_append)
                    json.dump(json_data, preset_file_write, indent=4)

            return preset_dict_to_append
        else:
            raise ValueError("ValueError: already existing preset")

    def get(self, name: str):
        """
        Check wether the preset name does exist, if not raise an exception, if
        yes return a dict containing timer values.
        """
        # Preset name is lowercased to be searched
        self.preset_name = name.lower()
        self.timer_values = {"hours": None,
                            "minutes": None,
                            "seconds": None}

        # Open the json preset file to search for the existing preset
        with open('preset.json', 'r') as preset_file_read:
            # Load json presets to be modified
            json_data = json.load(preset_file_read)
            for preset in json_data:
                # Search if the preset does exist
                if preset["name"] == self.preset_name:
                    # Get the preset's timing
                    self.timer_values["hours"] = preset["duration"]["hours"]
                    self.timer_values["minutes"] = preset["duration"]["min"]
                    self.timer_values["seconds"] = preset["duration"]["secs"]

        if (self.timer_values["hours"] or
            self.timer_values["minutes"] or
            self.timer_values["seconds"]) is None:
               raise ValueError("ValueError: Preset not found")

        return self.timer_values

    def delete(self, name: str) -> bool:
        """
        Check wether the preset name does exist, if not return None, if yes
        delete the preset from the preset.json file and return True.
        """
        # Check wether the preset exist
        # If not raise the corresponding exception
        try:
            self.get(name)
        except ValueError as exception:
            raise exception
        # Preset name is lowercased to be searched
        self.preset_name = name.lower()

        # Open the json preset file to search for the existing preset to delete
        with open('preset.json', 'r') as preset_file_read:
            # Load json presets to be modified
            json_data = json.load(preset_file_read)
            for preset in json_data:
                # Search for the preset to delete
                if preset["name"] == self.preset_name:
                    # Delete the preset
                    json_data.remove(preset)
                    with open('preset.json', 'w') as preset_file_write:
                        # Append the modified json object
                        json.dump(json_data, preset_file_write, indent=4)
                    return True

    def rename(self, old_name: str, new_name: str) -> bool:
        """
        Check wether the preset name to change does exist, if not raise an
        exception. Check wether the new preset name does exist, if not rename
        the preset in the preset.json file and return True, if yes raise an
        exception.
        """
        # Check wether the preset exist and if the new name is available
        try:
            self.get(old_name)
        except ValueError as exception:
            raise exception
        try:
            self.get(new_name)
        except ValueError:
            # Preset name is lowercased to be searched
            self.old_preset_name = old_name.lower()
            self.new_preset_name = new_name.lower()

            # Open the json preset file to search for the existing preset to rename
            with open('preset.json', 'r') as preset_file_read:
                # Load json presets to be modified
                json_data = json.load(preset_file_read)
                for preset in json_data:
                    # Search for the preset name
                    if preset["name"] == self.old_preset_name:
                        # Rename it if found
                        preset["name"] = self.new_preset_name
                        with open('preset.json', 'w') as preset_file_write:
                            # Append the modified json object
                            json.dump(json_data, preset_file_write, indent=4)
                        return True
        else:
            raise ValueError("ValueError: already existing preset")
    def set_duration(self, name: str, hours: int, minutes: int, seconds: int) -> bool:
        """
        Check wether the choosen name does exist, if not raise an exception, if
        yes update the preset duration according to parameters, write it in the
        preset.json file and return True.
        """
        # Check wether the preset exist
        try:
            self.get(name)
        except ValueError as exception:
            raise exception
        # Preset name is lowercased to be searched
        self.preset_name = name.lower()
        self.hours = hours
        self.min = minutes
        self.secs = seconds

        # Open the json preset file to search for the preset to modify
        with open('preset.json', 'r') as preset_file_read:
            # Load json presets to be modified
            json_data = json.load(preset_file_read)
            for preset in json_data:
                # Search for the preset name
                if preset["name"] == self.preset_name:
                    # Get the preset's timing
                    preset["duration"]["hours"] = self.hours
                    preset["duration"]["min"] = self.min
                    preset["duration"]["secs"] = self.secs
                    with open('preset.json', 'w') as preset_file_write:
                        # Append the modified json object
                        json.dump(json_data, preset_file_write, indent=4)
                    return True

def minutaria_cli(default_timer: str):
    """
    CLI for minutaria supporting choosing timer duration by hours, minutes
    and seconds separately and managing preset : add, delete, rename, change
    duration of an existing preset and use an existing preset
    """
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
        print("minutaria: Error: argument -H/--hours: invalid choice:"
              f" {args.hours} (choose from 0 to 23)")
        exit()
    if args.minutes and args.minutes not in range(0, 60):
        print(f"minutaria: Error: argument -M/--minutes: invalid choice:"
              f" {args.minutes} (choose from 0 to 59)")
        exit()
    if (args.seconds or args.seconds == 0) and args.seconds not in range(1, 60):
        print(f"minutaria: Error: argument -S/--seconds: invalid choice:"
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

        try:
            new_preset.add(args.add_preset,
                           timer_values["timer_hours"],
                           timer_values["timer_min"],
                           timer_values["timer_secs"])
            new_preset_duration = timedelta(hours =+ timer_values["timer_hours"],
                                            minutes =+ timer_values["timer_min"],
                                            seconds =+ timer_values["timer_secs"])
            print("New preset added: "
                  f"{args.add_preset.capitalize()} - "
                  f"{str(new_preset_duration)}")
            exit()
        except ValueError:
            print(f"The preset name {args.add_preset.capitalize()} "
                  f"already exist. Please choose an other name.")
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
        try:
            preset_to_modify = Preset()
            modified = preset_to_modify.set_duration(args.modify_preset_duration,
                                                     timer_values["timer_hours"],
                                                     timer_values["timer_min"],
                                                     timer_values["timer_secs"])
            modified_duration = timedelta(hours =+ timer_values["timer_hours"],
                                          minutes =+ timer_values["timer_min"],
                                          seconds =+ timer_values["timer_secs"])

            if modified:
                print("New preset duration: "
                      f"{args.modify_preset_duration.capitalize()}"
                      f" - {str(modified_duration)}")
                exit()
        except ValueError:
            print(f"The preset {args.modify_preset_duration.capitalize()} "
                 "does not exist. Please choose an existing name.")
            exit()

    # Check whether the preset to rename is the only user input
    if args.rename_preset and (args.hours or args.minutes or args.seconds):
        print("minutaria: Error: argument -rp/--rename_preset: invalid input: "
              "only indicate the names of the old and the new presets")
        exit()
    elif args.rename_preset:
        # Rename the corresponding preset and quit
        try:
            preset_to_rename = Preset()
            renamed = preset_to_rename.rename(args.rename_preset[0],
                                              args.rename_preset[1])
            if renamed:
                print(f"Preset {args.rename_preset[0].capitalize()} renamed: "
                      f"{args.rename_preset[1].capitalize()}")
                exit()
        except ValueError:
            print(f"The preset {args.rename_preset[0].capitalize()} "
                 f"does not exist or the new name "
                 f"{args.rename_preset[1].capitalize()} is not available.")
            exit()

    # Check whether the preset to delete is the only user input
    if args.del_preset and (args.hours or args.minutes or args.seconds):
        print("minutaria: Error: argument -dp/--del_preset: "
              "invalid input: only indicate the name of the preset to delete")
        exit()
    elif args.del_preset:
        # Delete the corresponding preset and quit
        try:
            preset_to_delete = Preset()
            deleted = preset_to_delete.delete(args.del_preset)
            if deleted:
                print(f"Preset deleted: {args.del_preset.capitalize()}")
                exit()
        except ValueError:
            print(f"The preset {args.del_preset.capitalize()} does not exist.")
            exit()

    # Check whether the preset to get and use is the only user input
    if args.use_preset and (args.hours or args.minutes or args.seconds):
        print("minutaria: Error: argument -p/--use_preset: "
              "invalid input: only indicate the name of the preset to use")
        exit()
    elif args.use_preset:
        try:
            # Use the corresponding preset
            preset_to_get = Preset()
            preset_to_use = preset_to_get.get(args.use_preset)

            # Check wether the preset does exist
            if preset_to_use:
                timer_values["timer_hours"] = preset_to_use["hours"]
                timer_values["timer_min"] = preset_to_use["minutes"]
                timer_values["timer_secs"] = preset_to_use["seconds"]
        except ValueError:
            print(f"The preset {args.use_preset.capitalize()} "
                 "does not exist. Please choose an existing preset.")
            exit()

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

    # Update timer parameters if modified by CLI
    if (timer_values["timer_hours"]
        or timer_values["timer_min"]
        or timer_values["timer_secs"]):
            TIMER_HOURS = timer_values["timer_hours"]
            TIMER_MIN = timer_values["timer_min"]
            TIMER_SEC = timer_values["timer_secs"]

    # Initialize and launch a timer according to parameters
    timer = Timer(hours = TIMER_HOURS,
                  minutes = TIMER_MIN,
                  seconds = TIMER_SEC)

    # Check remaining time along the timer and print it
    counter = timer.is_timing_reached()
    while counter == False:
        print("minutaria -", "Remaining :", timer.get_timing[:9], end='\r',
              flush=True)
        counter = timer.is_timing_reached()

    # Timer reached 00:00:00
    # Print 3 "GONG !" and some spaces to clear the line
    print("GONG ! " * 3 + ' '*17)
