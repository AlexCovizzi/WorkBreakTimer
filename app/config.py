import configparser
import os
import shutil


class Config:

    def __init__(self, path, default_path, section, mapper):
        self._path = path
        self._default_path = default_path
        self._section = section
        self._mapper = mapper
        self._config = self._read()

    @property
    def path(self):
        return self._path

    def read(self):
        self._config = self._read()

    def write(self):
        with open(self._path, 'w+') as f:
            self._config.write(f)

    def getstr(self, key, default_value=''):
        return self._config.get(self._section, key, fallback=default_value)

    def get(self, key, default_value=''):
        s = self._config.get(self._section, key, fallback=default_value)
        return self._mapper.map_to(key, s)

    def update(self, kwargs):
        for k, v in kwargs.items():
            s = self._mapper.map_from(k, v)
            self._config.set(self._section, k, s)

    def _read(self):
        self._ensure_config_file_exists()
        config = configparser.ConfigParser()
        config.read(self.path)
        return config

    def _ensure_config_file_exists(self):
        if os.path.isfile(self.path):
            return
        dir_path = os.path.dirname(self.path)
        os.makedirs(dir_path, exist_ok=True)
        shutil.copyfile(self._default_path, self.path)
