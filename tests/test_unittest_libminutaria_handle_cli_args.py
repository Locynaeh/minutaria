# TODO : make it work one day

import unittest
from unittest.mock import Mock
import libminutaria
from argparse import Namespace

#Preset = Mock()
#add_return_value = {"name": 'truc', "duration": {"hours": 1,
#                                               "min": 2,
#                                               "secs": 3}
#                   }
#get_return_value = {"hours": 1, "minutes": 2, "seconds": 3}
#Preset.return_value.add.return_value = add_return_value
#Preset.return_value.get.return_value = get_return_value
#Preset.return_value.delete.return_value = True
#Preset.return_value.rename.return_value = True
#Preset.return_value.set_duration.return_value = True
#ap = Preset('tric', seconds=24, preset_file='preset.json')
#Preset.assert_called_once_with('tric', seconds=24, preset_file='preset.json')
#print(ap)
#add_ap = ap.add()
#print(add_ap)
#Preset.assert_called()  # ok
#Preset.return_value.add.assert_called()  # ok
#get_ap = ap.get()
#Preset.return_value.get.assert_called()  # ok
#delete_ap = ap.delete()
#print(delete_ap)
#Preset.return_value.delete.assert_called()


class TestCommandLine(unittest.TestCase):
    def setUp(self):
        pass
        # Mock Preset class and configure methods
        #Preset = Mock()
        #
        #add_return_value = {"name": 'truc', "duration": {"hours": 1,
        #                                               "min": 2,
        #                                               "secs": 3}
        #                   }
        #get_return_value = {"hours": 1, "minutes": 2, "seconds": 3}
        #
        ##Preset.return_value.add.return_value = add_return_value
        #Preset.return_value.get.return_value = get_return_value
        #Preset.return_value.delete.return_value = True
        #Preset.return_value.rename.return_value = True
        #Preset.return_value.set_duration.return_value = True

    def test_handle_cli_args_duration(self):
        # Test with only a duration given
        # Create Namespace object as handle_cli_args() test's parameter
        dict_to_args = {"add_preset": None,
                "debug": False,
                "del_preset": None,
                "hours": 4,
                "minutes": 20,
                "modify_preset_duration": None,
                "rename_preset": None,
                "seconds": 22,
                "use_preset": None}
        duration = Namespace()
        for arg in dict_to_args:
            setattr(duration, arg, dict_to_args[arg])

        args = libminutaria.handle_cli_args(duration)
        self.assertEqual(args, ({"timer_hours": 4,
                                 "timer_min": 20,
                                 "timer_secs": 22},
                                False))

    def test_handle_cli_args_duration_debug(self):
        # Test with only a duration given and debug flag
        # Create Namespace object as handle_cli_args() test's parameter
        dict_to_args = {"add_preset": None,
                "debug": True,
                "del_preset": None,
                "hours": 4,
                "minutes": 20,
                "modify_preset_duration": None,
                "rename_preset": None,
                "seconds": 22,
                "use_preset": None}
        duration = Namespace()
        for arg in dict_to_args:
            setattr(duration, arg, dict_to_args[arg])

        args = libminutaria.handle_cli_args(duration)
        self.assertEqual(args, ({"timer_hours": 4,
                                 "timer_min": 20,
                                 "timer_secs": 22},
                                True))

    def test_handle_cli_args_add_preset_already_exist(self):
        # Test with only a duration given and debug flag
        # Mock Preset class and configure methods
        libminutaria.Preset = Mock()
        libminutaria.Preset.return_value.add.side_effect = ValueError
        __builtins__.print = Mock()
        #libminutaria.Preset.return_value.add.return_value = add_return_value
        # Create Namespace object as handle_cli_args() test's parameter
        dict_to_args = {"add_preset": 'truc',
                "debug": False,
                "del_preset": None,
                "hours": None,
                "minutes": None,
                "modify_preset_duration": None,
                "rename_preset": None,
                "seconds": 22,
                "use_preset": None}
        add_existing_preset = Namespace()
        for arg in dict_to_args:
            setattr(add_existing_preset, arg, dict_to_args[arg])

        with self.assertRaises(SystemExit):
            args = libminutaria.handle_cli_args(add_existing_preset)
            __builtins__.print.assert_called()
            __builtins__.print.assert_called_with('The preset name Truc '
                                                  'already exist. Please '
                                                  'choose an other name.')
            Preset.assert_called_once_with('truc', hours=0, minutes=0, seconds=22)
            Preset.return_value.add.assert_called()
"""
    def test_handle_cli_args_add_preset(self):
        # Test with only a duration given and debug flag
        # Mock Preset class and configure methods
        libminutaria.Preset = Mock()

        add_return_value = {"name": 'truc', "duration": {"hours": 1,
                                                       "min": 2,
                                                       "secs": 3}
                           }

        libminutaria.Preset.return_value.add.return_value = add_return_value
        # Create Namespace object as handle_cli_args() test's parameter
        dict_to_args = {"add_preset": 'truc',
                "debug": False,
                "del_preset": None,
                "hours": None,
                "minutes": None,
                "modify_preset_duration": None,
                "rename_preset": None,
                "seconds": 22,
                "use_preset": None}
        add_preset = Namespace()
        for arg in dict_to_args:
            setattr(add_preset, arg, dict_to_args[arg])

        with self.assertRaises(SystemExit):
            args = libminutaria.handle_cli_args(add_preset)
            self.assertEqual(args, 'New preset added: Truc - 0:00:22')
            Preset.assert_called_once_with('truc', hours=0, minutes=0, seconds=22)
            Preset.return_value.add.assert_called()
"""
if __name__ == '__main__':
    #pass
    unittest.main()
