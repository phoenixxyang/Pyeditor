import wx
from wx import stc

import keyword
import os
import sys
import time

from wx.py import dispatcher


if 'wxMSW' in wx.PlatformInfo:
    FACES = { 'times'     : 'Times New Roman',
              'mono'      : 'Courier New',
              'helv'      : 'Arial',
              'lucida'    : 'Lucida Console',
              'other'     : 'Comic Sans MS',
              'size'      : 10,
              'lnsize'    : 8,
              'backcol'   : '#FFFFFF',
              'calltipbg' : '#FFFFB8',
              'calltipfg' : '#404040',
            }

elif 'wxGTK' in wx.PlatformInfo and 'gtk2' in wx.PlatformInfo:
    FACES = { 'times'     : 'Serif',
              'mono'      : 'Monospace',
              'helv'      : 'Sans',
              'other'     : 'new century schoolbook',
              'size'      : 10,
              'lnsize'    : 9,
              'backcol'   : '#FFFFFF',
              'calltipbg' : '#FFFFB8',
              'calltipfg' : '#404040',
            }

elif 'wxMac' in wx.PlatformInfo:
#    FACES = { 'times': 'Times New Roman',
#              'mono' : 'Monaco',
#              'helv' : 'Arial',
#              'other': 'Comic Sans MS',
    FACES = { 'times'     : 'Lucida Grande',
              'mono'      : 'Monaco',
              'helv'      : 'Geneva',
              'other'     : 'new century schoolbook',
              'size'      : 12,
              'lnsize'    : 10,
              'backcol'   : '#FFFFFF',
              'calltipbg' : '#FFFFB8',
              'calltipfg' : '#404040',
            }

else: # GTK1, etc.
    FACES = { 'times'     : 'Times',
              'mono'      : 'Courier',
              'helv'      : 'Helvetica',
              'other'     : 'new century schoolbook',
              'size'      : 12,
              'lnsize'    : 10,
              'backcol'   : '#FFFFFF',
              'calltipbg' : '#FFFFB8',
              'calltipfg' : '#404040',
            }


class PSTC(stc.StyledTextCtrl):
    """PSTC based on StyledTextCtrl."""


    def __init__(self, parent, id=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.CLIP_CHILDREN | wx.SUNKEN_BORDER):
        stc.StyledTextCtrl.__init__(self, parent, id, pos, size, style)
        import __main__
        locals = __main__.__dict__
        self.__config()
        stc.EVT_STC_UPDATEUI(self, id, self.OnUpdateUI)
        dispatcher.connect(receiver=self._fontsizer, signal='FontIncrease')
        dispatcher.connect(receiver=self._fontsizer, signal='FontDecrease')
        dispatcher.connect(receiver=self._fontsizer, signal='FontDefault')
        self.Bind(stc.EVT_STC_MARGINCLICK, self.OnMarginClick)


    def _fontsizer(self, signal):
        """Receiver for Font* signals."""
        size = self.GetZoom()
        if signal == 'FontIncrease':
            size += 1
        elif signal == 'FontDecrease':
            size -= 1
        elif signal == 'FontDefault':
            size = 0
        self.SetZoom(size)


    def __config(self):
        
        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, ' '.join(keyword.kwlist))

        self.setDisplayLineNumbers(True)
        self.setStyles(FACES)
        self.SetViewWhiteSpace(False)
        self.SetTabWidth(8)
        self.SetUseTabs(True)
        self.SetTabIndents(True)
        # Do we want to automatically pop up command completion options?
        self.autoComplete = True
        self.autoCompleteIncludeMagic = True
        self.autoCompleteIncludeSingle = True
        self.autoCompleteIncludeDouble = True
        self.autoCompleteCaseInsensitive = True
        self.AutoCompSetIgnoreCase(self.autoCompleteCaseInsensitive)
        self.autoCompleteAutoHide = False
        self.AutoCompSetAutoHide(self.autoCompleteAutoHide)
        self.AutoCompStops(' .,;:([)]}\'"\\<>%^&+-=*/|`')
        # Do we want to automatically pop up command argument help?
        self.autoCallTip = True
        self.callTipInsert = True
        self.CallTipSetBackground(FACES['calltipbg'])
        self.CallTipSetForeground(FACES['calltipfg'])
        self.SetWrapMode(False)
        try:
            self.SetEndAtLastLine(False)
        except AttributeError:
            pass

    def setDisplayLineNumbers(self, state):
       # import pdb
       # pdb.set_trace()
        self.lineNumbers = state
        if state:
            self.SetMargins(0,0)
            self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
            self.SetMarginWidth(1, 25)
            self.SetMarginWidth(2, 15)
            self.SetProperty("fold", "1")
            self.SetProperty("tab.timmy.whinge.level", "1")
            #self.SetProperty("fold.comment.python", "1")
            self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
            self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
            self.SetMarginSensitive(2, True)
            #self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_CIRCLEMINUS,          "white", "#404040")
            #self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_CIRCLEPLUS,           "white", "#404040")
            #self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,                "white", "#404040")
            #self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNERCURVE,         "white", "#404040")
            #self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_CIRCLEPLUSCONNECTED,  "white", "#404040")
            #self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "#404040")
            #self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNERCURVE,         "white", "#404040")
            #another style of margin folder markers
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_BOXMINUS,          "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_BOXPLUS,           "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,             "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNER,           "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_BOXPLUSCONNECTED,  "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER,           "white", "#808080")
        else:
            # Leave a small margin so the feature hidden lines marker can be seen
            self.SetMarginType(1, 0)
            self.SetMarginWidth(1, 10)
        
    def setStyles(self, faces):
        """Configure font size, typeface and color for lexer."""

