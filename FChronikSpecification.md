# Data Becker FChronik - File Format Specification #

The _Data Becker Familienchronik_ family tree software uses a proprietary file format to save it's genealogy data. File extension is **.ahn**.

## File format ##

Each file simply is a sequence of datasets, one dataset per person.
A dataset consist of a predefined sequence of data fields.
Every field has a predefined length, which results in every dataset having exactly 1100 bytes.

## Dataset format ##

```
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
```

## Field format ##

Each field is of one of the three types:
  * string,
  * date or
  * binary

Strings smaller than their appropriate field length are padded right with spaces:
  * 

&lt;0x20&gt;



Each date field has 10 bytes. Dates are represented by dot separated ASCII digits:
  * **DD.MM.YYYY**

## Maximum number of datasets ##

4 bytes are used for IDs, so a practically unlimited number (256^4) of datasets can be stored.

## Characterset ##

Strings is standard ASCII. Explicit qualifiers, e.g. the gender, are german.

In german special vowels exist, ä, ö and ü, as well as a special s, the ß. Their hexadecimal representations are:
  * ä 

&lt;0xE4&gt;


  * ö 

&lt;0xF6&gt;


  * ü 

&lt;0xFC&gt;


  * ß 

&lt;0xDF&gt;

