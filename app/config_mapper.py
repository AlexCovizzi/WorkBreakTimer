from app.util import parse_time


class ConfigMapper:

    def __init__(self):
        self._value_mappers = {}

    def map_to(self, key, s):
        return self._value_mappers[key][0](s)

    def map_from(self, key, v):
        return self._value_mappers[key][1](v)

    def register(self, key, getter, setter):
        self._value_mappers[key] = [getter, setter]

    def register_int(self, key, minval=0, maxval=1000000, defval=0):
        self._value_mappers[key] = [
            lambda s: self._to_int(s, minval, maxval, defval), lambda v: str(v)
        ]

    def register_bool(self, key, defval=False):
        self._value_mappers[key] = [
            lambda s: self._to_bool(s, defval), lambda v: str(v)
        ]

    def register_time(self, key, defval='00:00'):
        self._value_mappers[key] = [
            lambda s: self._to_time(s, defval), lambda v: self._from_time(v)
        ]

    def _to_int(self, s, minval, maxval, defval):
        if not str(s).isnumeric():
            return defval
        try:
            v = int(s)
            return v if v >= minval and v <= maxval else defval
        except Exception:
            return defval

    def _to_bool(self, s, defval):
        s = str(s).lower()
        if s == 'true' or s == 'yes' or s == '1':
            return True
        if s == 'false' or s == 'no' or s == '0':
            return False
        return defval

    def _to_time(self, s, defval):
        try:
            return parse_time(s)
        except Exception:
            return parse_time(defval)

    def _from_time(self, v):
        if type(v) is str:
            return v
        return '{}:{}:{}'.format(v.hour, v.minute, v.second)
