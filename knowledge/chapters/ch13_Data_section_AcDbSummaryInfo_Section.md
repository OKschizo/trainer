# Chapter 13: Data section AcDb:SummaryInfo Section

13 Data section AcDb:SummaryInfo Section
Section property
Value
Name
AcDb:SummaryInfo
Compressed
1
Encrypted
0 if not encrypted, 1 if encrypted.
Page size
0x100


This section contains summary information about the drawing. Strings are encoded as a 16-bit length,
followed by the character bytes (0-terminated).

Type
Length
Description
String
2 + n
Title
String
2 + n
Subject
String
2 + n
Author
String
2 + n
Keywords
String
2 + n
Comments
String
2 + n
Last saved by
String
2 + n
Revision number
String
2 + n
Hyperlink base
?
8
Total editing time (ODA writes two zero Int32’s)
Julian date
8
Create date time
Julian date
8
Modified date time
Int16
2 + 2 * (2 +
Property count, followed by PropertyCount key/value string pairs.

Open Design Specification for .dwg files

92


n)
Int32
4
Unknown (write 0)
Int32
4
Unknown (write 0)

Open Design Specification for .dwg files

93