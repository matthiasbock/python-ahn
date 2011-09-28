#!//usr/bin/python
# -*- coding: cp1252 -*-
u"""
Translate an heredis file to a gedcom.
Heredis is a BSD CONCEPT copyright.

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

loic@fejoz.net
"""

__version__ = "0.3"

import codecs
import optparse
import sys
import time
import traceback
import hrlib
import logging
logger = logging.getLogger('hr2ged')

import hr2gedStandard

import encodings
import encodings.cp437
import encodings.utf_16
import encodings.utf_8
import encodings.ascii
import encodings.latin_1
import encodings.cp1252
import encodings.cp850


class CharCodeUnknown(ValueError):
    pass

class hr2gedOption:
    def __init__(self):
        self.filename = None
        self.media=None
        self.noteType = 'txt'
        self.indent = False
        self.private = False
        self.charCode = 'UTF8'
        self.mediaExport = 'STANDARD'
        self.gregorian = True
        self.changeDate = True
        self.mediaDir = None
	self.assoExport = 'STANDARD'
        self.keepgoing = False

def setAssoExportOptions(assoExport,translator):
    assoExport = assoExport.upper()
    if assoExport == 'INDI':
        import IndiAssoOption
        IndiAssoOption.setOption(translator)
    elif assoExport == 'STANDARD':
        pass
    else:
        optionName = assoExport[0].upper() + assoExport.lower()[1:]
        moduleName = '%sAssoOption' % optionName
        logger.info('External Asso Option: %s',moduleName)
        m = __import__(moduleName)
        m.setOption(translator)

def setMediaExportOptions(mediaExport,translator):
    mediaExport = mediaExport.upper()
    if mediaExport == 'INLINE':
        import InlineMediaOption
        InlineMediaOption.setOption(translator)
    elif mediaExport == 'EVENT':
        import EventMediaOption
        EventMediaOption.setOption(translator)
    elif mediaExport == 'STANDARD':
        pass
    else:
        optionName = mediaExport[0].upper() + mediaExport.lower()[1:]
        moduleName = '%sMediaOption' % optionName
        logger.info('External Media Option: %s',moduleName)
        m = __import__(moduleName)
        m.setOption(translator)

def translate(heredisFileName=None, options=None, translator=hr2gedStandard.hr2gedStandard, openedFile=None):
    if (not heredisFileName) and (not openedFile):
        return
    if not options:
        options = hr2gedOption()
    depart = time.time()
    if heredisFileName:
        if options.filename:
            gedcomFileName = options.filename
        else:
            gedcomFileName = heredisFileName[:-4]+'.ged'
        #gf = file(gedcomFileName,'w')
        gf = codecs.open(gedcomFileName, "w", translator.charCode,'replace')
    else:
        gedcomFileName = "stdout"
        gf = None
    hf = hrlib.open(fileName=heredisFileName, openedFile=openedFile)
    h2g = translator()
    logger.info("operation en cours...")
    try:
        h2g.heredis2gedcom(hf,gf,options.mediaDir,options.indent,options.noteType,options.charCode,options.private, not options.keepgoing)
    finally:
        hf.close()
        if gf:
            gf.close()
    fin = time.time()
    logger.info("resultat dans %s",gedcomFileName)
    logger.info("done in %d seconds",(fin-depart))
    del h2g
    return gedcomFileName

def getTranslator(options,translator=hr2gedStandard.hr2gedStandard):
    """ return a translator compliant to the given option"""
    logger = logging.getLogger('Heredis2Gedcom')
    charCodes = {'ANSEL':u'latin_1',
                 'ASCII':u'ascii',
                 'ANSI':u'iso8859_15',
                 'UNICODE':u'unicode',
                 'UTF16':u'utf_16',
                 'UTF8':u'utf_8_sig',
                 'DOS':u'cp437'}
    class SpecialTranslator(translator):
        pass
    translator = SpecialTranslator
    # char code
    if options.charCode:
        try:
            translator.charCode = charCodes[options.charCode.upper()]
            options.charCode = translator.charCode
        except KeyError:
            raise CharCodeUnknown(options.charCode)
    # mediaExport
    setMediaExportOptions(options.mediaExport.upper(),translator)
    # assoExport
    setAssoExportOptions(options.assoExport.upper(),translator)
    # gregorian
    if options.gregorian:
        import CalendarDateOption
        CalendarDateOption.setOption(translator)
    #ChangeDateOption
    if options.changeDate:
        import ChangeDateOption
        ChangeDateOption.setOption(translator)
    return translator
        
