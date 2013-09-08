
import wx
import os
import time
#import images
import pdb




class PFrame(wx.Frame):

    def __init__(self, parent=None, id=-1, title='Editor',
                 pos=wx.DefaultPosition, size=wx.DefaultSize, 
                 style=wx.DEFAULT_FRAME_STYLE,shellName='PyCrust'):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.psb = pStatusBar(self)
        self.SetStatusBar(self.psb)
        self.toolbox = self.CreateToolBar(wx.TB_HORIZONTAL
            | wx.NO_BORDER
            | wx.TB_FLAT)
        self.__setupToolBar()
        #self.SetStatusText('PFrame')
        self.shellName=shellName
        self.__createMenus()

        self.findDlg = None
        self.findData = wx.FindReplaceData()
        self.findData.SetFlags(wx.FR_DOWN)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
#        self.Bind(wx.EVT_ICONIZE, self.OnIconize)
#
#
#    def OnIconize(self, event):
#        """Event handler for Iconize."""
#        self.iconized = event.Iconized()

    def __setupToolBar(self):
        bmpSize = (24, 24)
        
        tb = self.toolbox
        tb.SetToolBitmapSize(bmpSize)
        new_bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, bmpSize)
        close_bmp = wx.ArtProvider.GetBitmap(wx.ART_CLOSE, wx.ART_TOOLBAR,
                                             bmpSize)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR,
                                            bmpSize)
        save_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR,
                                            bmpSize)
        saveas_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS,
                                              wx.ART_TOOLBAR, bmpSize)
        copy_bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY,
                                              wx.ART_TOOLBAR, bmpSize)
        cut_bmp = wx.ArtProvider.GetBitmap(wx.ART_CUT,
                                              wx.ART_TOOLBAR, bmpSize)
        paste_bmp = wx.ArtProvider.GetBitmap(wx.ART_PASTE,
                                              wx.ART_TOOLBAR, bmpSize)
        undo_bmp = wx.ArtProvider.GetBitmap(wx.ART_UNDO,
                                              wx.ART_TOOLBAR, bmpSize)
        redo_bmp = wx.ArtProvider.GetBitmap(wx.ART_REDO,
                                              wx.ART_TOOLBAR, bmpSize)

        #toolbar icon "New"
        tb.AddLabelTool(ID_TB_NEW, "New", new_bmp, shortHelp = "New File",
                            longHelp = "Open a new file with a new buffer.")
        self.Bind(wx.EVT_TOOL, self.OnFileNew, id = ID_TB_NEW)

        #toolbar icon "Open"
        tb.AddLabelTool(ID_TB_OPEN, "Open", open_bmp, shortHelp = "Open File",
                        longHelp = "Open a file in current tab if current buffer is not used")
        self.Bind(wx.EVT_TOOL, self.OnFileOpen, id = ID_TB_OPEN)

        #toolbar icon "Save"
        tb.AddLabelTool(ID_TB_SAVE, "Save", save_bmp, shortHelp = "Save File",
                        longHelp = "Save the current file.")
        self.Bind(wx.EVT_TOOL, self.OnFileSave, id = ID_TB_SAVE)

        #toolbar icon "Save As"
        tb.AddLabelTool(ID_TB_SAVE_AS, "Save As", saveas_bmp, shortHelp = "Save as",
                        longHelp = "Save as a specific file name.")
        self.Bind(wx.EVT_TOOL, self.OnFileSaveAs, id = ID_TB_SAVE_AS)

        #toolbar icon "Close"
        tb.AddLabelTool(ID_TB_ClOSE, "Close", close_bmp, shortHelp =
                        "Close File", longHelp = "Close the current file and buffer.")
        self.Bind(wx.EVT_TOOL, self.OnFileClose, id = ID_TB_ClOSE)
        
        tb.AddSeparator()

        #toolbar icon "Copy"
        tb.AddLabelTool(ID_TB_COPY, "Copy", copy_bmp, shortHelp = "Copy Content", 
                        longHelp = "")
        self.Bind(wx.EVT_TOOL, self.OnCopy, id = ID_TB_COPY)
        
        #toolbar icon "Cut"
        tb.AddLabelTool(ID_TB_CUT, "Cut", cut_bmp, shortHelp = "Cut Content", 
                        longHelp = "")
        self.Bind(wx.EVT_TOOL, self.OnCut, id = ID_TB_CUT)

        
        #toolbar icon "Paste"
        tb.AddLabelTool(ID_TB_PASTE, "Paste", paste_bmp, shortHelp = "Paste Content", 
                        longHelp = "")
        self.Bind(wx.EVT_TOOL, self.OnPaste, id = ID_TB_PASTE)
        
        tb.AddSeparator()

        #toolbar icon "Undo"
        tb.AddLabelTool(ID_TB_UNDO, "Undo", undo_bmp, shortHelp = "Undo operation", 
                        longHelp = "")
        self.Bind(wx.EVT_TOOL, self.OnUndo, id = ID_TB_UNDO)

        #toolbar icon "Redo"
        tb.AddLabelTool(ID_TB_REDO, "Redo", redo_bmp, shortHelp = "Redo operation", 
                        longHelp = "")
        self.Bind(wx.EVT_TOOL, self.OnRedo, id = ID_TB_REDO)
        
        tb.Realize()


