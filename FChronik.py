#! /usr/bin/python
# -*- coding: iso-8859-15 -*-

class dataset:
	def __init__(self, data):
		self.Name = data[0:20].strip()
		self.Geburtsname = data[20:40].strip()
		self.Vorname = data[40:60].strip()
		self.WeitereVornamen = data[60:80].strip()

		# 10 x 0x20
		self.spaces1 = data[80:90]

		self.GeborenAm = data[90:100]
		self.GeborenIn = data[100:130].strip()
		self.GetauftAm = data[130:140]
		self.GetauftIn = data[140:170].strip()
		self.Geschlecht = data[170:178]
		self.Religion = data[178:190].strip()
		self.Beruf = data[190:229].strip()
		self.GestorbenAm = data[229:239]
		self.GestorbenIn = data[239:269].strip()
		self.Alter = data[269:284].strip()
		self.BeerdigtAm = data[284:294]
		self.BeerdigtIn = data[294:324].strip()

		# 300 x 0x20
		self.spaces2 = data[324:624]

		self.binary1 = data[624:636]

		self.HochzeitAm = data[636:646]
		self.HochzeitIn = data[646:676].strip()

		self.binary2 = data[676:752]
		self.string1 = data[752:792]
		self.binary3 = data[792:868]
		self.string2 = data[868:908]
		self.binary4 = data[908:984]
		self.string3 = data[984:1024]
		self.binary5 = data[1024:1100]

class ahn:
	def __init__(self, filename=None):
		self.datasets = []
		if filename is not None:
			self.load(filename)

	def load(self, filename):
		f = open(filename)
		f.read(4)		# magic
		d = f.read(1100)
		while d:
			x = dataset(d)
			self.datasets.append( x )
			d = f.read(1100)
		f.close()

