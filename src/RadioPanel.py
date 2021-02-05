#!/usr/bin/env python3

import configparser
import wx

from FreqSelector import *

#class FreqDisplayCtrl(wx.StaticText):


# This class is a single panel of radio stack drawn in parent frame
# of the application window.
class RadioPanel(wx.Panel):

    def __init__(self, _parent, _pos, _label, _config):
        self.config = _config
        self.height = 100
        self.width = _parent.Size[0]
        super(RadioPanel, self).__init__(_parent, pos=(0, _pos * self.height), size=(self.width, self.height))
        self.SetBackgroundColour("GREY")
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.activeFreq = wx.StaticText(self, pos=(10, 5), style=wx.ALIGN_LEFT, label=_label)

        font = self.activeFreq.GetFont()
        font.SetFamily(wx.FONTFAMILY_TELETYPE)
        font.Scale(1.5)

        self.activeFreq = wx.StaticText(self, pos=(10, 23), size=(100,24), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.activeFreq.SetBackgroundColour("WHITE")
        self.activeFreq.SetLabel(self.config["Active"])
        self.activeFreq.SetFont(font)

        btnAdd = wx.Button(self, label="<>", pos=(120, 20), size=(30, 30))
        btnAdd.Bind(wx.EVT_BUTTON, self.SwitchFreq)

        self.standbyFreq = FreqSelectorCtlr(self, (160, 20), (135,30), self.config)

        btnClear = wx.Button(self, label="C", pos=(305, 20), size=(30, 30))
        btnClear.Bind(wx.EVT_BUTTON, self.ClearStandbyFreq)

    def SwitchFreq(self, event):
        newActive = self.standbyFreq.GetValue()
        newStandby = self.activeFreq.GetLabel()
        self.activeFreq.SetLabel(newActive)
        self.standbyFreq.SetValue(newStandby)
        self.config["Active"] = newActive
        self.config["Standby"] = newStandby

    def ClearStandbyFreq(self, event):
        self.standbyFreq.ChangeValue("")
        self.standbyFreq.SetFocus()

    def ChangeFreq(self, event):
        text = self.standbyFreq.GetValue()
        print(text)
        if self.Validate():
            self.config["Standby"] = text
        else:
            if len(text):
                pos = self.standbyFreq.GetInsertionPoint() - 1
                char = text[pos]
                print("fail @" + str(pos) + ": " + char)
                self.standbyFreq.ChangeValue(self.config["Standby"])
                self.standbyFreq.SetInsertionPoint(pos)

    def Presets(self, event):
        boxPresets = wx.ComboCtrl(self)
        pass

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.DrawLine((0, self.height - 1), (self.width - 1, self.height - 1))


### Test routine
if __name__ == '__main__':

    cfg = configparser.ConfigParser()
    cfg["test-1"] = {}
    cfg["test-1"]["Active"] = "128.256"
    cfg["test-1"]["Standby"] = "512.064"
    cfg["test-1"]["Frequency"] = "111.222,333.444,555.666"
    cfg["test-1"]["Description"] = "One Two,Tree Fower,Fife Six"
    #cfg2 = configparser.ConfigParser()

    app = wx.App()
    win = wx.Frame(None, size=(400, 300), style=wx.MINIMIZE_BOX|wx.CLOSE_BOX)
    RadioPanel(win, 0, "NAV1", cfg["test-1"])
    #RadioPanel(win, 1, "NAV2")

    win.Show()
    app.MainLoop()
