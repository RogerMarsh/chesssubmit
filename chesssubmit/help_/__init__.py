# __init__.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Help files for Submit Results."""

import os

ABOUT = "About"
GUIDE = "Guide"
ACTIONS = "Actions"

_textfile = {
    ABOUT: ("aboutresults",),
    GUIDE: ("guide",),
    ACTIONS: ("keyboard",),
}

folder = os.path.dirname(__file__)

for k in list(_textfile.keys()):
    _textfile[k] = tuple(
        os.path.join(folder, ".".join((n, "txt"))) for n in _textfile[k]
    )

del folder, k, os
