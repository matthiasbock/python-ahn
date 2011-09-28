import logging
import sys

def setLogFileName(fileName):
    logger = logging.getLogger()
    hdlr = logging.FileHandler(fileName,'w')
    formatter = logging.Formatter('%(name)s : %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.NOTSET)
    return logger

def setLogFile(file,format=None,loggerName=None):
    if not format:
        format = '%(name)s : %(levelname)s %(message)s'
    logger = logging.getLogger(loggerName)
    hdlr = logging.StreamHandler(file)
    formatter = logging.Formatter(format)
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.NOTSET)

def setLogStdErr(format=None):
    setLogFile(sys.stderr,format)

def setLogStdOut(format=None):
    setLogFile(sys.stdout,format)

    
