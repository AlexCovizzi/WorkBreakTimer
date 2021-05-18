import threading
import wx
from app.app_loop import AppLoop
from app.wx_notification_event import WxNotificationEvent


class WorkerThread(threading.Thread):

    def __init__(self, window, kwargs):
        threading.Thread.__init__(self)
        self._window = window
        self._app_loop = AppLoop(kwargs)

        self._app_loop.init()

    def run(self):
        self._app_loop.on_notification(self._on_notification)
        self._app_loop.runloop()

    def abort(self):
        self._app_loop.stop()

    def _on_notification(self, notification):
        wx.PostEvent(self._window, WxNotificationEvent(notification))