#test the toolbar
#    def OnToolNew(self, event):
#        self.bufferNew()



    def __createMenus(self):
        # File Menu
        m = self.fileMenu = wx.Menu()
        m.Append(ID_NEW, '&New \tCtrl+N',
                 'New file')
        m.Append(ID_OPEN, '&Open... \tCtrl+O',
                 'Open file')

        m.Append(ID_OPENSHELL, 'Open Shell \t',
                 'Open Shell')

        m.AppendSeparator()
        m.Append(ID_CLOSE, '&Close \tCtrl+W',
                 'Close file')
        m.AppendSeparator()
        m.Append(ID_SAVE, '&Save... \tCtrl+S',
                 'Save file')
        m.Append(ID_SAVEAS, 'Save &As \tCtrl+Shift+S',
                 'Save file with new name')
        m.AppendSeparator()
        m.Append(ID_NAMESPACE, '&Update Namespace \tCtrl+Shift+N',
                 'Update namespace for autocompletion and calltips')
        m.AppendSeparator()
        m.Append(ID_EXIT, 'E&xit\tCtrl+Q', 'Exit Program')

        # Edit
        m = self.editMenu = wx.Menu()
        m.Append(ID_UNDO, '&Undo \tCtrl+Z',
                 'Undo the last action')
        m.Append(ID_REDO, '&Redo \tCtrl+Y',
                 'Redo the last undone action')
        m.AppendSeparator()
        m.Append(ID_CUT, 'Cu&t \tCtrl+X',
                 'Cut the selection')
        m.Append(ID_COPY, '&Copy \tCtrl+C',
                 'Copy the selection')
        m.Append(ID_PASTE, '&Paste \tCtrl+V', 'Paste from clipboard')
        m.AppendSeparator()
        m.Append(ID_CLEAR, 'Cle&ar',
                 'Delete the selection')
        m.Append(ID_SELECTALL, 'Select A&ll \tCtrl+A',
                 'Select all text')
        m.AppendSeparator()
        m.Append(ID_EMPTYBUFFER, 'E&mpty Buffer...',
                 'Delete all the contents of the edit buffer')
        m.Append(ID_FIND, '&Find Text... \tCtrl+F',
                 'Search for text in the edit buffer')
        m.Append(ID_FINDNEXT, 'Find &Next \tCtrl+G',
                 'Find next instance of the search text')
        m.Append(ID_FINDPREVIOUS, 'Find Pre&vious \tCtrl+Shift+G',
                 'Find previous instance of the search text')
        
        # View
        m = self.viewMenu = wx.Menu()
        m.Append(ID_WRAP, '&Wrap Lines\tCtrl+Shift+W',
                 'Wrap lines at right edge', wx.ITEM_CHECK)
        m.Append(ID_SHOW_LINENUMBERS, '&Show Line Numbers\tCtrl+Shift+L',
                 'Show Line Numbers', wx.ITEM_CHECK)
        m.Append(ID_TOGGLE_MAXIMIZE, '&Toggle Maximize\tF11',
                 'Maximize/Restore Application')
        if hasattr(self, 'ToggleTools'):
            m.Append(ID_SHOWTOOLS,
                     'Show &Tools\tF4',
                     'Show the filling and other tools', wx.ITEM_CHECK)
        if self.shellName==['PySlices','SymPySlices']:
            m.Append(ID_HIDEFOLDINGMARGIN,
                                '&Hide Folding Margin',
                                'Hide Folding Margin', wx.ITEM_CHECK)
        
        # Options
        #m = self.autocompMenu = wx.Menu()
        #m.Append(ID_AUTOCOMP_SHOW, 'Show &Auto Completion\tCtrl+Shift+A',
        #         'Show auto completion list', wx.ITEM_CHECK)
        #m = self.optionsMenu = wx.Menu()
        #m.AppendMenu(ID_AUTOCOMP, '&Auto Completion', self.autocompMenu,
        #             'Auto Completion Options')
        #        
        m.AppendSeparator()


        m = self.helpMenu = wx.Menu()
        #m.Append(ID_HELP, '&Help\tF1', 'Help!')
        #m.AppendSeparator()
        m.Append(ID_ABOUT, '&About...', 'About this program')

        b = self.menuBar = wx.MenuBar()
        b.Append(self.fileMenu, '&File')
        b.Append(self.editMenu, '&Edit')
        b.Append(self.viewMenu, '&View')
        #b.Append(self.optionsMenu, '&Options')
        b.Append(self.helpMenu, '&Help')
        self.SetMenuBar(b)

        self.Bind(wx.EVT_MENU, self.OnFileNew, id=ID_NEW)
        self.Bind(wx.EVT_MENU, self.OnFileOpen, id=ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnShellOpen, id=ID_OPENSHELL)
        self.Bind(wx.EVT_MENU, self.OnFileClose, id=ID_CLOSE)
        self.Bind(wx.EVT_MENU, self.OnFileSave, id=ID_SAVE)
        self.Bind(wx.EVT_MENU, self.OnFileSaveAs, id=ID_SAVEAS)
