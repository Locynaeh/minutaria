minutaria
=========

minutaria is a basic Python timer. The project is educational, it aims to teach myself programming, python programming, python's stdlib, tools (pdb, venv...) and ecosystem, development best pratices, git and some software testing libraries or frameworks.

Done features
-------------

- Use OOP approach
- Use *datetime* module
- Display time ISO 8601 format like as hh:mm:ss.n
- ncurses interface via *curses* Python standard module with basic start/relaunch/quit command

Expected features
-----------------

- Accept argument in a terminal using a standard module to select duration
- Manage presets with a text file
- Usable with a GTK GUI and so :
    - theming light/dark
    - reset the timer
    - use preset
    - add preset
    - alarm period
    - alarm volume
    - play a sound at 00:00:00.0
- Pythonic code (idiomatic style, PEP8...)

Dependencies
------------

Nothing except Python 3 and modules from the standard library, currently only *datetime* and *curses* for the ncurses interface.

Use
---

libminutaria.py module contains a basic terminal example and so can be launched via command line.

minutaria_curses.py contains the basic ncurses interface and can also be launched via command line. It offers a start/relaunch/quit functionality.

License
-------

minutaria is licensed under `the MIT/Expat License
<https://spdx.org/licenses/MIT.html>`_. See LICENSE file for details.


