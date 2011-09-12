#! /usr/bin/python
# -*- coding: iso-8859-15 -*-

#from time import strptime

# field type
string = "string"
date = "date"
integer = "integer"

# pos in field tuple
descriptor = 0
fieldtype = 1
length = 2

Fields = [
		("ID", integer, 4),
		("Name", string, 20),
		("Geburtsname", string, 20),
		("Erster Vorname", string, 20),
		("Weitere Vornamen", string, 30),

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

		("Notizen", string, 300),

		("Vater", integer, 4),
		("Mutter", integer, 4),
	]

for Ehe in range(0,4):				# 4 marriages possible
	Nr = str(Ehe+1)+"."
	Fields += [
		(Nr+" Ehepartner", integer, 4),
		(Nr+" Hochzeit am", date, 10)
		]
	if Ehe+1 != 4:				# fix for a bug in the Data Becker Familienchronik
		Fields.append( (Nr+" Hochzeit in", string, 30) )
	else:
		Fields.append( (Nr+" Hochzeit in", string, 28) )
		Fields.append( ("bug", integer, 2) )
	for i in range(0,18):			# 18 children per marriage
		Fields.append( ("Kind "+str(i+1)+" aus Ehe "+str(Ehe+1), integer, 4) )

def str2int(s):
	result = 0
	shift = 0
	for i in range(0,len(s)):
		result += ord(s[i]) << shift
		shift += 8
	return result

def int2str(i, length):
	result = ""
	for j in range(0,length):
		result += chr(i & 255)
		i = i >> 8
	return result

class dataset:
	def __init__(self, data):
		self.fields = {}
		p = 0
		for field in Fields:
			value = data[ p : p+field[length] ]
			if field[fieldtype] in [string, date]:
				value = value.strip()				# remove whitespace
#			if field[fieldtype] == date and value != "":
#				value = strptime(value, "%d.%m.%Y")
			if field[fieldtype] == integer:
				value = str2int(value)				# convert to number
			if value != "" and value != 0 and field[descriptor] != "bug":
				self.fields[ field[descriptor] ] = value
			p += field[length]

	def export(self):
		result = ""
		for field in Fields:
			key = field[descriptor]
			if key in self.fields.keys():			# value exists
				value = self.fields[key]
			else:						# empty
				if field[fieldtype] == integer:
					value = 0
				elif field[fieldtype] == string:
					value = ""
			if field[fieldtype] == integer:
				value = int2str(value, field[length])
			elif field[fieldtype] == string:
				value = value.ljust(field[length], chr(0x20))
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

	def load(self, filename, show=False, debug=False):
		f = open(filename)
		d = f.read(1100)
		while d:
			x = dataset(d)
			self.datasets.append( x )
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
		print Fields
		f = open(filename, "w")
		for dataset in self.datasets:
			f.write(dataset.export())
		f.close()

	def exportAhnenblatt(self, filename):
		import Ahnenblatt
		export = Ahnenblatt.ahn()
		for dataset in self.datasets:
			export.datasets.append( dataset.exportAhnenblatt() )
		return export

