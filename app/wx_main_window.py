import os
import logging
import webbrowser
import wx
import wx.adv
from app.__meta__ import __display__, __issues__, __repo__
from app.util import is_dev
from app.wx_icon import wx_icon
from app.worker_thread import WorkerThread
from app.wx_taskbar_icon import WxTaskBarIcon
from app.wx_preferences_dialog import WxPreferencesDialog
from app.named_event import NamedEventBinder


class WxMainWindow(wx.Frame, NamedEventBinder):

    def __init__(self, config):
        wx.Frame.__init__(self, None, title=__display__)
        NamedEventBinder.__init__(self)
        self.config = config

        self.SetIcons()
        self.BindAll()
        self.Centre()

        self.worker_thread = WorkerThread(self, self.config)
        self.worker_thread.start()

        self.taskbar_icon = WxTaskBarIcon(self)

    def SetIcons(self):
        icon_bundle = wx.IconBundle()
        icon_bundle.AddIcon(wx_icon(16))
        icon_bundle.AddIcon(wx_icon(32))
        super().SetIcons(icon_bundle)

    def BindAll(self):
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)

        self.BindByName('notification', self.OnNotification)
        self.BindByName('icon-app-name', self.OnIconMenuAppName)
        self.BindByName('icon-report-issue', self.OnIconMenuReportIssue)
        self.BindByName('icon-preferences', self.OnIconMenuPreferences)
        self.BindByName('icon-show-logs', self.OnIconMenuShowLogs)
        self.BindByName('icon-app-exit', self.OnIconMenuAppExit)

    def OnClose(self, event):
        self.Destroy()

    def OnDestroy(self, event):
        if self.worker_thread:
            self.worker_thread.abort()
            self.worker_thread.join()
            self.worker_thread = None

    def OnNotification(self, event):
        notification = event.data
        wx_notification = wx.adv.NotificationMessage(
            notification.title,
            message=notification.message,
            parent=self,
            flags=wx.ICON_INFORMATION)
        wx_notification.Show(timeout=3)

    def OnIconMenuAppName(self, event):
        webbrowser.open(__repo__)

    def OnIconMenuReportIssue(self, event):
        webbrowser.open(__issues__)

    def OnIconMenuPreferences(self, event):
        preferences_dialog = WxPreferencesDialog(self, self.config)
        preferences_dialog.ShowModal()

    def OnIconMenuShowLogs(self, event):
        if is_dev():
            # No need to open the log file in dev
            return
        log_handler = logging.getLoggerClass().root.handlers[0]
        os.startfile(log_handler.baseFilename, 'open')

    def OnIconMenuAppExit(self, event):
        self.Close()
