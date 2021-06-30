#!/usr/bin/env python3

"""
libminutaria-gtk
================

:Authors:
    Locynaeh
:Version:
    1.0

GTK Graphical User Interface (GUI)) based on the libminutaria library.

This script is also directly usable in a terminal. Use -h/--help arguments
for more information on how to use the CLI provided.
"""

import logging
logging.basicConfig(level=logging.DEBUG)
from datetime import timedelta
from time import sleep
from libminutaria import Timer, Preset, logger
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MainWindow(Gtk.Window):
    """Main windows contaning all the containers of the application."""
    def __init__(self):
        Gtk.Window.__init__(self, title="minutaria", resizable=False)

        self.app_box = AppBox()
        self.add(self.app_box)


class AppBox(Gtk.Box):
    """Container to the timer part and the preset parts."""
    def __init__(self):
        Gtk.Box.__init__(self,
                         orientation=Gtk.Orientation.VERTICAL,
                         spacing=6,
                         halign='center',
                         valign='center',
                         margin_left=7,
                         margin_right=7,
                         margin_top=7,
                         margin_bottom=7)

        self.timer_box = TimerBox()
        self.pack_start(self.timer_box, False, True, 0)

        self.preset_grid = PresetGrid(self.timer_box)
        self.pack_start(self.preset_grid, False, True, 0)


class TimerBox(Gtk.Box):
    """Container to all the timer management elements."""
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.intro_box = IntroBox()
        self.pack_start(self.intro_box, False, True, 0)

        self.intro_separator = SeparatorBox()
        self.pack_start(self.intro_separator, False, True, 0)

        self.timing_box = TimingBox()
        self.pack_start(self.timing_box, False, True, 0)

        self.timing_separator = SeparatorBox()
        self.pack_start(self.timing_separator, False, True, 0)

        self.timing_print = Gtk.Label(label="0:00:00")
        self.pack_start(self.timing_print, False, True, 10)

        self.start_pause_button = Gtk.Button(label="Start/Pause")
        self.start_pause_button.connect('clicked',
                                        self.start_selected_timer,
                                        self.timing_print,
                                        self.timing_box)
        self.pack_start(self.start_pause_button, False, True, 0)

        self.reset_stop_button = Gtk.Button(label="Reset/Stop")
        self.reset_stop_button.connect('clicked',
                                        self.reset_stop_timer,
                                        self.timing_print,
                                        self.timing_box)
        self.pack_start(self.reset_stop_button, False, True, 0)

        self.end_timer_separator = SeparatorBox()
        self.pack_start(self.end_timer_separator, False, True, 0)

        self.state = 0  # 0: stopped, 1: running, 2: paused
        self.timer = Timer(hours=0, minutes=0, seconds=0)
        self.counter = False

    def zero_timing_dialog(self) -> None:
        """Display a message dialog corresponding to an empty timing selection.

        Create a warning message dialog with a corresponding title and text.
        Add an "OK" button to close the dialog. Manage in the same way a close
        action on the dialog by the user.
        """
        # Create and display a message dialog
        # to handle the no duration selection
        no_duration = Gtk.MessageDialog(buttons=Gtk.ButtonsType.NONE,
                                        modal=True,
                                        message_type=Gtk.MessageType.INFO,
                                        text="No duration selected")
        no_duration.format_secondary_text(f"Please select a duration "
                                          f"superior to 00:00:00")
        no_duration.add_button("OK", Gtk.ResponseType.OK)

        # Close the dialog if OK button is pressed or window is closed
        response = no_duration.run()
        if (response == Gtk.ResponseType.OK
            or response == Gtk.ResponseType.DELETE_EVENT):
            no_duration.destroy()

    def start_selected_timer(self, button, label, timing_box) -> None:
        """Handle start/pause/restart a choosen timer.

        Get the selected timing by the user on the spinboxes.
        Manage timing == 0 to display a message dialog in case of.
        Then check the state :
         - if "stopped", set it to "running" and initialize the timer
           according to the user selection
         - if "running", set it to "paused"
         - if "paused", set it to "running" and actualize the existing timer.
        Finally manage the timer to run it until 00:00:00 and print 3 times a
        "GONG !".
        Checking state in the process, break if "paused".
        A the end, set the state to "stopped".
        """
        # Get the selected timing
        selection = timing_box.get_entry()

        # Check whether the timing is valid and handle the state of the timer
        if (selection["timer_hours"] == 0
            and selection["timer_min"] == 0
            and selection["timer_secs"] == 0):
            self.zero_timing_dialog()

            # Actualize the state
            self.state = 0
        else:
            # Handle state
            if self.state == 0:
                # If state was "stopped", then change it to "running"
                self.state = 1

                # Initialize the timer according to the user selection
                self.timer = Timer(hours=selection["timer_hours"],
                                   minutes=selection["timer_min"],
                                   seconds=selection["timer_secs"])
            elif self.state == 1:
                # If the timer was running, change the state to "paused"
                self.state = 2
            elif self.state == 2:
                # The timer was "paused" and now relauched
                # So change the state to "started" and handle the pause effect
                self.state = 1
                self.timer.continue_after_pause()

            # Check remaining time along the timer and print it
            self.counter = self.timer.is_timing_reached()
            while self.counter is False:
                label.set_label(self.timer.get_timing[:9])
                while Gtk.events_pending():
                    Gtk.main_iteration()
                self.counter = self.timer.is_timing_reached()
                # Handle a pause state
                if self.state != 1:
                    break

            if self.counter:
                # Timer reached 00:00:00 so print 3 "GONG !"
                label.set_label("GONG ! GONG ! GONG !")

                # Set state to "stopped" since the timer ended
                self.state = 0

    def reset_stop_timer(self, button, label, timing_box) -> None:
        """Handle reset/stop the timer.

        Set the state of the timer to "stopped" (0) and set the timer label
        to the selected value by the user on the spinboxes.
        """
        self.state = 0
        selection = timing_box.get_entry()

        # Printable default duration
        printable_selection = timedelta(hours=+selection["timer_hours"],
                                     minutes=+selection["timer_min"],
                                     seconds=+selection["timer_secs"])
        label.set_label(str(printable_selection))

