# -*- coding: latin1 -*-
u"""GPL Copyright (C) 2004  Loïc Fejoz"""
import HeredisFileMemory
import SaveAsHeredis

__version__ = "0.0"

def open(fileName=None, openedFile=None):
    return HeredisFileMemory.open(fileName=fileName, openedFile=openedFile)

def save(heredisFile, fileName):
    f = file(fileName, 'wb')
    SaveAsHeredis.save(heredisFile, f)
    f.close()
