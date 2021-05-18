import configparser
import os
import shutil
from app.resources import get_resource_path


class Config:

    FILE_NAME = 'config.ini'
    SECTION_NAME = 'SETTINGS'

    def __init__(self, name):
        self._name = name
        self._path = os.path.join(self.dir_path, Config.FILE_NAME)
        self._config = self._read_config_file()

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def dir_path(self):
        return os.path.join(os.path.expanduser('~'), '.' + self.name)

    def reload(self):
        self._config = self._read_config_file()

    def get(self, key, default_value=''):
        value = self._config.get(Config.SECTION_NAME, key, fallback=default_value)
        if value.isnumeric():
            return int(value)
        return value

    def getint(self, key, default_value=0):
        return self._config.getint(Config.SECTION_NAME, key, fallback=default_value)

    def getfloat(self, key, default_value=0):
        return self._config.get(Config.SECTION_NAME, key, fallback=default_value)

    def set(self, key, value):
        self._config.set(Config.SECTION_NAME, key, value)

    def _read_config_file(self):
        self._ensure_config_file_exists()
        config = configparser.ConfigParser()
        config.read(self.path)
        return config

    def _ensure_config_file_exists(self):
        if os.path.isfile(self.path):
            return
        os.makedirs(self.dir_path, exist_ok=True)
        shutil.copyfile(get_resource_path('default_config.ini'), self.path)
