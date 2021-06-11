import enum
import datetime
import wx
import wx.adv


class InputType(enum.Enum):
    CHECKBOX = 'CHECKBOX'
    NUMBER = 'NUMBER'
    TIME = 'TIME'


class WxPreferencesInput(wx.Panel):

    def __init__(self,
                 parent: wx.Window,
                 label: str,
                 inputType: InputType,
                 tooltip=None,
                 **kwargs):
        super().__init__(parent)

        self.sizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.label = self.CreateLabel(label, tooltip)
        self.input = self.CreateInput(inputType, **kwargs)

        self.sizer.Add(self.label, 1, wx.ALIGN_CENTER | wx.ALL, 8)
        self.sizer.Add(self.input, 1, wx.ALIGN_CENTER | wx.ALL, 8)

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

        self.SetSizer(self.sizer)

    def GetValue(self):
        value = self.input.GetValue()
        if type(self.input) == wx.adv.TimePickerCtrl:
            value = datetime.time(value.GetHour(), value.GetMinute(), value.GetSecond())
        return value

    def OnEnterWindow(self, event):
        self.SetBackgroundColour(wx.Colour(232, 236, 234))
        self.Refresh()

    def OnLeaveWindow(self, event):
        if self.HitTest(event.Position) == wx.HT_WINDOW_OUTSIDE:
            self.SetBackgroundColour(wx.Colour(242, 246, 244))
            self.Refresh()

    def CreateLabel(self, labelText: str, tooltipText: str = None):
        tooltipText = tooltipText or labelText
        label = wx.StaticText(self, wx.ID_ANY, labelText, wx.DefaultPosition,
                              wx.DefaultSize, 0)
        # label.SetToolTip(tooltipText)
        label.SetFont(self.CreateFont(wx.FONTFAMILY_DEFAULT))
        label.SetForegroundColour(wx.Colour(54, 54, 54))
        return label

    def CreateInput(self, inputType: InputType, **kwargs):
        if inputType == InputType.CHECKBOX:
            return self.CreateCheckboxInput(**kwargs)
        if inputType == InputType.NUMBER:
            return self.CreateNumberInput(**kwargs)
        if inputType == InputType.TIME:
            return self.CreateTimeInput(**kwargs)

    def CreateCheckboxInput(self, **kwargs):
        initialValue = kwargs.get('initialValue', True)
        checkboxInput = wx.CheckBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                    wx.DefaultSize, 0)
        checkboxInput.SetValue(initialValue)
        checkboxInput.SetFont(self.CreateFont(wx.FONTFAMILY_MODERN))
        return checkboxInput

    def CreateNumberInput(self, **kwargs):
        initialValue = kwargs.get('initialValue', 0)
        minValue = kwargs.get('minValue', 0)
        maxValue = kwargs.get('maxValue', 2**31 - 1)
        numberInput = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                  wx.DefaultSize, wx.SP_ARROW_KEYS, minValue, maxValue,
                                  initialValue)
        numberInput.SetFont(self.CreateFont(wx.FONTFAMILY_MODERN))
        return numberInput

    def CreateTimeInput(self, **kwargs):
        initialValue = kwargs.get('initialValue', datetime.time(0, 0, 0))
        timeInput = wx.adv.TimePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime,
                                          wx.DefaultPosition, wx.DefaultSize,
                                          wx.adv.TP_DEFAULT)
        timeInput.SetTime(initialValue.hour, initialValue.minute, initialValue.second)
        timeInput.SetFont(self.CreateFont(wx.FONTFAMILY_MODERN))
        return timeInput

    def CreateFont(self, fontFamily):
        return wx.Font(wx.NORMAL_FONT.GetPointSize(), fontFamily,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString)
