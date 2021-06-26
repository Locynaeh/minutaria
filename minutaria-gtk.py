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

        self.preset_box = PresetBox()
        self.pack_start(self.preset_box, False, True, 0)


class TimerBox(Gtk.Box):
    """Container to all the timer management elements."""
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.intro_box = IntroBox()
        self.pack_start(self.intro_box, False, True, 0)

        self.separator = SeparatorBox()
        self.pack_start(self.separator, False, True, 0)

        self.timing_box = TimingBox()
        self.pack_start(self.timing_box, False, True, 0)

        self.separator = SeparatorBox()
        self.pack_start(self.separator, False, True, 0)

        self.start_pause_button = Gtk.Button(label="Start/Pause")
        self.pack_start(self.start_pause_button, False, True, 0)

        self.reset_stop_button = Gtk.Button(label="Reset/Stop")
        self.pack_start(self.reset_stop_button, False, True, 0)

        self.separator = SeparatorBox()
        self.pack_start(self.separator, False, True, 0)

        self.timing_print = Gtk.Label(label="00:00:00.0")
        self.pack_start(self.timing_print, False, True, 0)

        self.separator = SeparatorBox()
        self.pack_start(self.separator, False, True, 0)


class SeparatorBox(Gtk.Box):
    """Container to an horizontal separator."""
    def __init__(self):
        Gtk.Box.__init__(self)
        self.separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.pack_start(self.separator, True, True, 0)


class IntroBox(Gtk.Box):
    """Container to the instructions and the settings menu."""
    def __init__(self):
        Gtk.Box.__init__(self, spacing=6)
        self.instruction_label = Gtk.Label()
        self.instruction_label.set_label("Please enter a remaining time")
        self.param = Gtk.MenuButton(halign='end')

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

        self.minutes_label = Gtk.Label(label="Minutes")
        adjustment_minutes = Gtk.Adjustment(value=0,
                                          lower=0,
                                          upper=59,
                                          step_increment=1,
                                          page_increment=10,
                                          page_size=0)
        self.minutes_spin = Gtk.SpinButton(orientation=1)  # vertical
        self.minutes_spin.set_adjustment(adjustment_minutes)

        self.seconds_label = Gtk.Label(label="Seconds")
        adjustment_seconds = Gtk.Adjustment(value=0,
                                          lower=0,
                                          upper=59,
                                          step_increment=1,
                                          page_increment=10,
                                          page_size=0)
        self.seconds_spin = Gtk.SpinButton(orientation=1)  # vertical
        self.seconds_spin.set_adjustment(adjustment_seconds)

        self.pack_start(self.hour_label, True, True, 0)
        self.pack_start(self.hours_spin, True, True, 0)
        self.pack_start(self.minutes_label, True, True, 0)
        self.pack_start(self.minutes_spin, True, True, 0)
        self.pack_start(self.seconds_label, True, True, 0)
        self.pack_start(self.seconds_spin, True, True, 0)


class PresetBox(Gtk.Box):
    """Container to all the preset management elements."""
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.instruction_label = Gtk.Label()
        self.instruction_label.set_label("Preset")
        self.instruction_label.set_xalign(0)  # align to the left
        self.pack_start(self.instruction_label, False, True, 0)

        self.separator = SeparatorBox()
        self.pack_start(self.separator, False, True, 0)

        self.add_preset_box = AddPresetBox()
        self.pack_start(self.add_preset_box, False, True, 0)

        self.del_preset_box = DelPresetBox()
        self.pack_start(self.del_preset_box, False, True, 0)


class AddPresetBox(Gtk.Box):
    """Container to all the necessary elements to add a new preset."""
    def __init__(self):
        Gtk.Box.__init__(self, spacing=6)

        self.entry_preset_name = Gtk.Entry()
        self.pack_start(self.entry_preset_name, True, True, 0)

        self.add_button = Gtk.Button(label="Add")
        self.pack_start(self.add_button, True, True, 0)


class DelPresetBox(Gtk.Box):
    """Container to all the necessary elements to delete an existing preset."""
    def __init__(self):
        Gtk.Box.__init__(self, spacing=6)

        self.select_preset_name = Gtk.ComboBoxText()
        self.select_preset_name.prepend_text("Choose a preset")
        self.pack_start(self.select_preset_name, True, True, 0)

        self.del_button = Gtk.Button(label="Del")
        self.pack_start(self.del_button, True, True, 0)


if __name__ == '__main__':
    main_window = MainWindow()
    main_window.connect("destroy", Gtk.main_quit)
    main_window.show_all()
    Gtk.main()
