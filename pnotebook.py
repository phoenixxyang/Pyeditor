import wx
from wx.py import dispatcher

class PNotebook(wx.Notebook):
    """A notebook containing a page for each editor."""

    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=-1, style=wx.CLIP_CHILDREN)# |
                             #wx.TE_MULTILINE)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging, id=self.GetId())
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged, id=self.GetId())
        self.Bind(wx.EVT_IDLE, self.OnIdle)

    def OnIdle(self, event):
        self._updateTabText()
        event.Skip()

    def _updateTabText(self):
        size = 3
        changed = ' **'
        unchanged = ' --'
        selection = self.GetSelection()
        if selection < 1:
            return
        text = self.GetPageText(selection)
        window = self.GetPage(selection)
        if not window.editor:
            return
        if text.endswith(changed) or text.endswith(unchanged):
            name = text[:-size]
        else:
            name = text
        if name != window.editor.buffer.name:
            if "Shell" not in name:
                text = window.editor.buffer.name
        if window.editor.buffer.hasChanged():
            if text.endswith(changed):
                text = None
            elif text.endswith(unchanged):
                text = text[:-size] + changed
            else:
                text += changed
        else:
            if text.endswith(changed):
                text = text[:-size] + unchanged
            elif text.endswith(unchanged):
                text = None
            else:
                text += unchanged
        if text is not None:
            self.SetPageText(selection, text)
            self.Refresh()  # Needed on Win98.

    def OnPageChanging(self, event):
        event.Skip()

    def OnPageChanged(self, event):
        new = event.GetSelection()
        window = self.GetPage(new)
        dispatcher.send(signal='EditorChange', sender=self,
                        editor=window.editor)
        window.SetFocus()
        event.Skip()
