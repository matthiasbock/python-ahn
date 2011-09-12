#! /usr/bin/python
# -*- coding: iso-8859-15 -*-

# field type
string = 0
date = 1
binary = 2

# pos in field tuple
descriptor = 0
fieldtype = 1
length = 2

Fields = [	
		("Name", string, 20),
		("Geburtsname", string, 20),
		("Erster Vorname", string, 20),
		("Weitere Vornamen", string, 20),

		# 10 x 0x20
		("spaces1", string, 10),

		("geboren am", date, 10),
		("geboren in", string, 30),

		("getauft am", date, 10),
		("getauft in", string, 30),

		("Geschlecht", string, 8),
		("Konfession", string, 12),
		("Beruf", string, 39),

		("gestorben am", date, 10),
		("gestorben in", string, 30),

		("Alter", string, 15),

		("beerdigt am", date, 10),
		("beerdigt in", string, 30),

		# 300 x 0x20
		("spaces2", string, 300),

		("binary1", binary, 12),

		("Hochzeit am", date, 10),
		("Hochzeit in", string, 30),

		("binary2", binary, 76),
		("string1", string, 40),
		("binary3", binary, 76),
		("string2", string, 40),
		("binary4", binary, 76),
		("string3", string, 38),
		("binary5", binary, 74)
	]

class dataset:
	def __init__(self, data):
		self.fields = []
		p = 0
		for field in Fields:
			value = data[ p : p+field[length] ]
			if field[fieldtype] == string:
				value = value.strip()
			elif field[fieldtype] == binary:
				value = ord(value[0])+(ord(value[1])*256)
			self.fields.append( (field[descriptor], value) )
			p += field[length]

	def export(self):
		result = ""
		for i in range(0, len(Fields)):
			value = self.fields[i][1]
			if Fields[i][fieldtype] == binary:
				value = (chr(value)+chr(0)).rjust(Fields[i][length], chr(0))
			elif Fields[i][fieldtype] == string:
				value = value.ljust(Fields[i][length], chr(0x20))
			result += value
		return result

	def exportAhnenblatt(self):
		# blabla
		return ()

class ahn:
	def __init__(self, filename=None, show=False):
		self.header = chr(1)+chr(0)+chr(0)+chr(0)
		self.datasets = []
		if filename is not None:
			self.load(filename, show)

	def load(self, filename, show=False, debug=False):
		f = open(filename)
		self.header = f.read(4)		# magic
		d = f.read(1100)
		while d:
			x = dataset(d)
			self.datasets.append( x )
			if show:
				print x.fields
			if debug:
				if d == x.export():
					print "input and export are identical"
				else:
					print "input and export differ"
			d = f.read(1100)
		f.close()

	def saveto(self, filename):
		f = open(filename, "w")
		f.write(self.header)
		for dataset in self.datasets:
			f.write(dataset.export())
		f.close()

	def exportAhnenblatt(self, filename):
		import Ahnenblatt
		export = Ahnenblatt.ahn()
		for dataset in self.datasets:
			export.datasets.append( dataset.exportAhnenblatt() )
		return export

