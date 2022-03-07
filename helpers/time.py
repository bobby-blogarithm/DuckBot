from dateutil import tz
from string import Template

# Converts the current time from one timezone to another
def convert_tz(current_time, origin_tz, desired_tz):
    from_tz = tz.gettz(origin_tz)
    to_tz = tz.gettz(desired_tz)
    result = current_time.replace(tzinfo=from_tz)

    return result.astimezone(to_tz)

# Wrapper class for string.Template using the "%" delimiter
class DeltaTemplate(Template):
    delimiter = '%'

def strftdelta(tdelta, fmt):
    d = {'D': tdelta.days}
    d['H'], rem = divmod(tdelta.seconds, 3600)
    d['M'], d['S'] = divmod(rem, 60)
    template = DeltaTemplate(fmt)
    return template.subtitute(**d)