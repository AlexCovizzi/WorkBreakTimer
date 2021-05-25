import logging
import os
import webbrowser
import wx
import wx.adv
from app.__meta__ import __display__, __version__, __issues__, __repo__
from app.wx_preferences_dialog import WxPreferencesDialog
from app.resources import get_resource_path

log = logging.getLogger(__name__)

TRAY_TOOLTIP = 'Work/Break Timer'


class WxTaskBarIcon(wx.adv.TaskBarIcon):

    def __init__(self, main_window):
        wx.adv.TaskBarIcon.__init__(self)
        self._main_window = main_window
        self.set_icon()
        # self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        self.create_menu_item(menu, __display__ + ' v' + __version__, self.on_app_name)
        self.create_menu_item(menu, 'Report Issue', self.on_report_issue)
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Preferences', self.on_preferences)
        self.create_menu_item(menu, 'Show Log', self.on_show_log)
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def create_menu_item(self, menu, label, func=None):
        item = wx.MenuItem(menu, -1, label)
        if func:
            menu.Bind(wx.EVT_MENU, func, id=item.GetId())
        menu.Append(item)
        return item

    def set_icon(self):
        path = get_resource_path('icon.ico')
        icon = wx.Icon(path, wx.BITMAP_TYPE_ICO, desiredWidth=32, desiredHeight=32)
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_app_name(self, event):
        webbrowser.open(__repo__)

    def on_report_issue(self, event):
        webbrowser.open(__issues__)

    def on_show_log(self, event):
        os.startfile(logging.getLoggerClass().root.handlers[0].baseFilename, 'open')

    def on_exit(self, event):
        self.RemoveIcon()
        self.Destroy()
        self._main_window.Close()

    def on_preferences(self, event):
        preferences_dialog = WxPreferencesDialog(
            self._main_window.config, parent=self._main_window)
        preferences_dialog.Show(True)
