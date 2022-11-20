# sourceedit.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Schedule and results raw data edit class.

Add creation of ECF result submission file to SourceEdit class.

"""

import tkinter
import tkinter.messagebox
import os

from chessvalidate.gui import sourceedit
from chessvalidate.core.gameobjects import (
    get_game_rows_for_csv_format,
    split_codes_from_name,
)
from chessvalidate.core.gameresults import resultmapecf

from ..core import constants
from ..core import configuration


class SourceEdit(sourceedit.SourceEdit):
    """The Edit panel for raw results data."""

    _btn_submit = "sourceedit_submit"

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
            self._btn_submit,
            text="Submit",
            tooltip="Save submission generated from source data.",
            underline=1,
            command=self.on_submit,
        )
        self.define_button(
            self._btn_closedata,
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
                self._btn_closedata,
                self._btn_save,
                self._btn_report,
                self._btn_submit,
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
        conf = configuration.Configuration()
        filename = tkinter.filedialog.asksaveasfilename(
            parent=self.get_widget(),
            title="Create ECF Submission File",
            defaultextension=".txt",
            filetypes=(("ECF results submission file", "*.txt"),),
            initialdir=conf.get_configuration_value(
                constants.RECENT_SOURCE_SUBMISSION
            ),
        )
        if not filename:
            tkinter.messagebox.showwarning(
                parent=self.get_widget(),
                title="Create ECF Submission File",
                message="ECF Submission File file not saved",
            )
            return None
        conf.set_configuration_value(
            constants.RECENT_SOURCE_SUBMISSION,
            conf.convert_home_directory_to_tilde(os.path.dirname(filename)),
        )

        self._collate_unfinished_games()
        trro = {
            item: i
            for i, item in enumerate(constants.TABULAR_REPORT_ROW_ORDER)
        }
        players = {}
        events = {}
        for row in sorted(
            get_game_rows_for_csv_format(
                self.get_context().results_data.get_collated_games()
            )
        ):
            self._process_csv_row(
                {item: row[trro[item]] for item in trro}, players, events
            )
        with open(filename, "w", newline="") as file:
            # The event header is to be supplied.
            file.write("#".join(("\n", constants.PLAYER_LIST)))
            for player in sorted(players):
                file.write(players[player][-1])
            for event in sorted(events):
                subevents = events[event]
                for subevent in sorted(subevents):
                    sections = subevents[subevent]
                    for section in sections:
                        file.write("#".join(("\n", section)))
                        file.write("".join(sections[section]))
            file.write("#".join(("\n", constants.FINISH)))
        return True

    def _process_csv_row(self, row, players, events):
        """Collate row in section in events."""
        if row[constants.REPORT_HOME_PLAYER] is None:
            row[constants.REPORT_HOME_PLAYER] = ""
        if row[constants.REPORT_AWAY_PLAYER] is None:
            row[constants.REPORT_AWAY_PLAYER] = ""
        if row[constants.REPORT_EVENT] not in events:
            events[row[constants.REPORT_EVENT]] = {}
        event = events[row[constants.REPORT_EVENT]]
        if row[constants.REPORT_SECTION] not in event:
            event[row[constants.REPORT_SECTION]] = {}
        section = event[row[constants.REPORT_SECTION]]
        player1, player2 = self._create_players_for_row(players, row)
        if player1 is None or player2 is None:
            return
        if row[constants.REPORT_HOME_TEAM] and row[constants.REPORT_AWAY_TEAM]:
            section_name = "=".join(
                (
                    constants.MATCH_RESULTS,
                    " - ".join(
                        (
                            row[constants.REPORT_HOME_TEAM],
                            row[constants.REPORT_AWAY_TEAM],
                        )
                    ),
                )
            )
            game = self._create_game_list_entry(
                players[player1][0],
                row[constants.REPORT_RESULT],
                players[player2][0],
                row[constants.REPORT_DATE],
                row[constants.REPORT_HOME_PLAYER_COLOUR],
                board=row[constants.REPORT_BOARD],
            )
        elif row[constants.REPORT_ROUND] is not None:
            section_name = "=".join(
                (constants.SECTION_RESULTS, row[constants.REPORT_SECTION])
            )
            game = self._create_game_list_entry(
                players[player1][0],
                row[constants.REPORT_RESULT],
                players[player2][0],
                row[constants.REPORT_DATE],
                row[constants.REPORT_HOME_PLAYER_COLOUR],
                round_=row[constants.REPORT_ROUND],
            )
        else:
            section_name = "=".join(
                (constants.OTHER_RESULTS, row[constants.REPORT_SECTION])
            )
            game = self._create_game_list_entry(
                players[player1][0],
                row[constants.REPORT_RESULT],
                players[player2][0],
                row[constants.REPORT_DATE],
                row[constants.REPORT_HOME_PLAYER_COLOUR],
            )
        if section_name not in section:
            section[section_name] = []
        section[section_name].append(game)

    def _create_players_for_row(self, players, row):
        """Create entries in players for player names and codes in row."""
        name1, codes1 = split_codes_from_name(
            row[constants.REPORT_HOME_PLAYER]
        )
        if not name1:
            return (None, None)
        name2, codes2 = split_codes_from_name(
            row[constants.REPORT_AWAY_PLAYER]
        )
        if not name2:
            return (None, None)
        player1 = (  # "1" is ECF term.
            name1,
            row[constants.REPORT_SECTION],
            row[constants.REPORT_HOME_TEAM],  # "" unless MATCH SECTION.
        )
        player2 = (  # "2" is ECF term.
            name2,
            row[constants.REPORT_SECTION],
            row[constants.REPORT_AWAY_TEAM],  # "" unless MATCH SECTION.
        )
        if name1 and player1 not in players:
            pin = str(len(players) + 1)  # PIN 0 reserved by ECF.
            players[player1] = (
                pin,
                self._create_player_list_entry(
                    pin,
                    " ".join(codes1),
                    name1,
                    row[constants.REPORT_HOME_TEAM],
                ),
            )
        player = self._create_player_list_entry(
            players[player1][0],
            " ".join(codes1),
            name1,
            row[constants.REPORT_HOME_TEAM],
        )
        if player != players[player1][1]:
            raise RuntimeError("Player1 entry")  # Replace later.
        if name2 and player2 not in players:
            pin = str(len(players) + 1)  # PIN 0 reserved by ECF.
            players[player2] = (
                pin,
                self._create_player_list_entry(
                    pin,
                    " ".join(codes2),
                    name2,
                    row[constants.REPORT_AWAY_TEAM],
                ),
            )
        player = self._create_player_list_entry(
            players[player2][0],
            " ".join(codes2),
            name2,
            row[constants.REPORT_AWAY_TEAM],
        )
        if player != players[player2][1]:
            raise RuntimeError("Player2 entry")  # Replace later.
        return (player1, player2)

    # This method gets a too-many-arguments message from pylint.
    # The player entry requires four mandatory, and two optional, items
    # of information; and these should have helpful names in the argument
    # list.
    @staticmethod
    def _create_player_list_entry(
        pin, codes, name, club, clubcode="", countycode=""
    ):
        """Return ECF submission file player list entry."""
        return "#".join(
            (
                "\n",
                "=".join((constants.PIN, pin)),
                "=".join((constants.BCF_CODE, codes)),
                "=".join((constants.NAME, name)),
                "=".join((constants.CLUB, club)),
                "=".join((constants.CLUB_CODE, clubcode)),
                "=".join((constants.CLUB_COUNTY, countycode)),
            )
        )

    # This method gets a too-many-arguments message from pylint.
    # The game entry requires five mandatory, and two optional, items
    # of information; and these should have helpful names in the argument
    # list.
    # The gamedate and pin1colour items are optional downstream, when the
    # information is sent to the ECF, but it is best if they are always
    # present.
    def _create_game_list_entry(
        self, pin1, score, pin2, gamedate, pin1colour, round_=None, board=None
    ):
        """Return ECF submission file game list entry."""
        if round_ is not None:
            return "#".join(
                (
                    "\n",
                    "=".join((constants.PIN1, pin1)),
                    "=".join((constants.SCORE, resultmapecf[score])),
                    "=".join((constants.PIN2, pin2)),
                    "=".join((constants.ROUND, round_)),
                    self._convert_date_to_ecf_format(gamedate),
                    "=".join((constants.COLOUR, pin1colour)),
                )
            )
        if board is not None:
            return "#".join(
                (
                    "\n",
                    "=".join((constants.PIN1, pin1)),
                    "=".join((constants.SCORE, resultmapecf[score])),
                    "=".join((constants.PIN2, pin2)),
                    "=".join((constants.BOARD, board)),
                    self._convert_date_to_ecf_format(gamedate),
                    "=".join((constants.COLOUR, pin1colour)),
                )
            )
        return "#".join(
            (
                "\n",
                "=".join((constants.PIN1, pin1)),
                "=".join((constants.SCORE, resultmapecf[score])),
                "=".join((constants.PIN2, pin2)),
                self._convert_date_to_ecf_format(gamedate),
                "=".join((constants.COLOUR, pin1colour)),
            )
        )

    @staticmethod
    def _convert_date_to_ecf_format(gamedate):
        """Return date in 'dd/mm/yyyy' format assuming 'yyyy-mm-dd' input.

        The date format is not checked except for 'gamedate is None'.
        """
        return "=".join(
            (
                constants.GAME_DATE,
                "/".join(reversed(gamedate.split("-")))
                if gamedate is not None
                else "",
            )
        )
