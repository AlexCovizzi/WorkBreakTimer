from app.wx_preferences_input import InputType, WxPreferencesInput
import wx
from app.wx_preferences_section import WxPreferencesSection


class WxPreferencesGeneral(WxPreferencesSection):

    def __init__(self, parent: wx.Window, config):
        super().__init__(parent, 'General')

        self.enabledInput = WxPreferencesInput(
            self.panel,
            'Enabled:',
            InputType.CHECKBOX,
            tooltip='Enabled',
            initialValue=config.get('enabled'))
        self.enabledFromInput = WxPreferencesInput(
            self.panel,
            'Active from:',
            InputType.TIME,
            tooltip='Activate only during this time',
            initialValue=config.get('activate_from_hour'))
        self.enabledUntilInput = WxPreferencesInput(
            self.panel,
            'Active until:',
            InputType.TIME,
            tooltip='Activate only during this time',
            initialValue=config.get('activate_until_hour'))
        self.workIntervalInput = WxPreferencesInput(
            self.panel,
            'Work interval (Minutes):',
            InputType.NUMBER,
            tooltip=('The maximum work interval before a notification ' +
                     'is sent to remind of a break'),
            initialValue=config.get('max_work_time_seconds') / 60)
        self.breakIntervalInput = WxPreferencesInput(
            self.panel,
            'Break interval (Minutes):',
            InputType.NUMBER,
            tooltip=('The minimum time a break should last\n' +
                     'A notification is sent in case the user returns ' +
                     'to the computer before this time has passed.'),
            initialValue=config.get('min_break_time_seconds') / 60)

        self.inputSizer.Add(self.enabledInput, 0, wx.EXPAND, 8)
        self.inputSizer.Add(self.enabledFromInput, 0, wx.EXPAND, 8)
        self.inputSizer.Add(self.enabledUntilInput, 0, wx.EXPAND, 8)
        self.inputSizer.Add(self.workIntervalInput, 0, wx.EXPAND, 8)
        self.inputSizer.Add(self.breakIntervalInput, 0, wx.EXPAND, 8)

    def GetValue(self):
        return {
            "enabled": self.enabledInput.GetValue(),
            "activate_from_hour": self.enabledFromInput.GetValue(),
            "activate_until_hour": self.enabledUntilInput.GetValue(),
            "max_work_time_seconds": self.workIntervalInput.GetValue() * 60,
            "min_break_time_seconds": self.breakIntervalInput.GetValue() * 60
        }
