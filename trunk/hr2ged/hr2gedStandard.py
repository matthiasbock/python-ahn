#!/usr/bin/python
# -*- coding: cp1252 -*-
u"""
Translate an Heredis file to a standard gedcom.
Heredis(c) is a BSD CONCEPT copyright.

GPL Copyright (C) 2004  Loïc Fejoz

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

loic@fejoz.net"""

import datetime
import sys
import logging
logger = logging.getLogger('hr2ged')

try:
    import rtf.Rtf2Html
    import rtf.Rtf2Txt
except ImportError:
    logger.error("there is no rtf module.\n option for translating rtf to txt and html will be disabled")
    class DummyRtf:
        def __init__(self):
            self.Rtf2Html = self
            self.getHtml = unicode
            self.Rtf2Txt = self
            self.getTxt = unicode
    rtf = DummyRtf()


class hr2gedStandard:
    gedcom_event_type = {4:u'BIRT',
                         8:u'CHR',
                         12:u'DEAT',
                         16:u'GRAD',
                         6:u'CREM',
                         #24:u'acquisition',
                         34:u'ADOP',
                         #1:u'autre Baptême',
                         9:u'CHRA',
                         2:u'BARM',
                         3:u'BASM',
                         5:u'BLES',
                         10:u'CONF',
                         35:u'CREM',
                         #25:u'décoration',
                         13:u'EMIG',
                         #26:u'en vie',
                         20:u'PROB',
                         17:u'IMMI',
                         18:u'NATU',
                         19:u'ORDN',
                         32:u'FCOM',
                         23:u'OCCU',
                         7:u'CENS',
                         #30:u'résidence',
                         21:u'RETI',
                         #27:u'service militaire',
                         31:u'WILL',
                         33:u'TITL',
                         #28:"vente d'un bien",
                         #29:u'voyage',
                         0:u'BAPL',
                         11:u'CONL',
                         #14:u'dotation LDS',
                         #22:u'liens parental LDS',
                         61:u'MARR',
                         54:u'DIV',
                         68:u'MARR', #68:u'mariage religieux',
                         55:u'DIVF',
                         66:u'ADOP',
                         67:u'ANUL',
                         58:u'MARB',
                         59:u'MARC',
                         #60:u'certification de publication des bans',
                         64:u'RESI',
                         #57:u'évènement',
                         #15:u'évènement',
                         56:u'ENGA',
                         #65:u'séparation',
                         #63:u'lien conjugal LDS'
                         384384384:u'bidon'
                         }
    
    gedcom_date_modif = [u'0',
                         u'AFT',
                         u'BEF',
                         u'Error (between)',
                         u'ABT',
                         u'CAL',
                         u'EST',
                         u'AND']
    
    gedcom_calendriers = {0x4a:u'@#DJULIAN@',
                          0x00:u'@#DGREGORIAN@',
                          0x48:u'@#DHEBREW@',
                          0x52:u'@#FRENCH R@'}
    
    gedcom_month = [None,
                    u'JAN',
                    u'FEB',
                    u'MAR',
                    u'APR',
                    u'MAY',
                    u'JUN',
                    u'JUL',
                    u'AUG',
                    u'SEP',
                    u'OCT',
                    u'NOV',
                    u'DEC']
    
    gedcom_month_french = [None,
                           u'VEND',
                           u'BRUM',
                           u'FRIM',
                           u'NIVO',
                           u'PLUV',
                           u'VENT',
                           u'GERM',
                           u'FLOR',
                           u'PRAI',
                           u'MESS',
                           u'THER',
                           u'FRUC',
                           u'COMP']
    
    gedcom_month_hebrew = [None,
                           u'TSH',
                           u'CSH',
                           u'KSL',
                           u'TVT',
                           u'SHV',
                           u'ADR',
                           u'ADS',
                           u'NSN',
                           u'IYR',
                           u'SVN',
                           u'TMZ',
                           u'AAV',
                           u'ELL']
    
    reverseLinkTypes = {1:u'Descendant(e) --> Aïeul(e)',
                        2:u'Ami(e) -> Ami(e)',
                        3:u'Beau-frère/Belle-soeur -> Beau-frère/Belle-soeur',
                        4:u'Gendre/Bru -> Beau-père/Belle-mère',
                        5:u'Lien consanguin',
                        6:u'Cousin/Cousine -> Cousin/Cousine',
                        7:u'Doublon ? -> Doublon ?',
                        8:u'Frère/Soeur -> Frère/Soeur',
                        9:u'Jumeau/Jumelle -> Jumeau/Jumelle',
                        10:u'Héritier/Héritière -> Testateur/Testatrice',
                        11:u'Neveu/Nièce --> Oncle/Tante',
                        12:u'Parent(e) -> Parent(e)',
                        13:u'Reconnu par -> A reconnu',
                        14:u'Sous tutelle --> Tuteur/Tutrice',
                        15:u'Autre Lien',
                        #16
                        17:u'Déclarant',
                        18:u"Officier d'état civil",
                        19:u'Officiant Religieux',
                        20:u'Parrain/Marraine',
                        21:u'Présent(e)',
                        22:u'Témoin',
                        23:u'Autre Lien',
                        97:u'Parrain/Marraine'}
    
    refDate = datetime.date(1899,12,30)
    
    def __init__(self):
        self.set(None)

    def set(self,heredisFile,output=None,mediaDir=None,indent=False,noteType=None,charCode='ANSEL',private=False,stopOnError=True):
        self.delta = 255
        if output:
            self._output = output
        else:
            self._output = sys.stdout
        self.indented = indent
        self.noteType = noteType
        if mediaDir:
            if mediaDir[-1]!='\\' and mediaDir[-1]!='/':
                mediaDir =  mediaDir+"\\"
        self.mediaDir = mediaDir
        self.charCode = charCode
        self.heredisFile = heredisFile
        self.private = private
        self.stopOnError = stopOnError
    
    def heredis2gedcom(self, heredisFile, output=None, mediaDir=None, indent=False,noteType=None,charCode='ANSEL',private=False, stopOnError=True):
        self.set(heredisFile,output,mediaDir,indent,noteType,charCode,private, stopOnError)
        self.header(heredisFile)
        self.exportIndis()
        self.exportUnions()
        self.exportSources()
        self.exportMedias()
        self.writeGedLine(0,u"TRLR")

    def exportIndis(self):
        for  indi in self.heredisFile['individus'].itervalues():
            try:
                self.indi2gedcom(indi)
            except:
                logger.warn("error occur while exporting %s (%i)" % (indi.fullName, indi.id))
                if self.stopOnError:
                    raise

    def exportUnions(self):
        for union in self.heredisFile['unions'].itervalues():
            try:
                self.union2gedcom(union)
            except:
                logger.warn("error occur while exporting %s (%i)" % (union.fullName, union.id))
                if self.stopOnError:
                    raise

    def exportSources(self):
        for source in self.heredisFile['sources'].itervalues():
            self.source2gedcom(source)

    def exportMedias(self):
        for media in self.heredisFile['medias'].itervalues():
            self.media2gedcom(media)

    def header(self,heredisFile,level=0):
        w = self.writeGedLine
        w(0,u"HEAD")
        w(1,u"SOUR",u"hr2ged")
        #w(2,u"VERS " + hr2ged.__version__)
        w(2,u"CORP", u"loic fejoz")
        w(3,u"ADDR", u"http://sourceforge.net/projects/hr2ged/")
        w(3,u"ADDR", u"http://www.fejoz.net")
        w(1,u"PLAC")
        w(2,u"FORM", u"Subdivision, Town , Area code , County , Region , Country")
        w(1,u"CHAR", self.charCode)
        w(1,u"GEDC")
        w(2,u"VERS", u"5.5")


    def note2gedcom(self,note,level=0,noteTag=u'NOTE'):
        if not note:
            return
        #print type(note),note.encode('cp437','replace')
        theNote = note
        try:
            if self.noteType == 'html':
                theNote = rtf.Rtf2Html.getHtml(theNote, self.charCode)
            elif self.noteType == 'rtf':
                pass
            elif self.noteType == 'txt':
                theNote = rtf.Rtf2Txt.getTxt(theNote, self.charCode)
            else:
                pass
        except:
            logger.warn(u"Error with note:\n" + ('-' * 70) + unicode(type(note)) + "\n" + unicode(note))
            if self.stopOnError:
                raise
        w = self.writeGedLine
        lines = theNote.replace(u"\r",u"").split(u"\n")
        line = lines[0]
        w(level,noteTag ,line)
        for line in lines[1:]:
            w(level+1, u"CONT", line)

    def indi2gedcom(self,indi,level=0):
        w  = self.writeGedLine
        w(level, u"INDI", xrefId=u"@%dI@" % indi.id)
        w(level+1,u"NAME", u"%s/%s/" % (indi.name,indi.surname.name))
        if not self.private or not indi.confidentiel:
            if indi.titre:
                w(level+2, u"NPFX", u"%s" % indi.titre)
            w(level+2, u"GIVN", u"%s" % indi.name)
            w(level+2, u"SURN", u"%s" % indi.surname.name)
            if indi.surnom:
                w(level+2, u"NICK", u"%s" % indi.surnom)
            if indi.suffixe:
                w(level+2, u"NSFX", u"%s" % indi.suffixe)
            w(level+1,u"SEX", u"%s"  % indi.sex.upper())
            if indi.numero:
                w(level+1, u"REFN", u"%s" % indi.numero)
            if indi.titre:
                w(level+1, u"TITL", u"%s" % indi.titre)
            for evt in indi.events:
                self.evt2gedcom(evt,level+1)
            if indi.activity:
                w(level+1, u"OCCU", u"%s" % indi.activity)
            for union in indi.unions:
                w(level+1, u"FAMS", u"@%dU@" % union.id)
            if indi.family:
                w(level+1, u"FAMC", u"@%dU@" % indi.family.id)
            for addr in indi.addresses:
                w(level+1, u"RESI")
                self.addr2gedcom(addr,level+2)
            for linkMedia in indi.linkMedias:
                self.mediaLink2gedcom(linkMedia,level+1)
            self.indiLink2gedcom(indi, level)
            for link in indi.reverseLinks:
                self.reverseLink2gedcom(link,level+1)
            self.note2gedcom(indi.note,level+1)
            userFields = self.heredisFile.fileHeader.userFields
            for i in range(10):
                (attr,tag) = userFields[i]
                champ = indi.userFields[i]
                if champ and tag:
                    w(level+1, tag, u"%s" % champ)
                    w(level+2, u"TYPE", u"%s" % attr)
        if indi.confidentiel:
            w(level+1,u"RESN", u"privacy")
        # the change date
        self.changeDate2gedcom(indi,level+1)

    def indiLink2gedcom(self, indi, level=0):
        for link in indi.links:
            self.link2gedcom(link,level+1)

    def changeDate2gedcom(self,obj,level=0):
        w = self.writeGedLine
        if obj.modificationDate:
            d = self.refDate + datetime.timedelta(days=obj.modificationDate)
            w(level,u"CHAN")
            date = d.strftime(str('%%d %s %%Y' % self.gedcom_month[d.month])).upper()
            w(level+1,u"DATE", u"%s" % date)
