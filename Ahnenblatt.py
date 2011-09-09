#! /usr/bin/python
# -*- coding: iso-8859-15 -*-

Dataset_Start = chr(0x01)

Descriptor = {
	"f" : "Names",
	"e" : "Surnames",
	"}" : "Sex",
	"j" : "Father's Name",
	chr(0x97) : "Father's ID",
	"k" : "Mother's Name",
	chr(0x98) : "Mother's ID",
	"l" : "Sibling's Name",
	chr(0x99) : "Sibling's ID",
	"g" : "Birth Date",
	"h" : "Birth Place",
	"i" : "Occupation",
	"s" : "Religion",
	"t" : "Christening Date",
	"u" : "Christening Address",
	"v" : "Christening Place",
	"w" : "Godfather",
	"x" : "Confirmation Date",
	"y" : "Confirmation Address",
	"z" : "Confirmation Place",
	"m" : "Marriage Date",
	"n" : "Marriage Place",
	"o" : "Marriage Spouse's Name",
	chr(0x9A) : "Marriage Spouse's ID",
	"p" : "Child's Name",
	chr(0x9B) : "Child's ID",
	"q" : "Death Date",
	"r" : "Death Place",
	"{" : "Burial Date",
	"|" : "Burial Place",
	chr(0x83) : "Note",
	chr(0x84) : "Source",
	chr(0xa1) : "Picture Filename",
	chr(0xa3) : "Picture Absolute Path",
	chr(0xa4) : "Picture Relative Path",	# sometimes with filename, sometimes without
	}

Sex =	{
	chr(0x01) : "male",
	chr(0x02) : "female"
	}

class dataset:
	def __init__(self):
		self.fields = []

class ahn:
	def __init__(self, filename=None):
		self.datasets = []
		if filename is not None:
			self.load(filename)

	def load(self, filename):
		f = open(filename)
		f.read(201)		# header

		def read_Descriptor():	# 1 byte Descriptor
			return f.read(1)
		def read_length():	# 2 byte length
			return ord(f.read(1))+(ord(f.read(1))*256)
		def read_data():	# string
			return f.read(l)[:-1]

		current_dataset = None		
		q = read_Descriptor()
		while q:								# read until end-of-file
			if q == Dataset_Start:	# 0x01
				if (current_dataset is not None) and (current_dataset.fields != []):
					self.datasets.append( current_dataset )
				f.read(1)	# 0x03
				current_dataset = dataset()				# start new dataset
			else:
				l = read_length()					# read field
				d = read_data()
				if len(d) > 0:						# add field to current dataset
					if not q in Descriptor.keys():	# unknown Descriptor
						current_dataset.fields.append( ("------------??? "+q+" ???------------", d) )
					elif q == "}":			# sex
						current_dataset.fields.append( (Descriptor[q], Sex[d]) )
					elif len(d) == 1:		# some ID
						current_dataset.fields.append( (Descriptor[q], ord(d)+1) )
					else:				# some string
						current_dataset.fields.append( (Descriptor[q], d) )
			q = read_Descriptor()
		if (current_dataset is not None) and (current_dataset.fields != []):
			self.datasets.append( current_dataset )
		f.close()

	def saveto(self, filename):
		# blabla
		return

