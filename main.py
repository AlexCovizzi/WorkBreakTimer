import multiprocessing
from app.config import Config
from app.wx_app import WxApp

if __name__ == '__main__':
    multiprocessing.freeze_support()

    config = Config('WorkBreakTimer')
    app = WxApp(config)
    app.MainLoop()