##        else:
##            logger.error("%s has a null change date %d",obj,obj.modificationDate)
            
    def addr2gedcom(self,addr,level=0):
        if not self.private or not addr.private:
            w = self.writeGedLine
            w(level,u"ADDR", u"%s" % addr.contact)
            if addr.line1:
                w(level+1,u"ADR1", u"%s" % addr.line1)
            if addr.line2:
                w(level+1,u"ADR2", u"%s" % addr.line2)
            if addr.town:
                w(level+1,u"CITY", u"%s" % addr.town)
            if addr.postalCode:
                w(level+1,u"POST", u"%s" % addr.postalCode)
            if addr.region:
                w(level+1,u"STAE", u"%s" % addr.region)
            if addr.phone:
                w(level,u"PHON", u"%s" % addr.phone)
            if addr.email:
                w(level,u"EMAIL", u"%s" % addr.email)
            if addr.web:
                w(level,u"URL", u"%s" % addr.web)
            self.changeDate2gedcom(addr,level+1)

    def mediaLink2gedcom(self,mediaLink,level=0):
        w = self.writeGedLine
        w(level, u"OBJE", u"@%dM@" % mediaLink.mediaID)
        if mediaLink.mainMedia:
            w(level+1,u"NOTE", u"Media principal")
        # the change date
        self.changeDate2gedcom(mediaLink,level+1)

    def sourceLink2gedcom(self,sourceLink,level=0):
        w = self.writeGedLine
        w(level,u"SOUR", u"@%dS@" % sourceLink.sourceID)
        self.note2gedcom(sourceLink.note,level+1)
        self.changeDate2gedcom(sourceLink,level+1)
        
    def evt2gedcom(self,evt,level=0):
        w = self.writeGedLine
        try:
            type = self.gedcom_event_type[evt.type]
        except KeyError:
            type = u"EVEN"
        if type == u'OCCU':
            txt = rtf.Rtf2Txt.getTxt(evt.note, self.charCode).split('\n')[0].strip()[:70]
            if not txt:
                txt = u'Y'
            w(level, type, txt)
        else:
            w(level, type, "Y")
        w(level+1,u"TYPE", u"%s" % evt.typeName)
        date = self.event2gedcomDate(evt)
        if date:
            w(level+1,u"DATE", u"%s" % date)
        self.place2gedcom(evt.place,level+1,evt.placeSubdivision)
        if evt.findTheSource:
            w(level+1,u"NOTE", u"Acte à rechercher")
        if evt.ageOnAct:
            w(level+1,u"AGE", u"%s" % evt.ageOnAct)
        self.note2gedcom(evt.note,level+1)
        self.eventLink2gedcom(evt, level)
        for link in evt.reverseLinks:
            self.reverseLink2gedcom(link,level+1)
        for linkSource in evt.linkDocs:
            self.sourceLink2gedcom(linkSource,level+1)
        for linkMedia in evt.linkMedias:
            self.mediaLink2gedcom(linkMedia,level+1)
        # the change date
        self.changeDate2gedcom(evt,level+1)

    def eventLink2gedcom(self, evt, level=0):
        for link in evt.links:
            self.link2gedcom(link,level+1)

    def place2gedcom(self,place,level=0,subdivision=""):
        if not place:
            return
        w = self.writeGedLine
        subdiv = subdivision.replace(',','')
        w(level,u"PLAC", u"%s,%s,%s,%s,%s,%s" % (subdiv,place.town,place.code,place.department,place.region,place.country))

    def media2gedcom(self,media,level=0,withId=True):
        w = self.writeGedLine
        if self.mediaDir:
            mediaDir = self.mediaDir
        else:
            mediaDir = media.directory
        if withId:
            w(level,u"OBJE", xrefId=u"@%dM@" % media.id)
        else:
            w(level,u'OBJE')
        w(level+1,u"FILE", u"%s%s" % (mediaDir,media.fileName))
        if media.year:
            w(level+1,u"DATE", u"%d" % media.year)
        self.note2gedcom(media.comment,level+1)
        # the change date
        self.changeDate2gedcom(media,level+1)

    def source2gedcom(self,source,level=0):
        # to know the correspondance,
        # see <http://www.genealogie-standard.org/saisir/source.html#heredis>
        w = self.writeGedLine
        w(level, u"SOUR", xrefId=u"@%dS@" % source.id)
        w(level+1,u"TITL", source.document)
        w(level+1,u"REFN", source.name)
        w(level+1,u"ABBR", source.archivage)
        w(level+1,u"REPO", source.origin)
        w(level+2,u"CALN", source.cote)
        w(level+3,u"MEDI", source.nature)
        self.note2gedcom(source.note,level+1,'TEXT')
        for linkMedia in source.linkMedias:
            self.mediaLink2gedcom(linkMedia,level+1)
        # the change date
        self.changeDate2gedcom(source,level+1)

    def union2gedcom(self,union,level=0):
        w = self.writeGedLine
        w(level,u"FAM", xrefId=u"@%dU@" % union.id)
        w(level+1,u"HUSB", u"@%dI@" % union.husbandID)
        w(level+1,u"WIFE", u"@%dI@" % union.wifeID)
        if not self.private or (not union.husband.confidentiel and not union.wife.confidentiel):
            for child in union.children:
                w(level+1,u"CHIL", u"@%dI@" % child.id)
            for evt in union.events:
                self.evt2gedcom(evt,level+1)
            for link in union.links:
                self.link2gedcom(link,level+1)
            for link in union.reverseLinks:
                self.reverseLink2gedcom(link,level+1)
            self.note2gedcom(union.note,level+1)
        else:
            w(level+1,u"RESN", u"privacy")
        # the change date
        self.changeDate2gedcom(union,level+1)

    def getTypeOf(self,obj):
        type = obj.getType()
        types = {'Union':'FAM',
                 'Individu':'INDI',
                 'Media':'OBJE',
                 'Source':'SOUR'}
        try:
            return types[type]
        except KeyError:
            logger.warn("getTypeOf Warning:%s" % type)
            return type

    def getId(self,obj):
        type = obj.__class__.__name__
        types = {'Union':u'U',
                 'Individu':u'I',
                 'Media':u'M',
                 'Source':u'S'}
        try:
            return u"%d%s" % (obj.id,types[type])
        except KeyError:
            return u"%d%s" %(obj.id,type)

    def link2gedcom(self,link,level=0):
        w = self.writeGedLine
        w(level,u"ASSO", u"@%dI@" % link.toItemID)
        w(level+1,u"TYPE", self.getTypeOf(link.toItem))
        w(level+1,u"RELA", link.type)
        self.note2gedcom(link.note,level+1)

    def reverseLink2gedcom(self,link,level=0):
        w = self.writeGedLine
        if link.fromItem.getType() == "Event":
            evt = link.fromItem
            w(level,u"ASSO", u"@%s@" % self.getId(evt.item))
            w(level+1,u"TYPE", self.getTypeOf(evt.item))
            w(level+1,u"RELA", u"%s pour l'evenement %s de %s" % (self.getReverseLinkType(link.typeIndex),evt.typeName,evt.item.fullName))
        else:
            w(level,u"ASSO", u"@%dI@" % link.fromItemID)
            w(level+1,u"TYPE", self.getTypeOf(link.fromItem))
            w(level+1,u"RELA", self.getReverseLinkType(link.typeIndex))
        self.note2gedcom(link.note,level+1)

    def getReverseLinkType(self,typeID):
        result = self.reverseLinkTypes.get(typeID,None)
        if not result:
            print "Unknown Reverse Link Type : %d" % typeID
            result = "Other (%d)" % typeID
        return result
        
    def getCalendarEscape(self,cal):
        try:
            return self.gedcom_calendriers[cal]
        except KeyError:
            return u"@#DUNKNOWN@"

    def getMonth(self,month,cal):
        if cal == 0x4a or cal == 0x00: #julian or gregorian
            try:
                return self.gedcom_month[month]
            except:
                logger.warn("error occur while exporting julian or greogrian month %i" % (month))
                if self.stopOnError:
                    raise
                else:
                    return month
        elif cal == 0x48: #hebrew
            try:
                return self.gedcom_month_hebrew[month]
            except:
                logger.warn("error occur while exporting hebrew month %i" % (month))
                if self.stopOnError:
                    raise
                else:
                    return month
        elif cal == 0x52: # republican
            try:
                return self.gedcom_month_french[month]
            except:
                logger.warn("error occur while exporting republican month %i" % (month))
                if self.stopOnError:
                    raise
                else:
                    return month
        else:
            logger.warn("WARN: unknown calendar type %x" % (cal))
            return u"unknown"
            

    def simpleDate2Gedcom(self,cal,day,month,year):
        r = u''
        if not year:
            if day or month:
                r = u"(%s %s)" % (day,month)
        elif not month:
            r = u"%s %s" % (cal,year)
        elif not day:
            r = u"%s %s %s" % (cal,month,year)
        else:
            r = u"%s %s %s %s" % (cal,day,month,year)
        return r.strip()

    def event2gedcomDate(self,event):
        try:
            return self.date2gedcom(event.modif1,event.day1,event.month1,event.year1,event.calendar1,
                                event.modif2,event.day2,event.month2,event.year2,event.calendar2)
        except:
            logger.warn("error occur while exporting event's (%i %s) date" % (event.id, event.typeName))
            if self.stopOnError:
                raise   

    def date2gedcom(self,modif1,day1,month1,year1,cal1,modif2,day2,month2,year2,cal2):
        if modif1 == 3:
            date1 = self.simpleDate2Gedcom('',day1,self.getMonth(month1,cal1),year1)
            date2 = self.simpleDate2Gedcom('',day2,self.getMonth(month2,cal2),year2)
            return (u"%s %s %s %s %s" % (self.getCalendarEscape(cal1),'FROM ',date1,'TO',date2)).strip()
        else:
            date1 = self.simpleDate2Gedcom(self.getCalendarEscape(cal1),day1,self.getMonth(month1,cal1),year1).strip()
            if modif1:
                try:
                    return ("%s %s" % (self.gedcom_date_modif[modif1],date1)).strip()
                except IndexError:
                    logger.warn("Une date ne sera pas correcte (il manquera le modifieur) :" + date1)
                    return date1
            else:
                return date1

    def outputWrite(self, ch):
        self._output.write(ch)

    def writeGedLine(self, level, tag, lineValue=None, xrefId=None):
        ch = u""
        if xrefId:
            ch += unicode(xrefId) + u" "
        ch += unicode(tag)
        if lineValue:
            ch += u" " + unicode(lineValue)
        self.write(level, ch)

    def write(self, level, str):
        delta = self.delta
        if self.indented:
            tab = '\t' * level
        else:
            tab = ""
        ch = u"%s%d %s\r\n" % (tab,level,str)
        if len(ch) <= delta:
            self.outputWrite(ch)
        else:
            #print len(ch)
            delta = delta - 34 # because a gedcom tag is 31 long max and a number is below 99 that means 2+1+31
            n = 0
            line = str[:delta]
            self.write(level,line)
            n += delta
            line = str[n:n+delta]
            while len(str[n:]) > delta:
                self.writeGedLine(level, u"CONC", line)
                n += delta
                line = str[n:n+delta]
            self.writeGedLine(level,u"CONC", line)

if __name__=='__main__':
    import hr2ged
    hr2ged.interactive(hr2gedStandard)
