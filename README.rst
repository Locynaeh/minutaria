minutaria
=========

minutaria is a basic Python timer.

The project is educational, it aims to teach myself programming, python programming, python's stdlib, tools (pdb, venv...) and ecosystem, development best pratices, git and some software testing libraries or frameworks.

The project is separed in 3 parts :

- a module as a library, completely usable as a CLI utility
- a simple ncurses GUI using parts of the module
- a GTK GUI using the full module

Done
----

- Use OOP approach
- Use *datetime* module
- Use *argparse* module to built the CLI utility
- Display time ISO 8601 format like as hh:mm:ss.n
- ncurses interface via *curses* Python standard module with basic start/relaunch/quit command

Expected
--------

- Manage presets with a text file
- Usable with a GTK GUI and so :
    - theming light/dark
    - reset the timer
    - add/use/manage presets
    - alarm period
    - alarm volume
    - play a sound at 00:00:00.0
- Improve ncurses GUI with presets management
- Pythonic code (idiomatic style, PEP8...)
- Type checking

Dependencies
------------

Nothing except Python 3 and modules from the standard library, currently :

- *datetime*, *argparse* and *sys* for the lib
- *curses* and *datetime* for the ncurses interface.

Use
---

libminutaria.py module contains is fully usable (except presets management for now) via command line. Execute a default timer if launched without argument. Use -h/--help arguments for more information.

minutaria_curses.py contains the basic ncurses interface and so can also be launched via command line. It offers a start/relaunch/quit functionality but doesn't use CLI arguments at the moment.

License
-------

minutaria is licensed under `the MIT/Expat License
<https://spdx.org/licenses/MIT.html>`_. See LICENSE file for details.


