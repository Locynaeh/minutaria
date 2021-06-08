import unittest
import sys
import os
#sys.path.append('..')
#DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
#DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
#sys.path.append(DOSSIER_PARENT)
from datetime import datetime, timedelta
import json
from libminutaria import Timer, Preset

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


class TestPreset(unittest.TestCase):
    def setUp(self):
        self.test_preset = Preset('preset_test', 1, 2, 3, 'preset_test.json')

    def test_add(self):
        # Add the test preset to preset_test.json
        self.test_preset.add()
        is_preset_written_in_the_file = False
        # Load all data from the file to check if it was effectively written
        with open(self.test_preset._preset_file, 'r') as preset_file_read:
            # Load json presets to be modified
            json_data = json.load(preset_file_read)
            for preset in json_data:
                # Search if the preset does exist
                if preset["name"] == self.test_preset._name:
                    is_preset_written_in_the_file = True
        self.assertTrue(is_preset_written_in_the_file)

    def test_add_if_already_exist(self):
        self.test_preset.add()
        # Try to add again the same preset to raise an error
        with self.assertRaises(ValueError):
            self.test_preset.add()

    def test_get(self):
        # Add the test preset to preset_test.json
        self.test_preset.add()
        # Check if it was found by checking the returned value
        self.assertEqual(self.test_preset.get(),
                         {"hours": 1,
                         "minutes": 2,
                         "seconds": 3})

    def test_get_if_not_exist(self):
        # Change name and check if it raise an error because not found
        with self.assertRaises(ValueError):
            self.test_preset.get()

    def test_delete(self):
        # Add the test preset to preset_test.json
        self.test_preset.add()
        # Check if it was deleted by checking the return value
        self.assertTrue(self.test_preset.delete())

    def test_delete_if_not_exist(self):
        # Try to delete it again, it shall raise an error
        with self.assertRaises(ValueError):
            self.test_preset.delete()

    def test_rename(self):
        # Add the test preset to preset_test.json
        self.test_preset.add()
        # Check if it was renamed by checking the return value
        self.assertTrue(self.test_preset.rename('renamed_preset_test'))
        # Check the same with the Preset.get() method
        self.test_preset._name = 'renamed_preset_test'
        self.assertTrue(self.test_preset.get())

    def test_rename_if_not_exist(self):
        # Try to rename a non existing preset in the file
        self.test_preset._name = 'not_existing_preset_test'
        with self.assertRaises(ValueError):
            self.test_preset.rename('renamed_preset_test')

    def test_rename_if_new_name_is_already_taken(self):
        # Add the test preset to preset_test.json
        self.test_preset.add()
        self.test_preset._name = 'existing_preset_test'
        self.test_preset.add()
        with self.assertRaises(ValueError):
            self.test_preset.rename('existing_preset_test')

    def test_set_duration(self):
        # Add the test preset to preset_test.json
        self.test_preset.add()
        # Check if duration was modified by checking the return value
        self.assertTrue(self.test_preset.set_duration(2, 3, 4))
        # Check if duration was modified by checking the preset's duration
        self.assertEqual(self.test_preset.get(),
                         {"hours": 2,
                         "minutes": 3,
                         "seconds": 4})

    def test_set_duration_if_not_exist(self):
        # Try to change duration of a non existing preset
        # Shall raise an error
        with self.assertRaises(ValueError):
            self.test_preset.set_duration(2, 3, 4)

    def tearDown(self):
        # Remove the JSON preset test file
        os.remove(self.test_preset._preset_file)


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
