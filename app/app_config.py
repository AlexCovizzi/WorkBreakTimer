from app.config_mapper import ConfigMapper
import os
from app.__meta__ import __app__
from app.config import Config
from app.resources import get_resource_path


class AppConfig(Config):

    def __init__(self):
        path = os.path.join(os.path.expanduser('~'), '.' + __app__, 'config.ini')
        default_path = get_resource_path('default_config.ini')
        section = 'SETTINGS'
        super().__init__(path, default_path, section, self.mapper())

    def mapper(self):
        mapper = ConfigMapper()
        mapper.register_bool('enabled', defval=True)
        mapper.register_int(
            'calculate_notification_every_seconds', minval=1, maxval=1440, defval=60)
        mapper.register_time('activate_from_hour', defval='09:00')
        mapper.register_time('activate_until_hour', defval='17:00')
        mapper.register_int(
            'check_presence_every_seconds', minval=1, maxval=1440, defval=60)
        mapper.register_int('max_work_time_seconds', minval=1, maxval=1440, defval=3600)
        mapper.register_int('min_break_time_seconds', minval=1, maxval=1440, defval=300)
        mapper.register_int(
            'break_notification_cooldown_seconds', minval=1, maxval=1440, defval=120)
        mapper.register_bool('notify_when_camera_occupied', defval=False)
        mapper.register_int('camera', minval=0, maxval=10, defval=0)
        mapper.register_int('num_of_snapshots', minval=1, maxval=10, defval=1)
        mapper.register_int(
            'time_between_snapshots_millis', minval=40, maxval=1000, defval=100)
        return mapper
