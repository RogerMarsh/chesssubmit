# selectemail.py
# Copyright 2022 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Email selection filter User Interface for Submit Results application."""
from chessvalidate.gui import selectemail

from . import fileaccess


class SelectEmail(fileaccess.FileAccess, selectemail.SelectEmail):
    """Add store configuration file to select.Select for opening files."""
