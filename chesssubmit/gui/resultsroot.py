# resultsroot.py
# Copyright 2010 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Results submission application."""

from solentware_misc.gui.exceptionhandler import ExceptionHandler

import chessvalidate.gui.resultsroot

from .. import APPLICATION_NAME
from . import help_
from . import configure
from . import selectemail

# Cannot set by set_application_name() because chessvalidate.gui.resultsroot
# has already done a call to this method.
# ExceptionHandler.set_application_name(APPLICATION_NAME)
ExceptionHandler._application_name = APPLICATION_NAME


class Results(chessvalidate.gui.resultsroot.Results):
    """Results application."""

    def configure_extract_text_from_emails(self):
        """Set parameters that control results extraction from emails."""
        configure.Configure(
            master=self.root,
            use_toplevel=True,
            application_name="".join((APPLICATION_NAME, " (extract text)")),
        )

    def configure_email_selection(self):
        """Set parameters that control email selection from mailboxes."""
        selectemail.SelectEmail(
            master=self.root,
            use_toplevel=True,
            application_name="".join((APPLICATION_NAME, " (select emails)")),
        )

    def help_about(self):
        """Display information about Submit Results application."""
        help_.help_about(self.root)

    def help_guide(self):
        """Display brief User Guide for Submit Results application."""
        help_.help_guide(self.root)

    def help_keyboard(self):
        """Display list of keyboard actions for Submit Results application."""
        help_.help_keyboard(self.root)
