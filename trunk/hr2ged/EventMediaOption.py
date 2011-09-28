"""exporte les medias dans un evenement.

GPL Copyright (C) 2004  Loïc Fejoz
"""
def exportMedias(self):
    pass

def mediaLink2gedcom(self,mediaLink,level=0):
    w = self.writeGedLine
    w(level, u'EVEN')
    w(level+1, u'TYPE", u"IMAGE')
    self.media2gedcom(mediaLink.media,level+1,False)

def setOption(aTranslator):
    aTranslator.exportMedias = exportMedias
    aTranslator.mediaLink2gedcom = mediaLink2gedcom
