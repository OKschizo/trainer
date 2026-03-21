# Chapter 22: Data section: AcDb:Template

22 Data section: AcDb:Template
This section is optional in releases 13-15. The section is mandatory in the releases 18 and newer. The
template section only contains the MEASUREMENT system variable.
Type
Length
Description
Int16
2
Template description string length in bytes (the ODA always writes
0 here).
byte[]
n
Encoded string bytes of the template description (use the drawing’s
codepage to encode the bytes).
UInt16
2
MEASUREMENT system variable (0 = English, 1 = Metric).



Open Design Specification for .dwg files

251