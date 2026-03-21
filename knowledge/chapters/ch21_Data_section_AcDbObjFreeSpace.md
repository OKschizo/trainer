# Chapter 21: Data section AcDb:ObjFreeSpace

21 Data section AcDb:ObjFreeSpace
The meaning of this section is not completely known. The ODA knows how to write a valid section, but
the meaning is not known of every field.
### 21.1 Until R18
Type
Length
Description
Int32
4
0
UInt32
4
Approximate number of objects in the drawing (number of handles).
Julian
datetime
8
If version > R14 then system variable TDUPDATE otherwise
TDUUPDATE.
UInt32
4
Offset of the objects section in the stream.
UInt8
1
Number of 64-bit values that follow (ODA writes 4).
UInt32
4
ODA writes 0x00000032.
UInt32
4
ODA writes 0x00000000.
UInt32
4
ODA writes 0x00000064.
UInt32
4
ODA writes 0x00000000.
UInt32
4
ODA writes 0x00000200.
UInt32
4
ODA writes 0x00000000.
UInt32
4
ODA writes 0xffffffff.
UInt32
4
ODA writes 0x00000000.


Open Design Specification for .dwg files

250