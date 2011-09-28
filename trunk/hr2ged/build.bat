del hr2ged.zip
del hr2gedGui.zip

rmdir /S /Q hr2ged
python setup.py py2exe
rename dist hr2ged
7z a -tZIP hr2ged hr2ged\*.*

rmdir /S /Q hr2gedGui
copy hr2gedGui.py hr2gedGui.pyw
python gui_setup.py py2exe
del hr2gedGui.pyw
rename dist hr2gedGui
7z a -tZIP hr2gedGui hr2gedGui\*.*