class SeparatorBox(Gtk.Box):
    """Container to an horizontal separator."""
    def __init__(self, orientation=Gtk.Orientation.HORIZONTAL):
        Gtk.Box.__init__(self)
        self.orientation = orientation
        self.separator = Gtk.Separator(orientation=self.orientation)
        self.pack_start(self.separator, True, True, 0)


class IntroBox(Gtk.Box):
    """Container to the instructions and the settings menu."""
    def __init__(self):
        Gtk.Box.__init__(self, spacing=6)
        self.instruction_label = Gtk.Label()
        self.instruction_label.set_label("Please enter a remaining time")
        self.instruction_label.set_xalign(1)  # align to the center

        self.param = Gtk.MenuButton(halign='end')
        self.param.set_direction(Gtk.ArrowType(4))

        self.pack_start(self.instruction_label, True, True, 0)
        self.pack_start(self.param, True, True, 0)

class TimingBox(Gtk.Box):
    """Container to all the necessary elements to select a timing HH.MM.SS."""
    def __init__(self):
        Gtk.Box.__init__(self, spacing=6)
        self.hour_label = Gtk.Label(label="Hours")
        adjustment_hours = Gtk.Adjustment(value=0,
                                          lower=0,
                                          upper=23,
                                          step_increment=1,
                                          page_increment=10,
                                          page_size=0)
        self.hours_spin = Gtk.SpinButton(orientation=1)  # vertical
        self.hours_spin.set_adjustment(adjustment_hours)

        self.hm_separator = SeparatorBox(orientation=Gtk.Orientation.VERTICAL)

        self.minutes_label = Gtk.Label(label="Minutes")
        adjustment_minutes = Gtk.Adjustment(value=0,
                                          lower=0,
                                          upper=59,
                                          step_increment=1,
                                          page_increment=10,
                                          page_size=0)
        self.minutes_spin = Gtk.SpinButton(orientation=1)  # vertical
        self.minutes_spin.set_adjustment(adjustment_minutes)

        self.ms_separator = SeparatorBox(orientation=Gtk.Orientation.VERTICAL)

        self.seconds_label = Gtk.Label(label="Seconds")
        adjustment_seconds = Gtk.Adjustment(value=0,
                                          lower=0,
                                          upper=59,
                                          step_increment=1,
                                          page_increment=10,
                                          page_size=0)
        self.seconds_spin = Gtk.SpinButton(orientation=1)  # vertical
        self.seconds_spin.set_adjustment(adjustment_seconds)

        self.pack_start(self.hour_label, True, True, 2)
        self.pack_start(self.hours_spin, True, True, 1)
        self.pack_start(self.hm_separator, False, True, 5)
        self.pack_start(self.minutes_label, True, True, 2)
        self.pack_start(self.minutes_spin, True, True, 1)
        self.pack_start(self.ms_separator, False, True, 5)
        self.pack_start(self.seconds_label, True, True, 2)
        self.pack_start(self.seconds_spin, True, True, 1)

    def get_entry(self):
        """The values of the timing selection's spin buttons.

        Returns
        -------
        timer_selected: dict
            The duration (hours, minutes and seconds) input by the user.
        """
        timer_selected = {"timer_hours": self.hours_spin.get_value_as_int(),
                          "timer_min": self.minutes_spin.get_value_as_int(),
                          "timer_secs": self.seconds_spin.get_value_as_int()}
        return timer_selected


