import wx
import os.path

def getObject(parent,id):
    for child in parent.GetChildren():
        if child.GetId() == id:
            return child
    for child in parent.GetChildren():
        obj = getObject(child,id)
        if obj:
            return obj
    return None

def dirDialog(frame,path=""):
    dlg = wx.DirDialog(frame,defaultPath=path)
    if dlg.ShowModal() == wx.ID_OK:
        dir = dlg.GetPath()
        yield dir
    dlg.Destroy()


def fileDialog(frame,
               message="Choose a file",
               fileName="",
               wildcard="*.*",
               style=0,
               pos=wx.DefaultPosition):
    dlg = wx.FileDialog(frame,message,"",fileName,wildcard,style,pos)
    if dlg.ShowModal() == wx.ID_OK:
        for path in dlg.GetPaths():
            yield path
    dlg.Destroy()
