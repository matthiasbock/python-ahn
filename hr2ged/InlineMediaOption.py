"""Exporte les medias en place, ie sans utiliser les pointeurs

GPL Copyright (C) 2004  Loïc Fejoz
"""

def exportMedias(self):
    pass

def mediaLink2gedcom(self,mediaLink,level=0):
    self.media2gedcom(mediaLink.media,level,False)

def setOption(aClass):
    aClass.mediaLink2gedcom = mediaLink2gedcom
    aClass.exportMedias = exportMedias