class PresetGrid(Gtk.Grid):
    """Container to all the preset management elements."""
    def __init__(self, timer_box_access):
        Gtk.Grid.__init__(self)
        self.set_column_spacing(6)
        self.set_row_spacing(6)

        # Get the timer_box to access its methods
        self.timer_box_access = timer_box_access

        # Intro block : title + separator
        self.title_label = Gtk.Label()
        self.title_label.set_label("Preset")
        self.title_label.set_xalign(0)  # align to the left
        self.attach(self.title_label, 0, 0, 3, 1)

        self.separator = SeparatorBox()
        self.attach(self.separator, 0, 1, 3, 1)

        # Add, modify duration or rename existing preset part
        self.entry_preset_name = Gtk.Entry()
        self.entry_preset_name.set_placeholder_text(f"Enter a name to a new "
                                                    f"preset or a new name to "
                                                    f"an existing one")
        self.entry_preset_name.set_tooltip_text(f"Enter a name to a new preset"
                                                f" or a new name to an "
                                                f"existing one.")
        # Force entry to fill the space
        self.entry_preset_name.set_size_request(380, 10)
        self.attach(self.entry_preset_name, 0, 2, 3, 1)

        # Add
        self.add_button = Gtk.Button(label="Add")
        self.add_button.connect('clicked',
                                self.add_new_preset,
                                self.timer_box_access)
        self.attach(self.add_button, 0, 3, 1, 1)

        # Set new duration
        self.set_button = Gtk.Button(label="Set timing")
        self.set_button.connect('clicked',
                                self.set_preset_duration)
        self.attach(self.set_button, 1, 3, 1, 1)

        # Rename
        self.rename_button = Gtk.Button(label="Rename")
        self.rename_button.connect('clicked',
                                   self.rename_preset)
        self.attach(self.rename_button, 2, 3, 1, 1)

        # Deletion part
        self.select_preset_name = Gtk.ComboBoxText()
        self.select_preset_name.prepend_text("Choose a preset")
        self.select_preset_name.set_tooltip_text(f"Select a preset name to use"
                                                f" or to delete.")
        # Force entry to fill the space
        #self.select_preset_name.set_size_request(260, 10)
        self.attach(self.select_preset_name, 0, 4, 2, 1)

        self.del_button = Gtk.Button(label="Delete")
        self.del_button.connect('clicked',
                                self.rename_preset)
        self.attach(self.del_button, 2, 4, 1, 1)

    def empty_name_dialog(self) -> None:
        """Display a message dialog corresponding to an empty name entry.

        Create a warning message dialog with a corresponding title and text.
        Add an "OK" button to close the dialog. Manage in the same way a close
        action on the dialog by the user.
        """
        empty_name = Gtk.MessageDialog(buttons=Gtk.ButtonsType.NONE,
                                       modal=True,
                                       message_type=Gtk.MessageType.WARNING,
                                       text="No name entered")
        empty_name.format_secondary_text("Please enter a name")
        empty_name.add_button("OK", Gtk.ResponseType.OK)

        # Close the dialog if OK button is pressed or window is closed
        response = empty_name.run()
        if (response == Gtk.ResponseType.OK
            or response == Gtk.ResponseType.DELETE_EVENT):
            empty_name.destroy()

    def get_preset_entry(self):
        """The content of the entry.

        Returns
        -------
        str
            The text entered by the user to the corresponding entry.
        """

        return self.entry_preset_name.get_text().strip()

    def add_new_preset(self, button, timer_box_access) -> None:
        """Add a new preset.

        Manage following issue by displaying the appropriate message:
         - name does already exist
         - No name entered
         - Choosen duration equal 00:00:00
        If none of thses issues are raised, add the preset to the JSON preset
        file.
        """

        # Get the user's choosen name
        preset_name = self.get_preset_entry()

        # Check if it's empty and handle it
        if preset_name == "":
            self.empty_name_dialog()
            return

        # Get the selected timing
        selection = timer_box_access.timing_box.get_entry()
        #print(selection)
        if (selection["timer_hours"] == 0
            and selection["timer_min"] == 0
            and selection["timer_secs"] == 0):
            timer_box_access.zero_timing_dialog()
            return


        # Add new preset
        new_preset = Preset(preset_name,
                            selection["timer_hours"],
                            selection["timer_min"],
                            selection["timer_secs"])

        try:
            new_preset.add()
            new_preset_duration = timedelta(hours=+selection["timer_hours"],
                                            minutes=+selection["timer_min"],
                                            seconds=+selection["timer_secs"])

            msg_new = Gtk.MessageDialog(buttons=Gtk.ButtonsType.NONE,
                                        modal=True,
                                        message_type=Gtk.MessageType.WARNING,
                                        text="New preset added")
            msg_new.format_secondary_text(f"{preset_name.capitalize()} - "
                                          f"{str(new_preset_duration)}")
            msg_new.add_button("OK", Gtk.ResponseType.OK)

            # Close the dialog if OK button is pressed or window is closed
            response = msg_new.run()
            if (response == Gtk.ResponseType.OK
                or response == Gtk.ResponseType.DELETE_EVENT):
                msg_new.destroy()

            # Reset the entry
            self.entry_preset_name.set_text("")
        except ValueError:
            msg_not = Gtk.MessageDialog(buttons=Gtk.ButtonsType.NONE,
                                        modal=True,
                                        message_type=Gtk.MessageType.WARNING,
                                        text="Already existing name")
            msg_not.format_secondary_text(f"The preset name "
                                          f"{preset_name.capitalize()} already"
                                          f" exist. Please choose an "
                                          f"other name.")
            msg_not.add_button("OK", Gtk.ResponseType.OK)

            # Close the dialog if OK button is pressed or window is closed
            response = msg_not.run()
            if (response == Gtk.ResponseType.OK
                or response == Gtk.ResponseType.DELETE_EVENT):
                msg_not.destroy()

    def set_preset_duration(self, button):
        pass
        """
        # Modify existing preset
        # Modify the corresponding preset and quit
        try:
            preset_to_modify = Preset(args.modify_preset_duration)
            modified = preset_to_modify.set_duration(timer_values["timer_hours"],
                                                    timer_values["timer_min"],
                                                    timer_values["timer_secs"])
            modified_duration = timedelta(hours=+timer_values["timer_hours"],
                                        minutes=+timer_values["timer_min"],
                                        seconds=+timer_values["timer_secs"])

            if modified:
                print("New preset duration: "
                    f"{args.modify_preset_duration.capitalize()}"
                    f" - {str(modified_duration)}")
                exit()
        except ValueError:
            print(f"The preset {args.modify_preset_duration.capitalize()} "
                "does not exist. Please choose an existing name.")
            exit()
        """
    def rename_preset(self, button):
        pass
        """
        # Rename the corresponding preset and quit
        try:
            preset_to_rename = Preset(args.rename_preset[0])
            renamed = preset_to_rename.rename(args.rename_preset[1])

            if renamed:
                print(f"Preset {args.rename_preset[0].capitalize()} renamed: "
                    f"{args.rename_preset[1].capitalize()}")
                exit()
        except ValueError:
            print(f"The preset {args.rename_preset[0].capitalize()} "
                f"does not exist or the new name "
                f"{args.rename_preset[1].capitalize()} is not available.")
            exit()
        """

    def delete_preset(self, button):
        pass
        """
        # Delete the corresponding preset and quit
        try:
            preset_to_delete = Preset(args.del_preset)
            deleted = preset_to_delete.delete()

            if deleted:
                print(f"Preset deleted: {args.del_preset.capitalize()}")
                exit()
        except ValueError:
            print(f"The preset {args.del_preset.capitalize()} does not exist.")
            exit()
        """




if __name__ == '__main__':
    main_window = MainWindow()
    main_window.connect("destroy", Gtk.main_quit)
    main_window.show_all()
    Gtk.main()
