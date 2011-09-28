# -*- coding: latin1 -*-

import Item

class Link(Item.Item):
    linkTypes = {1:u'A�eul(e) -> Descendant(e)',
                 2:u'Ami(e) -> Ami(e)',
                 3:u'Beau-fr�re/Belle-soeur -> Beau-fr�re/Belle-soeur',
                 4:u'Beau-p�re/Belle-m�re -> Gendre/Bru',
                 5:u'Lien consanguin',
                 6:u'Cousin/Cousine -> Cousin/Cousine',
                 7:u'Doublon ? -> Doublon ?',
                 8:u'Fr�re/Soeur -> Fr�re/Soeur',
                 9:u'Jumeau/Jumelle -> Jumeau/Jumelle',
                 10:u'Testateur/Testatrice -> H�ritier/H�riti�re',
                 11:u'Oncle/Tante -> Neveu/Ni�ce',
                 12:u'Parent(e) -> Parent(e)',
                 13:u'A reconnu -> Reconnu par',
                 14:u'Tuteur/Tutrice -> Sous tutelle',
                 15:u'Autre Lien',
                 #16
                 17:u'D�clarant',
                 18:u"Officier d'�tat civil",
                 19:u'Officiant Religieux',
                 20:u'Parrain/Marraine',
                 21:u'Pr�sent(e)',
                 22:u'T�moin',
                 23:u'Autre Lien'}

    id = None
    creationDate = 0
    modificationDate = 0
    fromItemID = None
    toItemID = None
    note = u''
    typeIndex = 15

    def getType(self):
        return self.linkTypes.get(self.typeIndex,str(self.typeIndex))

    type = property(getType)
