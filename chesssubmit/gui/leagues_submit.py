# leagues_submit.py
# Copyright 2022 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Results submission Leagues frame class."""

import os

from chessvalidate.gui import leagues_validate

from . import sourceedit
from .. import ERROR_LOG
from ..core import configuration


class Leagues(leagues_validate.Leagues):
    """The Results frame for a Results database."""

    def document_edit(self, **kargs):
        """Return sourceedit.SourceEdit class instance."""
        return sourceedit.SourceEdit(**kargs)

    def set_error_file(self):
        """Set the error log for file being opened."""
        # Set the error file in folder of results source data
        Leagues.set_error_file_name(
            os.path.join(self.results_folder, ERROR_LOG)
        )

    def make_configuration_instance(self):
        """Return Configuration() made with imported configuration module.

        Subclasses should override this method to use their configuration
        module if appropriate.

        """
        return configuration.Configuration()
