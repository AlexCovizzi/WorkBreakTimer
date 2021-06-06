from app.named_event import NamedEvent
import logging
import wx
import wx.adv
from app.__meta__ import __display__, __version__
from app.wx_icon import wx_icon

log = logging.getLogger(__name__)


class WxTaskBarIcon(wx.adv.TaskBarIcon):

    def __init__(self, main: wx.EvtHandler):
        super().__init__()
        self.main = main

        self.SetIcon(wx_icon(32), __display__)
        # self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        self.CreateMenuItem(menu, __display__ + ' v' + __version__, self.OnMenuAppName)
        self.CreateMenuItem(menu, 'Report Issue', self.OnMenuReportIssue)
        menu.AppendSeparator()
        self.CreateMenuItem(menu, 'Preferences', self.OnMenuPreferences)
        self.CreateMenuItem(menu, 'Show Logs', self.OnMenuShowLogs)
        menu.AppendSeparator()
        self.CreateMenuItem(menu, 'Exit', self.OnMenuAppExit)
        return menu

    def CreateMenuItem(self, menu: wx.Menu, label: str, func=None):
        item = wx.MenuItem(menu, wx.ID_ANY, label)
        if func:
            menu.Bind(wx.EVT_MENU, func, id=item.GetId())
        menu.Append(item)
        return item

    def OnMenuAppName(self, event):
        self.main.QueueEvent(NamedEvent('icon-app-name'))

    def OnMenuReportIssue(self, event):
        self.main.QueueEvent(NamedEvent('icon-report-issue'))

    def OnMenuPreferences(self, event):
        self.main.QueueEvent(NamedEvent('icon-preferences'))

    def OnMenuShowLogs(self, event):
        self.main.QueueEvent(NamedEvent('icon-show-logs'))

    def OnMenuAppExit(self, event):
        self.RemoveIcon()
        self.Destroy()
        self.main.QueueEvent(NamedEvent('icon-app-exit'))
