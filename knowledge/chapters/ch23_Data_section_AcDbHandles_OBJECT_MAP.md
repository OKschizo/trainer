# Chapter 23: Data section AcDb:Handles (OBJECT MAP)

23 Data section AcDb:Handles (OBJECT MAP)
### 23.1 R13-15
The Object Map is a table which gives the location of each object in the file  This table is broken into
sections.  It is basically a list of handle/file loc pairs, and goes (something like) this:
Set the "last handle" to all 0 and the "last loc" to 0L;
Repeat until section size==2 (the last empty (except the CRC) section):
Short: size of this section.  Note this is in BIGENDIAN order (MSB
first)
Repeat until out of data for this section:
offset of this handle from last handle as modular char.
offset of location in file from last loc as modular char.  (note
that location offsets can be negative, if the terminating byte
has the 4 bit set).
End repeat.
CRC (most significant byte followed by least significant byte)
End of section
End top repeat
Note that each section is cut off at a maximum length of 2032.
### 23.2 R18
This section is compressed and contains the standard 32 byte section header.  The decompressed data in
this section is identical to the “Object Map” section data found in R15 and earlier files, excepts that
offsets are not absolute file addresses, but are instead offsets into the AcDb:Objects logical section
(starting with offset 0 at the beginning of this logical section).


Open Design Specification for .dwg files

252