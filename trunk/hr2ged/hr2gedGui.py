#!/usr/bin/python
# -*- coding: cp1252 -*-
"""GPL Copyright (C) 2004  Loic Fejoz"""
import wx
import wx.xrc
import MiscWx
import threading

import encodings
import encodings.latin_1
import encodings.ascii
import encodings.utf_16
import encodings.utf_8
import encodings.cp437
import encodings.cp1252
import encodings.cp850

import hr2ged
import sys
import LogService

class MyOutput:
    def __init__(self,txtCtrl):
        self.txtCtrl = txtCtrl
        txtCtrl.SetValue('')

    def write(self,line):
        self.txtCtrl.AppendText(line)

    def flush(self):
        pass

class hr2gedApp(wx.PySimpleApp):
    noteTypes = ['rtf',
                'html',
                'txt']
    
    charCodes = ['CP1252',
                'ASCII',
                'UTF16',
                'UTF8',
                'DOS']

    mediaExports = ['STANDARD',
                    'INLINE',
                    'EVENT',
                    'ANCESTROLOGIE']
                    
    assoExports = ['STANDARD',
                    'INDI']
    
    def __init__(self,RESFILE):
        wx.PySimpleApp.__init__(self)
        wx.InitAllImageHandlers()
        self._gedcomFileName = None
        res = wx.xrc.XmlResource(RESFILE)
        assert res != None
        print res
        self.frame = res.LoadFrame(None,'HEREDIS2GEDCOM_FRAME')
        assert self.frame != None
        for attr in dir(self.frame):
            print attr
        print self.frame.GetId()
        self.setObjects(self.frame)
        pseudoFile = MyOutput(self.output)
        LogService.setLogFile(pseudoFile,'%(message)s','Heredis')
        LogService.setLogFile(pseudoFile,'%(message)s','hr2ged')
        self.setHelpText()
        self.SetTopWindow(self.frame)
        self.frame.Show()         
        self.MainLoop()

    def setObjects(self,frame):
        wx.EVT_BUTTON(frame,wx.xrc.XRCID('QUIT_BUTTON'),self.onQuit)
        wx.EVT_BUTTON(frame,wx.xrc.XRCID('GO_BUTTON'),self.onGo)
        wx.EVT_BUTTON(frame,wx.xrc.XRCID('MEDIA_BUTTON'),self.onMediaButton)
        wx.EVT_BUTTON(frame,wx.xrc.XRCID('HEREDIS_BUTTON'),self.onHeredisButton)
        wx.EVT_BUTTON(frame,wx.xrc.XRCID('GEDCOM_BUTTON'),self.onGedcomButton)
        wx.EVT_BUTTON(frame,wx.xrc.XRCID('SEE_BUTTON'),self.onSeeButton)
        self.output = MiscWx.getObject(frame,wx.xrc.XRCID('OUTPUT'))
        self.indent = MiscWx.getObject(frame,wx.xrc.XRCID('INDENT'))
        self.private = MiscWx.getObject(frame,wx.xrc.XRCID('PRIVATE'))
        self.charcode = MiscWx.getObject(frame,wx.xrc.XRCID('CHARCODE'))
        self.notetype = MiscWx.getObject(frame,wx.xrc.XRCID('NOTETYPE'))
        self.media = MiscWx.getObject(frame,wx.xrc.XRCID('MEDIA_DIRECTORY'))
        self.heredis = MiscWx.getObject(frame,wx.xrc.XRCID('HEREDIS_FILENAME'))
        self.gedcom = MiscWx.getObject(frame,wx.xrc.XRCID('GEDCOM_FILENAME'))
        self.mediaExport = MiscWx.getObject(frame,wx.xrc.XRCID('MEDIAEXPORT'))
        self.assoExport = MiscWx.getObject(frame,wx.xrc.XRCID('ASSOEXPORT'))
        self.gregorian = MiscWx.getObject(frame,wx.xrc.XRCID('CALENDARDATE'))
        self.changeDate = MiscWx.getObject(frame,wx.xrc.XRCID('CHANGEDATE'))
        

    def setHelpText(self):
        for line in file('help.txt','r'):
            self.output.AppendText(line)

    def onSeeButton(self,event):
        import os
        gedcom = self._gedcomFileName or self.gedcom.GetValue() or ""
        cmd = os.getenv("EDITOR")
        if cmd:
            cmd += " "
        else:
            cmd = ""
        os.system(cmd + ('"%s"' % gedcom))

    def onMediaButton(self,event):
        for dir in MiscWx.dirDialog(self.frame,self.media.GetValue()):
            self.media.SetValue(dir)

    def onHeredisButton(self,event):
        for fileName in MiscWx.fileDialog(self.frame,
                                          "Choisissez un fichier heredis",
                                          self.heredis.GetValue(),
                                          "*.h?*"):
            self.heredis.SetValue(fileName)

    def onGedcomButton(self,event):
        for fileName in MiscWx.fileDialog(self.frame,
                                          "Choisissez un fichier gedcom",
                                          self.gedcom.GetValue(),
                                          "*.ged"):
            self.gedcom.SetValue(fileName)

    def onQuit(self,event=None):
        self.frame.Close()

    def onGo(self,event):
        # on doit forcement choisir un fichier gedcom
        if self.heredis.GetValue():
            def myGo(self=self):       
                options = hr2ged.hr2gedOption()
                options.filename = self.gedcom.GetValue() or None
                options.mediaDir = self.media.GetValue() or None
                options.noteType = self.noteTypes[self.notetype.GetSelection()]
                options.indent = self.indent.IsChecked()
                options.private = self.private.IsChecked()
                options.charCode = self.charCodes[self.charcode.GetSelection()]
                options.mediaExport = self.mediaExports[self.mediaExport.GetSelection()]
                options.assoExport = self.assoExports[self.assoExport.GetSelection()]
                options.gregorian = not self.gregorian.IsChecked()
                options.changeDate = self.changeDate.IsChecked()
                self._gedcomFileName = hr2ged.doIt(self.heredis.GetValue(),options)

            myGo(self)
            # why does it not work under linux ? 
            #t1 = threading.Thread(target=myGo,args=(self,))
            #t1.start()
        else:
            dlg = wx.wxMessageDialog(self.frame,
                                              message="Vous devez choisir un fichier Gedcom !",
                                              caption="Erreur",
                                              style=wx.wxICON_ERROR)
            if dlg.ShowModal() == wx.wxID_OK:
                pass
            dlg.Destroy()
        

if __name__ == "__main__":
    # Import Psyco if available
    try:
        import psyco
        psyco.full()
    except ImportError:
        print "psyco unavailable"
    LogService.setLogFileName('hr2gedGui.log')
    app = hr2gedApp('gui.xrc')
