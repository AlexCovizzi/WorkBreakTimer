import wx


class WxPreferencesSection(wx.Panel):

    def __init__(self, parent: wx.Window, section: str):
        super().__init__(parent)

        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.title = self.CreateTitle(section)
        self.panel = self.CreatePanel()

        self.inputSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.panel.SetSizer(self.inputSizer)

        self.sizer.Add(self.title, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 4)
        self.sizer.Add(self.panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)

        self.SetSizer(self.sizer)

    def CreateTitle(self, section: str):
        font = wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString)
        title = wx.StaticText(self, wx.ID_ANY, section, wx.DefaultPosition,
                              wx.DefaultSize, 0)
        title.Wrap(-1)
        title.SetFont(font)
        title.SetForegroundColour(wx.Colour(54, 54, 54))
        return title

    def CreatePanel(self):
        panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                         wx.TAB_TRAVERSAL)
        panel.SetBackgroundColour(wx.Colour(242, 246, 244))
        return panel
