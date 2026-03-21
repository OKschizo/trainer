# Chapter 15: Data section AcDb:VBAProject Section

15 Data section AcDb:VBAProject Section
The VBA project section is optional.
Section property
Value
Name
AcDb:VBAProject
Compressed
1
Encrypted
2 (meaning unknown).
Page size
Project data size + 0x80 + section alignment padding


The contents are currently unknown.The ODA reads and writes the contents of this section as is:

Type
Length
Description
byte
16
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1c, 0x00,
0x00, 0x19, 0x00, 0x00, 0x00
byte
n
The VBA project data
Int32
4
0

Open Design Specification for .dwg files

96