def doIt(fileName=None, options=None, translator=hr2gedStandard.hr2gedStandard, openedFile=None):
    translator = getTranslator(options, translator)
    try:
        return translate(fileName, options, translator, openedFile)
    except KeyboardInterrupt:
        logger.info('-' * 80)
        logger.info('End of Process ask by user...')
        logger.info('bye bye')
    except:
        logger.info('-'*80)
        logger.exception('Pourriez-vous envoyer votre fichier a loic@fejoz.net pour debugging, merci.')
        logger.info('-'*80)
        raise

def interactive(translator=hr2gedStandard.hr2gedStandard):
    print u"""
    hr2ged %s , Copyright (C) 2004 Loïc Fejoz
    hr2ged comes with ABSOLUTELY NO WARRANTY; for details
    type `show'.  This is free software, and you are welcome
    to redistribute it under certain conditions; type `show' 
    for details.
    """ % __version__
    import LogService
    LogService.setLogStdOut('%(message)s')
    LogService.setLogFileName('hr2ged.log')
    logger = logging.getLogger('hr2ged')
    parser = optparse.OptionParser(usage="%prog [options] fichier_heredis\nAller voir http://hr2ged.sourceforge.net/")
    parser.add_option("-f", "--file", dest="filename", default=None,
                  help="ecrire le gedcom  dans FILE", metavar="FILE")
    parser.add_option("-m", "--media",
                  action="store", dest="mediaDir", default=None,
                  help="indique  l'emplacement  des medias",metavar="DIRECTORY")
    parser.add_option("-n", "--note",
                  action="store", dest="noteType", default='txt',
                  help="convertir les notes en txt [ par defaut], html, rtf")
    parser.add_option("-i", "--indent",
                  action="store_true", dest="indent", default=False,
                  help="indenter le fichier (pour  debug  uniquement)")
    parser.add_option("-k", "--keepgoing",
                  action="store_true", dest="keepgoing", default=False,
                  help="Continue malgre des erreurs")
    parser.add_option("-p", "--private",
                  action="store_true", dest="private", default=False,
                  help="n'exporter que les noms et prenoms des individus confidentiels")
    parser.add_option("-c", "--char",
                  action="store", dest="charCode", default=u'UTF8',
                  help="encodage utilise pour les caracteres : ANSEL, ASCII, UTF16, UTF8[par defaut], DOS, ANSI")
    parser.add_option("-e", "--mediaExport",
                  action="store", dest="mediaExport", default=u'STANDARD',
                  help="type d'export des medias : STANDARD (par defaut), INLINE (sans pointeur), EVENT (dans un evenement)")
    parser.add_option("-g", "--gregorian",
                  action="store_false", dest="gregorian", default=True,
                  help="indique si l'on doit exporter le calendrier @#DGREGORIAN@ pour les dates en gregorien")
    parser.add_option("-d", "--changeDate",
                  action="store_false", dest="changeDate", default=True,
                  help="indique si l'on doit indiquer les dates de modifications a tous les niveaux")
    parser.add_option("-a", "--assoExport",
                  action="store", dest="assoExport", default=u'STANDARD',
                  help="type d'export des liens : STANDARD (par defaut), INDI (tout au niveau des individus)")    
    (options, args) = parser.parse_args()
    if len(args) ==1 and args[0] == 'show':
        print __doc__
        sys.exit(0)
    if len(args) != 1:
        print "nombre  d'arguments  incorrect"
        parser.print_help()
        sys.exit(1)
    try:
        doIt(args[0],options,translator)
        print 'fichier de log dans hr2ged.log'
    except CharCodeUnknown:
        logger.error('unkown char code : %s' % options.charCode)
        parser.print_help()
        sys.exit(1)
    except:
        logger.exception('Fin anormale ! ')
        sys.exit(1)

def profile():
    import profile
    profile.run("interactive()")

if __name__=='__main__':
    # Import Psyco if available
    try:
        import psyco
        psyco.full()
    except ImportError:
        print "psyco unavailable"
    #profile()
    import warnings
    warnings.filterwarnings('ignore')
    interactive()
