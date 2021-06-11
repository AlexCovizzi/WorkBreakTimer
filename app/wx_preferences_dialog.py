from app.named_event import NamedEvent
import wx
import wx.adv
import wx.lib.scrolledpanel
from app.wx_icon import wx_icon
from app.config import Config
from app.wx_preferences_detection import WxPreferencesDetection
from app.wx_preferences_notifications import WxPreferencesNotifications
from app.wx_preferences_general import WxPreferencesGeneral


class WxPreferencesDialog(wx.Dialog):

    def __init__(self, parent: wx.Window, config: Config):
        super().__init__(
            parent, wx.ID_ANY, 'Preferences', style=wx.DEFAULT_DIALOG_STYLE)
        self.main = parent

        self.SetForegroundColour(wx.Colour(32, 32, 32))
        self.SetBackgroundColour(wx.Colour(252, 254, 254))

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mainSizer)

        self.generalSection = WxPreferencesGeneral(self, config)
        self.notificationsSection = WxPreferencesNotifications(self, config)
        self.detectionSection = WxPreferencesDetection(self, config)

        self.mainSizer.Add(self.generalSection, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
        self.mainSizer.Add(self.notificationsSection, 0, wx.EXPAND | wx.LEFT | wx.RIGHT,
                           4)
        self.mainSizer.Add(self.detectionSection, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)

        btnSizer = wx.StdDialogButtonSizer()
        saveBtn = wx.Button(self, wx.ID_OK, label="Save")
        saveBtn.Bind(wx.EVT_BUTTON, self.OnSave)
        saveBtn.SetFont(self.CreateFont())

        cancelBtn = wx.Button(self, wx.ID_CANCEL, label="Cancel")
        cancelBtn.SetFont(self.CreateFont())

        btnSizer.AddButton(saveBtn)
        btnSizer.AddButton(cancelBtn)
        btnSizer.Realize()

        self.mainSizer.AddStretchSpacer()
        self.mainSizer.Add(btnSizer, 0, wx.ALL | wx.ALIGN_RIGHT, 8)

        bestSize = self.GetBestSize()
        self.SetSize(bestSize.GetWidth() * 1.2, bestSize.GetHeight())

        self.Centre()
        self.SetIcons()

    def SetIcons(self):
        icon_bundle = wx.IconBundle()
        icon_bundle.AddIcon(wx_icon(16))
        icon_bundle.AddIcon(wx_icon(32))
        super().SetIcons(icon_bundle)

    def OnSave(self, event):
        event = NamedEvent(
            'save-config',
            data={
                **self.generalSection.GetValue(),
                **self.notificationsSection.GetValue(),
                **self.detectionSection.GetValue()
            })
        self.main.QueueEvent(event)
        self.EndModal(0)

    def CreateFont(self):
        return wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString)
