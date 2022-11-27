# leagues_submit.py
# Copyright 2022 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Results submission Leagues frame class."""

import tkinter
import os

from chessvalidate.gui import leagues_validate

from ..core import configuration
from ..core import constants
from ..core.submission import Submission
from . import sourceedit
from . import submissionedit
from .. import ERROR_LOG


class Leagues(leagues_validate.Leagues):
    """The Results frame for a Results database."""

    _menu_opensubmission = "leagues_submit_menu_opensubmission"
    _tab_results = "leagues_submit_tab_results"
    _state_resultsopen = "leagues_submit_state_resultsopen"
    _state_dataopen_resultsopen = "leagues_submit_state_dataopen_resultsopen"

    def __init__(self, master=None, cnf=None, **kargs):
        """Extend and define the results database results frame."""
        super().__init__(master=master, cnf=cnf, **kargs)
        self._submission_folder = None
        self.submission_data = None

    @property
    def submission_folder(self):
        """Return path to folder containing open submission data file."""
        return self._submission_folder

    def define_menus(self):
        """Override. Define the application menus."""
        menu1 = tkinter.Menu(self.menubar, tearoff=False)
        menu1.add_command(
            label="Open",
            underline=0,
            command=self.try_command(self.submission_open, menu1),
        )
        menu1.add_command(
            label="Close",
            underline=0,
            command=self.try_command(self.submission_close, menu1),
        )
        menu1.add_separator()
        menu1.add_command(
            label="Delete",
            underline=0,
            command=self.try_command(self.delete_submission_file, menu1),
        )
        menu2 = tkinter.Menu(self.menubar, tearoff=False)
        menu2.add_command(
            label="Open",
            underline=0,
            command=self.try_command(self.results_open, menu2),
        )
        menu2.add_command(
            label="Close",
            underline=0,
            command=self.try_command(self.results_close, menu2),
        )

        # subclasses may want to add commands to menu2
        self.menu_results = menu2

        self.menubar.add_cascade(label="Documents", menu=menu2, underline=0)
        self.menubar.add_cascade(label="Results", menu=menu1, underline=0)

    def define_tabs(self):
        """Define the application tabs."""
        super().define_tabs()
        # The 'Edit' tab defined by super() call has no accelerator by
        # default because it is usually displayed by itself: here it is
        # worth setting.
        self._tab_description[self._tab_sourceedit].underline = 0
        self.define_tab(
            self._tab_results,
            text="Edit submission to ECF",
            tooltip="Open and close submission files and submit data.",
            underline=7,
            tabclass=self.submission_edit,
            create_actions=(),
            destroy_actions=(
                submissionedit.SubmissionEdit.btn_closesubmission,
            ),
        )

    def define_tab_states(self):
        """Return dict of <state>:tuple(<tab>, ...)."""
        tab_states = super().define_tab_states()
        tab_states.update(
            {
                self._state_resultsopen: (self._tab_results,),
                self._state_dataopen_resultsopen: (
                    self._tab_sourceedit,
                    self._tab_results,
                ),
            }
        )
        return tab_states

    def define_state_switch_table(self):
        """Return dict of tuple(<state>, <action>):list(<state>, <tab>)."""
        switch_table = super().define_state_switch_table()
        switch_table.update(
            {
                (self._state_resultsopen, self._menu_opendata): [
                    self._state_dataopen_resultsopen,
                    self._tab_sourceedit,
                ],
                (self._state_dataopen, self._menu_opensubmission): [
                    self._state_dataopen_resultsopen,
                    self._tab_results,
                ],
                (
                    self._state_dataopen_resultsopen,
                    self._menu_opendata,
                ): [self._state_dataopen_resultsopen, self._tab_sourceedit],
                (
                    self._state_dataopen_resultsopen,
                    self._menu_opensubmission,
                ): [self._state_dataopen_resultsopen, self._tab_results],
                (
                    self._state_dbclosed,
                    submissionedit.SubmissionEdit.btn_opensubmission,
                ): [self._state_resultsopen, self._tab_results],
                (
                    self._state_dataopen,
                    submissionedit.SubmissionEdit.btn_opensubmission,
                ): [self._state_dataopen_resultsopen, self._tab_sourceedit],
                (
                    self._state_dataopen_resultsopen,
                    sourceedit.SourceEdit.btn_closedata,
                ): [self._state_resultsopen, self._tab_results],
                (
                    self._state_resultsopen,
                    submissionedit.SubmissionEdit.btn_closesubmission,
                ): [self._state_dbclosed, None],
                (
                    self._state_dataopen_resultsopen,
                    submissionedit.SubmissionEdit.btn_closesubmission,
                ): [self._state_dataopen, self._tab_sourceedit],
                (self._state_dbclosed, self._menu_opensubmission): [
                    self._state_resultsopen,
                    self._tab_results,
                ],
            }
        )
        return switch_table

    @staticmethod
    def document_edit(**kargs):
        """Return sourceedit.SourceEdit class instance."""
        return sourceedit.SourceEdit(**kargs)

    def set_error_file(self):
        """Set the error log for file being opened."""
        # Set the error file in folder of results source data
        Leagues.set_error_file_name(
            os.path.join(
                self._results_folder or self._submission_folder, ERROR_LOG
            )
        )

    @staticmethod
    def make_configuration_instance():
        """Return Configuration() made with imported configuration module.

        Subclasses should override this method to use their configuration
        module if appropriate.

        """
        return configuration.Configuration()

    def results_open(self):
        """Open results source documents."""
        if self._submission_folder is None:
            super().results_open()
            return
        if self._read_results_documents(
            "Open Documents", self._submission_folder
        ):
            self.set_results_edit_context()

    def results_close(self):
        """Close results source document."""
        if self._submission_folder is None:
            super().results_close()
            return
        if self.results_data is None:
            return
        if tkinter.messagebox.askyesno(
            parent=self.get_widget(),
            message="".join(
                (
                    "Close\n",
                    self._results_folder,
                    "\nfolder containing results data",
                )
            ),
            title="Close",
        ):
            self.close_event_edition_results()
            self.switch_context(sourceedit.SourceEdit.btn_closedata)
            self._results_folder = None

    def submission_open(self):
        """Open submission file.

        If a results document is open the submission file in results folder
        is opened.

        """
        if self._results_folder is None:
            open_submission = self._submission_open()
            if open_submission:
                self.set_error_file()
        else:
            open_submission = self._read_submission_file(
                "Open Submission", self._results_folder
            )
        if open_submission:
            self.set_submission_edit_context()

    def set_submission_edit_context(self):
        """Display the submission edit page."""
        self.switch_context(self._menu_opensubmission)

    def _submission_open(self, title=" "):
        """Choose a folder and open it's submission file."""
        assert self._results_folder is None
        title = "".join(("Open", title, "Submission"))

        if not self.is_state_switch_allowed(self._menu_opensubmission):
            tkinter.messagebox.showinfo(
                parent=self.get_widget(),
                message="Cannot open a Submission file from the current tab",
                title=title,
            )
            return None

        if self.submission_data:
            tkinter.messagebox.showinfo(
                parent=self.get_widget(),
                message="".join(
                    (
                        "Close the submission document in\n",
                        self._submission_folder,
                        "\nfirst.",
                    )
                ),
                title=title,
            )
            return None

        conf = self.make_configuration_instance()
        initdir = conf.get_configuration_value(constants.RECENT_DOCUMENT)
        submission_folder = tkinter.filedialog.askdirectory(
            parent=self.get_widget(),
            title=" ".join((title, "folder")),
            initialdir=initdir,
        )
        if not submission_folder:
            return None
        if not os.path.exists(submission_folder):
            tkinter.messagebox.showinfo(
                parent=self.get_widget(),
                message="".join(
                    (
                        submission_folder,
                        "\ndoes not exist.",
                        "\nCreate initial submission via the ",
                        "Documents menu",
                    )
                ),
                title=title,
            )
            return None
        return self._read_submission_file(title, submission_folder, conf=conf)

    def _read_submission_file(self, title, submission_folder, conf=None):
        """Read submission file from submission folder."""
        submission_data = Submission(submission_folder)
        try:
            if not submission_data.open_documents(self.get_widget()):
                return None
        except FileNotFoundError:
            tkinter.messagebox.showinfo(
                parent=self.get_widget(),
                message="".join(
                    (
                        os.path.join(
                            submission_data.folder, constants.SUBMISSION
                        ),
                        "\ndoes not exist.",
                        "\nCreate initial submission via the ",
                        "Documents menu",
                    )
                ),
                title=title,
            )
            return None
        self.submission_data = submission_data
        if self._submission_folder != submission_folder:
            if conf is None:
                conf = self.make_configuration_instance()
            conf.set_configuration_value(
                constants.RECENT_DOCUMENT,
                conf.convert_home_directory_to_tilde(submission_folder),
            )
            self._submission_folder = submission_folder
        return True

    def delete_submission_file(self):
        """Delete submission file."""
        title = "".join(("Delete", " ", "Submission"))
        if self._submission_folder is None:
            tkinter.messagebox.showinfo(
                parent=self.get_widget(),
                message="Submission document is not open",
                title=title,
            )
            return
        self._submission_folder = None

    @staticmethod
    def submission_edit(**kargs):
        """Return control_database.Control class instance."""
        return submissionedit.SubmissionEdit(**kargs)

    def get_submission_context(self):
        """Return the submission input page."""
        return self

    def submission_close(self):
        """Close submission document."""
        if self._submission_folder is None:
            return
        if tkinter.messagebox.askyesno(
            parent=self.get_widget(),
            message="".join(
                (
                    "Close\n",
                    self._submission_folder,
                    "\nfolder containing results data",
                )
            ),
            title="Close",
        ):
            self.close_event_edition_submission()
            self._submission_folder = None
            self.switch_context(
                submissionedit.SubmissionEdit.btn_closesubmission
            )
            if self._results_folder is None:
                self.set_error_file_on_close_source()

    def close_event_edition_submission(self):
        """Close submission files."""
        self.submission_data.close()
        self.submission_data = None
