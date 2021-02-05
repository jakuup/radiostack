#!/usr/bin/env python3

import configparser
import wx


# This class is validator for FreqSelectorCtlr class
class FrequencyValidator(wx.Validator):

    def __init__(self):
        super(FrequencyValidator, self).__init__()

    def Clone(self):
        return FrequencyValidator()

    def TransferFromWindow(self):
        return True

    def TransferToWindow(self):
        return True

    def Validate(self, parent):
        ctrl = self.GetWindow()
        text = ctrl.GetValue()
        try:
            value = float(text)
            assert((value >= 0) and (value < 1000))
        except:
            return False
        return True


# This class is the popup for the FreqSelectorCtlr class
class PresetsPopup(wx.ComboPopup):

    def __init__(self):
        super(PresetsPopup, self).__init__()

    def Init(self):
        self.value = -1
        self.curitem = -1

    def Create(self, parent):
        self.control = wx.ListCtrl(parent, style=wx.LC_LIST|wx.LC_NO_HEADER|wx.LC_SINGLE_SEL)
        font = self.control.GetFont()
        font.SetFamily(wx.FONTFAMILY_TELETYPE)
        font.Scale(1)
        self.control.SetFont(font)
        self.control.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.control.Bind(wx.EVT_MOTION, self.OnMotion)
        return True

    def GetControl(self):
        return self.control

    def AddItem(self, text):
        self.control.InsertItem(self.control.GetItemCount(), text)

    def OnMotion(self, evt):
        item, flags = self.control.HitTest(evt.GetPosition())
        if item >= 0:
            self.control.Select(item)
            self.curitem = item

    def OnLeftDown(self, event):
        self.value = self.curitem
        self.Dismiss()

    def GetStringValue(self):
        if self.value >= 0:
            return self.control.GetItemText(self.value).split("|", 1)[0]
        return ""


# This class is the main frequency selector control, which is build from
# customized wx.ComboCtrl and customized wx.ComboPopup assigned as PopupCtrl.
# Both manually entered frequency and frequency selected from the popup
# are subject of validation by the FrequencyValidator object.
class FreqSelectorCtlr(wx.ComboCtrl):

    def __init__(self, parent, _pos, _size, config):
        super(FreqSelectorCtlr, self).__init__(parent, pos=_pos, size=_size,
                                               style=wx.ALIGN_CENTER_HORIZONTAL,
                                               validator=FrequencyValidator())
        self.config = config
        font = self.GetFont()
        font.SetFamily(wx.FONTFAMILY_TELETYPE)
        font.Scale(1.5)
        self.SetMargins((0,-1))
        self.SetBackgroundColour("WHITE")
        self.Bind(wx.EVT_TEXT, self.ChangeFreq)
        self.SetFont(font)
        self.SetMaxLength(7)

        popupPresets = PresetsPopup()
        self.SetPopupControl(popupPresets)
        freqList = self.config["Frequency"].split(",")
        descList = self.config["Description"].split(",")
        for freq, desc in zip(freqList, descList):
            popupPresets.AddItem(freq + "|" + desc)

        self.SetText(self.config["Standby"])

    def ChangeFreq(self, event):
        text = self.GetValue()
        if self.GetParent().Validate():
            self.config["Standby"] = text
            pass
        else:
            if len(text):
                pos = self.GetInsertionPoint() - 1
                char = text[pos]
                self.ChangeValue(self.config["Standby"])
                self.SetInsertionPoint(pos)


### Test routine
if __name__ == '__main__':
    
    print("WARNING: No test routine !!!")
    print("         The module is tested along with RadioPanel class.")
