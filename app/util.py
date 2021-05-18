import time
import datetime


def parse_time(s):
    time_struct = time.strptime(str(s), "%H:%M")
    return datetime.time(time_struct.tm_hour, time_struct.tm_min)
