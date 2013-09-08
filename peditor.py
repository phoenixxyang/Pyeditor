
import wx

from pbuffer import Buffer
from wx.py import crust
from wx.py import dispatcher
import keyword
import pnotebook
import pstc
import pframe
from wx.py.shell import Shell
from wx.py import version
import pdb


class PEditorFrame(pframe.PFrame):

    def __init__(self, parent=None, id=-1, title='PEditor',
                 pos=wx.DefaultPosition, size=(800, 600), 
                 style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE,
                 filename=None):
        pframe.PFrame.__init__(self, parent, id, title, pos, size, style)
        self.buffers = {}
        self.buffer = None  # Current buffer.
        self.editor = None
        self._defaultText = title + ' - my Python editor.'
        #self.psb.SetFieldsCount(2)

        self._statusText = self._defaultText
        self.SetStatusText(self._statusText)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.notebook = None
        if self.notebook:
            dispatcher.connect(receiver=self._editorChange,
                               signal='EditorChange', sender=self.notebook)
        self._setup()
        if filename:
            self.bufferCreate(filename)

    def _setup(self):
        """Setup prior to first buffer creation.

        Called automatically by base class during init."""
        self.notebook = pnotebook.PNotebook(parent=self)

        intro = 'Py %s' % version.VERSION
        import imp
        module = imp.new_module('__main__')
        import __builtin__
        module.__dict__['__builtins__'] = __builtin__
        namespace = module.__dict__.copy()
        self.crust = crust.Crust(parent=self.notebook, intro=intro, locals=namespace)
        self.shell = self.crust.shell
        # Override the filling so that status messages go to the status bar.
        self.crust.filling.tree.setStatusText = self.SetStatusText
        # Override the shell so that status messages go to the status bar.
        self.shell.setStatusText = self.SetStatusText
        # Fix a problem with the sash shrinking to nothing.
        self.crust.filling.SetSashPosition(200)
        self.notebook.AddPage(page=self.crust, text='*Shell*', select=True)
        self.setEditor(self.crust.editor)
        self.crust.editor.SetFocus()

#        buffer = Buffer()
#        panel = wx.Panel(parent=self.notebook, id=-1)
#        panel.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: x)        
#        editor = Editor(parent=panel)
#        panel.editor = editor
#        sizer = wx.BoxSizer(wx.VERTICAL)
#        sizer.Add(editor.window, 1, wx.EXPAND)
#        panel.SetSizer(sizer)
#        panel.SetAutoLayout(True)
#        sizer.Layout()
#        buffer.addEditor(editor)
#        buffer.open(None)
#        self.setEditor(editor)
#        self.notebook.AddPage(page=panel, text=self.buffer.name, select=True)
#        self.editor.setFocus()
        self.bufferCreate()


    def _editorChange(self, editor):
        self.setEditor(editor)

    def _updateStatus(self):
        """Show current status information."""
        if self.editor and hasattr(self.editor, 'getStatus'):
            status = self.editor.getStatus()
            text = 'File: %s  |  Line: %d  |  Column: %d' % status
        else:
            text = self._defaultText
        if text != self._statusText:
            self.psb.SetStatusText(text,1)
            self._statusText = text

    def _updateTabText(self):
        """Show current buffer information on notebook tab."""
