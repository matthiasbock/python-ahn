#! /usr/bin/python
# -*- coding: iso-8859-15 -*-

import FChronik, Ahnenblatt

#weber = FChronik.ahn("FChronik/weber.ahn")
#print str(len(weber.datasets))+" datasets"

Beispiel = Ahnenblatt.ahn("Ahnenblatt/Beispiele/Beispiel.ahn")

for dataset in Beispiel.datasets:
	print dataset.fields
	print