#        self.Bind(wx.EVT_MENU, self.OnFileUpdateNamespace, id=ID_NAMESPACE)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnUndo, id=ID_UNDO)
        self.Bind(wx.EVT_MENU, self.OnRedo, id=ID_REDO)
        self.Bind(wx.EVT_MENU, self.OnCut, id=ID_CUT)
        self.Bind(wx.EVT_MENU, self.OnCopy, id=ID_COPY)
        self.Bind(wx.EVT_MENU, self.OnPaste, id=ID_PASTE)
        self.Bind(wx.EVT_MENU, self.OnClear, id=ID_CLEAR)
        self.Bind(wx.EVT_MENU, self.OnSelectAll, id=ID_SELECTALL)
        self.Bind(wx.EVT_MENU, self.OnEmptyBuffer, id=ID_EMPTYBUFFER)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnHelp, id=ID_HELP)
        self.Bind(wx.EVT_MENU, self.OnAutoCompleteShow, id=ID_AUTOCOMP_SHOW)
#        self.Bind(wx.EVT_MENU, self.OnAutoCompleteMagic, id=ID_AUTOCOMP_MAGIC)
#        self.Bind(wx.EVT_MENU, self.OnAutoCompleteSingle, id=ID_AUTOCOMP_SINGLE)
#        self.Bind(wx.EVT_MENU, self.OnAutoCompleteDouble, id=ID_AUTOCOMP_DOUBLE)
#        self.Bind(wx.EVT_MENU, self.OnCallTipsShow, id=ID_CALLTIPS_SHOW)
#        self.Bind(wx.EVT_MENU, self.OnCallTipsInsert, id=ID_CALLTIPS_INSERT)
        self.Bind(wx.EVT_MENU, self.OnWrap, id=ID_WRAP)
        self.Bind(wx.EVT_MENU, self.OnToggleMaximize, id=ID_TOGGLE_MAXIMIZE)
        self.Bind(wx.EVT_MENU, self.OnShowLineNumbers, id=ID_SHOW_LINENUMBERS)
        self.Bind(wx.EVT_MENU, self.OnFindText, id=ID_FIND)
        self.Bind(wx.EVT_MENU, self.OnFindNext, id=ID_FINDNEXT)
        self.Bind(wx.EVT_MENU, self.OnFindPrevious, id=ID_FINDPREVIOUS)
        self.Bind(wx.EVT_MENU, self.OnToggleTools, id=ID_SHOWTOOLS)
        self.Bind(wx.EVT_MENU, self.OnHideFoldingMargin, id=ID_HIDEFOLDINGMARGIN)
        
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_NEW)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_OPEN)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_OPENSHELL)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_REVERT)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_CLOSE)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_SAVE)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_SAVEAS)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_NAMESPACE)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_PRINT)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_UNDO)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_REDO)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_CUT)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_COPY)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_PASTE)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_PASTE_PLUS)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_CLEAR)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_SELECTALL)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_EMPTYBUFFER)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_AUTOCOMP_SHOW)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_AUTOCOMP_MAGIC)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_AUTOCOMP_SINGLE)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_AUTOCOMP_DOUBLE)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_CALLTIPS_SHOW)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_CALLTIPS_INSERT)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_WRAP)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_SHOW_LINENUMBERS)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_ENABLESHELLMODE)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_ENABLEAUTOSYMPY)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_AUTO_SAVESETTINGS)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_SAVESETTINGS)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_DELSETTINGSFILE)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_EXECSTARTUPSCRIPT)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_SHOWPYSLICESTUTORIAL)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_SAVEHISTORY)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_SAVEHISTORYNOW)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_CLEARHISTORY)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_EDITSTARTUPSCRIPT)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_FIND)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_FINDNEXT)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_FINDPREVIOUS)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_SHOWTOOLS)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_HIDEFOLDINGMARGIN)
        
        self.Bind(wx.EVT_ACTIVATE, self.OnActivate)
        self.Bind(wx.EVT_FIND, self.OnFindNext)
        self.Bind(wx.EVT_FIND_NEXT, self.OnFindNext)
        self.Bind(wx.EVT_FIND_CLOSE, self.OnFindClose)
        
    
    def OnClose(self, event):
        self.Destroy()

    def OnShowLineNumbers(self, event):
        win = wx.Window.FindFocus()
        if hasattr(win, 'lineNumbers'):
            pdb.set_trace()
            win.lineNumbers = event.IsChecked()
            win.setDisplayLineNumbers(win.lineNumbers)

    def OnToggleMaximize(self, event):
        self.Maximize(not self.IsMaximized())

    def OnFileNew(self, event):
        self.bufferNew()

    def OnFileOpen(self, event):
        #pdb.set_trace()
        self.bufferOpen()

    def OnShellOpen(self, event):
        self.shellOpen()

    def OnFileClose(self, event):
        #pdb.set_trace()
        self.bufferClose()

    def OnFileSave(self, event):
        self.bufferSave()

    def OnFileSaveAs(self, event):
        self.bufferSaveAs()

