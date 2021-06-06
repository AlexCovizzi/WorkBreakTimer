import wx
from app.wx_preferences_section import WxPreferencesSection
from app.wx_preferences_input import InputType, WxPreferencesInput


class WxPreferencesDetection(WxPreferencesSection):

    def __init__(self, parent: wx.Window, config):
        super().__init__(parent, 'Presence detection')

        self.cameraInput = WxPreferencesInput(
            self.panel,
            'Camera:',
            InputType.NUMBER,
            tooltip=('The video camera to use to detect the presence.\n' +
                     '0 is the default video camera'),
            initialValue=config.get('camera'))
        self.detectionFrequencyInput = WxPreferencesInput(
            self.panel,
            'Detection frequency (Seconds):',
            InputType.NUMBER,
            tooltip=('How frequently it should detect the presence'),
            initialValue=config.get('check_presence_every_seconds'))
        self.numberOfSnapshotsInput = WxPreferencesInput(
            self.panel,
            'Number of snapshots:',
            InputType.NUMBER,
            tooltip=('Number of snapshots to take during each detection.\n' +
                     'It is recommanded to take at least 2-3 snapshots' +
                     'so that the camera can adjust.'),
            initialValue=config.get('num_of_snapshots'))
        self.timeBetweenSnapshotsInput = WxPreferencesInput(
            self.panel,
            'Time between snapshots (Millis):',
            InputType.NUMBER,
            tooltip=('Time in milliseconds between each snapshot.\n' +
                     'It is recommanded to wait at least 50 milliseconds between ' +
                     'each snapshot so that the camera can adjust.'),
            initialValue=config.get('time_between_snapshots_millis'))

        self.inputSizer.Add(self.cameraInput, 0, wx.EXPAND, 8)
        self.inputSizer.Add(self.detectionFrequencyInput, 0, wx.EXPAND, 8)
        self.inputSizer.Add(self.numberOfSnapshotsInput, 0, wx.EXPAND, 8)
        self.inputSizer.Add(self.timeBetweenSnapshotsInput, 0, wx.EXPAND, 8)

    def GetValue(self):
        return {
            "camera": self.cameraInput.GetValue(),
            "check_presence_every_seconds": self.detectionFrequencyInput.GetValue(),
            "num_of_snapshots": self.numberOfSnapshotsInput.GetValue(),
            "time_between_snapshots_millis": self.timeBetweenSnapshotsInput.GetValue()
        }
