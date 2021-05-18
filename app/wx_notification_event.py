import wx


EVT_NOTIFICATION_ID = wx.NewId()


class WxNotificationEvent(wx.PyEvent):

    def __init__(self, notification):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_NOTIFICATION_ID)
        self.notification = notification
