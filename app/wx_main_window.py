from app.notification_event import NotificationEvent
import wx
import wx.adv
from app.worker_thread import WorkerThread
from app.wx_notification_event import EVT_NOTIFICATION_ID
from app.resources import get_resource_path


class MainWindow(wx.Frame):

    def __init__(self, parent, id, kwargs):
        wx.Frame.__init__(self, parent, id, 'Work/Break Timer')
        self.config = kwargs

        self.Connect(-1, -1, EVT_NOTIFICATION_ID, self.OnNotification)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.worker = WorkerThread(self, kwargs)
        self.worker.start()

        self.set_icon()
        self.Centre()

    def OnCloseWindow(self, event):
        if self.worker:
            self.worker.abort()
            self.worker.join()
            self.worker = None
        self.Destroy()

    def OnNotification(self, event):
        if event.notification == NotificationEvent.BREAK:
            notification = wx.adv.NotificationMessage(
                "Break",
                message='Take a break!',
                parent=self,
                flags=wx.ICON_INFORMATION)
            notification.Show(timeout=3)

    def set_icon(self):
        path = get_resource_path('icon.ico')
        icon_bundle = wx.IconBundle()
        icon_bundle.AddIcon(
            wx.Icon(path, wx.BITMAP_TYPE_ICO, desiredWidth=16, desiredHeight=16))
        icon_bundle.AddIcon(
            wx.Icon(path, wx.BITMAP_TYPE_ICO, desiredWidth=32, desiredHeight=32))
        self.SetIcons(icon_bundle)
