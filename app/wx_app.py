import wx
from app.wx_main_window import WxMainWindow


class WxApp(wx.App):

    def __init__(self, config):
        self.config = config
        super().__init__()

    def OnInit(self):
        self.main = WxMainWindow(self.config)

        self.main.Show(False)
        self.SetTopWindow(self.main)

        return True

    def OnExit(self):
        return super().OnExit()
