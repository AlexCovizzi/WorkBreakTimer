import threading
from app.named_event import NamedEvent
from app.app_loop import AppLoop


class WorkerThread(threading.Thread):

    def __init__(self, main, config):
        threading.Thread.__init__(self)
        self.main = main
        self.app_loop = AppLoop(config)
        self.app_loop.subscribe('notification', self._on_notification)

    def run(self):
        self.app_loop.runloop()

    def abort(self):
        self.app_loop.stop()

    def _on_notification(self, notification):
        self.main.QueueEvent(NamedEvent('notification', data=notification))
