#! /usr/bin/python
# -*- coding: iso-8859-15 -*-

string = 0 # string
date = 1 # date
binary = 2 # binary

descriptor = 0	# pos in field tuple
fieldtype = 1
length = 2
alignment = 3

left = 0
right = 1

Fields = [	
		("Name", string, 20, left),
		("Geburtsname", string, 20, left),
		("Erster Vorname", string, 20, left),
		("Weitere Vornamen", string, 20, left),

		# 10 x 0x20
		("spaces1", string, 10, left),

		("geboren am", date, 10, None),
		("geboren in", string, 30, left),

		("getauft am", date, 10, None),
		("getauft in", string, 30, left),

		("Geschlecht", string, 8, left),
		("Konfession", string, 12, left),
		("Beruf", string, 39, left),

		("gestorben am", date, 10, None),
		("gestorben in", string, 30, left),

		("Alter", string, 15, left),

		("beerdigt am", date, 10, None),
		("beerdigt in", string, 30, left),

		# 300 x 0x20
		("spaces2", string, 300, left),

		("binary1", binary, 12, right),

		("Hochzeit am", date, 10, None),
		("Hochzeit in", string, 30, left),

		("binary2", binary, 76, right),
		("string1", string, 40, left),
		("binary3", binary, 76, right),
		("string2", string, 40, left),
		("binary4", binary, 76, right),
		("string3", string, 38, left),
		("binary5", binary, 74, right)
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
				value = chr(value)+chr(0)
				justify = chr(0)
			elif Fields[i][fieldtype] == string:
				justify = chr(0x20)
			if Fields[i][alignment] == right:
				value = value.rjust(Fields[i][length], justify)
			elif Fields[i][alignment] == left:
				value = value.ljust(Fields[i][length], justify)
			result += value
		return result

	def exportAhnenblatt(self):
		# blabla
		return ()

class ahn:
	def __init__(self, filename=None, show=False):
		self.datasets = []
		if filename is not None:
			self.load(filename, show)

	def load(self, filename, show=False):
		f = open(filename)
		self.header = f.read(4)		# magic
		d = f.read(1100)
		while d:
			x = dataset(d)
			self.datasets.append( x )
			if show:
				print x.fields
				print d
				print str(len(d))
				reexported = x.export()
				print reexported
				print str(len(reexported))
				print
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

