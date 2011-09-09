#! /usr/bin/python
# -*- coding: iso-8859-15 -*-

string = 0 # string
date = 1 # date
binary = 2 # binary

descriptor = 0	# pos in field tuple
fieldtype = 1
length = 2

Fields = [	# dataset = sequence of fields

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
		("binary5", binary, 78)
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

class ahn:
	def __init__(self, filename=None, show=False):
		self.datasets = []
		if filename is not None:
			self.load(filename, show)

	def load(self, filename, show=False):
		f = open(filename)
		f.read(4)		# magic
		d = f.read(1100)
		while d:
			x = dataset(d)
			self.datasets.append( x )
			if show:
				print x.fields
				print
			d = f.read(1100)
		f.close()

