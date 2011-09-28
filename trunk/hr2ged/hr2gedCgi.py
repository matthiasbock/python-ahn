#!/usr/bin/python
# -*- coding: latin1 -*-
import logging
import StringIO

def setLogger():
    global logHandler
    console = logging.StreamHandler(logHandler)
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

if __name__=='__main__':
    global logHandler
    logHandler = StringIO.StringIO()
    setLogger()
    
import sys
sys.path.append("/home/loic/python/")
import cgi
import cgitb; cgitb.enable()
import os
import hrlib
import hr2ged
import hr2ged.hr2ged
import hr2ged.hr2gedStandard
import codecs
import urllib

class hr2gedCgi(hr2ged.hr2gedStandard.hr2gedStandard):

    def set(self,heredisFile,output=None,mediaDir=None,indent=False,noteType=None,charCode='ANSEL',private=False):
        if not output:
            output = codecs.EncodedFile(sys.stdout, "unicode_internal", "latin1", "xmlcharrefreplace")
        hr2ged.hr2gedStandard.hr2gedStandard.set(self, heredisFile, output, mediaDir, indent, noteType, charCode, private)  

class hr2gedCgiHtml(hr2gedCgi):
    def set(self,heredisFile,output=None,mediaDir=None,indent=False,noteType=None,charCode='ANSEL',private=False):
        hr2gedCgi.set(self, heredisFile, output, mediaDir, indent, noteType, charCode, private)
        self.delta = 300
    
    def writeGedLine(self, level, tag, lineValue=None, xrefId=None):
        if tag == u"FILE":
            lineValue = '<a href="file://%s">%s</a>' % (urllib.quote(lineValue.replace("\\","/"), "/:"), lineValue)
        if lineValue and lineValue.startswith("@") and lineValue.endswith("@"):
            lineValue = '<a href="#%s">%s</a>' % (lineValue, lineValue)
        tag = u'<span class="tag">%s</span>' % tag
        if xrefId:
            xrefId = u'<a name="%s">%s</a>' % (xrefId, xrefId)
        hr2gedCgi.writeGedLine(self,
                               level,
                               tag,
                               lineValue,
                               xrefId)
    
    def outputWrite(self, ch):
        hr2gedCgi.outputWrite(self, ch + u"<br />\n")

def doHr2Ged(form):
    options = hr2ged.hr2ged.hr2gedOption()
    if form.has_key("mediaDir") and form["mediaDir"].value:
        options.mediaDir = form["mediaDir"].value
    if not form.has_key("contentType") or form["contentType"].value == "html":
        print "Content-Type: text/html"     # HTML is following
        print                               # blank line, end of headers
        print '<html><body>'
        translator = hr2gedCgiHtml
    else:
        print "Content-Type: text/plain"
        print
        translator = hr2gedCgi
    hr2ged.hr2ged.doIt(translator=translator, openedFile=form["userfile"].file, options=options)
    if form["contentType"].value == "html":
        print '</body></html>'

def doHr2WhatEver(f):
    hf = hrlib.open(openedFile=f)
    for indi in hf.individuGenerator():
        output.write(indi.name)
        output.write(u"<br />\n")

def doFormular():
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    print "<html>"
    print "<head>"
    print "<title>Heredis Cgi</title>"
    print "</head>"
    print "<body>"
    print "<h1>hrCgi</h1><p>Ce script permet de créer des listes à partir d'un fichier Heredis</p>"
    print '<form action="" method="post" enctype="multipart/form-data">'
    print '<input name="userfile" type="file" /><br />'
    print '<input type="radio" name="contentType" value="html" checked>HTML</input><br />'
    print '<input type="radio" name="contentType" value="text">Texte</input><br />'
    print '<label for="mediaDir">Media Directory: </label><input id="mediaDir" name="mediaDir" type="text" /><br />'
    print '<input type="submit" /><br/>'
    print '</form>'
    print "</body>"
    print "</html>"


def main():
    form = cgi.FieldStorage()
    if form.has_key("userfile") and form["userfile"].value and form["userfile"].file:
        doHr2Ged(form)
    else:
        doFormular()

if __name__=="__main__":
    try:
        main()
    except:
        print "Content-Type: text/html"     # HTML is following
        print                               # blank line, end of headers
        print logHandler
        raise