##         suffix = ' **'
##         notebook = self.notebook
##         selection = notebook.GetSelection()
##         if selection == -1:
##             return
##         text = notebook.GetPageText(selection)
##         window = notebook.GetPage(selection)
##         if window.editor and window.editor.buffer.hasChanged():
##             if text.endswith(suffix):
##                 pass
##             else:
##                 notebook.SetPageText(selection, text + suffix)
##         else:
##             if text.endswith(suffix):
##                 notebook.SetPageText(selection, text[:len(suffix)])

    def _updateTitle(self):
        """Show current title information."""
        title = self.GetTitle()
        if self.bufferHasChanged():
            if title.startswith('* '):
                pass
            else:
                self.SetTitle('* ' + title)
        else:
            if title.startswith('* '):
                self.SetTitle(title[2:])

        
    def bufferCreate(self, filename=None):
        buffer = Buffer()
        panel = wx.Panel(parent=self.notebook, id=-1)
        panel.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: x)        
        editor = Editor(parent=panel)
        panel.editor = editor
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(editor.window, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)
        sizer.Layout()
        buffer.addEditor(editor)
        buffer.open(filename)
        self.setEditor(editor)
        self.notebook.AddPage(page=panel, text=self.buffer.name, select=True)
        self.editor.setFocus()


    def hasBuffer(self):
        if self.buffers != {}:
            return True
        else:
            return False

    def bufferClose(self):
        if self.bufferHasChanged():
            cancel = self.bufferSuggestSave()
            if cancel:
                return cancel
        self.bufferDestroy()
        cancel = False
        return cancel


    def bufferHasChanged(self):
        if self.buffer:
            return self.buffer.hasChanged()
        else:
            return False


    def bufferSave(self):
        if self.buffer.doc.filepath:
            self.buffer.save()
            cancel = False
        else:
            cancel = self.bufferSaveAs()
        return cancel

    def bufferSaveAs(self):
        if self.bufferHasChanged() and self.buffer.doc.filepath:
            cancel = self.bufferSuggestSave()
            if cancel:
                return cancel
        filedir = ''
        if self.buffer and self.buffer.doc.filedir:
            filedir = self.buffer.doc.filedir
        result = saveSingle(directory=filedir)
        if result.path:
            self.buffer.saveAs(result.path)
            cancel = False
        else:
            cancel = True
        return cancel

    def bufferSuggestSave(self):
        """Suggest saving changes.  Return True if user selected Cancel."""
        result = messageDialog(parent=None,
                               message='%s has changed.\n'
                                       'Would you like to save it first'
                                       '?' % self.buffer.name,
                               title='Save current file?')
        if result.positive:
            cancel = self.bufferSave()
        else:
            cancel = result.text == 'Cancel'
        return cancel

#    def updateNamespace(self):
#        """Update the buffer namespace for autocompletion and calltips."""
#        if self.buffer.updateNamespace():
#            self.SetStatusText('Namespace updated')
#        else:
#            self.SetStatusText('Error executing, unable to update namespace')

    def bufferDestroy(self):
        selection = self.notebook.GetSelection()
##         print "Destroy Selection:", selection
        #if selection > 0:  # Don't destroy the PyCrust tab.
        if self.buffer:
            del self.buffers[self.buffer.id]
            self.buffer = None  # Do this before DeletePage().
        self.notebook.DeletePage(selection)

    def bufferNew(self):
        self.bufferCreate()
        cancel = False
        return cancel

    def bufferOpen(self):
        filedir = ''
        if self.buffer and self.buffer.doc.filedir:
            filedir = self.buffer.doc.filedir
        result = openMultiple(directory=filedir)
        for path in result.paths:
            if self.bufferHasChanged():
                self.bufferCreate(path)
            elif "NewFile" in self.buffer.name:
                self.buffer.open(path)
            else :
                self.bufferCreate(path)

        cancel = False
        return cancel

    def shellOpen(self):
        """Open a python interpretor"""
#        intro = 'Py %s' % version.VERSION
#        import imp
#        module = imp.new_module('__main__')
#        import __builtin__
#        module.__dict__['__builtins__'] = __builtin__
#        namespace = module.__dict__.copy()
        self.crust = crust.Crust(parent=self.notebook)#, intro=intro, locals=namespace)
        self.shell = self.crust.shell
        # Override the filling so that status messages go to the status bar.
        self.crust.filling.tree.setStatusText = self.SetStatusText
        # Override the shell so that status messages go to the status bar.
        self.shell.setStatusText = self.SetStatusText
        # Fix a problem with the sash shrinking to nothing.
        self.crust.filling.SetSashPosition(200)
        self.notebook.AddPage(page=self.crust, text='*Shell*', select=True)
        self.setEditor(self.crust.editor)
        self.crust.editor.SetFocus()
        

    def setEditor(self, editor):
        self.editor = editor
        self.buffer = self.editor.buffer
        self.buffers[self.buffer.id] = self.buffer

    def OnAbout(self, event):
        title = 'About PEditor'
        text = 'Simple Python Editor.'
        dialog = wx.MessageDialog(self, text, title,
                                  wx.OK | wx.ICON_INFORMATION)
        dialog.ShowModal()
        dialog.Destroy()

    def OnClose(self, event):
        for buffer in self.buffers.values():
            self.buffer = buffer
            if buffer.hasChanged():
                cancel = self.bufferSuggestSave()
                if cancel and event.CanVeto():
                    event.Veto()
                    return
        self.Destroy()

    def OnIdle(self, event):
        self._updateStatus()
        if hasattr(self, 'notebook'):
            self._updateTabText()
        self._updateTitle()
        event.Skip()

        








