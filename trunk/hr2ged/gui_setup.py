# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""GPL Copyright (C) 2004  Loïc Fejoz"""

from distutils.core import setup
import py2exe

import hr2ged
#python gui_setup.py py2exe, see also build.bat
setup(name="hr2gedGui",
      version=hr2ged.__version__,
      description="Convert Heredis(c) file (hr5,hr7, hr9 and h10) to Gedcom",
      author=u"Loïc Fejoz",
      author_email="loic@fejoz.net",
      url="http://hr2ged.sourceforge.net/",
      windows=['hr2gedGui.pyw'],
      data_files=[('',['gui.xrc','help.txt'])],            options = {"py2exe": {"packages": "encodings"}}
     )

