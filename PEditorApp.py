import os
import sys
import wx
import peditor

class PEditorApp(peditor.PEditorFrame):

    def __init__(self):
        super(PEditorApp, self).__init__()

if __name__ == "__main__":
    app = wx.App(False)
    frame = PEditorApp()
    frame.Show(True)
    app.MainLoop()