class Editor:
    """Editor having an PSTC."""

    def __init__(self, parent, id=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.CLIP_CHILDREN | wx.SUNKEN_BORDER |wx.TE_MULTILINE):
        self.window = PSTC(self, parent, id, pos, size, style)
        self.id = self.window.GetId()
        self.buffer = None
        # Assign handlers for keyboard events.
        self.window.Bind(wx.EVT_CHAR, self.OnChar)
        self.window.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def _setBuffer(self, buffer, text):
        self.buffer = buffer
        self.autoCompleteKeys = buffer.interp.getAutoCompleteKeys()
        self.clearAll()
        self.setText(text)
        self.emptyUndoBuffer()
        self.setSavePoint()

    def destroy(self):
        self.window.Destroy()

    def clearAll(self):
        self.window.ClearAll()

    def emptyUndoBuffer(self):
        self.window.EmptyUndoBuffer()

    def getStatus(self):
        """Return (filepath, line, column) status tuple."""
        if self.window:
            pos = self.window.GetCurrentPos()
            line = self.window.LineFromPosition(pos) + 1
            col = self.window.GetColumn(pos)
            if self.buffer:
                name = self.buffer.doc.filepath or self.buffer.name
            else:
                name = ''
            status = (name, line, col)
            return status
        else:
            return ('', 0, 0)

    def getText(self):
        return self.window.GetText()

    def hasChanged(self):
        """Return True if contents have changed."""
        return self.window.GetModify()

    def setFocus(self):
        self.window.SetFocus()

    def setSavePoint(self):
        self.window.SetSavePoint()

    def setText(self, text):
        self.window.SetText(text)

    def OnChar(self, event):
        """Keypress event handler."""

        key = event.GetKeyCode()
        self.promptPosEnd = 0
        if key in self.autoCompleteKeys:
            # Usually the dot (period) key activates auto completion.
            if self.window.AutoCompActive(): 
                self.window.AutoCompCancel()
            self.window.ReplaceSelection('')
            self.window.AddText(chr(key))
            #text, pos = self.window.GetCurLine()
            #text = text[:pos]

            currpos = self.window.GetCurrentPos()
            stoppos = self.promptPosEnd
            command = self.window.GetTextRange(stoppos,currpos) + chr(key)
            if self.window.autoComplete: 
                self.autoCompleteShow(command)
        elif key == ord('('):
            # The left paren activates a call tip and cancels an
            # active auto completion.
            if self.window.AutoCompActive(): 
                self.window.AutoCompCancel()
            self.window.ReplaceSelection('')

            self.window.AddText('(')
            text, pos = self.window.GetCurLine()
            text = text[:pos]
            self.autoCallTipShow(text)
        else:
            # Allow the normal event handling to take place.
            event.Skip()

    def OnKeyDown(self, event):
        """Key down event handler."""

        key = event.GetKeyCode()
        # If the auto-complete window is up let it do its thing.
        if self.window.AutoCompActive():
            event.Skip()
            return
        controlDown = event.ControlDown()
        altDown = event.AltDown()
        shiftDown = event.ShiftDown()
        # Let Ctrl-Alt-* get handled normally.
        if controlDown and altDown:
            event.Skip()
        # Increase font size.
        elif controlDown and key in (ord(']'),):
            dispatcher.send(signal='FontIncrease')
        # Decrease font size.
        elif controlDown and key in (ord('['),):
            dispatcher.send(signal='FontDecrease')
        # Default font size.
        elif controlDown and key in (ord('='),):
            dispatcher.send(signal='FontDefault')
        elif shiftDown and key in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
            self.window.OnShowCompHistory()
        else:
            event.Skip()

    def autoCompleteShow(self, command):
        """Display auto-completion popup list."""
        #list = self.buffer.interp.getAutoCompleteList(command, 
        #           includeMagic=self.window.autoCompleteIncludeMagic, 
        #            includeSingle=self.window.autoCompleteIncludeSingle, 
        #            includeDouble=self.window.autoCompleteIncludeDouble)
        list = keyword.kwlist
        if list:
            options = ' '.join(list)
            offset = 0
            self.window.AutoCompShow(offset, options)

    def autoCallTipShow(self, command):
        """Display argument spec and docstring in a popup window."""
        if self.window.CallTipActive():
            self.window.CallTipCancel()
        (name, argspec, tip) = self.buffer.interp.getCallTip(command)
        if tip:
            dispatcher.send(signal='Shell.calltip', sender=self, calltip=tip)
        if not self.window.autoCallTip:
            return
        startpos = self.window.GetCurrentPos()
        if argspec:
            self.window.AddText(argspec + ')')
            endpos = self.window.GetCurrentPos()
            self.window.SetSelection(startpos, endpos)
        if tip:
            tippos = startpos - (len(name) + 1)
            fallback = startpos - self.GetColumn(startpos)
            # In case there isn't enough room, only go back to the
            # fallback.
            tippos = max(tippos, fallback)
            self.CallTipShow(tippos, tip)


