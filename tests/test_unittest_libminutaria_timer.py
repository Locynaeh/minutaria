import unittest
#import sys
#import os
#sys.path.append('..')
#DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
#DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
#sys.path.append(DOSSIER_PARENT)
from datetime import datetime, timedelta
from libminutaria import Timer

class TestTimer(unittest.TestCase):
    def setUp(self):
        self.timer = Timer(hours=0, minutes=0, seconds=5)
        # 2021-01-01 12:00:00
        self.timer._base = datetime(2021, 1, 1, 12, 0, 0, 0)
        self.timer._actualization = datetime(self.timer._base.year,
                                             self.timer._base.month,
                                             self.timer._base.day,
                                             self.timer._base.hour,
                                             self.timer._base.minute,
                                             self.timer._base.second,
                                             self.timer._base.microsecond)

    def test_convert_delta_to_datetime(self):
        self.assertEqual(self.timer._convert_delta_to_datetime(),
                         datetime(2021, 1, 1, 12, 0, 5, 0))

    def test_rebase_current_time(self):
        # Not really accurate but can't do better
        self.timer._rebase_current_time()
        # Check if _actualization was updated with a more
        # recent (greater) datetime
        self.assertGreater(self.timer._actualization, self.timer._base)
        # Check if _actualized_delta was reduced
        self.assertLess(self.timer._actualized_delta, self.timer._delta)

    def test_is_timing_reached(self):
        # Set timer as if it has just begun
        # Sufficient with a 5sec timer to pass the test
        self.timer._base = datetime.now()
        self.assertFalse(self.timer.is_timing_reached())
        # Set timer as if it was ended for a long time
        # With a 5sec, the timer already ended to pass the test
        self.timer._base = datetime(2021, 1, 1, 12, 0, 0, 0)
        self.assertTrue(self.timer.is_timing_reached())


if __name__ == '__main__':
#     if __package__ is None:
#         import sys
#         import os
#         sys.path.append(os.path.dirname(os.path.dirname(path.abspath(__file__))))
#         import libminutaria
#     else:
#         import libminutaria
#
    unittest.main()
