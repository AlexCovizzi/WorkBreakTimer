import time
import datetime
import sys
import os


def parse_time(s: str):
    fmt = '%H:%M:%S' if len(s.split(':')) > 2 else '%H:%M'
    time_struct = time.strptime(str(s), fmt)
    return datetime.time(time_struct.tm_hour, time_struct.tm_min)


def resource_path(rel_path):
    return os.path.join(getattr(sys, '_MEIPASS', ''), 'resources', rel_path)


def is_dev():
    return getattr(sys, '_MEIPASS', None) is None


def is_prod():
    return not is_dev()