class PSTC(pstc.PSTC):
    """PSTC based on StyledTextCtrl."""

    def __init__(self, editor, parent, id=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.CLIP_CHILDREN | wx.SUNKEN_BORDER):
        pstc.PSTC.__init__(self, parent, id, pos, size, style)
        self.editor = editor


class DialogResults:

    def __init__(self, returned):
        """Create wrapper for results returned by dialog."""
        self.returned = returned
        self.positive = returned in (wx.ID_OK, wx.ID_YES)
        self.text = self._asString()
        

    def __repr__(self):
        return str(self.__dict__)

    def _asString(self):
        returned = self.returned
        if returned == wx.ID_OK:
            return "Ok"
        elif returned == wx.ID_CANCEL:
            return "Cancel"
        elif returned == wx.ID_YES:
            return "Yes"
        elif returned == wx.ID_NO:
            return "No"


def fileDialog(parent=None, title='Open', directory='', filename='',
               wildcard='All Files (*.*)|*.*',
               style=wx.OPEN | wx.MULTIPLE):
    dialog = wx.FileDialog(parent, title, directory, filename,
                           wildcard, style)
    result = DialogResults(dialog.ShowModal())
    if result.positive:
        result.paths = dialog.GetPaths()
    else:
        result.paths = []
    dialog.Destroy()
    return result


def openSingle(parent=None, title='Open', directory='', filename='',
               wildcard='All Files (*.*)|*.*', style=wx.OPEN):
    dialog = wx.FileDialog(parent, title, directory, filename,
                           wildcard, style)
    result = DialogResults(dialog.ShowModal())
    if result.positive:
        result.path = dialog.GetPath()
    else:
        result.path = None
    dialog.Destroy()
    return result


def openMultiple(parent=None, title='Open', directory='', filename='',
                 wildcard='All Files (*.*)|*.*',
                 style=wx.OPEN | wx.MULTIPLE):
    return fileDialog(parent, title, directory, filename, wildcard, style)


def saveSingle(parent=None, title='Save', directory='', filename='',
               wildcard='All Files (*.*)|*.*',
               style=wx.SAVE | wx.OVERWRITE_PROMPT):
    dialog = wx.FileDialog(parent, title, directory, filename,
                           wildcard, style)
    result = DialogResults(dialog.ShowModal())
    if result.positive:
        result.path = dialog.GetPath()
    else:
        result.path = None
    dialog.Destroy()
    return result


#def directory(parent=None, message='Choose a directory', path='', style=0,
#              pos=wx.DefaultPosition, size=wx.DefaultSize):
#    """Dir dialog wrapper function."""
#    dialog = wx.DirDialog(parent, message, path, style, pos, size)
#    result = DialogResults(dialog.ShowModal())
#    if result.positive:
#        result.path = dialog.GetPath()
#    else:
#        result.path = None
#    dialog.Destroy()
#    return result


def messageDialog(parent=None, message='', title='Message box',
                  style=wx.YES_NO | wx.CANCEL | wx.CENTRE | wx.ICON_QUESTION,
                  pos=wx.DefaultPosition):
    dialog = wx.MessageDialog(parent, message, title, style, pos)
    result = DialogResults(dialog.ShowModal())
    dialog.Destroy()
    return result

class CommandHis(wx.TextCtrl):

    """Text control containing all commands for session."""

    def __init__(self, parent=None, id=-1,ShellClassName='Shell'):
        style = (wx.TE_MULTILINE | wx.TE_READONLY |
                 wx.TE_RICH2 | wx.TE_DONTWRAP)
        wx.TextCtrl.__init__(self, parent, id, style=style)
        dispatcher.connect(receiver=self.addHistory,
                           signal="PSTC"+".addHistory")
        dispatcher.connect(receiver=self.clearHistory,
                           signal="PSTC"+".clearHistory")
        dispatcher.connect(receiver=self.loadHistory,
                           signal="PSTC"+".loadHistory")

        df = self.GetFont()
        font = wx.Font(df.GetPointSize(), wx.TELETYPE, wx.NORMAL, wx.NORMAL)
        self.SetFont(font)

    def loadHistory(self, history):
        # preload the existing history, if any
        hist = history[:]
        hist.reverse()
        self.SetValue('\n'.join(hist) + '\n')
        self.SetInsertionPointEnd()

    def addHistory(self, command):
        if command:
            self.SetInsertionPointEnd()
            self.AppendText(command + '\n')

    def clearHistory(self):
        self.SetValue("")
