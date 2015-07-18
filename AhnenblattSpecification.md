# Dirk Böttcher's Ahnenblatt - File Format Specification #

_Dirk Böttcher's Ahnenblatt_ family tree software uses a proprietary file format to save it's genealogy data. File extension is **.ahn**.

The file consists of a header with magic bytes and meta information, followed by a sequence of datasets, one dataset per person.

## Dataset format ##
A dataset is a sequence of fields. Each field starts with a one byte qualifier, defining what kind of information will follow, followed by a 2 byte little-endian word, defining how many bytes of information follow. The information itself is stored as standard ASCII string, terminated by:
  * 

&lt;0x00&gt;


In contrast to the FChronik format, the length varies from dataset to dataset, as it depends on the number and length of the fields stored in it.

## Fields ##

```
Dataset_Start = chr(0x01)

Qualifier = {
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
```

## Maximum number of datasets ##
Only one byte is used for IDs, so the maxmimum number of datasets is limited to 256.