
try:
    import psyco
    psyco.full()
except ImportError:
    print "psyco unavailable"


import hr2ged
import os
import os.path
import LogService
import logging
import traceback

os.system("del *.log")

logger = logging.getLogger('testAll')

LogService.setLogFileName('testAll.log')

##class Option:
##    pass

##options = Option()

##options.filename = None
##options.mediaDir = None
##options.noteType = 'rtf'
##options.indent = False
##options.private = False
##options.charCode= 'ANSEL'
##options.mediaExport = 'STANDARD'
##options.gregorian = False
##options.changeDate = False

options = '-ntxt'

def isHeredisFile(fileName):
    ext = fileName.split('.')[-1]
    if ext in ['hr5','hr7','hr8','hr9','h10']:
        return True
    return False

top ='D:\\Home\\loic\\genealogie'
for root, dirs, files in os.walk(top):
    for fileName in files:
        if isHeredisFile(fileName):
            filePath = os.path.join(root,fileName)
            logger.info('Translating %s',filePath)
            print 'Translating',filePath
            r = os.system('python hr2ged.py %s "%s"' % (options,filePath))
            if r == 0:
                print '\tok'
            else:
                print '\tError with',fileName
                logger.error('Error with %s',fileName)
            os.system('copy hr2ged.log "%s.log"' % fileName)
##            try:
##                Heredis2Gedcom.doIt(fileName,options)
##            except KeyboardInterrupt:
##                print 'bye bye'
##                raise
##            except:
##                print '\tError with',fileName
##                traceback.print_exc()
##            else:
##                print '\tok'
