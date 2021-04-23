minutaria
=========

minutaria is a basic Python timer. The project is educational, it aims to teach myself programming, python programming, python's stdlib, tools (pdb, venv...) and ecosystem, development best pratices, git and some software testing libraries or frameworks.

Done features
-------------

- Use OOP approach
- Use *datetime* module
- Display time ISO 8601 format like as hh:mm:ss.n
- ncurses interface via curses Python standard module

Expected features
-----------------

- Accept argument in a terminal using a standard module
- Manage presets with a text file
- Pythonic code (idiomatic style, PEP8...)
- Play a sound at 00:00:00.0
- Usable with a GTK GUI and so :
    - theming light/dark
    - reset the timer
    - use preset
    - add preset
    - alarm period
    - alarm volume

Dependencies
------------

Nothing except Python 3 and modules from the standard library, currently only *datetime*, *curses* for the ncurses interface.

Use
---

minutaria.py module contains a basic term example.
minutaria_curses.py is the basic ncurses interface.

License
-------

minutaria is licensed under `the MIT/Expat License
<https://spdx.org/licenses/MIT.html>`_. See LICENSE file for details.


