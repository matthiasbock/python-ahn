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

Format_Bug = "bug"

for Ehe in range(0,4):						# 4 marriages possible
	Nr = str(Ehe+1)+". "
	Fields += [
		(Nr+"Ehepartner", integer, 4),
		(Nr+"Hochzeit am", date, 10)
		]

	if Ehe+1 <= 3:						# Format_Bug, see Wiki
		Fields.append( (Nr+"Hochzeit in", string, 30) )	# 1.-3.
	else:
		Fields.append( (Nr+"Hochzeit in", string, 28) ) # 4.
		Fields.append( (Format_Bug, integer, 2) )

	for i in range(0,18):					# 18 children per marriage
		Fields.append( (str(i+1)+". Kind aus "+str(Ehe+1)+". Ehe", integer, 4) )

def str2int(s):
	result = 0
	shift = 0
	for i in range(0,len(s)):
		result += (ord(s[i]) << shift)
		shift += 8
	return result

def int2str(i, length):
	result = ""
	for j in range(0, length):
		result += chr(i & 255)
		i = i >> 8
	return result

class dataset:
	def __init__(self, data):
		self.fields = {}
		position = 0
		for field in Fields:							# for all Fields
			q = position+field[length]
			value = data[position:q]
			position = q
			if field[fieldtype] in [string, date]:				# remove whitespace
				value = value.strip()
#			if field[fieldtype] == date and value != "":			# convert to date
#				value = strptime(value, "%d.%m.%Y")
			if field[fieldtype] == integer:					# convert to integer
				value = str2int(value)
			if value != "" and value != 0:
				self.fields[ field[descriptor] ] = value		# save acquired info to python class

	def export(self):
		result = ""
		for field in Fields:							# for all Fields
			key = field[descriptor]
			if key in self.fields.keys():					# info is present
				value = self.fields[key]
			else:								# info is not present
				value = ""
				if field[fieldtype] == integer:				# ... defaults
					value = 0
			if field[fieldtype] == integer:
				value = int2str(value, field[length])			# convert properly
			elif field[fieldtype] in [string, date]:
				value = value.ljust(field[length], chr(0x20))
			result += value							# export
		return result

class ahn:
	def __init__(self, filename=None, debug=False, compare_import_export=False):
		self.datasets = []
		if filename is not None:
			self.load(filename, debug, compare_import_export)

	def load(self, filename, debug=False, compare_import_export=False):
		f = open(filename)
		data = f.read(1100)						# read file
		while data:
			d = dataset(data)					# append new instance of class dataset
			self.datasets.append(d)
			if debug:
				print d.fields					# print dataset
			if compare_import_export:				# compare import and dataset export
				exported = d.export()
				if data == exported:
					print "Import and Export are identical."
				else:
					print "Import and Export differ:"
					print str(len(data))+" characters"
					print data.replace(" ","_")
					print str(len(exported))+" characters"
					print exported.replace(" ","_")
					for i in range(0,len(data)):
						if data[i] != exported[i]:
							print "Character No. "+str(i)+" differs:"
							print "\timport: "+str(ord(data[i]))
							print "\texport: "+str(ord(exported[i]))
			data = f.read(1100)
		f.close()

	def saveto(self, filename):
		f = open(filename, "w")						# write to file
		for dataset in self.datasets:
			f.write(dataset.export())
		f.close()

	def exportAhnenblatt(self, filename):
		import Ahnenblatt
		export = Ahnenblatt.ahn()
		for dataset in self.datasets:
			export.datasets.append( dataset.exportAhnenblatt() )
		return export

