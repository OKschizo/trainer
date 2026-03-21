# Chapter 3: R13-R15 DWG FILE FORMAT ORGANIZATION

3 R13-R15 DWG FILE FORMAT ORGANIZATION
### 3.1 FILE STRUCTURE
The structure of the DWG file format changed between R13 C2 and R13 C3. Notations regarding C3
below indicate the differences.
The general arrangement of data in an R13/R14/R15 file is as follows:
HEADER
FILE HEADER
DWG HEADER VARIABLES
CRC

CLASS DEFINITIONS
TEMPLATE (R13 only, optional)
PADDING (R13C3 AND LATER, 200 bytes, minutes the template section above if present)
IMAGE DATA (PRE-R13C3)
OBJECT DATA
All entities, table entries, dictionary entries, etc. go in this
section.
OBJECT MAP
OBJECT FREE SPACE (optional)
TEMPLATE (R14-R15, optional)
SECOND HEADER
IMAGE DATA (R13C3 AND LATER)
### 3.2 FILE HEADER
3.2.1
VERSION ID:
The first 6 bytes are:
Bytes (ascii encoded)
Version
AC1012
R13
AC1014
R14
AC1015
R2000
AC1018
R2004
AC1021
R2007
AC1024
R2010
AC1027
R2013
AC1032
R2018


Open Design Specification for .dwg files

21


The next 7 starting at offset 0x06 are to be six bytes of 0 (in R14, 5 0’s and the ACADMAINTVER
variable) and a byte of 1. We have occasionally seen other values here but their meaning (and importance)
is unclear.
3.2.2
IMAGE SEEKER:
At 0x0D is a seeker (4 byte long absolute address) for the beginning sentinel of the image data.
3.2.3
OBJECT FREE SPACE
TODO.
3.2.4
TEMPLATE
This section is optional, see chapter 22.
3.2.5
DWGCODEPAGE:
Bytes at 0x13 and 0x14 are a raw short indicating the value of the code page for this drawing file.
3.2.6
SECTION-LOCATOR RECORDS:
At 0x15 is a long that tells how many sets of recno/seeker/length records follow. Each record has the
following format:
Record number (raw byte) | Seeker (raw long) | Size (raw long)
The records are as follows:


0 : Header variables (covers beginning and ending sentinels).

1 : Class section.

2 : Object map.

3 : (C3 and later.)  A special table (no sentinels). See unknown section (R13 C3 and
later). The presence of the 4th record (3) indicates that the C3 file format
applies.  Just look at the long at 21; if it's 4 or greater, it's the C3-and-later
format.

4 : In R13-R15, points to a location where there may be data stored.  Currently we
have seen only the MEASUREMENT variable stored here. See chapter 22. This section
is optional.
Remarks:

We have seen files with up to 6 sets in this section; the meaning of the sixth one
is unknown.  The Open Design Toolkit emits files with the first 5 sets only.

RS : CRC for BOF to this point.  Use 0 for the initial value, and depending on the
number of sets of section-locators, XOR the result with one of the following:

3 : 0xA598

Open Design Specification for .dwg files

22



4 : 0x8101

5 : 0x3CC4

6 : 0x8461
The following 16 byte sentinel appears after the CRC:
0x95,0xA0,0x4E,0x28,0x99,0x82,0x1A,0xE5,0x5E,0x41,0xE0,0x5F,0x9D,0x3A,0x4D,0x00

Open Design Specification for .dwg files

23