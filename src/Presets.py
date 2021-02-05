#!/usr/bin/env python3

import wx
import wx.grid
import wx.lib.scrolledpanel

# This class is a dialog window which allow to manage (add, modify, remove)
# presets provided in the _config dictionary. The class uses grid wxWidget
# consisting of two columns. The dictionary must have following form:
# {"keyA":"keyAval1[,[keyAval2,][...]]", "keyB":"keyBval1[,[keyBval2,][...]]"}
# Both "keyA" and "keyB" constitute the grid columns.
# A single preset is formed as "keyAvalX->keyBvalX"
# The "keyA" record must not contain empty values.
# The "keyB" record may contain empty values.
class PresetsDialog(wx.Dialog):

    def __init__(self, _parent, _title, _config):
        super(PresetsDialog, self).__init__(_parent, title=_title, size=(450, 270))
        self.config = _config
        self.items = list(self.config)
        self.InitUi()
        self.FillData()

    def InitUi(self):
        panelGrid = wx.lib.scrolledpanel.ScrolledPanel(self, pos=(0, 0), size=(450, 200))
        panelRight = wx.Panel(self, pos=(370, 0), size=(130, 200))
        panelBottom = wx.Panel(self, pos=(0, 200), size=(450, 100))
        panelButtons = wx.Panel(panelBottom, pos=(0, 0), size=(205, 100))

        self.grid = wx.grid.Grid(panelGrid)
        self.grid.CreateGrid(1, 2)
        self.grid.SetColLabelValue(0, self.items[0])
        self.grid.SetColFormatFloat(0, 7, 3)
        self.grid.SetColLabelValue(1, self.items[1])
        self.grid.SetColSize(1, 200)

        sizerGrid = wx.BoxSizer(wx.VERTICAL)
        sizerGrid.Add(self.grid, 1, wx.EXPAND)
        panelGrid.SetSizer(sizerGrid)

        sizerBottom = wx.BoxSizer(wx.HORIZONTAL)
        sizerBottom.AddStretchSpacer(1)
        sizerBottom.Add(panelButtons, 0, wx.ALIGN_CENTER)
        sizerBottom.AddStretchSpacer(1)
        panelBottom.SetSizer(sizerBottom)

        btnAdd = wx.Button(panelRight, label="Add", pos=(0, 140), size=(65, 20))
        btnAdd.Bind(wx.EVT_BUTTON, self.Add)
        btnDel = wx.Button(panelRight, label="Delete", pos=(0, 170), size=(65, 20))
        btnDel.Bind(wx.EVT_BUTTON, self.Del)
        btnOk = wx.Button(panelButtons, label="OK", pos=(10, 5))
        btnOk.Bind(wx.EVT_BUTTON, self.Ok)
        btnCancel = wx.Button(panelButtons, label="Cancel", pos=(110, 5))
        btnCancel.Bind(wx.EVT_BUTTON, self.Cancel)

    def FillData(self):
        freqList = self.config[self.items[0]].split(",")
        descList = self.config[self.items[1]].split(",")
        table = self.grid.GetTable()
        row = 0
        for freq, desc in zip(freqList, descList):
            table.SetValue(row, 0, freq)
            table.SetValue(row, 1, desc)
            table.AppendRows(1)
            row = row + 1

    def Add(self, e):
        self.grid.AppendRows(1)

    def Del(self, e):
        while True:
            row = self.grid.GetSelectedRows()
            if row:
                self.grid.DeleteRows(row[0], 1)
            else:
                break

    def Ok(self, e):
        self.config[self.items[0]] = ""
        self.config[self.items[1]] = ""
        table = self.grid.GetTable()
        for row in range(0, table.GetNumberRows()):
            freq = table.GetValue(row, 0)
            desc = table.GetValue(row, 1)
            if freq:
                if self.config[self.items[0]]:
                    self.config[self.items[0]] = self.config[self.items[0]] + ","
                    self.config[self.items[1]] = self.config[self.items[1]] + ","
                self.config[self.items[0]] = self.config[self.items[0]] + freq
                self.config[self.items[1]] = self.config[self.items[1]] + desc
        self.EndModal(wx.ID_OK)

    def Cancel(self, e):
        self.EndModal(wx.ID_CANCEL)


### Test routine
if __name__ == '__main__':

    def test1(event):
        config = {"F1":"", "F2":""}
        dlg = PresetsDialog(win, "Test 1", config)
        if dlg.ShowModal() == wx.ID_OK:
            print(config)

    def test2(event):
        config = {"F1":"1,2,5,9", "F2":"one,two,fifth,niner"}
        dlg = PresetsDialog(win, "Test 2", config)
        if dlg.ShowModal() == wx.ID_OK:
            print(config)

    def test3(event):
        config = {"F1":"1,2,5,7,9", "F2":"one,two,fifth,,niner"}
        dlg = PresetsDialog(win, "Test 2", config)
        if dlg.ShowModal() == wx.ID_OK:
            print(config)

    app = wx.App()
    win = wx.Frame(None, size=(120, 160))
    pan = wx.Panel(win)
    btnTest1 = wx.Button(win, label="Test 1", pos=(20, 10))
    btnTest1.Bind(wx.EVT_BUTTON, test1)
    btnTest2 = wx.Button(win, label="Test 2", pos=(20, 50))
    btnTest2.Bind(wx.EVT_BUTTON, test2)
    btnTest3 = wx.Button(win, label="Test 3", pos=(20, 90))
    btnTest3.Bind(wx.EVT_BUTTON, test3)
    win.Show()
    app.MainLoop()
