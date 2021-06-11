import wx


class NamedEvent(wx.PyEvent):

    EVT_TYPE = wx.NewEventType()

    def __init__(self, name, data=None):
        super().__init__(id=wx.ID_ANY, eventType=NamedEvent.EVT_TYPE)
        self.name = name
        self.data = data


class NamedEventBinder:

    def __init__(self):
        self._handler_map = {}

        self.Connect(wx.ID_ANY, wx.ID_ANY, NamedEvent.EVT_TYPE, self.OnNamedEvent)

    def BindByName(self, name, handler):
        self._handler_map[name] = handler

    def OnNamedEvent(self, event):
        handler = self._handler_map.get(event.name)
        if handler:
            handler(event)
