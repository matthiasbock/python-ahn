# -*- coding: cp1252 -*-
"""exporte les medias comme ancestrologie.
cf http://perso.club-internet.fr/sypey/expimages.htm

GPL Copyright (C) 2004  Loïc Fejoz
"""
import InlineMediaOption

def media2gedcom(self,media,level=0,withId=True):
    w = self.writeGedLine
    if self.mediaDir:
        mediaDir = self.mediaDir
    else:
        mediaDir = media.directory
    if withId:
        w(level, u"PICT", xrefId=u"@%dM@" % media.id)
    else:
        w(level,u'PICT')
    w(level+1,u"PATH", u"%s%s" % (mediaDir,media.fileName))
    w(level+1,u"XTYPE", u"P")
    w(level+1,u"XIDEN", u"0")
    w(level+1,u"XMODE", u"0")
    if media.year:
        w(level+1,u"DATE", "%d" % media.year)
    self.note2gedcom(media.comment,level+1)
    # the change date
    self.changeDate2gedcom(media,level+1)

def setOption(aTranslator):
    InlineMediaOption.setOption(aTranslator)
    aTranslator.media2gedcom = media2gedcom
