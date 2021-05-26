minutaria
=========

minutaria is a basic Python timer.

The project is educational, it aims to teach myself programming, python programming, python's stdlib, tools (pdb, venv, mypy...) and ecosystem, development best pratices, git and some software testing libraries or frameworks.

The project is separed in 3 parts :

- a module as a library, completely usable as a CLI utility
- a simple ncurses GUI using parts of the module
- a GTK GUI using the full module

Done
----

- Use OOP approach
- Use *datetime* module
- Display time ISO 8601 format like as hh:mm:ss.n
- Use *argparse* module to build the CLI utility
- Manage presets and use *json* module to store them
- ncurses interface via *curses* Python standard module with basic start/relaunch/quit command also usable with the lib's CLI
- Gradually introduce type hints

Expected
--------

- Usable with a GTK GUI and so :
    - theming light/dark
    - reset the timer
    - add/use/manage presets
    - alarm period
    - alarm volume
    - play a sound at 00:00:00.0
- Pythonic code (idiomatic style, PEP8...)
- Type checking
- Unit tests

Dependencies
------------

Nothing except Python 3 and modules from the standard library, currently :

- *datetime*, *argparse*, *sys* and *json* for the lib
- *curses* and *datetime* for the ncurses interface.

Use
---

libminutaria.py module contains is fully usable via command line. Execute a default timer if launched without argument. Use -h/--help arguments for more information.

minutaria_curses.py contains the basic ncurses interface and so shall be launched via command line. It offers a start/relaunch/quit functionality and is fully usable with CLI arguments identically to libminutaria.py. This user interface shall only be use on Unix system as the Windows version isn't included in the standard library, nervertheless it should be usable with WSL (not tested).

License
-------

minutaria is licensed under `the MIT/Expat License
<https://spdx.org/licenses/MIT.html>`_. See LICENSE file for details.


