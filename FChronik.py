#! /usr/bin/python
# -*- coding: iso-8859-15 -*-

#from time import strptime

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

		("Vater", binary, 12),

		("Hochzeit am", date, 10),
		("Hochzeit in", string, 30),

		("Kinder", binary, 76),
		("string1", string, 40),
		("binary3", binary, 76),
		("string2", string, 40),
		("binary4", binary, 76),
		("string3", string, 38),
		("Geschwister", binary, 74)
	]

class dataset:
	def __init__(self, data, ID):
		self.fields = {"ID":ID}
		p = 0
		for field in Fields:
			value = data[ p : p+field[length] ]
			if field[fieldtype] in [string, date]:
				value = value.strip()				# remove whitespace
#			if field[fieldtype] == date and value != "":
#				value = strptime(value, "%d.%m.%Y")
			if field[fieldtype] == binary:
				value = ord(value[0])+(ord(value[1])*256)	# convert to number
			if value != "" and value != 0:
				self.fields[ field[descriptor] ] = value
			p += field[length]

	def export(self):
		result = ""
		for field in Fields:
			key = field[descriptor]
			if key in self.fields.keys():			# value exists
				value = self.fields[key]
			else:						# empty
				if field[fieldtype] == binary:
					value = 0
				elif field[fieldtype] == string:
					value = ""
			if field[fieldtype] == binary:
				value = (chr(value)+chr(0)).rjust(field[length], chr(0))
			elif field[fieldtype] == string:
				value = value.ljust(field[length], chr(0x20))
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
		ID = 1
		while d:
			x = dataset(d, ID)
			self.datasets.append( x )
			ID += 1
			if show:
				print x.fields
				print
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

