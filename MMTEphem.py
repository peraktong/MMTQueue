"""Create MMTEphem Class that contains the ephemeris for a given night.

Input : Local date
"""
import ephem


def mmtObserver(dateObs):
    """Return an mmt XEphem observer for given night."""
    mmt = ephem.Observer()
    mmt.pressure = 0

    # Set the USNO definition of sunset (to match the almanac)
    # This will get overwritten when doing sunrise/sunset
    mmt.horizon = "-0:34"
    mmt.lat = "31:41:19.6"
    mmt.lon = "-110:53:04.4"
    mmt.elevation = 2600

    return mmt


def mmtTwilightDefinition():
    """Return the default value for twilight.

    Returns the degrees the sun must be below the horizon
    to define twilight.

    Nautical twilight : -12 degrees
    Astronomical twilight : -18 degrees

    For now, I'm setting to nautical, but this may need to be
    a switch for Binospec.
    """
    twilight = "-12"

    return twilight


class MMTEphem(object):
    """Return object with import times at MMT telescope."""

    def __init__(self, dateObs):
        """Initialize object."""
        # Append 19:00 to make sure the date references
        # noon MST.
        self.dateObs = dateObs + " 19:00"

        # Calculate sunrise and sunset
        mmt = mmtObserver(dateObs)
        mmt.horizon = "-0:34"
        self.sunset = mmt.next_setting(ephem.Sun())
        self.sunrise = mmt.next_rising(ephem.Sun())

        # Calculate morning and evening twilight
        mmt.horizon = mmtTwilightDefinition()
        self.eveningTwilight = mmt.next_setting(ephem.Sun())
        self.morningTwilight = mmt.next_rising(ephem.Sun())

        # Calculate Moon rise and moon set
        self.moonrise = mmt.next_rising(ephem.Moon())
        self.moonset = mmt.next_setting(ephem.Moon())

        # Save the observer in case other calculations need it.
        self.mmtObserver = mmt

if __name__ == "__main__":
    mmt = MMTEphem("2016/02/09")
