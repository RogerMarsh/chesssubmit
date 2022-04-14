# configuration.py
# Copyright 2022 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Access and update names of last used configuration files.

The initial values are taken from file named in self._RESULTS_CONF in the
user's home directory if the file exists.

"""

from chessvalidate.core import configuration

from ..core import constants


class Configuration(configuration.Configuration):
    """Identify configuration and recent files and delegate to superclass."""

    _RESULTS_CONF = ".chesssubmit.conf"
    _DEFAULT_RECENTS = (
        (constants.RECENT_EMAIL_SELECTION, "~"),
        (constants.RECENT_EMAIL_EXTRACTION, "~"),
        (constants.RECENT_DOCUMENT, "~"),
        (constants.RECENT_SOURCE_SUBMISSION, "~"),
    )
