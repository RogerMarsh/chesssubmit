# submissionedit.py
# Copyright 2022 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Submission file data edit class."""

import tkinter
import tkinter.messagebox

from solentware_misc.gui import panel


class SubmissionEdit(panel.PlainPanel):
    """The Edit panel for submission data."""

    btn_opensubmission = "submission_open"  # menu button only
    btn_closesubmission = "submission_close"
    _btn_savesubmission = "submission_save"
    _btn_submit = "submission_submit"

    def __init__(self, parent=None, cnf=None, **kargs):
        """Extend and define results data input panel for results database."""
        super().__init__(parent=parent, cnf=cnf, **kargs)
        self.show_buttons_for_submit()
        self.create_buttons()
        self.folder = tkinter.Label(
            master=self.get_widget(),
            text=self.get_context().submission_folder,
        )
        self.folder.pack(side=tkinter.TOP, fill=tkinter.X)
        self.toppane = tkinter.PanedWindow(
            master=self.get_widget(),
            opaqueresize=tkinter.FALSE,
            orient=tkinter.HORIZONTAL,
        )
        self.toppane.pack(side=tkinter.TOP, expand=True, fill=tkinter.BOTH)
        self.show_submission()
        # self.editedtext.edit_modified(tkinter.FALSE)

    def close(self):
        """Close resources prior to destroying this instance.

        Used, at least, as callback from AppSysFrame container.

        """

    def describe_buttons(self):
        """Define all action buttons that may appear on data input page."""
        self.define_button(
            self._btn_savesubmission,
            text="Save",
            tooltip=(
                "Save edited results data with changes from original noted."
            ),
            underline=2,
            command=self.on_save,
        )
        self.define_button(
            self._btn_submit,
            text="Submit",
            tooltip="Save submission generated from source data.",
            underline=1,
            command=self.on_submit,
        )
        self.define_button(
            self.btn_closesubmission,
            text="Close",
            tooltip="Close the folder containing data.",
            underline=0,
            switchpanel=True,
            command=self.on_close_data,
        )

    def get_context(self):
        """Return the data input page."""
        return self.get_appsys().get_submission_context()

    def on_close_data(self, event=None):
        """Close the source document."""
        del event
        self.close_data_folder()
        self.inhibit_context_switch(self.btn_closesubmission)

    def on_save(self, event=None):
        """Save source document."""
        del event
        self.save_data_folder()

    def on_submit(self, event=None):
        """Create ECF submission file from validated source document.

        Reported ECF codes are used witout question or by references to
        entries in the event configuration file.

        """
        del event
        self.submit_results_to_ecf()

    def show_buttons_for_submit(self):
        """Show buttons for actions allowed after generating reports."""
        self.hide_panel_buttons()
        self.show_panel_buttons(
            (
                self.btn_closesubmission,
                self._btn_savesubmission,
                self._btn_submit,
            )
        )

    def show_submission(self):
        """Display widgets showing submission data."""
        self._hide_panes()

    def _hide_panes(self):
        """Forget the configuration of PanedWindows on submission page."""
        for pane in (self.toppane,):
            if pane is not None:
                for widget in pane.panes():
                    pane.forget(widget)

    def close_data_folder(self):
        """Show close data input file dialogue and return True if closed."""
        if self.is_report_modified():
            if not tkinter.messagebox.askyesno(
                parent=self.get_widget(),
                message="".join(
                    (
                        "Event data has been modified.\n\n",
                        "Do you want to close without saving?",
                    )
                ),
                title="Close",
            ):
                return
        self.get_context().submission_close()

    def save_data_folder(self):
        """Show save data input file dialogue and return True if saved."""
        tkinter.messagebox.showinfo(
            parent=self.get_widget(),
            message="Placeholder for save submission dialogue",
            title="Save ECF Submission File",
        )

    def is_report_modified(self):
        """Return Text.edit_modified(). Work around see Python issue 961805."""
        # return self.editedtext.edit_modified()
        # return self.editedtext.winfo_toplevel().tk.call(
        #     "eval", "%s edit modified" % self.editedtext
        # )
        return True

    def submit_results_to_ecf(self):
        """Create submission file and enter dialogue to submit to ECF."""
        tkinter.messagebox.showinfo(
            parent=self.get_widget(),
            message="Placeholder for submission to ECF dialogue",
            title="Submit ECF Submission File",
        )
