# resultsroot.py
# Copyright 2010 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Results submission application."""

from solentware_bind.gui.exceptionhandler import ExceptionHandler

import chessvalidate.gui.resultsroot

from .. import APPLICATION_NAME
from . import help_
from . import eventdetails

# This statement gets a protected-access message from pylint.
# Cannot set by set_application_name() because chessvalidate.gui.resultsroot
# has already done a call to this method.
# ExceptionHandler.set_application_name(APPLICATION_NAME)
ExceptionHandler._application_name = APPLICATION_NAME


class Results(chessvalidate.gui.resultsroot.Results):
    """Results application."""

    def help_about(self):
        """Display information about Submit Results application."""
        help_.help_about(self.root)

    def help_guide(self):
        """Display brief User Guide for Submit Results application."""
        help_.help_guide(self.root)

    def help_keyboard(self):
        """Display list of keyboard actions for Submit Results application."""
        help_.help_keyboard(self.root)

    def configure_event_details(self):
        """Set event details to event and for ECF results submission files."""
        eventdetails.EventDetails(
            master=self.root,
            use_toplevel=True,
            application_name="".join(
                (self.get_application_name(), " (event details)")
            ),
        )
