# constants.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Constants used in ChessResultsReport application."""

# Chosen way of presenting game results in readable format.
LOSS = "0-1"  # _loss = '0-1'
DRAWN = "draw"  # _draw = 'draw'
WIN = "1-0"  # _win = '1-0'

# Game score identifiers on database game records.
# h... refers to first-named player usually the home player in team context.
# a... refers to second-named player usually the away player in team context.
# No assumption is made about which player has the white or black pieces.
HWIN = "h"
AWIN = "a"
DRAW = "d"
HWIN_DEFAULT = "hd"
AWIN_DEFAULT = "ad"
DOUBLEDEFAULT = "dd"
DRAWDEFAULT = "=d"
HBYE = "hb"
ABYE = "ab"
HBYEHALF = "hbh"
ABYEHALF = "abh"
TOBEREPORTED = None
_VOID = "v"
NOTARESULT = "not a result"
DEFAULTED = "gd"

# Commentary on printed results.
TBRSTRING = "to be reported"

# Encoding of values used on ECF submission files.
#
# The Results File Field Definitions document (FieldDef.htm dated Oct 2006)
# reserves PIN PIN1 and PIN2 value "0" for use with results encoded by the
# SCORE values "d1" "d5" and "dd".
#
# This conflicts with the use of database record numbers as PIN PIN1 and
# PIN2 values for database engines which use 0 as a record number (after
# use of the standard conversion of integer to string).
#
# The ECF submission file generator will replace "0" by "zero_not_0" in PIN
# PIN1 and PIN2 to comply with the convention.
#
# It is hoped that this value will provide those who look at the submission
# file with a sufficient clue to what is going on: and at least assure them
# that it is not a mistake.
#
# It is also hoped that "zero_not_0" is a sufficiently unusual value that
# it will not be used by other grading programs as a valid PIN separate
# from "0".  Thus avoiding problems that may arise from the conventional
# use of "zero_not_0" by this program to cope with the ECF submission file
# conventional use of "0".
RESULT_01 = "01"
RESULT_55 = "55"
RESULT_10 = "10"
ECF_RESULT_DD = "dd"
ECF_RESULT_1D = "1d"
ECF_RESULT_D1 = "d1"

# Keys used on league database extract.

# Keys used on ECF submission files.

# Those used in ECF submissions generated by this package.
EVENT_DETAILS = "EVENT DETAILS"
EVENT_CODE = "EVENT CODE"
EVENT_NAME = "EVENT NAME"
SUBMISSION_INDEX = "SUBMISSION INDEX"
EVENT_DATE = "EVENT DATE"
FINAL_RESULT_DATE = "FINAL RESULT DATE"
RESULTS_OFFICER = "RESULTS OFFICER"
RESULTS_OFFICER_ADDRESS = "RESULTS OFFICER ADDRESS"
TREASURER = "TREASURER"
TREASURER_ADDRESS = "TREASURER ADDRESS"
MOVES_FIRST_SESSION = "MOVES FIRST SESSION"
MINUTES_FIRST_SESSION = "MINUTES FIRST SESSION"
MOVES_SECOND_SESSION = "MOVES SECOND SESSION"
MINUTES_SECOND_SESSION = "MINUTES SECOND SESSION"
MINUTES_REST_OF_GAME = "MINUTES REST OF GAME"
MINUTES_FOR_GAME = "MINUTES FOR GAME"
SECONDS_PER_MOVE = "SECONDS PER MOVE"
ADJUDICATED = "ADJUDICATED"
INFORM_GRAND_PRIX = "INFORM GRAND PRIX"
INFORM_FIDE = "INFORM FIDE"
INFORM_CHESSMOVES = "INFORM CHESSMOVES"
INFORM_UNION = "INFORM UNION"
PLAYER_LIST = "PLAYER LIST"
PIN = "PIN"
BCF_CODE = "BCF CODE"
NAME = "NAME"
BCF_CODE = "BCF CODE"
CLUB = "CLUB"
CLUB_CODE = "CLUB CODE"
CLUB_COUNTY = "CLUB COUNTY"
MATCH_RESULTS = "MATCH RESULTS"
SECTION_RESULTS = "SECTION RESULTS"
OTHER_RESULTS = "OTHER RESULTS"
WHITE_ON = "WHITE ON"
PIN1 = "PIN1"
SCORE = "SCORE"
PIN2 = "PIN2"
ROUND = "ROUND"
GAME_DATE = "GAME DATE"
BOARD = "BOARD"
COLOUR = "COLOUR"
FINISH = "FINISH"

