"""exporte tous les liens au niveau individu

GPL Copyright (C) 2004  Loïc Fejoz
"""

def indiLink2gedcom(self, indi, level=0):
    for link in indi.links:
        self.link2gedcom(link,level+1)
    for evt in indi.events:
        for link in evt.links:
            self.link2gedcom(link,level+1)

def eventLink2gedcom(self, evt, level=0):
    pass

def setOption(aTranslator):
    aTranslator.indiLink2gedcom = indiLink2gedcom
    aTranslator.eventLink2gedcom = eventLink2gedcom
