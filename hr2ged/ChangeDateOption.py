# -*- coding: cp1252 -*-
"""GPL Copyright (C) 2004  Loïc Fejoz"""

def changeDate2gedcom(self,obj,level=0):
    if level == 1:
        self.oldChangeDate2Gedcom(obj,level)

def setOption(translator):
    translator.oldChangeDate2Gedcom = translator.changeDate2gedcom
    translator.changeDate2gedcom = changeDate2gedcom
