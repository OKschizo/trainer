# Chapter 17: Data section AcDb:FileDepList

17 Data section AcDb:FileDepList
Contains file dependencies (e.g. IMAGE files, or fonts used by STYLE).
Section property
Value
Name
AcDb:FileDepList
Compressed
1
Encrypted
2 (meaning unknown)
Page size
0x80 if number of entries is 0 or 1. If more than 1, then 0x80 x number of
entries.
In R18 the app info section consists of the following fields. Strings are encoded as a 32-bit length,
followed by the character bytes (without trailing 0).
Type
Length
Description
Int32
4
Feature count (ftc)
String32
ftc * (4 + n)
Feature name list. A feature name is one of the following:
“Acad:XRef” (for block table record)
“Acad:Image” (for image definition)
“Acad:PlotConfig” (for plotsetting)
“Acad:Text” (for text style)
Int32
4
File count
Then follows an array of features (repeated file count times). The feature name + the full filename
constitute the lookup key of a file dependency:

Type
Length
Description
String32
4 + n
Full filename
String32
4 + n
Found path, path at which file was found

Open Design Specification for .dwg files

99


String32
4 + n
Fingerprint GUID (applies to xref’s only)
String32
4 + n
Version GUID (applies to xref’s only)
Int32
4
Feature index in the feature list above.
Int32
4
Timestamp (Seconds since 1/1/1980)
Int32
4
Filesize
Int16
2
Affects graphics (1 = true, 0 = false)
Int32
4
Reference count



Open Design Specification for .dwg files

100