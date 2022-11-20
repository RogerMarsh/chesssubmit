# configure.py
# Copyright 2014 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Describe the emails and attachments containing event results."""
from chessvalidate.gui import configure

from . import fileaccess


class Configure(fileaccess.FileAccess, configure.Configure):
    """Define and use an event result's extraction configuration file."""

    _READ_FILE_TITLE = "Submit Extraction Rules"
