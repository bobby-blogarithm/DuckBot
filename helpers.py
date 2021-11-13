from dateutil import tz

"""
    This file is dedicated to utility and helper functions that
    are NOT associated with a specific class or feature
"""

def convert_tz(current_time, origin_tz, desired_tz):
    from_tz = tz.gettz(origin_tz)
    to_tz = tz.gettz(desired_tz)
    result = current_time.replace(tzinfo=from_tz)

    return result.astimezone(to_tz)