# Those available for use in ECF submissions (so merges.py must know).

# Event configuration file.

# Most recently accessed database and configuation files for selecting and
# extracting text from emails to documents.
# Some could be per database, but done per user.
RECENT_EMAIL_SELECTION = "collection"
RECENT_EMAIL_EXTRACTION = "event"
RECENT_DOCUMENT = "document"
RECENT_SOURCE_SUBMISSION = "source_submission"

# Names of columns in tabular game reports generated by ChessResults.
# These are not used by emailextractor module which defines names of entries
# in the extract text configuration file which name the columns.
# The constants defined here are REPORT_SECTION, and so forth, while the
# constants in emailextractor are _REPORT_SECTION, and so forth.
REPORT_SECTION = "Section"
REPORT_DAY = "Day"
REPORT_DATE = "Date"
REPORT_ROUND = "Round"
REPORT_HOME_TEAM = "HomeTeam"
REPORT_HOME_TEAM_SCORE = "HTScore"
REPORT_HOME_PLAYER = "HomePlayer"
REPORT_RESULT = "Result"
REPORT_AWAY_PLAYER = "AwayPlayer"
REPORT_AWAY_TEAM_SCORE = "ATScore"
REPORT_AWAY_TEAM = "AwayTeam"
REPORT_BOARD = "Board"
REPORT_HOME_PLAYER_COLOUR = "HPColour"
REPORT_EVENT = "Event"

# Suitable for sorting rows into order for easy eyeball inspection.
TABULAR_REPORT_ROW_ORDER = (
    REPORT_EVENT,
    REPORT_SECTION,
    REPORT_HOME_TEAM,
    REPORT_AWAY_TEAM,
    REPORT_ROUND,
    REPORT_BOARD,
    REPORT_HOME_PLAYER,
    REPORT_AWAY_PLAYER,
    REPORT_DATE,
    REPORT_HOME_PLAYER_COLOUR,
    REPORT_RESULT,
    REPORT_HOME_TEAM_SCORE,
    REPORT_AWAY_TEAM_SCORE,
    REPORT_DAY,
)

# Suitable for generating parsable " ".join(row) from csv file.
# ECF code and ECF membership number should be prefixes to the player name
# in REPORT_HOME_PLAYER, and suffixes in REPORT_AWAY_PLAYER, if they are
# reported to avoid confusion if only one player has these.
TABULAR_REPORT_DEFAULT_SOURCE_ORDER = (
    REPORT_SECTION,
    REPORT_DAY,
    REPORT_DATE,
    REPORT_ROUND,
    REPORT_HOME_TEAM,
    REPORT_HOME_TEAM_SCORE,
    REPORT_HOME_PLAYER,
    REPORT_RESULT,
    REPORT_AWAY_PLAYER,
    REPORT_AWAY_TEAM_SCORE,
    REPORT_AWAY_TEAM,
    REPORT_BOARD,
    REPORT_HOME_PLAYER_COLOUR,
    REPORT_EVENT,
)

# Display value for side indicator in game records and structures.
FIRST_PLAYER_WHITE_PIECES = "White"
FIRST_PLAYER_BLACK_PIECES = "Black"

# Problem indicators for duplicate game reports.
# Some have suffix _DUP_REP because at least one other constant had the
# same name originally, defined in another module.
NULL_PLAYER = "null"
HOME_PLAYER_WHITE = "home player white"
GRADING_ONLY = "grading only"
SECTION = "section"
HOME_TEAM_NAME = "home team name"
AWAY_TEAM_NAME = "away team name"
HOME_PLAYER = "home player"
AWAY_PLAYER = "away player"
GAME_COUNT = "game count"
MATCH_SCORE = "match and game scores in earlier reports"
ONLY_REPORT = "match and game scores in only report"
AUTHORIZATION = "authorization"
ROUND_DUP_REP = "round"
COMPETITION_DUP_REP = "competition"
SOURCE_DUP_REP = "source"
BOARD_DUP_REP = "board"
RESULT_DUP_REP = "result"
