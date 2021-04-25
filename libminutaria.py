#! /usr/bin/python3
# -*-coding:Utf-8 -*

from datetime import datetime, timedelta

class Timer:
    """Simple timer printing as HH:MM:SS"""
    def __init__(self, hours = 0, minutes = 0, seconds = 0):
        self._base = datetime.now()
        self._actualization = datetime(self._base.year, self._base.month,
                                    self._base.day, self._base.hour,
                                    self._base.minute, self._base.second,
                                    self._base.microsecond)
        self._delta = timedelta(seconds=+seconds, minutes=+minutes,
                                    hours=+hours)
        self._actualized_delta = timedelta(seconds=+seconds, minutes=+minutes,
                                    hours=+hours)
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
        """Return the actual remaining time to reach 00:00:00 as string"""
        return str(self._actualized_delta)

if __name__ == '__main__':
    timer = Timer(seconds = 5)

    counter = timer.is_timing_reached()
    while counter == False:
        print("minutaria -", "Remaining :", timer.get_timing, end='\r', flush=True)
        counter = timer.is_timing_reached()

    # Print 3 "GONG !" and some spaces to clear the line
    print("GONG ! " * 3 + ' '*17)
