import multiprocessing
import logging
import os
from app.__meta__ import __app__
from app.app_config import AppConfig
from app.wx_app import WxApp

log_file = os.path.join(os.path.expanduser('~'), '.' + __app__, 'app.log')
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    multiprocessing.freeze_support()

    config = AppConfig()
    app = WxApp(config)
    app.MainLoop()
