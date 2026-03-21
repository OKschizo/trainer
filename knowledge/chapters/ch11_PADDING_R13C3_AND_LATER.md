# Chapter 11: PADDING (R13C3 AND LATER)

11  PADDING (R13C3 AND LATER)
0x200 bytes of padding. Can be ignored. When writing, the Open Design Toolkit writes all 0s.
Occasionally AutoCAD will use the first 4 bytes of this area to store the value of the “measurement”
variable. This padding was evidently required to allow pre-R13C3 versions of AutoCAD to read files
produced by R13C3 and later.

Open Design Specification for .dwg files

90


12 Data section: “”
The empty data section was introduced in R18. This section contains no data.

Section property
Value
Name
“”
Section ID
Always 0
Compressed
2
Page size
0x7400
Encrypted
0


Open Design Specification for .dwg files

91