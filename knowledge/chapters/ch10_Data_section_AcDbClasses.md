# Chapter 10: Data section AcDb:Classes

10 Data section AcDb:Classes
### 10.1 R13-R15
This section contains the defined classes for the drawing.


SN : 0x8D 0xA1 0xC4 0xB8 0xC4 0xA9 0xF8 0xC5 0xC0 0xDC 0xF4 0x5F 0xE7 0xCF 0xB6 0x8A.

RL : size of class data area.
Then follows the class data:


BS : classnum

BS : version – in R14, becomes a flag indicating whether objects can be moved, edited,
etc.  We are still examining this.

TV : appname

TV : cplusplusclassname

TV : classdxfname

B : wasazombie

BS : itemclassid -- 0x1F2 for classes which produce entities, 0x1F3 for classes which
produce objects.
We read sets of these until we exhaust the data.


RS : CRC
This following 16-byte sentinel appears after the CRC:
0x72,0x5E,0x3B,0x47,0x3B,0x56,0x07,0x3A,0x3F,0x23,0x0B,0xA0,0x18,0x30,0x49,0x75
For R18 and later 8 unknown bytes follow. The ODA writes 0 bytes.
### 10.2 R18+
This section is compressed and contains the standard 32 byte section header.
This section contains the defined classes for the drawing.

Open Design Specification for .dwg files

87




SN : 0x8D 0xA1 0xC4 0xB8 0xC4 0xA9 0xF8 0xC5 0xC0 0xDC 0xF4 0x5F 0xE7 0xCF 0xB6 0x8A.

RL : size of class data area.
R2010+ (only present if the maintenance version is greater than 3!)

RL : unknown, possibly the high 32 bits of a 64-bit size?
R2004+

BS : Maxiumum class number

RC : 0x00

RC : 0x00

B : true
Then follows the class data (note that strings are in the string stream for R2007+):


BS : classnum

BS : Proxy flags:

Erase allowed = 1,
transform allowed = 2,
color change allowed = 4,
layer change allowed = 8,
line type change allowed = 16,
line type scale change allowed = 32,
visibility change allowed = 64,
cloning allowed = 128,
Lineweight change allowed = 256,
Plot Style Name change allowed = 512,
Disables proxy warning dialog = 1024,
is R13 format proxy= 32768

TV : appname

TV : cplusplusclassname

TV : classdxfname

B : wasazombie

BS : itemclassid -- 0x1F2 for classes which produce entities, 0x1F3 for classes which
produce objects.

BL : Number of objects created of this type in the current DB (DXF 91).

BS : Dwg Version

BS : Maintenance release version.

BL : Unknown (normally 0L)

BL : Unknown (normally 0L)
We read sets of these until we exhaust the data.


RS : CRC

Open Design Specification for .dwg files

88


This following 16-byte sentinel appears after the CRC:
0x72,0x5E,0x3B,0x47,0x3B,0x56,0x07,0x3A,0x3F,0x23,0x0B,0xA0,0x18,0x30,0x49,0x75


Open Design Specification for .dwg files

89