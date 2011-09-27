#! /usr/bin/python
# -*- coding: iso-8859-15 -*-

import FChronik, Ahnenblatt

weber = FChronik.ahn("FChronik/Beispiel.ahn", debug=True, compare_import_export=True)

print str(len(weber.datasets))+" datasets"

weber.saveto("FChronik/Beispiel_written_by_python.ahn")

#weber.exportAhnenblatt().saveto("Fchronik/Beispiel2Ahnenblatt.ahn")

#Beispiel = Ahnenblatt.ahn("Ahnenblatt/Beispiele/Beispiel.ahn")

#for dataset in Beispiel.datasets:
#	print dataset.fields
#	print
