import multiprocessing
from app.app_config import AppConfig
from app.wx_app import WxApp

if __name__ == '__main__':
    multiprocessing.freeze_support()

    config = AppConfig()
    app = WxApp(config)
    app.MainLoop()
