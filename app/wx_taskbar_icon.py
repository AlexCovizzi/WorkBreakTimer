import wx
import wx.adv
from app.resources import get_resource_path


TRAY_TOOLTIP = 'Work/Break Timer'
TRAY_ICON = get_resource_path('icon.png')


class WxTaskBarIcon(wx.adv.TaskBarIcon):

    def __init__(self, main_window):
        wx.adv.TaskBarIcon.__init__(self)
        self._main_window = main_window
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        # self.create_menu_item(menu, 'Open', self.on_open)
        # self.create_menu_item(menu, 'Say Hello', self.on_hello)
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def create_menu_item(self, menu, label, func):
        item = wx.MenuItem(menu, -1, label)
        menu.Bind(wx.EVT_MENU, func, id=item.GetId())
        menu.Append(item)
        return item

    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        print('Tray icon was left-clicked.')

    def on_hello(self, event):
        notification = wx.adv.NotificationMessage(
            "Hello", message='Hello, world!', parent=None, flags=wx.ICON_INFORMATION)
        notification.Show(timeout=3)

    def on_exit(self, event):
        self.RemoveIcon()
        self.Destroy()
        self._main_window.Close()

    def on_open(self, event):
        frame = wx.Frame(parent=None, title='Hello World')
        frame.Show()
