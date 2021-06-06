import wx
from app.wx_preferences_section import WxPreferencesSection
from app.wx_preferences_input import InputType, WxPreferencesInput


class WxPreferencesNotifications(WxPreferencesSection):

    def __init__(self, parent: wx.Window, config):
        super().__init__(parent, 'Notifications')

        self.silenceWhenCameraInUseInput = WxPreferencesInput(
            self.panel,
            'Do not disturb while camera is in use:',
            InputType.CHECKBOX,
            tooltip=(
                'Do not send any notification while the video camera is in use.\n' +
                'Notifications will resume once the camera is available again.\n' +
                'Keep this checked in case you do not want to be disturbed ' +
                'during video calls or meetings'),
            initialValue=(not config.get('notify_when_camera_occupied')))
        self.cooldownInput = WxPreferencesInput(
            self.panel,
            'Cooldown (Seconds):',
            InputType.NUMBER,
            tooltip=('Send a new notification only after ' +
                     'the cooldown time has passed since the last notification'),
            initialValue=config.get('break_notification_cooldown_seconds'))

        self.inputSizer.Add(self.silenceWhenCameraInUseInput, 0, wx.EXPAND, 8)
        self.inputSizer.Add(self.cooldownInput, 0, wx.EXPAND, 8)

    def GetValue(self):
        return {
            "notify_when_camera_occupied":
                (not self.silenceWhenCameraInUseInput.GetValue()),
            "break_notification_cooldown_seconds": self.cooldownInput.GetValue()
        }
