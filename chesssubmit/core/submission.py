# submission.py
# Copyright 2022 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Represent the Player list and Result Details in an ECF submission file.

Two additional sections are used to construct the submission: Team List and
Person List.  These allow for team names used in match reports to be mapped
to ECF club names; and for arbitrary player names to be mapped to ECF player
names including cases where various spellings of a name are given.

It is expected two Submission instances will be involved: one representing
the state saved from report edition <n>, and one representing report edition
<n+1> which has to be merged with edition <n> before being saved.

Sometimes just the saved state will be worked on: when the ECF submission
is prepared in several sessions.

"""
import os

from ecfformat.core import constants as ecf_constants

from chessvalidate.core.gameobjects import (
    get_game_rows_for_csv_format,
    split_codes_from_name,
)
from chessvalidate.core.gameresults import resultmapecf

from ..core import constants

_next_fields = {
    True: frozenset((ecf_constants.NAME_PLAYER_LIST,)),
    ecf_constants.NAME_PLAYER_LIST: frozenset(
        (
            ecf_constants.PIN,
            ecf_constants.NAME_MATCH_RESULTS,
            ecf_constants.NAME_OTHER_RESULTS,
            ecf_constants.NAME_SECTION_RESULTS,
            ecf_constants.FINISH,
        )
    ),
    ecf_constants.PIN: frozenset((ecf_constants.NAME_ECF_CODE,)),
    ecf_constants.NAME_ECF_CODE: frozenset((ecf_constants.NAME,)),
    ecf_constants.NAME: frozenset((ecf_constants.CLUB,)),
    ecf_constants.CLUB: frozenset((ecf_constants.NAME_CLUB_CODE,)),
    ecf_constants.NAME_CLUB_CODE: frozenset(
        (
            ecf_constants.PIN,
            ecf_constants.NAME_MATCH_RESULTS,
            ecf_constants.NAME_OTHER_RESULTS,
            ecf_constants.NAME_SECTION_RESULTS,
            ecf_constants.FINISH,
        )
    ),
    ecf_constants.NAME_MATCH_RESULTS: frozenset((ecf_constants.NAME_PIN1,)),
    ecf_constants.NAME_OTHER_RESULTS: frozenset((ecf_constants.NAME_PIN1,)),
    ecf_constants.NAME_SECTION_RESULTS: frozenset((ecf_constants.NAME_PIN1,)),
    ecf_constants.NAME_PIN1: frozenset((ecf_constants.SCORE,)),
    ecf_constants.SCORE: frozenset((ecf_constants.NAME_PIN2,)),
    ecf_constants.NAME_PIN2: frozenset(
        (
            ecf_constants.BOARD,
            ecf_constants.ROUND,
            ecf_constants.NAME_GAME_DATE,
        )
    ),
    ecf_constants.BOARD: frozenset((ecf_constants.NAME_GAME_DATE,)),
    ecf_constants.ROUND: frozenset((ecf_constants.NAME_GAME_DATE,)),
    ecf_constants.NAME_GAME_DATE: frozenset((ecf_constants.COLOUR,)),
    ecf_constants.COLOUR: frozenset(
        (
            ecf_constants.NAME_PIN1,
            ecf_constants.NAME_MATCH_RESULTS,
            ecf_constants.NAME_OTHER_RESULTS,
            ecf_constants.NAME_SECTION_RESULTS,
            ecf_constants.FINISH,
        )
    ),
    ecf_constants.FINISH: frozenset((constants.TEAM_LIST, constants.FINAL)),
    constants.TEAM_LIST: frozenset(
        (constants.TEAM_SECTION, constants.PERSON_LIST)
    ),
    constants.TEAM_SECTION: frozenset((constants.TEAM_NAME,)),
    constants.TEAM_NAME: frozenset((constants.TEAM_CLUB_NAME,)),
    constants.TEAM_CLUB_NAME: frozenset((constants.TEAM_CLUB_CODE,)),
    constants.TEAM_CLUB_CODE: frozenset(
        (constants.TEAM_SECTION, constants.PERSON_LIST)
    ),
    constants.PERSON_LIST: frozenset(
        (constants.PERSON_NUMBER, constants.FINAL)
    ),
    constants.PERSON_NUMBER: frozenset((constants.PERSON_NAME,)),
    constants.PERSON_NAME: frozenset((constants.PERSON_TEAM_SECTION,)),
    constants.PERSON_TEAM_SECTION: frozenset((constants.PERSON_TEAM_NAME,)),
    constants.PERSON_TEAM_NAME: frozenset((constants.PERSON_ALIAS,)),
    constants.PERSON_ALIAS: frozenset((constants.PERSON_ECF_NAME,)),
    constants.PERSON_ECF_NAME: frozenset((constants.PERSON_ECF_CODE,)),
    constants.PERSON_ECF_CODE: frozenset((constants.PERSON_CODE,)),
    constants.PERSON_CODE: frozenset(
        (constants.PERSON_CODE, constants.PERSON_NUMBER, constants.FINAL)
    ),
    constants.FINAL: False,
}


class Submission:
    """Player List, Result Details, Team List, and Person List, data.

    The data is presented in ECF submission style sections:
    PLAYER LIST
    (MATCH RESULTS | SECTION RESULTS | OTHER RESULTS)+
    FINISH
    TeamList
    PersonList
    Final

    The CamelCase sections are not defined in the ECF Rating Results File
    Layout document, but provide scaffolding to build a valid results
    submission file.

    A gui.sourceedit.SourceEdit instance provides data from reported
    results.

    A tkinter.Text.dump() file provides the data from saved state.

    A tkinter.Text widget provides data for a new saved state.

    """

    def __init__(self, folder):
        """Create Submission instance for event results in folder.

        folder - contains files of event data.

        """
        self.folder = folder
        self.players = {}
        self.events = {}
        self.persons = {}
        self.teams = {}

    def open_documents(self, parent):
        """Extract data from tkinter.Text.dump() file and return True if ok."""
        nvsep = ecf_constants.NAME_VALUE_SEPARATOR
        with open(
            os.path.join(self.folder, constants.SUBMISSION), "r", newline=""
        ) as file:
            current_field = True
            for field in file.read().split(ecf_constants.FIELD_SEPARATOR):
                field = field.split(nvsep)
                name = field[0].strip()
                if len(field) == 2:
                    value = field[1].strip()
                else:
                    value = ""
                    if not name:
                        continue
                if name not in _next_fields[current_field]:
                    return False
                current_field = name
            if _next_fields[current_field]:
                return False
        return True

    def convert_document_to_submission_style(self, results_data):
        """Generate text lines for the games in game rows.

        Stubs for Player List entries are put in self.players, keyed to be
        sorted into alphabetic order by player name.

        The game results are put in self.events, keyed to be sorted into
        alphabetic order by section.  For matches this likely means board
        order within match within division.

        The players, as reported, are put in self.persons, keyed to be
        sorted into alphabetic order by player name and team name.

        The teams, as reported, are put in self.teams, keyed to be
        sorted into alphabetic order by team name.

        """
        trro = {
            item: i
            for i, item in enumerate(constants.TABULAR_REPORT_ROW_ORDER)
        }
        for row in sorted(
            get_game_rows_for_csv_format(results_data.get_collated_games())
        ):
            self._process_csv_row({item: row[trro[item]] for item in trro})

    def _process_csv_row(self, row):
        """Collate row in section in events."""
        events = self.events
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
        player1 = self._create_home_player_entries_for_row(row)
        player2 = self._create_away_player_entries_for_row(row)
        if player1 is None or player2 is None:
            return
        players = self.players
        if row[constants.REPORT_HOME_TEAM] and row[constants.REPORT_AWAY_TEAM]:
            section_name = ecf_constants.NAME_VALUE_SEPARATOR.join(
                (
                    ecf_constants.NAME_MATCH_RESULTS,
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
            section_name = ecf_constants.NAME_VALUE_SEPARATOR.join(
                (
                    ecf_constants.NAME_SECTION_RESULTS,
                    row[constants.REPORT_SECTION],
                )
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
            section_name = ecf_constants.NAME_VALUE_SEPARATOR.join(
                (
                    ecf_constants.NAME_OTHER_RESULTS,
                    row[constants.REPORT_SECTION],
                )
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

    def _create_away_player_entries_for_row(self, row):
        """Add away details to players, events, persons, and teams."""
        return self._create_player_entries_for_row(
            row, constants.REPORT_AWAY_PLAYER, constants.REPORT_AWAY_TEAM
        )

    def _create_home_player_entries_for_row(self, row):
        """Add home details to players, events, persons, and teams."""
        return self._create_player_entries_for_row(
            row, constants.REPORT_HOME_PLAYER, constants.REPORT_HOME_TEAM
        )

    def _create_player_entries_for_row(self, row, player, team):
        """Add  details to players, events, persons, and teams."""
        name, codes = split_codes_from_name(row[player])
        if not name:
            return None
        person = (
            name,
            row[constants.REPORT_SECTION],
            row[team],  # "" unless MATCH SECTION.
        )
        players = self.players
        if person not in players:
            pin = str(len(players) + 1)  # PIN 0 reserved by ECF.
            players[person] = (
                pin,
                self._create_player_list_entry(
                    pin,
                    " ".join(codes),  # Probably put "" here.
                    name,
                    club=row[team],  # Probably keep for name duplication.
                ),
            )
        else:
            pin = players[person][0]
        persons = self.persons
        if person not in persons:
            persons[person] = (pin, set())
        if codes:
            reported_codes = persons[person][1]
            reported_codes.update(codes)
        teams = self.teams
        team = person[1:]
        if team not in teams:
            teams[team] = self._create_team_list_entry(*team)
        return person

    def write_entries_to_submission_file(self):
        """Write players, events, teams, and persons, to lines file.

        The event details are in the sibling file event.conf which is
        prepended to the submission data when an actual submission file
        is created for upload to ECF.

        """
        fsep = ecf_constants.FIELD_SEPARATOR
        players = self.players
        events = self.events
        persons = self.persons
        teams = self.teams
        with open(
            os.path.join(self.folder, constants.SUBMISSION), "w", newline=""
        ) as file:
            file.write("".join((fsep, ecf_constants.NAME_PLAYER_LIST)))
            for item in sorted(players):
                file.write(players[item][-1])
            for item in sorted(events):
                event = events[item]
                for subevent in sorted(event):
                    sections = event[subevent]
                    for section in sections:
                        file.write(fsep.join(("\n", section)))
                        file.write("".join(sections[section]))
            file.write(fsep.join(("\n", ecf_constants.FINISH)))
            file.write(fsep.join(("\n", constants.TEAM_LIST)))
            for item in sorted(teams.items()):
                file.write(item[1])
            file.write(fsep.join(("\n", constants.PERSON_LIST)))
            for item in sorted(persons.items()):
                file.write(self._create_person_list_entry(*item))
            file.write(fsep.join(("\n", constants.FINAL)))

    @staticmethod
    def _create_player_list_entry(pin, codes, name, club="", clubcode=""):
        r"""Return ECF submission file player list entry.

        clubcode is probably left as default because there is no pattern
        which reliably picks club codes (4 characters) but not 4 character
        club names.  Most club codes are \d\S\S\S so a mis-typed first
        character could give a club name, for example.

        """
        nvsep = ecf_constants.NAME_VALUE_SEPARATOR
        return ecf_constants.FIELD_SEPARATOR.join(
            (
                "\n",
                nvsep.join((ecf_constants.PIN, pin)),
                nvsep.join((ecf_constants.NAME_ECF_CODE, codes)),
                nvsep.join((ecf_constants.NAME, name)),
                nvsep.join((ecf_constants.CLUB, club)),
                nvsep.join((ecf_constants.NAME_CLUB_CODE, clubcode)),
            )
        )

    @staticmethod
    def _create_person_list_entry(key, value):
        """Return ECF submission file person list entry."""
        name, section, team = key
        pin, codes = value
        fsep = ecf_constants.FIELD_SEPARATOR
        nvsep = ecf_constants.NAME_VALUE_SEPARATOR
        if codes:
            codes = fsep.join(
                nvsep.join((constants.PERSON_CODE, c)) for c in codes
            )
        else:
            codes = nvsep.join((constants.PERSON_CODE, ""))
        return fsep.join(
            (
                "\n",
                nvsep.join((constants.PERSON_NUMBER, pin)),
                nvsep.join((constants.PERSON_NAME, name)),
                nvsep.join((constants.PERSON_TEAM_SECTION, section)),
                nvsep.join((constants.PERSON_TEAM_NAME, team)),
                nvsep.join((constants.PERSON_ALIAS, "")),
                nvsep.join((constants.PERSON_ECF_NAME, "")),
                nvsep.join((constants.PERSON_ECF_CODE, "")),
                codes,
            )
        )

    @staticmethod
    def _create_team_list_entry(section, team, teamclub="", teamclubcode=""):
        """Create entry in teamss for team."""
        nvsep = ecf_constants.NAME_VALUE_SEPARATOR
        return ecf_constants.FIELD_SEPARATOR.join(
            (
                "\n",
                nvsep.join((constants.TEAM_SECTION, section)),
                nvsep.join((constants.TEAM_NAME, team)),
                nvsep.join((constants.TEAM_CLUB_NAME, teamclub)),
                nvsep.join((constants.TEAM_CLUB_CODE, teamclubcode)),
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
        nvsep = ecf_constants.NAME_VALUE_SEPARATOR
        if round_ is not None:
            return ecf_constants.FIELD_SEPARATOR.join(
                (
                    "\n",
                    nvsep.join((ecf_constants.NAME_PIN1, pin1)),
                    nvsep.join((ecf_constants.SCORE, resultmapecf[score])),
                    nvsep.join((ecf_constants.NAME_PIN2, pin2)),
                    nvsep.join((ecf_constants.ROUND, round_)),
                    self._convert_date_to_ecf_format(gamedate),
                    nvsep.join((ecf_constants.COLOUR, pin1colour)),
                )
            )
        if board is not None:
            return ecf_constants.FIELD_SEPARATOR.join(
                (
                    "\n",
                    nvsep.join((ecf_constants.NAME_PIN1, pin1)),
                    nvsep.join((ecf_constants.SCORE, resultmapecf[score])),
                    nvsep.join((ecf_constants.NAME_PIN2, pin2)),
                    nvsep.join((ecf_constants.BOARD, board)),
                    self._convert_date_to_ecf_format(gamedate),
                    nvsep.join((ecf_constants.COLOUR, pin1colour)),
                )
            )
        return ecf_constants.FIELD_SEPARATOR.join(
            (
                "\n",
                nvsep.join((ecf_constants.NAME_PIN1, pin1)),
                nvsep.join((ecf_constants.SCORE, resultmapecf[score])),
                nvsep.join((ecf_constants.NAME_PIN2, pin2)),
                self._convert_date_to_ecf_format(gamedate),
                nvsep.join((ecf_constants.COLOUR, pin1colour)),
            )
        )

    @staticmethod
    def _convert_date_to_ecf_format(gamedate):
        """Return date in 'dd/mm/yyyy' format assuming 'yyyy-mm-dd' input.

        The date format is not checked except for 'gamedate is None'.
        """
        return ecf_constants.NAME_VALUE_SEPARATOR.join(
            (
                ecf_constants.NAME_GAME_DATE,
                "/".join(reversed(gamedate.split("-")))
                if gamedate is not None
                else "",
            )
        )

    def close(self):
        """Discard references to the event data."""
        self.folder = None
        self.players = None
        self.events = None
        self.persons = None
        self.teams = None
