import wx
import wx.adv
from app.config import Config


class WxPreferencesDialog(wx.Dialog):

    def __init__(self, config: Config, parent=None):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, 'Preferences')
        self._config = config
        self.createWidgets()

    def createWidgets(self):
        self._mainsizer = wx.BoxSizer(wx.VERTICAL)
        self._options = []

        self._addOption('enabled', 'Enabled:')
        self._addOption('activate_from_hour', 'Activate from:')
        self._addOption('activate_until_hour', 'Activate until:')
        self._addOption('calculate_notification_every_seconds',
                        'Calculate notification every (seconds):')
        self._addOption('check_presence_every_seconds',
                        'Detect presence every (seconds):')
        self._addOption('max_work_time_seconds', 'Max work time (seconds):')
        self._addOption('min_break_time_seconds', 'Min break time (seconds):')
        self._addOption('break_notification_cooldown_seconds',
                        'Notification cooldown (seconds):')
        self._addOption('camera', 'Camera:')

        btnSizer = wx.StdDialogButtonSizer()
        saveBtn = wx.Button(self, wx.ID_OK, label="Save")
        saveBtn.Bind(wx.EVT_BUTTON, self.onSave)
        btnSizer.AddButton(saveBtn)

        cancelBtn = wx.Button(self, wx.ID_CANCEL)
        btnSizer.AddButton(cancelBtn)
        btnSizer.Realize()

        self._mainsizer.Add(btnSizer, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        self.SetSizer(self._mainsizer)

        self.Fit()
        self.Centre()

    def onSave(self, event):
        updated = {item['key']: str(item['extractor']()) for item in self._options}
        self._config.update(updated)
        self._config.write()
        self._config.read()
        self.Close(0)

    def _addOption(self, key, label):
        font = wx.Font(wx.FONTSIZE_SMALL, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_NORMAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, label=label)
        label.SetFont(font)
        edit = wx.TextCtrl(self, value=self._config.getstr(key), name=key)
        sizer.Add(label, 1, wx.ALL, 8)
        sizer.Add(edit, 1, wx.ALL, 8)
        self._mainsizer.Add(sizer, 0, wx.EXPAND)

        self._options.append({'key': key, 'extractor': lambda: edit.GetValue()})
