minutaria
=========

minutaria is a basic Python timer.

The project is educational, it aims to teach myself programming, python programming, python's stdlib, tools (pdb, venv, mypy...) and ecosystem, development best pratices, git and some software testing libraries or frameworks.

The project is separed in 3 parts:

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
- Some fixes with Flake8 and PyLint
- Minimal documentation
- Minimal log system

Expected
--------

- Usable with a GTK GUI and so:
    - theming light/dark
    - reset the timer
    - add/use/manage presets
    - alarm period
    - alarm volume
    - play a sound at 00:00:00.0
- Pythonic code (idiomatic style, PEP8...)
- Unit tests

Dependencies
------------

Nothing except Python 3 and modules from the standard library for the lib and the ncurses TUI, currently :

- *datetime*, *argparse*, *logging* and *json* for the lib
- *curses*, *datetime*, *logging* and *os* for the ncurses interface.

For the GTK GUI, please follow `the guide <https://pygobject.readthedocs.io/en/latest/getting_started.html#gettingstarted>`_.

For me, in short, on Debian, with pip in a venv virtual environment:

- Create virtual environment:
    ``python3 -m venv venv``
- Enter it:
    ``source venv/bin/activate``
- Execute the following command to install the build dependencies and GTK:
    ``sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0``
- Execute:
    ``pip3 install pycairo``
- Execute
    ``pip3 install PyGObject``

A requirement.txt is inclued in this repository for the two last steps.

Use
---

libminutaria.py module contains is fully usable via command line. Execute a default timer if launched without argument. Use -h/--help arguments for more information.

minutaria_curses.py contains the basic ncurses interface and so shall be launched via command line. It offers a start/relaunch/quit functionality and is fully usable with CLI arguments identically to libminutaria.py. This user interface shall only be use on Unix system as the Windows version isn't included in the standard library, the script contains a WINDOWS_CHECK parameter for this purpose. Nervertheless it should be usable with WSL (not tested).

License
-------

minutaria is licensed under `the MIT/Expat License
<https://spdx.org/licenses/MIT.html>`_. See LICENSE file for details.


