from app.wx_taskbar_icon import WxTaskBarIcon
import wx
from app.wx_main_window import MainWindow


class WxApp(wx.App):

    def __init__(self, kwargs):
        self._kwargs = kwargs
        super().__init__()

    def OnInit(self):
        self.window = MainWindow(None, -1, self._kwargs)
        self.taskbar_icon = WxTaskBarIcon(self.window)
        self.window.Show(False)
        return True
