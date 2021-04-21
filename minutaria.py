# -*-coding:Utf-8 -*

from datetime import datetime, timedelta

class Timer:
    """Simple timer printing as HH:MM:SS"""
    def __init__(self, hours = 0, minutes = 0, seconds = 0):
        self.base = datetime.now()
        self.actualization = datetime(self.base.year, self.base.month,
                                    self.base.day, self.base.hour,
                                    self.base.minute, self.base.second,
                                    self.base.microsecond)
        self.delta = timedelta(seconds=+seconds, minutes=+minutes,
                                    hours=+hours)
        self.actualized_delta = timedelta(seconds=+seconds, minutes=+minutes,
                                    hours=+hours)
    def _convert_delta_to_datetime(self):
        """Convert the timedelta object to a datetime object allowing arithmetic
        on it"""
        return self.base + self.delta

    def _rebase_current_time(self):
        """Actualize timing according to current time"""
        self.actualization = datetime.now()
        self.actualized_delta = (self._convert_delta_to_datetime()
                                - self.actualization)

    def is_timing_reached(self):
        """Check if timing reached 00:00:00 and return TRUE if so"""
        self._rebase_current_time()
        timing_to_reach = self._convert_delta_to_datetime()
        return self.actualization >= timing_to_reach

    def print_timing(self):
        """Print the actual remaining time to reach 00:00:00"""
        print(self.actualized_delta)
        
if __name__ == '__main__':
    timer = Timer(seconds = 10)
    
    counter = timer.is_timing_reached()
    while counter == False:
        timer.print_timing()
        counter = timer.is_timing_reached()
    print("GONG !")

    
    