#    def OnFileUpdateNamespace(self, event):
#        self.updateNamespace()

    def OnExit(self, event):
        self.Close(False)

    def OnUndo(self, event):
        win = wx.Window.FindFocus()
        win.Undo()

    def OnRedo(self, event):
        win = wx.Window.FindFocus()
        win.Redo()

    def OnCut(self, event):
        win = wx.Window.FindFocus()
        win.Cut()

    def OnCopy(self, event):
        win = wx.Window.FindFocus()
        win.Copy()

    def OnPaste(self, event):
        win = wx.Window.FindFocus()
        win.Paste()

    def OnClear(self, event):
        win = wx.Window.FindFocus()
        win.Clear()
    
    def OnEmptyBuffer(self, event):
        win = wx.Window.FindFocus()
        d = wx.MessageDialog(self,
                             "Are you sure you want to clear the edit buffer,\n"
                             "deleting all the text?",
                             "Empty Buffer", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        answer = d.ShowModal()
        d.Destroy()
        if (answer == wx.ID_OK):
            win.ClearAll()
            if hasattr(win,'prompt'):
                win.prompt()

    def OnSelectAll(self, event):
        win = wx.Window.FindFocus()
        win.SelectAll()

    def OnAbout(self, event):
        """Display an About window."""
        title = 'About'
        text = 'Editor of Phoenixx.'
        dialog = wx.MessageDialog(self, text, title,
                                  wx.OK | wx.ICON_INFORMATION)
        dialog.ShowModal()
        dialog.Destroy()

    def OnHelp(self, event):
        """Display a Help window."""
        title = 'Help'        
        text = "Type 'shell.help()' in the shell window."
        dialog = wx.MessageDialog(self, text, title,
                                  wx.OK | wx.ICON_INFORMATION)
        dialog.ShowModal()
        dialog.Destroy()

    def OnAutoCompleteShow(self, event):
        win = wx.Window.FindFocus()
        win.autoComplete = event.IsChecked()

    def OnAutoCompleteMagic(self, event):
        win = wx.Window.FindFocus()
        win.autoCompleteIncludeMagic = event.IsChecked()

    def OnAutoCompleteSingle(self, event):
        win = wx.Window.FindFocus()
        win.autoCompleteIncludeSingle = event.IsChecked()

    def OnAutoCompleteDouble(self, event):
        win = wx.Window.FindFocus()
        win.autoCompleteIncludeDouble = event.IsChecked()

    def OnCallTipsShow(self, event):
        win = wx.Window.FindFocus()
        win.autoCallTip = event.IsChecked()

    def OnCallTipsInsert(self, event):
        win = wx.Window.FindFocus()
        win.callTipInsert = event.IsChecked()

    def OnWrap(self, event):
        win = wx.Window.FindFocus()
        win.SetWrapMode(event.IsChecked())
        wx.FutureCall(1, self.shell.EnsureCaretVisible)

    def OnSaveHistory(self, event):
        self.autoSaveHistory = event.IsChecked()

    def OnSaveHistoryNow(self, event):
        self.SaveHistory()

    def OnClearHistory(self, event):
        self.shell.clearHistory()

    def OnEnableShellMode(self, event):
        self.enableShellMode = event.IsChecked()
    
    def OnEnableAutoSympy(self, event):
        self.enableAutoSympy = event.IsChecked()
    
    def OnHideFoldingMargin(self, event):
        self.hideFoldingMargin = event.IsChecked()
    
    def OnAutoSaveSettings(self, event):
        self.autoSaveSettings = event.IsChecked()

    def OnSaveSettings(self, event):
        self.DoSaveSettings()

    def OnDelSettingsFile(self, event):
        if self.config is not None:
            d = wx.MessageDialog(
                self, "Do you want to revert to the default settings?\n" + 
                "A restart is needed for the change to take effect",
                "Warning", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
            answer = d.ShowModal()
            d.Destroy()
            if (answer == wx.ID_OK):
                self.config.DeleteAll()
                self.LoadSettings()


#    def OnEditStartupScript(self, event):
#        if hasattr(self, 'EditStartupScript'):
#            self.EditStartupScript()
#            
#    def OnExecStartupScript(self, event):
#        self.execStartupScript = event.IsChecked()
#        self.SaveSettings(force=True)
#    
#    def OnShowPySlicesTutorial(self,event):
#        self.showPySlicesTutorial = event.IsChecked()
#        self.SaveSettings(force=True)

    def OnFindText(self, event):
        if self.findDlg is not None:
            return
        win = wx.Window.FindFocus()
        if self.shellName == 'PyCrust':
            self.findDlg = wx.FindReplaceDialog(win, self.findData,
                                               "Find",wx.FR_NOWHOLEWORD)
        else:
            self.findDlg = wx.FindReplaceDialog(win, self.findData,
                "Find & Replace", wx.FR_NOWHOLEWORD|wx.FR_REPLACEDIALOG)
        self.findDlg.Show()
        
    def OnFindNext(self, event,backward=False):
        if backward and (self.findData.GetFlags() & wx.FR_DOWN):
            self.findData.SetFlags( self.findData.GetFlags() ^ wx.FR_DOWN )
        elif not backward and not (self.findData.GetFlags() & wx.FR_DOWN):
            self.findData.SetFlags( self.findData.GetFlags() ^ wx.FR_DOWN )
        
        if not self.findData.GetFindString():
            self.OnFindText(event)
            return
        if isinstance(event, wx.FindDialogEvent):
            win = self.findDlg.GetParent()
        else:
            win = wx.Window.FindFocus()
        win.editor.window.DoFindNext(self.findData, self.findDlg)
        if self.findDlg is not None:
            self.OnFindClose(None)

    def OnFindPrevious(self, event):
        self.OnFindNext(event,backward=True)
    
    def OnFindClose(self, event):
        self.findDlg.Destroy()
        self.findDlg = None
    
    def OnToggleTools(self, event):
        self.ToggleTools()
        

    def OnUpdateMenu(self, event):
        """Update menu items based on current status and context."""
        win = wx.Window.FindFocus()
        id = event.GetId()
        event.Enable(True)
        try:
            if id == ID_NEW:
                event.Enable(hasattr(self, 'bufferNew'))
            elif id == ID_OPEN:
                event.Enable(hasattr(self, 'bufferOpen'))
            elif id == ID_OPENSHELL:
                event.Enable(hasattr(self, 'shellOpen'))
#            elif id == ID_REVERT:
#                event.Enable(hasattr(self, 'bufferRevert')
#                             and self.hasBuffer())
            elif id == ID_CLOSE:
                event.Enable(hasattr(self, 'bufferClose')
                             and self.hasBuffer())
            elif id == ID_SAVE:
                event.Enable(hasattr(self, 'bufferSave')
                             and self.bufferHasChanged())
            elif id == ID_SAVEAS:
                event.Enable(hasattr(self, 'bufferSaveAs')
                             and self.hasBuffer())
#            elif id == ID_SAVEACOPY:
#                event.Enable(hasattr(self, 'bufferSaveACopy')
#                             and self.hasBuffer())
#            elif id == ID_NAMESPACE:
#                event.Enable(hasattr(self, 'updateNamespace')
#                             and self.hasBuffer())
#            elif id == ID_PRINT:
#                event.Enable(hasattr(self, 'bufferPrint')
#                             and self.hasBuffer())
            elif id == ID_UNDO:
                event.Enable(win.CanUndo())
            elif id == ID_REDO:
                event.Enable(win.CanRedo())
            elif id == ID_CUT:
                event.Enable(win.CanCut())
            elif id == ID_COPY:
                event.Enable(win.CanCopy())
            elif id == ID_PASTE:
                event.Enable(win.CanPaste())
            elif id == ID_CLEAR:
                event.Enable(win.CanCut())
            elif id == ID_SELECTALL:
                event.Enable(hasattr(win, 'SelectAll'))
            elif id == ID_EMPTYBUFFER:
                event.Enable(hasattr(win, 'ClearAll') and not win.GetReadOnly())
            elif id == ID_AUTOCOMP_SHOW:
                event.Check(win.autoComplete)
            elif id == ID_AUTOCOMP_MAGIC:
                event.Check(win.autoCompleteIncludeMagic)
            elif id == ID_AUTOCOMP_SINGLE:
                event.Check(win.autoCompleteIncludeSingle)
            elif id == ID_AUTOCOMP_DOUBLE:
                event.Check(win.autoCompleteIncludeDouble)
            elif id == ID_CALLTIPS_SHOW:
                event.Check(win.autoCallTip)
            elif id == ID_CALLTIPS_INSERT:
                event.Check(win.callTipInsert)
            elif id == ID_WRAP:
                event.Check(win.GetWrapMode())

            elif id == ID_SHOW_LINENUMBERS:
                event.Check(win.lineNumbers)
            elif id == ID_ENABLESHELLMODE:
                event.Check(self.enableShellMode)
                event.Enable(self.config is not None)
            elif id == ID_ENABLEAUTOSYMPY:
                event.Check(self.enableAutoSympy)
                event.Enable(self.config is not None)
            elif id == ID_AUTO_SAVESETTINGS:
                event.Check(self.autoSaveSettings)
                event.Enable(self.config is not None)
            elif id == ID_SAVESETTINGS:
                event.Enable(self.config is not None and
                             hasattr(self, 'DoSaveSettings'))
            elif id == ID_DELSETTINGSFILE:
                event.Enable(self.config is not None)
                
            elif id == ID_EXECSTARTUPSCRIPT:
                event.Check(self.execStartupScript)
                event.Enable(self.config is not None)
            
            elif id == ID_SHOWPYSLICESTUTORIAL:
                event.Check(self.showPySlicesTutorial)
                event.Enable(self.config is not None)

            elif id == ID_SAVEHISTORY:
                event.Check(self.autoSaveHistory)
                event.Enable(self.dataDir is not None)
            elif id == ID_SAVEHISTORYNOW:
                event.Enable(self.dataDir is not None and
                             hasattr(self, 'SaveHistory'))
            elif id == ID_CLEARHISTORY:
                event.Enable(self.dataDir is not None)
                
            elif id == ID_EDITSTARTUPSCRIPT:
                event.Enable(hasattr(self, 'EditStartupScript'))
                event.Enable(self.dataDir is not None)
                
            elif id == ID_FIND:
                event.Enable(hasattr(win, 'DoFindNext'))
            elif id == ID_FINDNEXT:
                event.Enable(hasattr(win, 'DoFindNext'))
            elif id == ID_FINDPREVIOUS:
                event.Enable(hasattr(win, 'DoFindNext'))

            elif id == ID_SHOWTOOLS:
                event.Check(self.ToolsShown())
            
            elif id == ID_HIDEFOLDINGMARGIN:
                event.Check(self.hideFoldingMargin)
                event.Enable(self.config is not None)
            
            else:
                event.Enable(False)
        except AttributeError:
            # This menu option is not supported in the current context.
            event.Enable(False)


    def OnActivate(self, event):
        if not event.GetActive():
            # If autocomplete active, cancel it.  Otherwise, the
            # autocomplete list will stay visible on top of the
            # z-order after switching to another application
            win = wx.Window.FindFocus()
            if hasattr(win, 'AutoCompActive') and win.AutoCompActive():
                win.AutoCompCancel()
        event.Skip()

class pStatusBar(wx.StatusBar):
    def __init__(self,parent):
        wx.StatusBar.__init__(self,parent, -1)
        self.SetFieldsCount(2)
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000)
        self.Notify()

    # Handles events from the timer we started in __init__().
    # We're using it to drive a 'clock' in field 2 (the third field).
    def Notify(self):
        t = time.localtime(time.time())
        st = time.strftime("%d-%b-%Y   %I:%M:%S", t)
        self.SetStatusText(st, 0)

ID_NEW = wx.ID_NEW
ID_OPEN = wx.ID_OPEN
ID_OPENSHELL = wx.NewId()
ID_REVERT = wx.ID_REVERT
ID_CLOSE = wx.ID_CLOSE
ID_SAVE = wx.ID_SAVE
ID_SAVEAS = wx.ID_SAVEAS
ID_PRINT = wx.ID_PRINT
ID_EXIT = wx.ID_EXIT
ID_UNDO = wx.ID_UNDO
ID_REDO = wx.ID_REDO
ID_CUT = wx.ID_CUT
ID_COPY = wx.ID_COPY
ID_PASTE = wx.ID_PASTE
ID_CLEAR = wx.ID_CLEAR
ID_SELECTALL = wx.ID_SELECTALL
ID_EMPTYBUFFER = wx.NewId()
ID_ABOUT = wx.ID_ABOUT
ID_HELP = wx.NewId()
ID_AUTOCOMP = wx.NewId()
ID_AUTOCOMP_SHOW = wx.NewId()
ID_AUTOCOMP_MAGIC = wx.NewId()
ID_AUTOCOMP_SINGLE = wx.NewId()
ID_AUTOCOMP_DOUBLE = wx.NewId()
ID_CALLTIPS = wx.NewId()
ID_CALLTIPS_SHOW = wx.NewId()
ID_CALLTIPS_INSERT = wx.NewId()
ID_COPY_PLUS = wx.NewId()
ID_NAMESPACE = wx.NewId()
ID_PASTE_PLUS = wx.NewId()
ID_WRAP = wx.NewId()
ID_TOGGLE_MAXIMIZE = wx.NewId()
ID_SHOW_LINENUMBERS = wx.NewId()
ID_ENABLESHELLMODE = wx.NewId()
ID_ENABLEAUTOSYMPY = wx.NewId()
ID_AUTO_SAVESETTINGS = wx.NewId()
ID_SAVEACOPY = wx.NewId()
ID_SAVEHISTORY = wx.NewId()
ID_SAVEHISTORYNOW = wx.NewId()
ID_CLEARHISTORY = wx.NewId()
ID_SAVESETTINGS = wx.NewId()
ID_DELSETTINGSFILE = wx.NewId()
ID_EDITSTARTUPSCRIPT = wx.NewId()
ID_EXECSTARTUPSCRIPT = wx.NewId()
ID_SHOWPYSLICESTUTORIAL = wx.NewId()
ID_STARTUP = wx.NewId()
ID_SETTINGS = wx.NewId()
ID_FIND = wx.ID_FIND
ID_FINDNEXT = wx.NewId()
ID_FINDPREVIOUS = wx.NewId()
ID_SHOWTOOLS = wx.NewId()
ID_HIDEFOLDINGMARGIN = wx.NewId()
ID_TB_NEW = wx.NewId()
ID_TB_OPEN = wx.NewId()
ID_TB_ClOSE = wx.NewId()
ID_TB_SAVE = wx.NewId()
ID_TB_SAVE_AS= wx.NewId()
ID_TB_COPY = wx.NewId()
ID_TB_CUT = wx.NewId()
ID_TB_PASTE = wx.NewId()
ID_TB_UNDO = wx.NewId()
ID_TB_REDO = wx.NewId()
