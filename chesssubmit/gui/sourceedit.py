# sourceedit.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Schedule and results raw data edit class.

Add creation of ECF result submission file to SourceEdit class.

"""

import tkinter
import tkinter.messagebox

from chessvalidate.gui import sourceedit

from ..core import constants
from ..core import configuration
from ..core import submission


class SourceEdit(sourceedit.SourceEdit):
    """The Edit panel for raw results data."""

    _btn_submission = "sourceedit_submission"

    def describe_buttons(self):
        """Define all action buttons that may appear on data input page."""
        self.define_button(
            self._btn_generate,
            text="Generate",
            tooltip="Generate data for input to League database.",
            underline=0,
            command=self.on_generate,
        )
        self.define_button(
            self._btn_toggle_compare,
            text="Show Original",
            tooltip=" ".join(
                (
                    "Display original and edited results data but",
                    "not generated data.",
                )
            ),
            underline=5,
            command=self.on_toggle_compare,
        )
        self.define_button(
            self._btn_toggle_generate,
            text="Hide Original",
            tooltip=" ".join(
                (
                    "Display edited source and generated data but",
                    "not original source.",
                )
            ),
            underline=5,
            command=self.on_toggle_generate,
        )
        self.define_button(
            self._btn_save,
            text="Save",
            tooltip=(
                "Save edited results data with changes from original noted."
            ),
            underline=2,
            command=self.on_save,
        )
        self.define_button(
            self._btn_report,
            text="Report",
            tooltip="Save reports generated from source data.",
            underline=2,
            command=self.on_report,
        )
        self.define_button(
            self._btn_submission,
            text="Submit",
            tooltip="Save submission generated from source data.",
            underline=1,
            command=self.on_submit,
        )
        self.define_button(
            self.btn_closedata,
            text="Close",
            tooltip="Close the folder containing data.",
            underline=0,
            switchpanel=True,
            command=self.on_close_data,
        )

    def on_submit(self, event=None):
        """Create ECF submission file from validated source document.

        Reported ECF codes are used witout question or by references to
        entries in the event configuration file.

        """
        del event
        if self.create_ecf_submission():
            self.show_buttons_for_generate()
            self.create_buttons()

    def show_buttons_for_update(self):
        """Show buttons for actions allowed after generating reports."""
        self.hide_panel_buttons()
        self.show_panel_buttons(
            (
                self._btn_generate,
                self._btn_toggle_compare,
                self.btn_closedata,
                self._btn_save,
                self._btn_report,
                self._btn_submission,
            )
        )

    def create_ecf_submission(self):
        """Show create ECF submission dialogue and return True if created."""
        if self.is_report_modified():
            tkinter.messagebox.showinfo(
                parent=self.get_widget(),
                message="".join(
                    (
                        "Event data has been modified.\n\n",
                        "Save the data first.",
                    )
                ),
                title="Create ECF Submission File",
            )
            return False
        folder = self.get_context().results_folder
        conf = configuration.Configuration()
        conf.set_configuration_value(
            constants.RECENT_SOURCE_SUBMISSION,
            conf.convert_home_directory_to_tilde(folder),
        )

        self._collate_unfinished_games()
        results = submission.Submission(folder)
        results.convert_document_to_submission_style(
            self.get_context().results_data
        )
        results.write_entries_to_submission_file()
        return True
