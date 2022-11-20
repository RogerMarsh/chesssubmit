# eventdetails.py
# Copyright 2022 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Set and modify event details."""
from ecfformat.gui import header

from ..core import configuration


class EventDetails(header.Header):
    """Customise Header for setting event details.

    Header can be used 'as-is' but conventions such as field name styles
    and file storage options assume the target is always an ECF result
    submission file.

    """

    _RSF_EXT = ".conf"
    _RSF_PATTERN = "submit" + _RSF_EXT

    def _make_configuration(self):
        """Return a configuration.Configuration instance."""
        return configuration.Configuration()
