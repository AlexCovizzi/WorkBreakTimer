import wx
from app.util import resource_path

ICO_PATH = resource_path('icon.ico')


def wx_icon(size):
    return wx.Icon(ICO_PATH, wx.BITMAP_TYPE_ICO, desiredWidth=size, desiredHeight=size)