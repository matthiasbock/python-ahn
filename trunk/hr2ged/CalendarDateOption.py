# -*- coding: cp1252 -*-
u"""Ne met le type du calendrier que si il est different de gregorien

GPL Copyright (C) 2004  Loïc Fejoz
"""
def getCalendarEscape(self,cal):
    if cal==0x00:
        return ''
    try:
        return self.gedcom_calendriers[cal]
    except KeyError:
        return u"@#DUNKNOWN@"

def setOption(aClass):
    aClass.getCalendarEscape = getCalendarEscape