#        # Default style
#        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,
#                          "face:%(mono)s,size:%(size)d,back:%(backcol)s" % \
#                          faces)
#
#        self.StyleClearAll()
#        self.SetSelForeground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
#        self.SetSelBackground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
#       
#       # Built in styles
#        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,
#                          "back:#C0C0C0,face:%(mono)s,size:%(lnsize)d" % FACES)
#        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR,
#                          "face:%(mono)s" % faces)
#        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,
#                          "fore:#0000FF,back:#FFFF88")
#        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,
#                          "fore:#FF0000,back:#FFFF88")
#
#       # Python styles
#        self.StyleSetSpec(stc.STC_P_DEFAULT,
#                          "face:%(mono)s" % faces)
#        self.StyleSetSpec(stc.STC_P_COMMENTLINE,
#                          "fore:#007F00,face:%(mono)s" % faces)
#        self.StyleSetSpec(stc.STC_P_NUMBER,
#                          "")
#        self.StyleSetSpec(stc.STC_P_STRING,
#                          "fore:#7F007F,face:%(mono)s" % faces)
#        self.StyleSetSpec(stc.STC_P_CHARACTER,
#                          "fore:#7F007F,face:%(mono)s" % faces)
#        self.StyleSetSpec(stc.STC_P_WORD,
#                          "fore:#00007F,bold")
#        self.StyleSetSpec(stc.STC_P_TRIPLE,
#                          "fore:#7F0000")
#        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE,
#                          "fore:#000033,back:#FFFFE8")
#        self.StyleSetSpec(stc.STC_P_CLASSNAME,
#                          "fore:#0000FF,bold")
#        self.StyleSetSpec(stc.STC_P_DEFNAME,
#                          "fore:#007F7F,bold")
#        self.StyleSetSpec(stc.STC_P_OPERATOR,
#                          "")
#        self.StyleSetSpec(stc.STC_P_IDENTIFIER,
#                          "")
#        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK,
#                          "fore:#7F7F7F")
#        self.StyleSetSpec(stc.STC_P_STRINGEOL,
#                          "fore:#000000,face:%(mono)s,back:#E0C0E0,eolfilled" % faces)

        # Default style
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(mono)s,size:%(size)d" % faces)
        self.StyleClearAll()  # Reset all to be like the default

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(mono)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,
                          "back:#C0C0C0,face:%(mono)s,size:%(lnsize)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")

       # Python styles
        # Default 
        self.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000,face:%(mono)s,size:%(size)d" % faces)
        # Comments
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
        # Number
        self.StyleSetSpec(stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % faces)
        # String
        self.StyleSetSpec(stc.STC_P_STRING, "fore:#7F007F,face:%(mono)s,size:%(size)d" % faces)
        # Single quoted string
        self.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#7F007F,face:%(mono)s,size:%(size)d" % faces)
        # Keyword
        self.StyleSetSpec(stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % faces)
        # Triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % faces)
        # Triple double quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % faces)
        # Class name definition
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % faces)
        # Function or method name definition
        self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces)
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)
        # Identifiers
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(mono)s,size:%(size)d" % faces)
        # Comment-blocks
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % faces)
        # End of line where string is not closed
        self.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)

    def OnUpdateUI(self, event):
        """Check for matching braces."""
        # If the auto-complete window is up let it do its thing.
        if self.AutoCompActive() or self.CallTipActive():
            return
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()
        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)

        # Check before.
        if charBefore and chr(charBefore) in '[]{}()' \
        and styleBefore == stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1

        # Check after.
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)
            if charAfter and chr(charAfter) in '[]{}()' \
            and styleAfter == stc.STC_P_OPERATOR:
                braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)

        if braceAtCaret != -1  and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)

    def CanCopy(self):
        """Return True if text is selected and can be copied."""
        return self.GetSelectionStart() != self.GetSelectionEnd()

    def CanCut(self):
        """Return True if text is selected and can be cut."""
        return self.CanCopy() and self.CanEdit()

    def CanEdit(self):
        """Return True if editing should succeed."""
        return not self.GetReadOnly()

    def CanPaste(self):
        """Return True if pasting should succeed."""
        return stc.StyledTextCtrl.CanPaste(self) and self.CanEdit()


    def GetLastPosition(self):
        return self.GetLength()

    def GetRange(self, start, end):
        return self.GetTextRange(start, end)

    def GetSelection(self):
        return self.GetAnchor(), self.GetCurrentPos()

    def ShowPosition(self, pos):
        line = self.LineFromPosition(pos)
        #self.EnsureVisible(line)
        self.GotoLine(line)

    def DoFindNext(self, findData, findDlg=None):
        backward = not (findData.GetFlags() & wx.FR_DOWN)
        matchcase = (findData.GetFlags() & wx.FR_MATCHCASE) != 0
        end = self.GetLastPosition()
        # Changed to reflect the fact that StyledTextControl is in UTF-8 encoding
        textstring = self.GetRange(0, end).encode('utf-8')
        findstring = findData.GetFindString().encode('utf-8')
        if not matchcase:
            textstring = textstring.lower()
            findstring = findstring.lower()
        if backward:
            start = self.GetSelection()[0]
            loc = textstring.rfind(findstring, 0, start)
        else:
            start = self.GetSelection()[1]
            loc = textstring.find(findstring, start)

        # if it wasn't found then restart at begining
        if loc == -1 and start != 0:
            if backward:
                start = end
                loc = textstring.rfind(findstring, 0, start)
            else:
                start = 0
                loc = textstring.find(findstring, start)

        # was it still not found?
        if loc == -1:
            dlg = wx.MessageDialog(self, 'Unable to find the search text.',
                          'Not found!',
                          wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        if findDlg:
            if loc == -1:
                wx.CallAfter(findDlg.SetFocus)
                return
            else:
                findDlg.Close()

        # show and select the found text
        self.ShowPosition(loc)
        self.SetSelection(loc, loc + len(findstring))

    def OnMarginClick(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())

                if self.GetFoldLevel(lineClicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)


    def FoldAll(self):
        lineCount = self.GetLineCount()
        expanding = True

        # find out if we are folding or unfolding
        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break

        lineNum = 0

        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & stc.STC_FOLDLEVELHEADERFLAG and \
               (level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:

                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)

                    if lastChild > lineNum:
                        self.HideLines(lineNum+1, lastChild)

            lineNum = lineNum + 1



    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        lastChild = self.GetLastChild(line, level)
        line = line + 1

        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)

            if level == -1:
                level = self.GetFoldLevel(line)

            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)

                    line = self.Expand(line, doExpand, force, visLevels-1)

                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, visLevels-1)
                    else:
                        line = self.Expand(line, False, force, visLevels-1)
            else:
                line = line + 1

        return line

    def OnShowCompHistory(self):
        """Show possible autocompletion Words from already typed words."""
        
    #    #copy from history
    #    his = self.history[:]
    #    
    #    #put together in one string
    #    joined = " ".join (his)
        joined = self.GetText()
        import re

        #sort out only "good" words
        newlist = re.split("[ \.\[\]=}(\)\,0-9\"\n\t]", joined)
        
        #length > 1 (mix out "trash")
        thlist = []
        for i in newlist:
            if len (i) > 1:
                thlist.append (i)
        
        #unique (no duplicate words
        #oneliner from german python forum => unique list
        unlist = [thlist[i] for i in xrange(len(thlist)) if thlist[i] not in thlist[:i]]
            
        #sort lowercase
        unlist.sort(lambda a, b: cmp(a.lower(), b.lower()))
        
        #this is more convenient, isn't it?
        self.AutoCompSetIgnoreCase(True)
        
        #join again together in a string
        stringlist = " ".join(unlist)

        stringlist = " ".join(keyword.kwlist)
        #pos von 0 noch ausrechnen

        #how big is the offset?
        cpos = self.GetCurrentPos() - 1
        while chr (self.GetCharAt (cpos)).isalnum():
            cpos -= 1
            
        #the most important part
        self.AutoCompShow(self.GetCurrentPos() - cpos -1, stringlist)
