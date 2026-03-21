# Chapter 20: Data section AcDb:AcDbObjects

20 Data section AcDb:AcDbObjects
Section property
Value
Name
AcDb:AcDbObjects
Compressed
2
Encrypted
0 if not encrypted, 1 if encrypted
Page size
0x7400
This region holds the actual objects in the drawing. These can be entities, table entries, dictionary entries,
and objects. This second use of objects is somewhat confusing; all items stored in the file are “objects”,
but only some of them are object objects. Others are entities, table entries, etc. The objects in this section
can appear in any order.
Not all objects present in the file are actually used. All used objects can eventually be traced back to
handle references in the Header section. So the proper way to read a file is to start reading the header and
then tracing all references from there until all references have been followed. Very occasionally a file
contains e.g. two APPID objects with the same name, of which one is used, and the other is not. Reading
both would be incorrect due to a name clash. To complicate matters more, files also exist with table
records with duplicate names. This is incorrect, and the software should rename the record to be unique
upon reading.
For R18 and later the section data (right after the page header) starts with a RL value of 0x0dca (meaning
unknown).
### 20.1 Common non-entity object format
Objects (non-entities) have the following general format:
Version
Field
type
DXF
grou
p
Description

MS

Size in bytes of object, not including the CRC
R2010+

MC

Size in bits of the handle stream (unsigned, 0x40 is not interpreted as
sign). This includes the padding bits at the end of the handle stream (the
padding bits make sure the object stream ends on a byte boundary).
Commmon

OT

Object type
R2000-R2007

RL

Size of object data in bits (number of bits before the handles), or the
“endbit” of the pre-handles section.
Common:

Open Design Specification for .dwg files

104



H
5
Object’s handle

BS

Size of extended object data, if any

X

Extended object data, if any. See EED section, chapter 28.
R13-R14

RL

Size of object data in bits

BL

Number of persistent reactors attached to this object
R2004+

B

If 1, no XDictionary handle is stored for this object, otherwise
XDictionary handle is stored as in R2000 and earlier.
R2013+

B

Indicates whether the object has associated binary data in the data store
section (see chapter 24 for more details about this section).
Common

X

Object data (varies by type of object)
R2007+

X

String data (optional)

B

String stream present bit (last bit in pre-handles section). If 1, then the
“endbit” location should be decremented by 16 bytes, and a short should
be read at location endbit – 128 (bits), call this short strDataSize.  If this
short has the 0x8000 bit set, then decrement endbit by an additional 16
bytes, strip the 0x8000 bit off of strDataSize, and read the short at this
new location, calling it hiSize.  Then set strDataSize to (strDataSize |
(hiSize << 15)).  “endbit” should then be decremented by this final
strDataSize value, and this bit location marks the start of the
“string stream” within this object.  All unicode strings in this object are
located in the “string stream”, and should be read from this stream, even
though the location of the TV type fields in the object descriptions list
these fields in among the normal object data.
Common



Below begins the handles stream, this begins at offset specified by number
of bits before handles above

H

Parent handle (soft pointer)

H

[Reactors (soft pointer)], repeated as many times as specified by the
number of persistent reactors

H

xdictionary (hard owner), present if the has xdictionary flag is true

X

Object specific handles

B*

Padding bits are added until the next byte boundary is reached.

RS

CRC

The CRC includes the size bytes.
### 20.2 Common entity format
Drawing entities, which are of course objects, have the same format as objects, with some additional
standard items:


MS : Size of object, not including the CRC

Open Design Specification for .dwg files

105


R2010+:

MC : Size in bits of the handle stream (unsigned, 0x40 is not interpreted as sign).
Commmon:

OT : Object type
R2000+ Only:

RL : Size of object data in bits
Common:

H : Object’s handle

BS : Size of extended object data, if any

X : Extended object data, if any

B : Flag indicating presence of graphic image.

if (graphicimageflag is 1) {
R13-R007:

RL: Size of graphic image in bytes
R2010+:

BLL: Size of graphic image in bytes
Common:

X: The graphic image

}
R13-R14 Only:

RL : Size of object data in bits

6B : Flags

6B : Common parameters
R2000+ Only:

B : 0 if the previous and next linkers are present; 1 if they are BOTH defaults (1
back and 1 forward).

ENC : Entity color

BD : Linetype Scale

BB : Line type flags

00 – BYLAYER linetype

01 – BYBLOCK linetype

10 – CONTINUOUS linetype

11 – Indicates that a linetype handle will be stored in the handles section of the
entity.

BB : Plotstyle flags:

00 – BYLAYER plotstyle

01 – BYBLOCK plotstyle

10 – CONTINUOUS plotstyle

11 – Indicates that a plotstyle handle will be stored in the handles section of
the entity.
R2007+:

Open Design Specification for .dwg files

106



BB : Material flags:

00 – BYLAYER material

01 – BYBLOCK material

10 – global material?

11 – Indicates that a material handle will be stored in the handles section of the
entity.

RC : Shadow flags
R2010+:

B : Has full visual style

B : Has face visual style

B : Has edge visual style
Common:

BS : Invisible flag (bit 0: 0 = visible, 1 = invisible)
R2000+:

RC : Entity lineweight flag
Common:

X : Object data (varies by type of object)

X : Handles associated with this object

B* : Padding bits are added until the next byte boundary is reached.

RS : CRC
The R13-R14 FLAGS area (6 bits) indicates which handle references are present in the HANDLE REFS
area. They are as follows:
FEDCBA

FE : Entity mode (entmode).  Generally, this indicates whether or not the owner
relative handle reference is present.  The values go as follows:

00 : The owner relative handle reference is present.
Applies to the following:
VERTEX, ATTRIB, and SEQEND.
BLOCK, ENDBLK, and the defining entities in all
block defs except *MODEL_SPACE and *PAPER_SPACE.

01 : PSPACE entity without a owner relative handle ref.

10 : MSPACE entity without a owner relative handle ref.

11 : Not used.


DC : This is the number of reactors attached to an entity as a bitshort. This feature
may have been dormant in R13, but it appears in R14, and in files saved as R13 by
R14.

B : 0 if a linetype reference is present; 1 if it's not (the default being BYLAYER --
even though there IS a BYLAYER linetype entity and it has a handle).

A : 0 if the previous and next linkers are present; 1 if they are BOTH defaults (1
back and 1 forward).

Open Design Specification for .dwg files

107


The COMMON PARAMETERS (6 bits):
CCSSII

CC : Color bitshort

SS : Linetype scale bitdouble

II : "Invisible" flag bitshort (bit 0: 0 = visible, 1 = invisible).
The ENTITY-SPECIFIC PARAMETERS area is coded with bitcodes. Each entity has its own parameter
prescription. Some parameters ALWAYS appear in raw form -- even if bitcode abbreviations could be
used (the 10 and 11 points in TEXT, for example). Generally the raw form is used in conditions wherein
it cannot reasonably be assumed that the likely value for the particular parameter is one of the
compressible values.
One method for loading these objects is to follow the object map.  Doing so will cause each object to be
loaded once and only once. Alternatively one can try to scan the objects as they are found, and replace
objects with duplicated object handles with the ones found later in the file. The Teigha Classic for .dwg
files Toolkit uses a hybrid approach, loading the control objects first, then the objects they contain.
### 20.3 Object types
Some object types have fixed values, others have values which vary with the drawing. Here are the fixed
values:



UNUSED
0
RAY
0x28

TEXT
1
XLINE
0x29

ATTRIB
2
DICTIONARY
0x2A

ATTDEF
3
OLEFRAME
0x2B

BLOCK
4
MTEXT
0x2C

ENDBLK
5
LEADER
0x2D

SEQEND
6
TOLERANCE
0x2E

INSERT
7
MLINE
0x2F

MINSERT
8
BLOCK CONTROL OBJ
0x30


9
BLOCK HEADER
0x31

VERTEX (2D)
0x0A
LAYER CONTROL OBJ
0x32

VERTEX (3D)
0x0B
LAYER
0x33

VERTEX (MESH)
0x0C
STYLE CONTROL OBJ
0x34

VERTEX (PFACE)
0x0D
STYLE
0x35

VERTEX (PFACE FACE)
0x0E

0x36

POLYLINE (2D)
0x0F

0x37

POLYLINE (3D)
0x10
LTYPE CONTROL OBJ
0x38

ARC
0x11
LTYPE
0x39

Open Design Specification for .dwg files

108



CIRCLE
0x12

0x3A

LINE
0x13

0x3B

DIMENSION (ORDINATE) 0x14
VIEW CONTROL OBJ
0x3C

DIMENSION (LINEAR)
0x15
VIEW
0x3D

DIMENSION (ALIGNED)
0x16
UCS CONTROL OBJ
0x3E

DIMENSION (ANG 3-Pt) 0x17
UCS
0x3F

DIMENSION (ANG 2-Ln) 0x18
VPORT CONTROL OBJ
0x40

DIMENSION (RADIUS)
0x19
VPORT
0x41

DIMENSION (DIAMETER) 0x1A
APPID CONTROL OBJ
0x42

POINT
0x1B
APPID
0x43

3DFACE
0x1C
DIMSTYLE CONTROL OBJ 0x44

POLYLINE (PFACE)
0x1D
DIMSTYLE
0x45

POLYLINE (MESH)
0x1E
VP ENT HDR CTRL OBJ
0x46

SOLID
0x1F
VP ENT HDR
0x47

TRACE
0x20
GROUP
0x48

SHAPE
0x21
MLINESTYLE
0x49

VIEWPORT
0x22
OLE2FRAME
0x4A

ELLIPSE
0x23
(DUMMY)
0x4B

SPLINE
0x24
LONG_TRANSACTION
0x4C

REGION
0x25
LWPOLYLINE
0x4D

3DSOLID
0x26
HATCH
0x4E

BODY
0x27
XRECORD
0x4F



ACDBPLACEHOLDER
0x50



VBA_PROJECT
0x51



LAYOUT
0x52



ACAD_PROXY_ENTITY
0x1f2



ACAD_PROXY_OBJECT
0x1f3
There are a number of objects with non-fixed values. These are:
ACAD_TABLE
CELLSTYLEMAP
DBCOLOR
DICTIONARYVAR
DICTIONARYWDFLT
FIELD
GROUP
HATCH
IDBUFFER
IMAGE
IMAGEDEF
IMAGEDEFREACTOR
LAYER_INDEX
LAYOUT
LWPLINE
MATERIAL

Open Design Specification for .dwg files

109


MLEADER
MLEADERSTYLE
OLE2FRAME
PLACEHOLDER
PLOTSETTINGS
RASTERVARIABLES
SCALE
SORTENTSTABLE
SPATIAL_FILTER
SPATIAL_INDEX
TABLEGEOMETRY
TABLESTYLES
VBA_PROJECT
VISUALSTYLE
WIPEOUTVARIABLE
XRECORD
For objects with non-fixed values, taking the object type minus 500 gives an index into the class list,
which then determines the type of object.  For instance, an object type of 501 means that this object is of
the class which is second in the class list; the classdxfname field determines the type of the object.
See the sections on EED a description of that areas.
### 20.4 OBJECT PRESCRIPTIONS
The object prescriptions are given in the following form:
ITEM    TYPE-CODE    DXF-CODE    DESCRIPTION
See the top of this document for the key to the data types used here.

#### 20.4.1 Common Entity Data
The following data appears at the beginning of each entity in the file, and will be referred to as Common
Entity Data in the subsequent entity descriptions.

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
1 (internal DWG type code).
R2000+ Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
code 0, length followed by the handle bytes.

EED size
BS

size of extended entity data, if any

EED
X
-3
See EED section.

Graphic present Flag
B

1 if a graphic is present

Graphics
X

if graphicpresentflag is 1, the graphic goes here.

Open Design Specification for .dwg files

110





See the section on Proxy Entity Graphics for the
format of this section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Entmode
BB

entity mode

Numreactors
BL

number of persistent reactors attached to this
object
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
R2013+:

Has DS binary data
B

If 1 then this object has associated binary data
stored in the data store. See for more details
chapter 24.
R13-R14 Only:

Isbylayerlt
B

1 if bylayer linetype, else 0
Common:

Nolinks
B

1 if major links are assumed +1, -1, else 0




For R2004+ this always has value 1




(links are not used)

Color
CMC(B)
62

Ltype scale
BD
48
R2000+:

Ltype flags
BB

00 = bylayer, 01 = byblock, 10 = continous, 11 =
linetype handle present at end of object

Plotstyle flags
BB

00 = bylayer, 01 = byblock, 11 = plotstyle handle
present at end of object
R2007+:

Material flags
BB

00 = bylayer, 01 = byblock, 11 = material handle
present at end of object

Shadow flags
RC
Common:

Invisibility
BS
60
R2000+:

Lineweight
RC
370

#### 20.4.2 Common Entity Handle Data
The following data appears in the handles section of each entity, and will be referred to as Common
Entity Handle Data in the subsequent entity descriptions.
Handle refs

Open Design Specification for .dwg files

111




[Owner ref handle (soft pointer)]


[Reactors (soft pointer)]


xdicobjhandle  (hard owner)
R13-R14 Only:

8 LAYER (hard pointer)

6 [LTYPE (hard pointer)] (present if Isbylayerlt is 0)
R13-R2000 Only:


previous/next handles present if Nolinks is 0


[PREVIOUS ENTITY (relative soft pointer)]


[NEXT ENTITY (relative soft pointer)]
R2004+:


[Color book color handle (hard pointer)]
R2000+ Only:

8 LAYER (hard pointer)

6 [LTYPE (hard pointer)] present if linetype flags


were 11
R2007+:


MATERIAL present if material flags were 11
R2000+:


PLOTSTYLE (hard pointer) present if plotstyle flags


were 11
R2010+:

If has full visual style, the full visual style handle (hard pointer).

If has face visual style, the face visual style handle (hard pointer).

If has edge visual style, the full visual style handle (hard pointer).

#### 20.4.3 TEXT (1)

Common Entity Data
R13-14 Only:

Elevation
BD
---

Insertion pt
2RD
10

Alignment pt
2RD
11

Extrusion
3BD
210

Thickness
BD
39

Oblique ang
BD
51

Rotation ang
BD
50

Height
BD
40

Width factor
BD
41

Text value
TV
1

Open Design Specification for .dwg files

112



Generation
BS
71

Horiz align.
BS
72

Vert align.
BS
73
R2000+ Only:

DataFlags
RC

Used to determine presence of subsquent data

Elevation
RD
---
present if !(DataFlags & 0x01)

Insertion pt
2RD
10


Alignment pt
2DD
11
present if !(DataFlags & 0x02), use 10 & 20 values
for 2 default values.

Extrusion
BE
210


Thickness
BT
39


Oblique ang
RD
51
present if !(DataFlags & 0x04)

Rotation ang
RD
50
present if !(DataFlags & 0x08)

Height
RD
40


Width factor
RD
41
present if !(DataFlags & 0x10)

Text value
TV
1

Generation
BS
71
present if !(DataFlags & 0x20)

Horiz align.
BS
72
present if !(DataFlags & 0x40)

Vert align.
BS
73
present if !(DataFlags & 0x80)
Common:

Common Entity Handle Data


H
7
STYLE (hard pointer)


CRC
X
---
##### 20.4.3.1 R14 Example:
OBJECT: text (1H), len 49H (73), handle: 4C    00559 49 00                     I.         0100 1001 0000 0000
0055B 40 40 53 20 58 10 00 05   @@S X...   0100 0000 0100 0000 0101 0011 0010 0000 0101 1000 0001 0000 0000 0000 0000 0101
00563 5B 40 00 00 00 00 00 01   [@......   0101 1011 0100 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001
0056B 08 00 00 00 00 00 00 02   ........   0000 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0010
00573 08 00 00 00 00 00 00 00   ........   0000 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
0057B 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
00583 00 14 D4 4D 4C CC CC CC   ...ML...   0000 0000 0001 0100 1101 0100 0100 1101 0100 1100 1100 1100 1100 1100 1100 1100
0058B CC E4 9F A8 63 A3 43 4B   ....c.CK   1100 1100 1110 0100 1001 1111 1010 1000 0110 0011 1010 0011 0100 0011 0100 1011
00593 99 03 4B 99 03 A3 2B C3   ..K...+.   1001 1001 0000 0011 0100 1011 1001 1001 0000 0011 1010 0011 0010 1011 1100 0011
0059B A5 46 0A 21 E8 08 0A 22   .F.!..."   1010 0101 0100 0110 0000 1010 0010 0001 1110 1000 0000 1000 0000 1010 0010 0010
005A3 00                        .          0000 0000
005A4 C9 72                     crc
ENDOBJECT
#### 20.4.4 ATTRIB (2)

Common TEXT Entity Data
R2010+:

Version
RC
?
R2018+:

Open Design Specification for .dwg files

113



Attribute type
RC
71
1 = Single line,




2 = Multi line (ATTRIB),




4 = Multie line (ATTDEF)
IF Attribute type is multi line

MTEXT fields
…

Here all fields of an embedded MTEXT object




are written, starting from the Entmode




(entity mode). The owner handle can be 0.





For DXF this is marked with <101, Embedded Object>,




Followed by the MTEXT fields, starting with the




Insertion point (group 10).

Annotative data size
BS
IF Annotative data size greater than zero

Annotative data bytes RC

Byte array with length Annotative data size.

Registered application H

Hard pointer.

Unknown
BS
72?
Value 0.
END IF

Tag string
VT
2

Unknown
BS
73?
Value 0

Flags
RC
70
0 = None,




1 = Invisible,




2 = Constant,




4 = Input verification required,




8 = Preset

Lock position
B
280
END IF
Common:
IF Attribute type is single line

Tag
TV
2

Field length
BS
73
unused

Flags
RC
70
NOT bit-pair-coded.
R2007+:

Lock position flag
B
280
END IF (single line)

Common:

CRC
X
---
##### 20.4.4.1 R14 Example:
OBJECT: attrib (2H), len 58H (88), handle: 52

Open Design Specification for .dwg files

114


00614 58 00                     X.         0101 1000 0000 0000
00616 40 80 54 A3 F8 10 00 01   @.T.....   0100 0000 1000 0000 0101 0100 1010 0011 1111 1000 0001 0000 0000 0000 0000 0001
0061E 5B 40 00 00 00 00 00 02   [@......   0101 1011 0100 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0010
00626 88 00 00 00 00 00 00 03   ........   1000 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0011
0062E 88 00 00 00 00 00 00 00   ........   1000 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
00636 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
0063E 00 14 D4 4D CC CC CC CC   ...M....   0000 0000 0001 0100 1101 0100 0100 1101 1100 1100 1100 1100 1100 1100 1100 1100
00646 CC E4 9F 9F FF FF FF FF   ........   1100 1100 1110 0100 1001 1111 1001 1111 1111 1111 1111 1111 1111 1111 1111 1111
0064E FF FD E7 E8 5B 6B CB 0B   ....[k..   1111 1111 1111 1101 1110 0111 1110 1000 0101 1011 0110 1011 1100 1011 0000 1011
00656 A3 A1 03 B3 0B 63 AB 2D   .....c.-   1010 0011 1010 0001 0000 0011 1011 0011 0000 1011 0110 0011 1010 1011 0010 1101
0065E 48 2A 6A CA 0A A2 A4 01   H*j.....   0100 1000 0010 1010 0110 1010 1100 1010 0000 1010 1010 0010 1010 0100 0000 0001
00666 00 60 A2 1E 80 80 A2 21   .`.....!   0000 0000 0110 0000 1010 0010 0001 1110 1000 0000 1000 0000 1010 0010 0010 0001

0066E 6F A6                     crc
#### 20.4.5 ATTDEF (3)

Common ATTRIB Entity Data
R2010+:

Version
RC
?

Common:

Prompt
TV
3


CRC
X
---
20.4.5.1
R14 Example:
spec3.dwg

OBJECT: attdef (3H), len 50H (80), handle: 4C

00559 50 00                     P.         0101 0000 0000 0000

0055B 40 C0 53 22 08 10 00 05   @.S"....   0100 0000 1100 0000 0101 0011 0010 0010 0000 1000 0001 0000 0000 0000 0000 0101

00563 5B 40 00 00 00 00 00 01   [@......   0101 1011 0100 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001

0056B 08 00 00 00 00 00 00 02   ........   0000 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0010

00573 08 00 00 00 00 00 00 00   ........   0000 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

0057B 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

00583 00 14 D4 4D 4C CC CC CC   ...ML...   0000 0000 0001 0100 1101 0100 0100 1101 0100 1100 1100 1100 1100 1100 1100 1100

0058B CC E4 9F B5 48 2A 6A CA   ....H*j.   1100 1100 1110 0100 1001 1111 1011 0101 0100 1000 0010 1010 0110 1010 1100 1010

00593 0A A2 A4 00 85 A2 B7 3A   .......:   0000 1010 1010 0010 1010 0100 0000 0000 1000 0101 1010 0010 1011 0111 0011 1010

0059B 32 B9 10 36 BC B0 BA 3A   2..6...:   0011 0010 1011 1001 0001 0000 0011 0110 1011 1100 1011 0000 1011 1010 0011 1010

005A3 18 28 87 A0 20 28 88 00   .(.. (..   0001 1000 0010 1000 1000 0111 1010 0000 0010 0000 0010 1000 1000 1000 0000 0000

005AB 78 53                     crc
#### 20.4.6 BLOCK (4)

Common Entity Data

Open Design Specification for .dwg files

115



Block name
TV
2

Common Entity Handle Data

CRC
X
---
##### 20.4.6.1 Example:
OBJECT: block (4H), len 16H (22), handle: 4E
00BC2 16 00                     ..         0001 0110 0000 0000
00BC4 41 00 53 A3 D8 00 00 01   A.S.....   0100 0001 0000 0000 0101 0011 1010 0011 1101 1000 0000 0000 0000 0000 0000 0001
00BCC 5B 20 A9 AB 28 49 89 70   [ ..(I.p   0101 1011 0010 0000 1010 1001 1010 1011 0010 1000 0100 1001 1000 1001 0111 0000
00BD4 06 0A 21 E8 08 00         ..!...     0000 0110 0000 1010 0010 0001 1110 1000 0000 1000 0000 0000
00BDA 39 F3                     crc
NOTES:  The BLOCK_RECORD entity seems to have all the goodies that show up in a BLOCK entget -
- except for the common parameters.  The actual BLOCK entity seems to be almost a dummy.
#### 20.4.7 ENDBLK (5)

Common Entity Data

Common Entity Handle Data

CRC
X
---
##### 20.4.7.1 Example:
OBJECT: endblk (5H), len FH (15), handle: 1B
00685 0F 00                     ..         0000 1111 0000 0000
00687 41 40 46 E2 48 00 00 05   A@F.H...   0100 0001 0100 0000 0100 0110 1110 0010 0100 1000 0000 0000 0000 0000 0000 0101
0068F 5B 18 28 87 A0 20 20      [.(..      0101 1011 0001 1000 0010 1000 1000 0111 1010 0000 0010 0000 0010 0000
00696 2E 8B                     crc
#### 20.4.8 SEQEND (6)

Common Entity Data

Common Entity Handle Data

CRC
X
---
##### 20.4.8.1 Example:
OBJECT: seqend (6H), len 11H (17), handle: 53
00670 11 00                     ..         0001 0001 0000 0000
00672 41 80 54 E2 48 00 00 01   A.T.H...   0100 0001 1000 0000 0101 0100 1110 0010 0100 1000 0000 0000 0000 0000 0000 0001
0067A 5B 60 81 18 28 87 A0 20   [`..(..    0101 1011 0110 0000 1000 0001 0001 1000 0010 1000 1000 0111 1010 0000 0010 0000
00682 08                        .          0000 1000
00683 88 C7                     crc
#### 20.4.9 INSERT (7)

Common Entity Data

Ins pt
3BD
10
R13-R14 Only:

X Scale
BD
41

Y Scale
BD
42

Open Design Specification for .dwg files

116



Z Scale
BD
43
R2000+ Only:

Data flags
BB



Scale Data


Varies with Data flags:




11 - scale is (1.0, 1.0, 1.0), no data stored.




01 – 41 value is 1.0, 2 DD’s are present, each using
### 1.0 as the default value, representing the 42 and 43
values.




10 – 41 value stored as a RD, and 42 & 43 values are
not stored, assumed equal to 41 value.




00 – 41 value stored as a RD, followed by a 42 value
stored as DD (use 41 for default value), and a 43
value stored as a DD (use 41 value for default
value).
Common:

Rotation
BD
50

Extrusion
3BD
210

Has ATTRIBs
B
66
Single bit; 1 if ATTRIBs follow.
R2004+:

Owned Object Count
BL

Number of objects owned by this object.
Common:

Common Entity Handle Data


H
2
BLOCK HEADER (hard pointer)
R13-R200:


H

[1st ATTRIB (soft pointer)]  if 66 bit set; can be
NULL


H

[last ATTRIB](soft pointer)] if 66 bit set; can be
NULL
R2004:


H

[ATTRIB (hard owner)] Repeats “Owned Object Count”
times.
Common:


H

[SEQEND (hard owner)]      if 66 bit set

CRC
X
---
##### 20.4.9.1 R14 Example:
OBJECT: insert (7H), len 29H (41), handle: 51
005E7 29 00                     ).         0010 1001 0000 0000    005E9 41 C0 54 66 F0 00 00 05   A.Tf....   0100 0001 1100 0000 0101
0100 0110 0110 1111 0000 0000 0000 0000 0000 0000 0101
005F1 5B 00 00 00 00 00 00 01   [.......   0101 1011 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001
005F9 08 00 00 00 00 00 00 00   ........   0000 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
00601 82 04 AD 4C C1 44 3D 01   ...L.D=.   1000 0010 0000 0100 1010 1101 0100 1100 1100 0001 0100 0100 0011 1101 0000 0001
00609 01 45 35 05 49 05 48 C5   .E5.I.H.   0000 0001 0100 0101 0011 0101 0000 0101 0100 1001 0000 0101 0100 1000 1100 0101
00611 4C                        L          0100 1100
00612 CB 54                     crc

Open Design Specification for .dwg files

117


#### 20.4.10 MINSERT (8)

Common Entity Data

Ins pt
3BD
10
R13-R14 Only:

X Scale
BD
41

Y Scale
BD
42

Z Scale
BD
43
R2000+ Only:

Data flags
BB



Scale Data


Varies with Data flags:




11 - scale is (1.0, 1.0, 1.0), no data stored.




01 – 41 value is 1.0, 2 DD’s are present, each using
### 1.0 as the default value, representing the 42 and 43
values.




10 – 41 value stored as a RD, and 42 & 43 values are
not stored, assumed equal to 41 value.




00 – 41 value stored as a RD, followed by a 42 value
stored as DD (use 41 for default value), and a 43
value stored as a DD (use 41 value for default
value).
Common:

Rotation
BD
50

Extrusion
3BD
210

Has ATTRIBs
B
66
Single bit; 1 if ATTRIBs follow.
R2004+:

Owned Object Count
BL

Number of objects owned by this object.
Common:

Numcols
BS
70

Numrows
BS
71

Col spacing
BD
44

Row spacing
BD
45

Common Entity Handle Data


H
2
BLOCK HEADER (hard pointer)
R13-R2000:


H

[1st  ATTRIB (soft pointer)]  if 66 bit set; can be
NULL


H

[last ATTRIB](soft pointer)]  if 66 bit set; can be
NULL
R2004+:


H

[ATTRIB (soft pointer)] Repeats “Owned Object Count”
times.
Common:


H

[SEQEND (hard owner)]       if 66 bit set

Open Design Specification for .dwg files

118



CRC
X
---
##### 20.4.10.1 R14 Example:
OBJECT: minsert (8H), len 36H (54), handle: 59
0069E 36 00                     6.         0011 0110 0000 0000
006A0 42 00 56 63 B0 08 00 05   B.Vc....   0100 0010 0000 0000 0101 0110 0110 0011 1011 0000 0000 1000 0000 0000 0000 0101
006A8 5B 00 00 00 00 00 00 00   [.......   0101 1011 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
006B0 08 00 00 00 00 00 00 00   ........   0000 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
006B8 42 04 AD 49 04 40 C0 00   B..I.@..   0100 0010 0000 0100 1010 1101 0100 1001 0000 0100 0100 0000 1100 0000 0000 0000
006C0 00 00 00 00 00 84 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 1000 0100 0000 0000 0000 0000
006C8 00 00 00 00 00 01 00 C1   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001 0000 0000 1100 0001
006D0 44 3D 01 01 45 44         D=..ED     0100 0100 0011 1101 0000 0001 0000 0001 0100 0101 0100 0100
006D6 84 2E                     crc
#### 20.4.11 VERTEX (2D) (10)

Common Entity Data

Flags
EC
70
NOT bit-pair-coded.

Point
3BD
10
NOTE THAT THE Z SEEMS TO ALWAYS BE 0.0! The Z must
be taken from the 2D POLYLINE elevation.

Start width
BD
40
If it's negative, use the abs val for start AND end
widths (and note that no end width will be present).
This is a compression trick for cases where the
start and end widths are identical and non-0.

End width
BD
41
Not present if the start width is < 0.0; see above.

Bulge
BD
42
R2010+:

Vertex ID
BL
91
Common:

Tangent dir
BD
50

Common Entity Handle Data

CRC
X
---
20.4.11.1
Example:
OBJECT: pline vert (AH), len 22H (34), handle: 4D

00B39 22 00                     ".         0010 0010 0000 0000

00B3B 42 80 53 66 F8 00 00 01   B.Sf....   0100 0010 1000 0000 0101 0011 0110 0110 1111 1000 0000 0000 0000 0000 0000 0001

00B43 5B 00 00 00 00 00 00 00   [.......   0101 1011 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

00B4B 00 08 00 00 00 00 00 00   ........   0000 0000 0000 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

00B53 00 02 05 55 00 60 A2 1E   ...U.`..   0000 0000 0000 0010 0000 0101 0101 0101 0000 0000 0110 0000 1010 0010 0001 1110

00B5B 80 C1                     ..         1000 0000 1100 0001

00B5D B2 FC                     crc
NOTES:  Neither elevation nor thickness are present in the 2D VERTEX data. Both should be taken from
the 2D POLYLINE entity (15).

Open Design Specification for .dwg files

119


#### 20.4.12 VERTEX (3D) (11)

Common Entity Data

Flags
EC
70
NOT bit-pair-coded.

Point
3BD
10

Common Entity Handle Data

CRC
X
---
##### 20.4.12.1 Example:
OBJECT: 3d pline vert (BH), len 1AH (26), handle: 62

00D74 1A 00                     ..         0001 1010 0000 0000

00D76 42 C0 58 A4 B8 00 00 01   B.X.....   0100 0010 1100 0000 0101 1000 1010 0100 1011 1000 0000 0000 0000 0000 0000 0001

00D7E 5B 10 00 00 00 00 00 00   [.......   0101 1011 0001 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

00D86 00 08 0D 82 08 60 A2 1F   .....`..   0000 0000 0000 1000 0000 1101 1000 0010 0000 1000 0110 0000 1010 0010 0001 1111

00D8E 00 80                     ..         0000 0000 1000 0000

00D90 8C 03                     crc
#### 20.4.13 VERTEX (MESH) (12)
Same as VERTEX (3D) (11) except for type code.
##### 20.4.13.1 Example:
OBJECT: 3d surf sol vert (CH), len 21H (33), handle: 67

00E36 21 00                     !.         0010 0001 0000 0000

00E38 43 00 59 E6 B8 00 00 01   C.Y.....   0100 0011 0000 0000 0101 1001 1110 0110 1011 1000 0000 0000 0000 0000 0000 0001

00E40 5B 20 19 1D 70 D1 7F E3   [ ..p...   0101 1011 0010 0000 0001 1001 0001 1101 0111 0000 1101 0001 0111 1111 1110 0011

00E48 FF 47 E1 72 DB 05 A8 C4   .G.r....   1111 1111 0100 0111 1110 0001 0111 0010 1101 1011 0000 0101 1010 1000 1100 0100

00E50 58 CA 05 00 60 A2 1E 80   X...`...   0101 1000 1100 1010 0000 0101 0000 0000 0110 0000 1010 0010 0001 1110 1000 0000

00E58 C0                        .          1100 0000

00E59 B3 50                     crc
#### 20.4.14 VERTEX (PFACE) (13)
Same as VERTEX (3D) (11) except for type code.
R13 .dwg files seem to have color and linetype data for all PFACE VERTEXs (both types), but R12 and
SAVEASR12 seem to omit color and linetype when writing out the location VERTEXs.
##### 20.4.14.1 Example:
OBJECT: pface pt (DH), len 21H (33), handle: 56

00BDD 21 00                     !.         0010 0001 0000 0000

Open Design Specification for .dwg files

120



00BDF 43 40 55 A6 B8 00 00 01   C@U.....   0100 0011 0100 0000 0101 0101 1010 0110 1011 1000 0000 0000 0000 0000 0000 0001

00BE7 5B 60 20 00 00 00 00 00   [` .....   0101 1011 0110 0000 0010 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

00BEF 00 02 00 00 00 00 00 00   ........   0000 0000 0000 0010 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

00BF7 00 10 81 00 60 A2 1E 80   ....`...   0000 0000 0001 0000 1000 0001 0000 0000 0110 0000 1010 0010 0001 1110 1000 0000

00BFF C1                        .          1100 0001

00C00 3D 1E                     crc
#### 20.4.15 VERTEX (PFACE FACE) (14)

Common Entity Data

Vert index
BS
71
1-based vertex index (see DXF doc)

Vert index
BS
72
1-based vertex index (see DXF doc)

Vert index
BS
73
1-based vertex index (see DXF doc)

Vert index
BS
74
1-based vertex index (see DXF doc)

Common Entity Handle Data

CRC
X
---
20.4.15.1
Example:
OBJECT: pface face def (EH), len 13H (19), handle: 5A

00C7E 13 00                     ..         0001 0011 0000 0000

00C80 43 80 56 A3 48 00 00 01   C.V.H...   0100 0011 1000 0000 0101 0110 1010 0011 0100 1000 0000 0000 0000 0000 0000 0001

00C88 7B 20 28 1A 05 60 82 98   { (..`..   0111 1011 0010 0000 0010 1000 0001 1010 0000 0101 0110 0000 1000 0010 1001 1000

00C90 28 87 80                  (..        0010 1000 1000 0111 1000 0000

00C93 C3 BA                     crc
#### 20.4.16 2D POLYLINE (15)

Common Entity Data

Flags
BS
70

Curve type
BS
75
Curve and smooth surface type.

Start width
BD
40
Default start width

End width
BD
41
Default end width

Thickness
BT
39

Elevation
BD
10
The 10-pt is (0,0,elev)

Extrusion
BE
210
R2004+:

Owned Object Count
BL

Number of objects owned by this object.
Common:

Common Entity Handle Data

Open Design Specification for .dwg files

121


R13-R2000:


H

1st  VERTEX (soft pointer)


H

last VERTEX ( soft pointer)
R2004+:


H

[VERTEX (hard owner)] Repeats “Owned Object Count”
times.
Common:


H

SEQEND (hard owner)

CRC
X
---
##### 20.4.16.1 R14 Example:
OBJECT: pline st (FH), len 18H (24), handle: 4C

00B1D 18 00                     ..         0001 1000 0000 0000

00B1F 43 C0 53 22 D8 00 00 05   C.S"....   0100 0011 1100 0000 0101 0011 0010 0010 1101 1000 0000 0000 0000 0000 0000 0101

00B27 5B 55 55 26 0A 21 E8 14   [UU&.!..   0101 1011 0101 0101 0101 0101 0010 0110 0000 1010 0010 0001 1110 1000 0001 0100

00B2F 21 28 29 A8 29 E6 2A 01   !().).*.   0010 0001 0010 1000 0010 1001 1010 1000 0010 1001 1110 0110 0010 1010 0000 0001

00B37 13 EA                     crc
#### 20.4.17 3D POLYLINE (16)

Common Entity Data

Flags
RC
70
NOT DIRECTLY THE 75.  Bit-coded (76543210):



75
0 : Splined (75 value is 5)




1 : Splined (75 value is 6)




(If either is set, set 70 bit 2 (4) to indicate
splined.)

Flags
RC
70
NOT DIRECTLY THE 70.  Bit-coded (76543210):




0 : Closed (70 bit 0 (1))




(Set 70 bit 3 (8) because this is a 3D POLYLINE.)
R2004+:

Owned Object Count
BL

Number of objects owned by this object.
Common:

Common Entity Handle Data
R13-R2000:


H

first VERTEX (soft pointer)


H

last  VERTEX (soft pointer)
R2004+:


H

[VERTEX (hard owner)] Repeats “Owned Object Count”
times.
Common:


H

SEQEND (hard owner)

Open Design Specification for .dwg files

122



CRC
X
---
##### 20.4.17.1 Example:
OBJECT: 3d poly start (10H), len 19H (25), handle: 5E

00CDA 19 00                     ..         0001 1001 0000 0000

00CDC 44 00 57 A2 C8 00 00 05   D.W.....   0100 0100 0000 0000 0101 0111 1010 0010 1100 1000 0000 0000 0000 0000 0000 0101

00CE4 5B 00 00 18 28 87 E0 84   [...(...   0101 1011 0000 0000 0000 0000 0001 1000 0010 1000 1000 0111 1110 0000 1000 0100

00CEC D0 83 20 AF A0 B1 18 B1   .. .....   1101 0000 1000 0011 0010 0000 1010 1111 1010 0000 1011 0001 0001 1000 1011 0001

00CF4 80                        .          1000 0000

00CF5 4A A6                     crc
#### 20.4.18 ARC (17)

Common Entity Data

Center
3BD
10

Radius
BD
40

Thickness
BT
39

Extrusion
BE
210

Start angle
BD
50

End   angle
BD
51

Common Entity Handle Data

CRC
X
---
##### 20.4.18.1 R14 Example:
OBJECT: arc (11H), len 3AH (58), handle: 64

00DA7 3A 00                     :.         0011 1010 0000 0000

00DA9 44 40 59 24 E8 08 00 05   D@Y$....   0100 0100 0100 0000 0101 1001 0010 0100 1110 1000 0000 1000 0000 0000 0000 0101

00DB1 5B 0F 61 AA 41 EB F9 A0   [.a.A...   0101 1011 0000 1111 0110 0001 1010 1010 0100 0001 1110 1011 1111 1001 1010 0000

00DB9 88 05 DD 50 53 3A 0A 70   ...PS:.p   1000 1000 0000 0101 1101 1101 0101 0000 0101 0011 0011 1010 0000 1010 0111 0000

00DC1 EA 04 13 B4 FD AC 6D CB   ......m.   1110 1010 0000 0100 0001 0011 1011 0100 1111 1101 1010 1100 0110 1101 1100 1011

00DC9 7A 9F D4 88 6D E1 F9 BC   z...m...   0111 1010 1001 1111 1101 0100 1000 1000 0110 1101 1110 0001 1111 1001 1011 1100

00DD1 BC 60 08 00 27 5B 70 E5   .`..'[p.   1011 1100 0110 0000 0000 1000 0000 0000 0010 0111 0101 1011 0111 0000 1110 0101

00DD9 02 68 7A 01 82 88 7E 08   .hz...~.   0000 0010 0110 1000 0111 1010 0000 0001 1000 0010 1000 1000 0111 1110 0000 1000

00DE1 33 05                     3.         0011 0011 0000 0101

00DE3 91 5F                     crc

Open Design Specification for .dwg files

123


#### 20.4.19 ARC_DIMENSION
Class properties:
App name
ObjectDBX Classes
Class number
Dynamic (>= 500)
DWG version
R18
Maintenance version
0
Class proxy flags
0x401
C++ class name
AcDbArcDimension
DXF name
ARC_DIMENSION

The arc length dimension was introduced in AutoCAD 2004. The DXF format is slightly different from
the other dimension entities. The entity type in DXF is ARC_DIMENSION, rather than DIMENSION.
Common Entity Data
Common Dimension Data


See paragraph 20.4.22.
Common:
Dim line arc point
3BD
10

Extension line 1 point
3BD
13

Extension line 2 point
3BD
14

Arc center
3BD
15
Is partial?
B
70
Start angle (radians)
BD
40
End angle (radians)
BD
41
Has leader?
B
71
Leader point 1
3BD
16
Leader point 2
3BD
17
Common Entity Handle Data

H
3
DIMSTYLE (hard pointer)

H
2
anonymous BLOCK (hard pointer)
CRC
X
---
#### 20.4.20 CIRCLE (18)

Common Entity Data

Center
3BD
10

Radius
BD
40

Thickness
BT
39

Extrusion
BE
210

Common Entity Handle Data

CRC
X
---
##### 20.4.20.1 R14 Example:
OBJECT: circle (12H), len 2BH (43), handle: 92


Open Design Specification for .dwg files

124


0154E 2B 00                     +.         0010 1011 0000 0000

01550 44 80 64 A0 C8 08 00 05   D.d.....   0100 0100 1000 0000 0110 0100 1010 0000 1100 1000 0000 1000 0000 0000 0000 0101

01558 5B 0A 88 A1 BF 90 3F C3   [.....?.   0101 1011 0000 1010 1000 1000 1010 0001 1011 1111 1001 0000 0011 1111 1100 0011

01560 48 00 45 2D C2 C7 6F 28   H.E-..o(   0100 1000 0000 0000 0100 0101 0010 1101 1100 0010 1100 0111 0110 1111 0010 1000

01568 FA 04 6A 9D CD 75 A2 1A   ..j..u..   1111 1010 0000 0100 0110 1010 1001 1101 1100 1101 0111 0101 1010 0010 0001 1010

01570 72 9F D4 98 28 87 E0 96   r...(...   0111 0010 1001 1111 1101 0100 1001 1000 0010 1000 1000 0111 1110 0000 1001 0110

01578 50 86 6D                  P.m        0101 0000 1000 0110 0110 1101

0157B 36 1C                     crc
#### 20.4.21 LINE (19)

Common Entity Data
R13-R14 Only:

Start pt
3BD
10

End   pt
3BD
11
R2000+:

Z’s are zero bit
B


Start Point x
RD
10

End Point x
DD
11
Use 10 value for default

Start Point y
RD
20

End Point y
DD
21
Use 20 value for default

Start Point z
RD
30
Present only if “Z’s are zero bit” is 0

End Point z
DD
31
Present only if “Z’s are zero bit” is 0, use 30
value for default.

Common:

Thickness
BT
39

Extrusion
BE
210

Common Entity Handle Data

CRC
X
---
##### 20.4.21.1 R14 Example:
OBJECT: line (13H), len 35H (53), handle: CC

004A5 35 00                     5.         0011 0101 0000 0000

004A7 44 C0 73 22 E8 08 00 01   D.s"....   0100 0100 1100 0000 0111 0011 0010 0010 1110 1000 0000 1000 0000 0000 0000 0001

004AF 13 00 6B B5 95 B2 D9 24   ..k....$   0001 0011 0000 0000 0110 1011 1011 0101 1001 0101 1011 0010 1101 1001 0010 0100

004B7 08 04 88 93 FD FD 9A 00   ........   0000 1000 0000 0100 1000 1000 1001 0011 1111 1101 1111 1101 1001 1010 0000 0000

004BF FA 04 53 E6 F4 DB B6 B6   ..S.....   1111 1010 0000 0100 0101 0011 1110 0110 1111 0100 1101 1011 1011 0110 1011 0110


Open Design Specification for .dwg files

125


004C7 90 20 12 02 4F F7 F6 68   . ..O..h   1001 0000 0010 0000 0001 0010 0000 0010 0100 1111 1111 0111 1111 0110 0110 1000

004CF 03 E8 15 4E 08 11 82 88   ...N....   0000 0011 1110 1000 0001 0101 0100 1110 0000 1000 0001 0001 1000 0010 1000 1000

004D7 7A 88 9A 03 06            z....      0111 1010 1000 1000 1001 1010 0000 0011 0000 0110

004DC FA FE                     crc
#### 20.4.22 COMMON DIMENSION DATA
R2010:

Version
RC
280
0 = R2010
Common:

Extrusion
3BD
210

Text midpt
2RD
11
See DXF documentation.

Elevation
BD
11
Z-coord for the ECS points (11, 12, 16).



12
(The 16 remains (0,0,0) in entgets of this entity,
since the 16 is not used in this type of dimension
and is not present in the binary form here.)

Flags 1
RC
70
Non-bit-pair-coded.  NOT the 70 group, but helps
define it.  Apparently only the two lowest bit are
used:




76543210:




Bit 0 : The OPPOSITE of bit 7 (128) of 70.




Bit 1 : Same as bit 5 (32) of the 70 (but 32 is not
doc'd by ACAD).




The actual 70-group value comes from 3 things:




6 for being an ordinate DIMENSION, plus whatever
bits "Flags 1" and "Flags 2" specify.

User text
TV
1

Text rot
BD
53
See DXF documentation.

Horiz dir
BD
51
See DXF documentation.

Ins X-scale
BD
41
Undoc'd.  These apply to the insertion of the

Ins Y-scale
BD
42
anonymous block.  None of them can be

Ins Z-scale
BD
43
dealt with via entget/entmake/entmod.

Ins rotation
BD
54
The last 2 (43 and 54) are reported by DXFOUT (when
not default values).  ALL OF THEM can be set via
DXFIN, however.
R2000+:

Attachment Point
BS
71

Linespacing Style
BS
72

Linespacing Factor
BD
41

Actual Measurement
BD
42
R2007+:

Unknown
B
73

Flip arrow1
B
74

Open Design Specification for .dwg files

126



Flip arrow2
B
75
Common:

12-pt
2RD
12
See DXF documentation.

#### 20.4.23 DIMENSION (ORDINATE) (20)

Common Entity Data

Common Dimension Data


See paragraph 20.4.22.
Common:

10-pt
3BD
10
See DXF documentation.

13-pt
3BD
13
See DXF documentation.

14-pt
3BD
14
See DXF documentation.

Flags 2
RC
70
Non-bit-pair-coded.  NOT the 70 group, but helps
define it.  Apparently only the lowest bit is used;
it's bit 6 (64) of the 70 group.

Common Entity Handle Data


H
3
DIMSTYLE (hard pointer)


H
2
anonymous BLOCK (hard pointer)

CRC
X
---
##### 20.4.23.1 R14 Example:
OBJECT: dim ordinate (14H), len 5CH (92), handle: 9E

0157D 5C 00                     \.         0101 1100 0000 0000

0157F 45 00 67 A4 08 10 00 05   E.g.....   0100 0101 0000 0000 0110 0111 1010 0100 0000 1000 0001 0000 0000 0000 0000 0101

01587 5B 52 6B 24 C2 1F B9 8C   [Rk$....   0101 1011 0101 0010 0110 1011 0010 0100 1100 0010 0001 1111 1011 1001 1000 1100

0158F 32 80 21 6E 4C 98 C7 73   2.!nL..s   0011 0010 1000 0000 0010 0001 0110 1110 0100 1100 1001 1000 1100 0111 0111 0011

01597 F0 7F 05 D4 AC 00 00 00   ........   1111 0000 0111 1111 0000 0101 1101 0100 1010 1100 0000 0000 0000 0000 0000 0000

0159F 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

015A7 00 00 00 00 01 50 D8 84   .....P..   0000 0000 0000 0000 0000 0000 0000 0000 0000 0001 0101 0000 1101 1000 1000 0100

015AF 7F 51 B7 94 26 80 2C 78   .Q..&.,x   0111 1111 0101 0001 1011 0111 1001 0100 0010 0110 1000 0000 0010 1100 0111 1000

015B7 71 23 C3 5B 81 20 40 61   q#.[. @a   0111 0001 0010 0011 1100 0011 0101 1011 1000 0001 0010 0000 0100 0000 0110 0001

015BF B6 92 67 34 E8 BA 00 21   ..g4...!   1011 0110 1001 0010 0110 0111 0011 0100 1110 1000 1011 1010 0000 0000 0010 0001

015C7 6E 4C 98 C7 73 F0 7F 00   nL..s...   0110 1110 0100 1100 1001 1000 1100 0111 0111 0011 1111 0000 0111 1111 0000 0000

015CF 18 28 87 E0 86 50 87 28   .(...P.(   0001 1000 0010 1000 1000 0111 1110 0000 1000 0110 0101 0000 1000 0111 0010 1000

015D7 8E A8 C9 80               ....       1000 1110 1010 1000 1100 1001 1000 0000

015DB 8E 48                     crc

Open Design Specification for .dwg files

127


#### 20.4.24 DIMENSION (LINEAR) (21)

Common Entity Data

Common Dimension Data


See paragraph 20.4.22.
Common:

13-pt
3BD
13
See DXF documentation.

14-pt
3BD
14
See DXF documentation.

10-pt
3BD
10
See DXF documentation.

Ext ln rot
BD
52
Extension line rotation; see DXF documentation.

Dim rot
BD
50
Linear dimension rotation; see DXF documentation.

Common Entity Handle Data


H
3
DIMSTYLE (hard pointer)


H
2
anonymous BLOCK (hard pointer)

CRC
X
---
##### 20.4.24.1 R14 Example:
OBJECT: dim linear (15H), len 6BH (107), handle: AC

015DD 6B 00                     k.         0110 1011 0000 0000

015DF 45 40 6B 27 E8 10 00 05   E@k'....   0100 0101 0100 0000 0110 1011 0010 0111 1110 1000 0001 0000 0000 0000 0000 0101

015E7 5B 52 A8 5F BD 44 3D 70   [R._.D=p   0101 1011 0101 0010 1010 1000 0101 1111 1011 1101 0100 0100 0011 1101 0111 0000

015EF 3C 80 80 18 62 E8 57 62   <...b.Wb   0011 1100 1000 0000 1000 0000 0001 1000 0110 0010 1110 1000 0101 0111 0110 0010

015F7 24 81 05 D4 AC 00 00 00   $.......   0010 0100 1000 0001 0000 0101 1101 0100 1010 1100 0000 0000 0000 0000 0000 0000

015FF 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

01607 00 00 00 00 00 72 6E 2A   .....rn*   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0111 0010 0110 1110 0010 1010

0160F 01 C0 D2 8D 20 09 11 EC   .... ...   0000 0001 1100 0000 1101 0010 1000 1101 0010 0000 0000 1001 0001 0001 1110 1100

01617 04 B1 82 01 48 11 C5 80   ....H...   0000 0100 1011 0001 1000 0010 0000 0001 0100 1000 0001 0001 1100 0101 1000 0000

0161F 66 42 BC CA 42 80 5C 7C   fB..B.\|   0110 0110 0100 0010 1011 1100 1100 1010 0100 0010 1000 0000 0101 1100 0111 1100

01627 B9 38 1C BB 05 20 47 16   .8... G.   1011 1001 0011 1000 0001 1100 1011 1011 0000 0101 0010 0000 0100 0111 0001 0110

0162F 01 99 0A F3 29 0A 00 80   ....)...   0000 0001 1001 1001 0000 1010 1111 0011 0010 1001 0000 1010 0000 0000 1000 0000

01637 18 62 E8 57 62 24 81 51   .b.Wb$.Q   0001 1000 0110 0010 1110 1000 0101 0111 0110 0010 0010 0100 1000 0001 0101 0001

0163F 82 88 7E 08 75 08 72 88   ..~.u.r.   1000 0010 1000 1000 0111 1110 0000 1000 0111 0101 0000 1000 0111 0010 1000 1000

01647 EA 8C FB                  ...        1110 1010 1000 1100 1111 1011

0164A 48 DA                     crc
#### 20.4.25 DIMENSION (ALIGNED) (22)

Common Entity Data

Common Dimension Data


See paragraph 20.4.22.

Open Design Specification for .dwg files

128


Common:

13-pt
3BD
13
See DXF documentation.

14-pt
3BD
14
See DXF documentation.

10-pt
3BD
10
See DXF documentation.

Ext ln rot
BD
52
Extension line rotation; see DXF documentation.

Common Entity Handle Data


H
3
DIMSTYLE (hard pointer)


H
2
anonymous BLOCK (hard pointer)

CRC
X
---
##### 20.4.25.1 R14 Example:
OBJECT: dim aligned (16H), len 6BH (107), handle: BA

0164C 6B 00                     k.         0110 1011 0000 0000

0164E 45 80 6E A7 D8 10 00 05   E.n.....   0100 0101 1000 0000 0110 1110 1010 0111 1101 1000 0001 0000 0000 0000 0000 0101

01656 5B 53 B7 92 B9 9A CA CA   [S......   0101 1011 0101 0011 1011 0111 1001 0010 1011 1001 1001 1010 1100 1010 1100 1010

0165E 1C 81 55 6D 19 67 3E 90   ..Um.g>.   0001 1100 1000 0001 0101 0101 0110 1101 0001 1001 0110 0111 0011 1110 1001 0000

01666 28 81 05 D4 AC 00 00 00   (.......   0010 1000 1000 0001 0000 0101 1101 0100 1010 1100 0000 0000 0000 0000 0000 0000

0166E 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

01676 00 00 00 00 00 2A 41 59   .....*AY   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0010 1010 0100 0001 0101 1001

0167E E6 59 20 09 20 04 E7 DE   .Y . ...   1110 0110 0101 1001 0010 0000 0000 1001 0010 0000 0000 0100 1110 0111 1101 1110

01686 65 A9 1D 81 E8 11 E8 B7   e.......   0110 0101 1010 1001 0001 1101 1000 0001 1110 1000 0001 0001 1110 1000 1011 0111

0168E 57 AB F5 B4 22 80 6E 48   W...".nH   0101 0111 1010 1011 1111 0101 1011 0100 0010 0010 1000 0000 0110 1110 0100 1000

01696 CB DF EC 81 08 20 46 F7   ..... F.   1100 1011 1101 1111 1110 1100 1000 0001 0000 1000 0010 0000 0100 0110 1111 0111

0169E 1E 19 C7 7A E8 92 00 60   ...z...`   0001 1110 0001 1001 1100 0111 0111 1010 1110 1000 1001 0010 0000 0000 0110 0000

016A6 DD 30 19 D6 34 28 81 46   .0..4(.F   1101 1101 0011 0000 0001 1001 1101 0110 0011 0100 0010 1000 1000 0001 0100 0110

016AE 0A 21 F8 21 D4 21 EA 23   .!.!.!.#   0000 1010 0010 0001 1111 1000 0010 0001 1101 0100 0010 0001 1110 1010 0010 0011

016B6 AA 35 BB                  .5.        1010 1010 0011 0101 1011 1011

016B9 EA 25                     crc
#### 20.4.26 DIMENSION (ANGULAR, 3-PT) (23)

Common Entity Data

Common Dimension Data


See paragraph 20.4.22.
Common:

10-pt
3BD
10
See DXF documentation.

13-pt
3BD
13
See DXF documentation.

14-pt
3BD
14
See DXF documentation.

Open Design Specification for .dwg files

129



15-pt
3BD
15
See DXF documentation.

Common Entity Handle Data


H

3
DIMSTYLE (hard pointer)


H

2
anonymous BLOCK (hard pointer)

CRC
X
---
##### 20.4.26.1 R14 Example:
OBJECT: dim angular (17H), len 7BH (123), handle: C9

016BB 7B 00                     {.         0111 1011 0000 0000

016BD 45 C0 72 63 F8 18 00 05   E.rc....   0100 0101 1100 0000 0111 0010 0110 0011 1111 1000 0001 1000 0000 0000 0000 0101

016C5 5B 53 DC 3A 57 CD 05 40   [S.:W..@   0101 1011 0101 0011 1101 1100 0011 1010 0101 0111 1100 1101 0000 0101 0100 0000

016CD 2E 80 C0 5E B2 D6 6F 22   ...^..o"   0010 1110 1000 0000 1100 0000 0101 1110 1011 0010 1101 0110 0110 1111 0010 0010

016D5 40 81 05 D4 AC 00 00 00   @.......   0100 0000 1000 0001 0000 0101 1101 0100 1010 1100 0000 0000 0000 0000 0000 0000

016DD 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

016E5 00 00 00 00 00 68 08 AF   .....h..   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0110 1000 0000 1000 1010 1111

016ED 7C 2C 5E 0C A0 11 C0 E9   |,^.....   0111 1100 0010 1100 0101 1110 0000 1100 1010 0000 0001 0001 1100 0000 1110 1001

016F5 18 9D 34 04 28 10 D2 BA   ..4.(...   0001 1000 1001 1101 0011 0100 0000 0100 0010 1000 0001 0000 1101 0010 1011 1010

016FD AD A6 B9 2C 3A 80 61 CA   ...,:.a.   1010 1101 1010 0110 1011 1001 0010 1100 0011 1010 1000 0000 0110 0001 1100 1010

01705 13 3A 13 1C 90 20 45 65   .:... Ee   0001 0011 0011 1010 0001 0011 0001 1100 1001 0000 0010 0000 0100 0101 0110 0101

0170D 3A 06 5E 80 38 EA 00 D8   :.^.8...   0011 1010 0000 0110 0101 1110 1000 0000 0011 1000 1110 1010 0000 0000 1101 1000

01715 3B 7A 98 A2 88 3A 81 0A   ;z...:..   0011 1011 0111 1010 1001 1000 1010 0010 1000 1000 0011 1010 1000 0001 0000 1010

0171D 88 A1 BF 90 3F C3 48 00   ....?.H.   1000 1000 1010 0001 1011 1111 1001 0000 0011 1111 1100 0011 0100 1000 0000 0000

01725 55 2D C2 C7 6F 28 FA 04   U-..o(..   0101 0101 0010 1101 1100 0010 1100 0111 0110 1111 0010 1000 1111 1010 0000 0100

0172D 60 A2 1F 82 1F 42 18 A2   `....B..   0110 0000 1010 0010 0001 1111 1000 0010 0001 1111 0100 0010 0001 1000 1010 0010

01735 3A A3 76                  :.v        0011 1010 1010 0011 0111 0110

01738 42 38                     crc
#### 20.4.27 DIMENSION (ANGULAR, 2-LINE) (24)

Common Entity Data

Common Dimension Data


See paragraph 20.4.22.
Common:

16-pt
2RD
16
See DXF documentation.

13-pt
3BD
13
See DXF documentation.

14-pt
3BD
14
See DXF documentation.

15-pt
3BD
15
See DXF documentation.

10-pt
3BD
10
See DXF documentation.

Open Design Specification for .dwg files

130



Common Entity Handle Data


H
3
DIMSTYLE (hard pointer)


H
2
anonymous BLOCK (hard pointer)

CRC
X
---

#### 20.4.28 DIMENSION (RADIUS) (25)

Common Entity Data

Common Dimension Data


See paragraph 20.4.22.
Common:

10-pt
3BD
10
See DXF documentation.

15-pt
3BD
15
See DXF documentation.

Leader len
D
40
Leader length.

Common Entity Handle Data


H
3
DIMSTYLE (hard pointer)


H
2
anonymous BLOCK (hard pointer)

CRC
X
---
20.4.28.1
R14 Example:
OBJECT: dim radial (19H), len 71H (113), handle: D5

0173A 71 00                     q.         0111 0001 0000 0000

0173C 46 40 75 51 45 11 10 00   F@uQE...   0100 0110 0100 0000 0111 0101 0101 0001 0100 0101 0001 0001 0001 0000 0000 0000

01744 60 01 E4 45 35 45 94 C4   `..E5E..   0110 0000 0000 0001 1110 0100 0100 0101 0011 0101 0100 0101 1001 0100 1100 0100

0174C 50 20 04 62 00 14 60 10   P .b..`.   0101 0000 0010 0000 0000 0100 0110 0010 0000 0000 0001 0100 0110 0000 0001 0000

01754 00 20 18 5E 06 00 01 56   . .^...V   0000 0000 0010 0000 0001 1000 0101 1110 0000 0110 0000 0000 0000 0001 0101 0110

0175C D4 BE B8 AD 7A BB 82 11   ....z...   1101 0100 1011 1110 1011 1000 1010 1101 0111 1010 1011 1011 1000 0010 0001 0001

01764 20 48 89 3F DF D9 A0 0F    H.?....   0010 0000 0100 1000 1000 1001 0011 1111 1101 1111 1101 1001 1010 0000 0000 1111

0176C A0 41 55 2B 00 00 00 00   .AU+....   1010 0000 0100 0001 0101 0101 0010 1011 0000 0000 0000 0000 0000 0000 0000 0000

01774 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

0177C 00 00 00 00 0A A8 A1 BF   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 1010 1010 1000 1010 0001 1011 1111

01784 90 3F C3 48 00 55 2D C2   .?.H.U-.   1001 0000 0011 1111 1100 0011 0100 1000 0000 0000 0101 0101 0010 1101 1100 0010

0178C C7 6F 28 FA 04 27 F9 9E   .o(..'..   1100 0111 0110 1111 0010 1000 1111 1010 0000 0100 0010 0111 1111 1001 1001 1110

01794 65 FB 50 0E A0 07 FF E7   e.P.....   0110 0101 1111 1011 0101 0000 0000 1110 1010 0000 0000 0111 1111 1111 1110 0111

0179C 46 14 F3 63 E8 14 60 A2   F..c..`.   0100 0110 0001 0100 1111 0011 0110 0011 1110 1000 0001 0100 0110 0000 1010 0010

017A4 1F 82 19 42 18 A2 3A A3   ...B..:.   0001 1111 1000 0010 0001 1001 0100 0010 0001 1000 1010 0010 0011 1010 1010 0011

017AC 94                        .          1001 0100


Open Design Specification for .dwg files

131


017AD EA 1E                     crc
#### 20.4.29 DIMENSION (DIAMETER) (26)

Common Entity Data

Common Dimension Data


See paragraph 20.4.22.
Common:

15-pt
3BD
15
See DXF documentation.

10-pt
3BD
10
See DXF documentation.

Leader len
BD
40
Leader length.

Common Entity Handle Data


H
3
DIMSTYLE (hard pointer)


H
2
anonymous BLOCK (hard pointer)

CRC
X
---
##### 20.4.29.1 R14 Example:
OBJECT: dim diameter (1AH), len 70H (112), handle: E1

017AF 70 00                     p.         0111 0000 0000 0000

017B1 46 80 78 51 45 11 10 00   F.xQE...   0100 0110 1000 0000 0111 1000 0101 0001 0100 0101 0001 0001 0001 0000 0000 0000

017B9 60 01 E4 45 35 45 94 C4   `..E5E..   0110 0000 0000 0001 1110 0100 0100 0101 0011 0101 0100 0101 1001 0100 1100 0100

017C1 50 20 04 62 00 14 60 10   P .b..`.   0101 0000 0010 0000 0000 0100 0110 0010 0000 0000 0001 0100 0110 0000 0001 0000

017C9 00 20 18 5E 06 00 01 56   . .^...V   0000 0000 0010 0000 0001 1000 0101 1110 0000 0110 0000 0000 0000 0001 0101 0110

017D1 D4 AE 72 3A F7 9A B2 10   ..r:....   1101 0100 1010 1110 0111 0010 0011 1010 1111 0111 1001 1010 1011 0010 0001 0000

017D9 A0 4A 92 A4 03 41 DC 0E   .J...A..   1010 0000 0100 1010 1001 0010 1010 0100 0000 0011 0100 0001 1101 1100 0000 1110

017E1 20 41 55 2B 00 00 00 00    AU+....   0010 0000 0100 0001 0101 0101 0010 1011 0000 0000 0000 0000 0000 0000 0000 0000

017E9 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

017F1 00 00 00 00 1B 6E ED 97   .....n..   0000 0000 0000 0000 0000 0000 0000 0000 0001 1011 0110 1110 1110 1101 1001 0111

017F9 4E 85 E3 A8 06 3F D6 3A   N....?.:   0100 1110 1000 0101 1110 0011 1010 1000 0000 0110 0011 1111 1101 0110 0011 1010

01801 B1 4B 40 F2 04 65 89 57   .K@..e.W   1011 0001 0100 1011 0100 0000 1111 0010 0000 0100 0110 0101 1000 1001 0101 0111

01809 1E C7 E6 8C 20 14 94 EA   .... ...   0001 1110 1100 0111 1110 0110 1000 1100 0010 0000 0001 0100 1001 0100 1110 1010

01811 95 BB 16 24 08 14 60 A2   ...$..`.   1001 0101 1011 1011 0001 0110 0010 0100 0000 1000 0001 0100 0110 0000 1010 0010

01819 1F 82 18 C0 A2 3A A3 AD   .....:..   0001 1111 1000 0010 0001 1000 1100 0000 1010 0010 0011 1010 1010 0011 1010 1101

01821 37 B4                     crc
#### 20.4.30 LARGE_RADIAL_DIMENSION
Class properties:
App name
ObjectDBX Classes

Open Design Specification for .dwg files

132


Class number
Dynamic (>= 500)
DWG version
R18
Maintenance version
0
Class proxy flags
0x401
C++ class name
AcDbRadialDimensionLarge
DXF name
LARGE_RADIAL_DIMENSION

The large radial dimension was introduced in AutoCAD 2004. The DXF format is slightly different from
the other dimension entities. The entity type in DXF is LARGE_RADIAL_DIMENSION, rather than DIMENSION.
Common Entity Data
Common Dimension Data


See paragraph 20.4.22.
Common:
Center point
3BD
10

Chord point
3BD
13

Unknown
BD
40
Value 0
Override center
3BD
14
Jog point
3BD
15
Common Entity Handle Data

H
3
DIMSTYLE (hard pointer)

H
2
anonymous BLOCK (hard pointer)
CRC
X
---
#### 20.4.31 POINT (27)

Common Entity Data

Point
3BD
10

Thickness
BT
39

Extrusion
BE
210

X-axis ang
BD
50
See DXF documentation

Common Entity Handle Data

CRC
X
---
20.4.31.1
R14 Example:
OBJECT: point (1BH), len 23H (35), handle: D2

0062A 23 00                     #.         0010 0011 0000 0000

0062C 46 C0 74 A6 C8 00 00 01   F.t.....   0100 0110 1100 0000 0111 0100 1010 0110 1100 1000 0000 0000 0000 0000 0000 0001

00634 33 09 FE 67 99 7E D4 03   3..g.~..   0011 0011 0000 1001 1111 1110 0110 0111 1001 1001 0111 1110 1101 0100 0000 0011

0063C A8 01 FF F9 D1 85 3C D8   ......<.   1010 1000 0000 0001 1111 1111 1111 1001 1101 0001 1000 0101 0011 1100 1101 1000

00644 FA 05 53 60 84 18 28 CC   ..S`..(.   1111 1010 0000 0101 0101 0011 0110 0000 1000 0100 0001 1000 0010 1000 1100 1100

0064C A8 89 86                  ...        1010 1000 1000 1001 1000 0110

0064F 09 DF                     crc

Open Design Specification for .dwg files

133


#### 20.4.32 3DFACE (28)

Common Entity Data
R13-R14 Only:

1st corner
3BD
10

2nd corner
3BD
11

3rd corner
3BD
12

4th corner
3BD
13

Invis flags
BS
70
Invisible edge flags
R2000+:

Has no flag ind.
B



Z is zero bit
B

1st corner x
RD
10

1st corner y
RD
20

1st corner z
RD
30
Present only if “Z is zero bit” is 0.

2nd corner
3DD
11
Use 10 value as default point

3rd corner
3DD
12
Use 11 value as default point

4th corner
3DD
13
Use 12 value as default point

Invis flags
BS
70
Present it “Has no flag ind.” is 0.
Common:

Common Entity Handle Data

CRC
X
---
##### 20.4.32.1 R14 Example:
OBJECT: 3d face (1CH), len 50H (80), handle: E3

01846 50 00                     P.         0101 0000 0000 0000

01848 47 00 78 E3 18 10 00 05   G.x.....   0100 0111 0000 0000 0111 1000 1110 0011 0001 1000 0001 0000 0000 0000 0000 0101

01850 7B 06 54 B1 62 D9 BA E4   {.T.b...   0111 1011 0000 0110 0101 0100 1011 0001 0110 0010 1101 1001 1011 1010 1110 0100

01858 28 00 02 01 84 E7 8E 80   (.......   0010 1000 0000 0000 0000 0010 0000 0001 1000 0100 1110 0111 1000 1110 1000 0000

01860 12 04 4F 73 C2 29 98 53   ..Os.).S   0001 0010 0000 0100 0100 1111 0111 0011 1100 0010 0010 1001 1001 1000 0101 0011

01868 12 20 16 8C 3C B6 E3 69   . ..<..i   0001 0010 0010 0000 0001 0110 1000 1100 0011 1100 1011 0110 1110 0011 0110 1001

01870 E2 08 10 14 77 8D 5D FA   ....w.].   1110 0010 0000 1000 0001 0000 0001 0100 0111 0111 1000 1101 0101 1101 1111 1010

01878 52 4C 80 50 0B 36 A4 30   RL.P.6.0   0101 0010 0100 1100 1000 0000 0101 0000 0000 1011 0011 0110 1010 0100 0011 0000

01880 F0 FF 1F C5 51 57 68 85   ....QWh.   1111 0000 1111 1111 0001 1111 1100 0101 0101 0001 0101 0111 0110 1000 1000 0101

01888 48 51 12 00 40 84 CA FB   HQ..@...   0100 1000 0101 0001 0001 0010 0000 0000 0100 0000 1000 0100 1100 1010 1111 1011

01890 AF DF EC 7F 46 0A 21 FA   ....F.!.   1010 1111 1101 1111 1110 1100 0111 1111 0100 0110 0000 1010 0010 0001 1111 1010

01898 1A A6                     crc

Open Design Specification for .dwg files

134


#### 20.4.33 POLYLINE (PFACE) (29)

Common Entity Data

Numverts
BS
71
Number of vertices in the mesh.

Numfaces
BS
72
Number of faces
R2004+:

Owned Object Count
BL

Number of objects owned by this object.
Common:

Common Entity Handle Data
R13-R2000:


H

first VERTEX (soft pointer)


H

last  VERTEX (soft pointer)
R2004+:


H

[VERTEX (soft pointer)] Repeats “Owned Object Count”
times.
Common:


H

SEQEND (hard owner)

CRC
X
---
##### 20.4.33.1 Example:
OBJECT: pface start (1DH), len 19H (25), handle: 55

00BC0 19 00                     ..         0001 1001 0000 0000

00BC2 47 40 55 62 E8 00 00 05   G@Ub....   0100 0111 0100 0000 0101 0101 0110 0010 1110 1000 0000 0000 0000 0000 0000 0101

00BCA 5B 20 88 19 82 88 7E 08   [ ....~.   0101 1011 0010 0000 1000 1000 0001 1001 1000 0010 1000 1000 0111 1110 0000 1000

00BD2 4D 08 4A 0A B2 0A E1 8A   M.J.....   0100 1101 0000 1000 0100 1010 0000 1010 1011 0010 0000 1010 1110 0001 1000 1010

00BDA E8                        .          1110 1000

00BDB D7 3E                     crc
#### 20.4.34 POLYLINE (MESH) (30)

Common Entity Data

Flags
BS
70

Curve type
BS
75
Curve and smooth surface type.

M vert count
BS
71
M vertex count

N vert count
BS
72
N vertex count

M density
BS
73
M vertex count

N density
BS
74
N vertex count
R2004+:

Owned Object Count
BL

Number of objects owned by this object.
Common:

Common Entity Handle Data

Open Design Specification for .dwg files

135


R13-R2000:


H

FIRST VERTEX (soft pointer)


H

LAST  VERTEX (soft pointer)
R2004+:


H

[VERTEX (soft pointer)] Repeats “Owned Object Count”
times.
Common:


H

SEQEND (CODE 3)

CRC
X
---
##### 20.4.34.1 Example:
OBJECT: 3d surf sol st (1EH), len 1AH (26), handle: 66

00E18 1A 00                     ..         0001 1010 0000 0000

00E1A 47 80 59 A3 68 00 00 05   G.Y.h...   0100 0111 1000 0000 0101 1001 1010 0011 0110 1000 0000 0000 0000 0000 0000 0101

00E22 5B 22 32 0C 83 D1 82 88   ["2.....   0101 1011 0010 0010 0011 0010 0000 1100 1000 0011 1101 0001 1000 0010 1000 1000

00E2A 7C 05 09 62 0B 3A 0C 81   |..b.:..   0111 1100 0000 0101 0000 1001 0110 0010 0000 1011 0011 1010 0000 1100 1000 0001

00E32 8C 8C                     ..         1000 1100 1000 1100

00E34 3C E7                     crc
#### 20.4.35 SOLID (31)

Common Entity Data

Thickness
BT
39

Elevation
BD
---
Z for 10 - 13.

1st corner
2RD
10

2nd corner
2RD
11

3rd corner
2RD
12

4th corner
2RD
13

Extrusion
BE
210

Common Entity Handle Data

CR
X
---
##### 20.4.35.1 R14 Example:
OBJECT: solid (1FH), len 52H (82), handle: CF

00566 52 00                     R.         0101 0010 0000 0000

00568 47 C0 73 E2 98 10 00 01   G.s.....   0100 0111 1100 0000 0111 0011 1110 0010 1001 1000 0001 0000 0000 0000 0000 0001

00570 33 50 A8 BE 18 24 52 D8   3P...$R.   0011 0011 0101 0000 1010 1000 1011 1110 0001 1000 0010 0100 0101 0010 1101 1000

00578 F2 07 52 C3 01 40 1D 30   ..R..@.0   1111 0010 0000 0111 0101 0010 1100 0011 0000 0001 0100 0000 0001 1101 0011 0000

00580 FA 00 FF 31 0A 96 82 A0   ...1....   1111 1010 0000 0000 1111 1111 0011 0001 0000 1010 1001 0110 1000 0010 1010 0000

Open Design Specification for .dwg files

136



00588 F2 06 8B FA 70 47 8B 40   ....pG.@   1111 0010 0000 0110 1000 1011 1111 1010 0111 0000 0100 0111 1000 1011 0100 0000

00590 FA 02 7F 99 E6 5F B5 00   ....._..   1111 1010 0000 0010 0111 1111 1001 1001 1110 0110 0101 1111 1011 0101 0000 0000

00598 EA 01 FF F9 D1 85 3C D8   ......<.   1110 1010 0000 0001 1111 1111 1111 1001 1101 0001 1000 0101 0011 1100 1101 1000

005A0 FA 02 7F 99 E6 5F B5 00   ....._..   1111 1010 0000 0010 0111 1111 1001 1001 1110 0110 0101 1111 1011 0101 0000 0000

005A8 EA 01 FF F9 D1 85 3C D8   ......<.   1110 1010 0000 0001 1111 1111 1111 1001 1101 0001 1000 0101 0011 1100 1101 1000

005B0 FA 05 38 20 A6 0A 21 EA   ..8 ..!.   1111 1010 0000 0101 0011 1000 0010 0000 1010 0110 0000 1010 0010 0001 1110 1010

005B8 22 6A                     "j         0010 0010 0110 1010

005BA 18 03                     crc
#### 20.4.36 TRACE (32)

Common Entity Data

Thickness
BT
39

Elevation
BD
---
Z for 10 - 13.

1st corner
2RD
10

2nd corner
2RD
11

3rd corner
2RD
12

4th corner
2RD
13

Extrusion
BE
210

Common Entity Handle Data

CRC
X
---
##### 20.4.36.1 R14 Example:
OBJECT: trace (20H), len 51H (81), handle: E7

018EF 51 00                     Q.         0101 0001 0000 0000

018F1 48 00 79 E2 98 10 00 05   H.y.....   0100 1000 0000 0000 0111 1001 1110 0010 1001 1000 0001 0000 0000 0000 0000 0101

018F9 5B 53 70 DA A0 AD EE C1   [Sp.....   0101 1011 0101 0011 0111 0000 1101 1010 1010 0000 1010 1101 1110 1110 1100 0001

01901 42 05 BA E0 2A DA A9 60   B...*..`   0100 0010 0000 0101 1011 1010 1110 0000 0010 1010 1101 1010 1010 1001 0110 0000

01909 02 05 75 29 DE 3E FF 89   ..u).>..   0000 0010 0000 0101 0111 0101 0010 1001 1101 1110 0011 1110 1111 1111 1000 1001

01911 42 03 4E 20 B3 8F 50 C0   B.N ..P.   0100 0010 0000 0011 0100 1110 0010 0000 1011 0011 1000 1111 0101 0000 1100 0000

01919 02 00 4B 2A 12 65 70 A9   ..K*.ep.   0000 0010 0000 0000 0100 1011 0010 1010 0001 0010 0110 0101 0111 0000 1010 1001

01921 52 04 9E 9B A5 92 BF 40   R......@   0101 0010 0000 0100 1001 1110 1001 1011 1010 0101 1001 0010 1011 1111 0100 0000

01929 A2 06 1D 16 C2 A5 61 81   ......a.   1010 0010 0000 0110 0001 1101 0001 0110 1100 0010 1010 0101 0110 0001 1000 0001

01931 52 02 6F 4E 85 D6 E7 88   R.oN....   0101 0010 0000 0010 0110 1111 0100 1110 1000 0101 1101 0110 1110 0111 1000 1000

01939 A2 05 26 0A 21 F8 20 6C   ..&.!. l   1010 0010 0000 0101 0010 0110 0000 1010 0010 0001 1111 1000 0010 0000 0110 1100

01941 1A                        .          0001 1010

Open Design Specification for .dwg files

137



01942 7E C2                     crc
#### 20.4.37 SHAPE (33)

Common Entity Data

Ins pt
3BD
10

Scale
BD
40
Scale factor, default value 1.

Rotation
BD
50
Rotation in radians, default value 0.

Width factor
BD
41
Width factor, default value 1.

Oblique
BD
51
Oblique angle in radians, default value 0.

Thickness
BD
39

Shapeno
BS
2
This is the shape index. In DXF the shape name is
stored. When reading from DXF, the shape is found by
iterating over all the text styles (SHAPEFILE, see
paragraph 20.4.56) and when the text style contains
a shape file, iterating over all the shapes until
the one with the matching name is found.

Extrusion
3BD
210

Common Entity Handle Data


H

SHAPEFILE (hard pointer)

CRC
X
--
20.4.37.1
Example:
OBJECT: shape (21H), len 26H (38), handle: F5

008BC 26 00                     &.         0010 0110 0000 0000

008BE 48 40 7D 67 48 00 00 01   H@}gH...   0100 1000 0100 0000 0111 1101 0110 0111 0100 1000 0000 0000 0000 0000 0000 0001

008C6 5B 14 AF 3D 96 39 59 A1   [..=.9Y.   0101 1011 0001 0100 1010 1111 0011 1101 1001 0110 0011 1001 0101 1001 1010 0001

008CE 48 04 20 D5 14 35 41 08   H. ..5A.   0100 1000 0000 0100 0010 0000 1101 0101 0001 0100 0011 0101 0100 0001 0000 1000

008D6 8A 04 CD 32 F4 C0 18 28   ...2...(   1000 1010 0000 0100 1100 1101 0011 0010 1111 0100 1100 0000 0001 1000 0010 1000

008DE 87 A0 30 28 F9 ED         ..0(..     1000 0111 1010 0000 0011 0000 0010 1000 1111 1001 1110 1101

008E4 38 74                     crc
#### 20.4.38 VIEWPORT ENTITY (34)

Common Entity Data

Center
3BD
10

Width
BD
40

Height
BD
41
R2000+:

View Target
3BD
17

View Direction
3BD
16

View Twist Angle
BD
51

Open Design Specification for .dwg files

138



View Height
BD
45

Lens Length
BD
42

Front Clip Z
BD
43

Back Clip Z
BD
44

Snap Angle
BD
50

View Center
2RD
12

Snap Base
2RD
13

Snap Spacing
2RD
14

Grid Spacing
2RD
15

Circle Zoom
BS
72
R2007+:

Grid Major
BS
61
R2000+:

Frozen Layer Count
BL

Status Flags
BL
90

Style Sheet
TV
1

Render Mode
RC
281

UCS at origin
B
74

UCS per Viewport
B
71

UCS Origin
3BD
110

UCS X Axis
3BD
111

UCS Y Axis
3BD
112

UCS Elevation
BD
146

UCS Ortho View Type
BS
79
R2004+:

ShadePlot Mode
BS
170
R2007+:

Use def. lights
B
292

Def. lighting type
RC
282

Brightness
BD
141

Contrast
BD
142

Ambient light color
CMC
63
Common:

Common Entity Handle Data
R13-R14 Only:


H

VIEWPORT ENT HEADER (hard pointer)
R2000+:


H
341
Frozen Layer Handles (use count from above) (hard
pointer until R2000, soft pointer from R2004
onwards)


H
340
Clip boundary handle (soft pointer)

Open Design Specification for .dwg files

139


R2000:


H

VIEWPORT ENT HEADER ((hard pointer))
R2000+:


H
345
Named UCS Handle (hard pointer)


H
346
Base UCS Handle (hard pointer)
R2007+:


H
332
Background (soft pointer)


H
348
Visual Style (hard pointer)


H
333
Shadeplot ID (soft pointer)


H
361
Sun (hard owner)

##### 20.4.38.1 R14 Example:
OBJECT: vpent (22H), len 117H (279), handle: 01 26

03934 17 01                     ..         0001 0111 0000 0001

03936 48 80 80 49 9D F5 11 10   H..I....   0100 1000 1000 0000 1000 0000 0100 1001 1001 1101 1111 0101 0001 0001 0001 0000

0393E 00 50 01 E4 D5 64 94 55   .P...d.U   0000 0000 0101 0000 0000 0001 1110 0100 1101 0101 0110 0100 1001 0100 0101 0101

03946 70 20 04 61 00 00 A0 00   p .a....   0111 0000 0010 0000 0000 0100 0110 0001 0000 0000 0000 0000 1010 0000 0000 0000

0394E 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

03956 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

0395E 00 00 00 00 00 00 00 A0   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 1010 0000

03966 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

0396E 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

03976 00 00 00 00 00 0F 03 F2   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 1111 0000 0011 1111 0010

0397E 80 00 00 00 00 00 00 00   ........   1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

03986 02 80 00 00 00 00 00 02   ........   0000 0010 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0010

0398E 24 02 87 89 21 A6 5A CA   $...!.Z.   0010 0100 0000 0010 1000 0111 1000 1001 0010 0001 1010 0110 0101 1010 1100 1010

03996 21 A4 02 80 00 00 00 00   !.......   0010 0001 1010 0100 0000 0010 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000

0399E 00 01 24 02 80 00 00 00   ..$.....   0000 0000 0000 0001 0010 0100 0000 0010 1000 0000 0000 0000 0000 0000 0000 0000

039A6 00 00 04 94 02 80 00 00   ........   0000 0000 0000 0000 0000 0100 1001 0100 0000 0010 1000 0000 0000 0000 0000 0000

039AE 00 00 00 00 00 02 80 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0010 1000 0000 0000 0000

039B6 00 00 00 00 00 00 04 60   .......`   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0100 0110 0000

039BE 00 04 66 40 04 60 10 04   ..f@.`..   0000 0000 0000 0100 0110 0110 0100 0000 0000 0100 0110 0000 0001 0000 0000 0100

039C6 60 10 04 60 00 04 60 00   `..`..`.   0110 0000 0001 0000 0000 0100 0110 0000 0000 0000 0000 0100 0110 0000 0000 0000

039CE 04 60 00 04 60 00 02 80   .`..`...   0000 0100 0110 0000 0000 0000 0000 0100 0110 0000 0000 0000 0000 0010 1000 0000

Open Design Specification for .dwg files

140



039D6 00 00 00 00 00 00 00 02   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0010

039DE 80 00 00 00 00 00 00 00   ........   1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

039E6 02 80 00 00 00 00 00 00   ........   0000 0010 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

039EE 00 02 80 00 00 00 00 00   ........   0000 0000 0000 0010 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

039F6 0E 03 F2 80 00 00 00 00   ........   0000 1110 0000 0011 1111 0010 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000

039FE 00 0E 03 F2 80 00 00 00   ........   0000 0000 0000 1110 0000 0011 1111 0010 1000 0000 0000 0000 0000 0000 0000 0000

03A06 00 00 0E 03 F2 80 00 00   ........   0000 0000 0000 0000 0000 1110 0000 0011 1111 0010 1000 0000 0000 0000 0000 0000

03A0E 00 00 00 0E 03 F4 60 00   ......`.   0000 0000 0000 0000 0000 0000 0000 1110 0000 0011 1111 0100 0110 0000 0000 0000

03A16 00 20 00 20 10 20 18 DA   . . . ..   0000 0000 0010 0000 0000 0000 0010 0000 0001 0000 0010 0000 0001 1000 1101 1010

03A1E 10 00 00 D6 C3 C4 90 D3   ........   0001 0000 0000 0000 0000 0000 1101 0110 1100 0011 1100 0100 1001 0000 1101 0011

03A26 2D 65 10 D2 00 00 00 00   -e......   0010 1101 0110 0101 0001 0000 1101 0010 0000 0000 0000 0000 0000 0000 0000 0000

03A2E 00 00 00 24 81 0F 12 43   ...$...C   0000 0000 0000 0000 0000 0000 0010 0100 1000 0001 0000 1111 0001 0010 0100 0011

03A36 4C B5 94 45 48 00 00 00   L..EH...   0100 1100 1011 0101 1001 0100 0100 0101 0100 1000 0000 0000 0000 0000 0000 0000

03A3E 00 00 00 01 12 01 82 88   ........   0000 0000 0000 0000 0000 0000 0000 0001 0001 0010 0000 0001 1000 0010 1000 1000

03A46 7A 05 08 12 90 09 28      z.....(    0111 1010 0000 0101 0000 1000 0001 0010 1001 0000 0000 1001 0010 1000

03A4D 6C 19                     crc
#### 20.4.39 ELLIPSE (35)
Note that the 10 pt and the 11 vector are WCS -- even though an ellipse is planar and has an extrusion
vector (210-group).

Common Entity Data

Center
3BD
10
(WCS)

SM axis vec
3BD
11
Semi-major axis vector (WCS)

Extrusion
3BD
210

Axis ratio
BD
40
Minor/major axis ratio

Beg angle
BD
41
Starting angle (eccentric anomaly, radians)

End angle
BD
42
Ending   angle (eccentric anomaly, radians)

Common Entity Handle Data

CRC
X
---
##### 20.4.39.1 Example:
OBJECT: ellipse (23H), len 4CH (76), handle: 01 22

0381E 4C 00                     L.         0100 1100 0000 0000

03820 48 C0 80 48 A1 48 10 00   H..H.H..   0100 1000 1100 0000 1000 0000 0100 1000 1010 0001 0100 1000 0001 0000 0000 0000

03828 05 5B 0C 0A 03 29 8A E7   .[...)..   0000 0101 0101 1011 0000 1100 0000 1010 0000 0011 0010 1001 1000 1010 1110 0111

Open Design Specification for .dwg files

141



03830 42 48 01 F0 9F BC 53 10   BH....S.   0100 0010 0100 1000 0000 0001 1111 0000 1001 1111 1011 1100 0101 0011 0001 0000

03838 40 DA 04 51 23 D0 F1 D6   @..Q#...   0100 0000 1101 1010 0000 0100 0101 0001 0010 0011 1101 0000 1111 0001 1101 0110

03840 AF 7B 9F 9A 89 15 EA 36   .{.....6   1010 1111 0111 1011 1001 1111 1001 1010 1000 1001 0001 0101 1110 1010 0011 0110

03848 B2 DD 17 F5 00 20 00 00   ..... ..   1011 0010 1101 1101 0001 0111 1111 0101 0000 0000 0010 0000 0000 0000 0000 0000

03850 00 00 1E 07 E5 D2 A4 7D   .......}   0000 0000 0000 0000 0001 1110 0000 0111 1110 0101 1101 0010 1010 0100 0111 1101

03858 B0 4C 5E F9 FC 0C 16 A2   .L^.....   1011 0000 0100 1100 0101 1110 1111 1001 1111 1100 0000 1100 0001 0110 1010 0010

03860 2A 7D 90 8C A0 18 28 87   *}....(.   0010 1010 0111 1101 1001 0000 1000 1100 1010 0000 0001 1000 0010 1000 1000 0111

03868 E0 83 A0 69               ...i       1110 0000 1000 0011 1010 0000 0110 1001

0386C ED 08                     crc
#### 20.4.40 SPLINE (36)

Common Entity Data

Scenario
BL

a flag which is 2 for fitpts only, 1 for
ctrlpts/knots.




In 2013 the meaning is somehwat more sophisticated,
see knot parameter below.
R2013+:

Spline flags 1
BL

Spline flags 1:

method fit points = 1,
CV frame show = 2,
Is closed = 4. At this point the regular spline
flags closed bit is made equal to this bit. Value is
overwritten below in scenario 2 though,
Use knot parameter = 8

Knot parameter
BL

Knot parameter:

Chord = 0,
Square root = 1,
Uniform = 2,
Custom = 15

The scenario flag becomes 1 if the knot parameter is
Custom or has no fit data, otherwise 2. If the
spline does not have fit data, then the knot
parameter should become Custom.
Common:

Degree
BL

degree of this spline
If (scenario==2) {

Fit Tol
BD
44

Beg tan vec
3BD
12
Beginning tangent direction vector (normalized).

End tan vec
3BD
13
Ending    tangent direction vector (normalized).

num fit pts
BL
74
Number of fit points. Stored as a LONG, although it
is defined in DXF as a short.  You can see this if
you create a spline with >=256 fit points

Open Design Specification for .dwg files

142




}
if (scenario==1) {

Rational
B

flag bit 2

Closed
B

flag bit 0

Periodic
B

flag bit 1

Knot tol
BD
42

Ctrl tol
BD
43

Numknots
BL
72
This is stored as a LONG, although it is defined in
DXF as a short. You can see this if you create a
spline with >=256 knots.

Numctrlpts
BL
73
Number of 10's (and 41's, if weighted) that follow.
Same, stored as LONG, defined in DXF as a short.

Weight
B

Seems to be an echo of the 4 bit on the flag for
"weights present".
}
Repeat numknots times {

Knot
BD

knot value
}
Repeat numctrlpts times {

Control pt
3BD
10

Weight
D
41
if present as indicated by 4 bit on flag
}
Repeat numfitpts times {

Fit pt
3BD
}

Common Entity Handle Data

CRC
X
---
##### 20.4.40.1 Example:
OBJECT: spline (24H), len 61H (97), handle: 01 01

01AC5 61 00                     a.         0110 0001 0000 0000

01AC7 49 00 80 40 66 A8 10 00   I..@f...   0100 1001 0000 0000 1000 0000 0100 0000 0110 0110 1010 1000 0001 0000 0000 0000

01ACF 05 5B 20 48 19 77 7B AF   .[ H.w{.   0000 0101 0101 1011 0010 0000 0100 1000 0001 1001 0111 0111 0111 1011 1010 1111

01AD7 B3 BE F9 B6 7B 55 48 21   ....{UH!   1011 0011 1011 1110 1111 1001 1011 0110 0111 1011 0101 0101 0100 1000 0010 0001

01ADF D1 F6 EC 49 3D 16 1C 80   ...I=...   1101 0001 1111 0110 1110 1100 0100 1001 0011 1101 0001 0110 0001 1100 1000 0000

01AE7 60 3C 07 63 43 16 F8 9F   `<.cC...   0110 0000 0011 1100 0000 0111 0110 0011 0100 0011 0001 0110 1111 1000 1001 1111

01AEF C0 E4 4E 53 64 CA 30 B2   ..NSd.0.   1100 0000 1110 0100 0100 1110 0101 0011 0110 0100 1100 1010 0011 0000 1011 0010

01AF7 01 F0 33 3C 1C A7 C2 0E   ..3<....   0000 0001 1111 0000 0011 0011 0011 1100 0001 1100 1010 0111 1100 0010 0000 1110


Open Design Specification for .dwg files

143


01AFF 81 01 85 80 9A FE 6F 63   ......oc   1000 0001 0000 0001 1000 0101 1000 0000 1001 1010 1111 1110 0110 1111 0110 0011

01B07 88 02 07 89 BE 3C 1B 4F   .....<.O   1000 1000 0000 0010 0000 0111 1000 1001 1011 1110 0011 1100 0001 1011 0100 1111

01B0F 51 FC 5F 51 14 FA 2F CF   Q._Q../.   0101 0001 1111 1100 0101 1111 0101 0001 0001 0100 1111 1010 0010 1111 1100 1111

01B17 94 20 04 18 CB 8B BB C6   . ......   1001 0100 0010 0000 0000 0100 0001 1000 1100 1011 1000 1011 1011 1011 1100 0110

01B1F 9D 67 F1 82 88 7E 08 13   .g...~..   1001 1101 0110 0111 1111 0001 1000 0010 1000 1000 0111 1110 0000 1000 0001 0011

01B27 05                        .          0000 0101

01B28 99 F5                     crc
OBJECT: spline (24H), len BBH (187), handle: 01 02

01B2A BB 00                     ..         1011 1011 0000 0000

01B2C 49 00 80 40 A5 C8 28 00   I..@..(.   0100 1001 0000 0000 1000 0000 0100 0000 1010 0101 1100 1000 0010 1000 0000 0000

01B34 05 7B 20 28 18 12 2B EF   .{ (..+.   0000 0101 0111 1011 0010 0000 0010 1000 0001 1000 0001 0010 0010 1011 1110 1111

01B3C 26 BC B5 DE 8F 84 8A FB   &.......   0010 0110 1011 1100 1011 0101 1101 1110 1000 1111 1000 0100 1000 1010 1111 1011

01B44 C9 AF 2D 77 A3 E4 29 06   ..-w..).   1100 1001 1010 1111 0010 1101 0111 0111 1010 0011 1110 0100 0010 1001 0000 0110

01B4C 55 01 E2 91 A5 D0 17 80   U.......   0101 0101 0000 0001 1110 0010 1001 0001 1010 0101 1101 0000 0001 0111 1000 0000

01B54 88 04 31 35 FD 44 D0 08   ..15.D..   1000 1000 0000 0100 0011 0001 0011 0101 1111 1101 0100 0100 1101 0000 0000 1000

01B5C AA 01 79 09 BE 48 77 C4   ..y..Hw.   1010 1010 0000 0001 0111 1001 0000 1001 1011 1110 0100 1000 0111 0111 1100 0100

01B64 48 80 5E 42 6F 92 1D F1   H.^Bo...   0100 1000 1000 0000 0101 1110 0100 0010 0110 1111 1001 0010 0001 1101 1111 0001

01B6C 12 20 17 90 9B E4 87 7C   . .....|   0001 0010 0010 0000 0001 0111 1001 0000 1001 1011 1110 0100 1000 0111 0111 1100

01B74 44 88 05 E4 26 F9 21 DF   D...&.!.   0100 0100 1000 1000 0000 0101 1110 0100 0010 0110 1111 1001 0010 0001 1101 1111

01B7C 11 22 00 51 81 5C A9 30   .".Q.\.0   0001 0001 0010 0010 0000 0000 0101 0001 1000 0001 0101 1100 1010 1001 0011 0000

01B84 EA 18 80 40 1B 4B CF 66   ...@.K.f   1110 1010 0001 1000 1000 0000 0100 0000 0001 1011 0100 1011 1100 1111 0110 0110

01B8C F3 7D 9F C4 63 6D AF 9B   .}..cm..   1111 0011 0111 1101 1001 1111 1100 0100 0110 0011 0110 1101 1010 1111 1001 1011

01B94 7D A8 82 00 51 75 80 5C   }...Qu.\   0111 1101 1010 1000 1000 0010 0000 0000 0101 0001 0111 0101 1000 0000 0101 1100

01B9C B0 1C 0C 81 09 D0 81 4C   .......L   1011 0000 0001 1100 0000 1100 1000 0001 0000 1001 1101 0000 1000 0001 0100 1100

01BA4 07 B7 62 A8 05 58 F7 A1   ..b..X..   0000 0111 1011 0111 0110 0010 1010 1000 0000 0101 0101 1000 1111 0111 1010 0001

01BAC 59 01 E8 9A 04 5B 36 58   Y....[6X   0101 1001 0000 0001 1110 1000 1001 1010 0000 0100 0101 1011 0011 0110 0101 1000

01BB4 8C 6B 16 0E 20 1F C2 20   .k.. ..    1000 1100 0110 1011 0001 0110 0000 1110 0010 0000 0001 1111 1100 0010 0010 0000

01BBC 5C 89 E6 DA 97 F1 0C 22   \......"   0101 1100 1000 1001 1110 0110 1101 1010 1001 0111 1111 0001 0000 1100 0010 0010

01BC4 B6 2B 1A 3A 48 80 23 05   .+.:H.#.   1011 0110 0010 1011 0001 1010 0011 1010 0100 1000 1000 0000 0010 0011 0000 0101

01BCC 1E F2 8C 22 74 9F C6 74   ..."t..t   0001 1110 1111 0010 1000 1100 0010 0010 0111 0100 1001 1111 1100 0110 0111 0100

01BD4 99 BC 06 F0 C9 42 01 A0   .....B..   1001 1001 1011 1100 0000 0110 1111 0000 1100 1001 0100 0010 0000 0001 1010 0000

01BDC 40 6E 0F 6C A7 F0 7F 18   @n.l....   0100 0000 0110 1110 0000 1111 0110 1100 1010 0111 1111 0000 0111 1111 0001 1000


Open Design Specification for .dwg files

144


01BE4 28 87 D7                  (..        0010 1000 1000 0111 1101 0111

01BE7 E3 F3                     crc
#### 20.4.41 REGION  (37)       3DSOLID (38)     BODY    (39)
These are all ACIS entities.  We do not have a complete decryption of these, although we can step them,
and write them, properly.

Common Entity Data
After this, data are read as groups starting with a short which seems to indicate the type of data.  This is
not completely understood.  The current algorithm is:

ACIS Empty bit B
X
If 1, then no data follows

Unknown bit
B
X

Version
BS

Can be 1 or 2.
Version == 1 (following 2 items repeat until Block Size is 0):

Block Size
BL
X
Number of bytes of SAT data in this block. if value
is between 0x20 and 0x7E, calculate 0x9F-the value
to get the real character.  If it's a tab, we
convert to a space.

SAT data
RC
X
Length is specified by the above count.
Version == 2:

Immediately following will be an acis file.  Header value of “ACIS BinaryFile” indicates
SAB, otherwise it is a text SAT file.  No length is given.  SAB files will end with
“End\x0E\x02of\x0E\x04ACIS\x0D\x04data”.  SAT files must be parsed to find the end.

Common:

Wireframe data present B
X
True if wireframe data is present
Wireframe == true:

Point present
B
X
If true, following point is present, otherwise
assume 0,0,0 for point

Point
3BD
X
Present if above bit is 1.

Num IsoLines
BL
X


IsoLines present
B
X
If true, isoline data is present.

Num Wires
BL
X
Number of ISO lines that follow.
Repeat Num Wires times:

Wire type
RC
X

Wire selection marker BL
X

Wire color
BS
X

Wire Acis Index
BL
X

Wire # of points
BL
X

Open Design Specification for .dwg files

145



Point
3BD
X
Repeats “Wire # of points” times.

Transform present
B
X
If “Transform present” == 1:

X Axis
3BD
X

Y Axis
3BD
X

Z Axis
3BD
X

Translation
3BD
X

Scale
BD
X

Has rotation
B
X

Has reflection
B
X

Has shear
B
X
End If
End Repeat

Num. silhouettes
BL
X
Repeat “Num. silhouettes” times:

VP id
BL
X

VP Target
3BD
X

VP dir. From target
3BD
X

VP up dir.
3BD
X

VP perspective
B
X

Num Wires
BL
X
Repeat “Num Wires” times:

Same as above
End Repeat

ACIS Empty bit
B
X
Normally 1.  If 0, then acis data follows in the
same format as described above, except no wireframe
of silhouette data will be present (no empty bits
for these items either).
R2007+:

Unknown
BL
Common:

Common Entity Handle Data
R2007+:


H
350
History ID
Common:

CRC
X
---
##### 20.4.41.1 Example:
OBJECT: region (25H), len 22DH (557), handle: 01 03

01BE9 2D 02                     -.         0010 1101 0000 0010

01BEB 49 40 80 40 E2 48 88 00   I@.@.H..   0100 1001 0100 0000 1000 0000 0100 0000 1110 0010 0100 1000 1000 1000 0000 0000

Open Design Specification for .dwg files

146



01BF3 05 7B 28 08 0C 04 00 00   .{(.....   0000 0101 0111 1011 0010 1000 0000 1000 0000 1100 0000 0100 0000 0000 0000 0000

01BFB DC DE D2 40 DC DC 40 DC   ...@..@.   1101 1100 1101 1110 1101 0010 0100 0000 1101 1100 1101 1100 0100 0000 1101 1100

01C03 40 DE 40 40 40 40 40 40   @.@@@@@@   0100 0000 1101 1110 0100 0000 0100 0000 0100 0000 0100 0000 0100 0000 0100 0000

01C0B 40 40 40 40 1A 14 7A 60   @@@@..z`   0100 0000 0100 0000 0100 0000 0100 0000 0001 1010 0001 0100 0111 1010 0110 0000

01C13 76 4C 40 F6 E4 DC 40 F6   vL@...@.   0111 0110 0100 1100 0100 0000 1111 0110 1110 0100 1101 1100 0100 0000 1111 0110

01C1B DC 40 F6 E4 DC 40 F6 E4   .@...@..   1101 1100 0100 0000 1111 0110 1110 0100 1101 1100 0100 0000 1111 0110 1110 0100

01C23 DC 40 F8 1A 14 66 54 64   .@...fTd   1101 1100 0100 0000 1111 1000 0001 1010 0001 0100 0110 0110 0101 0100 0110 0100

01C2B 5E 40 F6 E4 DC 40 F6 E4   ^@...@..   0101 1110 0100 0000 1111 0110 1110 0100 1101 1100 0100 0000 1111 0110 1110 0100

01C33 DC 40 F6 DA 40 F6 DE 40   .@..@..@   1101 1100 0100 0000 1111 0110 1101 1010 0100 0000 1111 0110 1101 1110 0100 0000

01C3B F8 1A 14 58 6E 74 66 66   ...Xntff   1111 1000 0001 1010 0001 0100 0101 1000 0110 1110 0111 0100 0110 0110 0110 0110

01C43 40 F6 E4 DC 40 F6 E4 DC   @...@...   0100 0000 1111 0110 1110 0100 1101 1100 0100 0000 1111 0110 1110 0100 1101 1100

01C4B 40 F6 E4 DC 40 F6 D8 40   @...@..@   0100 0000 1111 0110 1110 0100 1101 1100 0100 0000 1111 0110 1101 1000 0100 0000

01C53 F6 DC 40 F8 1A 14 72 7C   ..@...r|   1111 0110 1101 1100 0100 0000 1111 1000 0001 1010 0001 0100 0111 0010 0111 1100

01C5B 78 74 40 F6 E4 DC 40 F6   xt@...@.   0111 1000 0111 0100 0100 0000 1111 0110 1110 0100 1101 1100 0100 0000 1111 0110

01C63 E4 DC 40 F6 D6 40 F6 DA   ..@..@..   1110 0100 1101 1100 0100 0000 1111 0110 1101 0110 0100 0000 1111 0110 1101 1010

01C6B 40 F6 E4 DC 40 F6 D4 40   @...@..@   0100 0000 1111 0110 1110 0100 1101 1100 0100 0000 1111 0110 1101 0100 0100 0000

01C73 72 60 5A 50 7C 5A 76 40   r`ZP|Zv@   0111 0010 0110 0000 0101 1010 0101 0000 0111 1100 0101 1010 0111 0110 0100 0000

01C7B 76 60 54 7A 66 74 40 60   v`Tzft@`   0111 0110 0110 0000 0101 0100 0111 1010 0110 0110 0111 0100 0100 0000 0110 0000

01C83 54 56 40 F8 1A 14 66 60   TV@...f`   0101 0100 0101 0110 0100 0000 1111 1000 0001 1010 0001 0100 0110 0110 0110 0000

01C8B 60 5E 40 F6 E4 DC 40 F6   `^@...@.   0110 0000 0101 1110 0100 0000 1111 0110 1110 0100 1101 1100 0100 0000 1111 0110

01C93 E4 DC 40 F6 D2 40 F6 D8   ..@..@..   1110 0100 1101 1100 0100 0000 1111 0110 1101 0010 0100 0000 1111 0110 1101 1000

01C9B 40 F8 1A 14 5E 66 7C 62   @...^f|b   0100 0000 1111 1000 0001 1010 0001 0100 0101 1110 0110 0110 0111 1100 0110 0010

01CA3 74 E4 58 54 5A 72 7C 78   t.XTZr|x   0111 0100 1110 0100 0101 1000 0101 0100 0101 1010 0111 0010 0111 1100 0111 1000

01CAB 74 40 F6 E4 DC 40 CE E2   t@...@..   0111 0100 0100 0000 1111 0110 1110 0100 1101 1100 0100 0000 1100 1110 1110 0010

01CB3 DC DE DC CC D0 D2 D8 DC   ........   1101 1100 1101 1110 1101 1100 1100 1100 1101 0000 1101 0010 1101 1000 1101 1100

01CBB DA D6 D6 D0 D6 CC CC D4   ........   1101 1010 1101 0110 1101 0110 1101 0000 1101 0110 1100 1100 1100 1100 1101 0100

01CC3 40 DC E2 CE D0 D6 DC D0   @.......   0100 0000 1101 1100 1110 0010 1100 1110 1101 0000 1101 0110 1101 1100 1101 0000

01CCB DC D2 DC CE D4 D4 DA DE   ........   1101 1100 1101 0010 1101 1100 1100 1110 1101 0100 1101 0100 1101 1010 1101 1110

01CD3 D2 DC D2 40 DE 40 DE 40   ...@.@.@   1101 0010 1101 1100 1101 0010 0100 0000 1101 1110 0100 0000 1101 1110 0100 0000

01CDB DE 40 DC 40 DC 40 DE 40   .@.@.@.@   1101 1110 0100 0000 1101 1100 0100 0000 1101 1100 0100 0000 1101 1110 0100 0000

01CE3 DE 40 DE 40 AC 40 AC 40   .@.@.@.@   1101 1110 0100 0000 1101 1110 0100 0000 1010 1100 0100 0000 1010 1100 0100 0000

01CEB AC 40 AC 40 F8 1A 14 78   .@.@...x   1010 1100 0100 0000 1010 1100 0100 0000 1111 1000 0001 1010 0001 0100 0111 1000

Open Design Specification for .dwg files

147



01CF3 60 74 76 70 74 40 F6 E4   `tvpt@..   0110 0000 0111 0100 0111 0110 0111 0000 0111 0100 0100 0000 1111 0110 1110 0100

01CFB DC 40 F6 D2 40 F6 D2 40   .@..@..@   1101 1100 0100 0000 1111 0110 1101 0010 0100 0000 1111 0110 1101 0010 0100 0000

01D03 F6 E4 DC 40 F6 D0 40 DE   ...@..@.   1111 0110 1110 0100 1101 1100 0100 0000 1111 0110 1101 0000 0100 0000 1101 1110

01D0B 40 F6 D6 40 F6 E4 DC 40   @..@...@   0100 0000 1111 0110 1101 0110 0100 0000 1111 0110 1110 0100 1101 1100 0100 0000

01D13 F8 1A 14 74 76 70 74 40   ...tvpt@   1111 1000 0001 1010 0001 0100 0111 0100 0111 0110 0111 0000 0111 0100 0100 0000

01D1B F6 E4 DC 40 F6 CE 40 F6   ...@..@.   1111 0110 1110 0100 1101 1100 0100 0000 1111 0110 1100 1110 0100 0000 1111 0110

01D23 CE 40 F6 D2 40 F6 CC 40   .@..@..@   1100 1110 0100 0000 1111 0110 1101 0010 0100 0000 1111 0110 1100 1100 0100 0000

01D2B DE 40 F8 1A 14 52 74 5A   .@...RtZ   1101 1110 0100 0000 1111 1000 0001 1010 0001 0100 0101 0010 0111 0100 0101 1010

01D33 56 74 4E 40 F6 E4 DC 40   VtN@...@   0101 0110 0111 0100 0100 1110 0100 0000 1111 0110 1110 0100 1101 1100 0100 0000

01D3B F6 D0 40 F6 DC DE 40 F8   ..@...@.   1111 0110 1101 0000 0100 0000 1111 0110 1101 1100 1101 1110 0100 0000 1111 1000

01D43 1A 14 74 66 66 6C 5E 58   ..tffl^X   0001 1010 0001 0100 0111 0100 0110 0110 0110 0110 0110 1100 0101 1110 0101 1000

01D4B 74 E4 78 54 5A 52 74 40   t.xTZRt@   0111 0100 1110 0100 0111 1000 0101 0100 0101 1010 0101 0010 0111 0100 0100 0000

01D53 F6 E4 DC 40 CE E2 DC DE   ...@....   1111 0110 1110 0100 1101 1100 0100 0000 1100 1110 1110 0010 1101 1100 1101 1110

01D5B DC CC D0 D2 D8 DC DA D6   ........   1101 1100 1100 1100 1101 0000 1101 0010 1101 1000 1101 1100 1101 1010 1101 0110

01D63 D6 D0 D4 DE DC D8 40 DC   ......@.   1101 0110 1101 0000 1101 0100 1101 1110 1101 1100 1101 1000 0100 0000 1101 1100

01D6B E2 CE D0 D6 DC D0 DC D2   ........   1110 0010 1100 1110 1101 0000 1101 0110 1101 1100 1101 0000 1101 1100 1101 0010

01D73 DC CE D4 D4 DA DE D2 D8   ........   1101 1100 1100 1110 1101 0100 1101 0100 1101 1010 1101 1110 1101 0010 1101 1000

01D7B D6 40 DE 40 DE 40 DE 40   .@.@.@.@   1101 0110 0100 0000 1101 1110 0100 0000 1101 1110 0100 0000 1101 1110 0100 0000

01D83 DC 40 DE E2 D2 D8 D0 D4   .@......   1101 1100 0100 0000 1101 1110 1110 0010 1101 0010 1101 1000 1101 0000 1101 0100

01D8B DE D2 D8 CE DA D2 D0 D4   ........   1101 1110 1101 0010 1101 1000 1100 1110 1101 1010 1101 0010 1101 0000 1101 0100

01D93 D6 DA CE DC D6 40 E4 DE   .....@..   1101 0110 1101 1010 1100 1110 1101 1100 1101 0110 0100 0000 1110 0100 1101 1110

01D9B E2 CC DA DA D0 DA D0 CC   ........   1110 0010 1100 1100 1101 1010 1101 1010 1101 0000 1101 1010 1101 0000 1100 1100

01DA3 DE DA D2 D6 D8 D6 D8 D0   ........   1101 1110 1101 1010 1101 0010 1101 0110 1101 1000 1101 0110 1101 1000 1101 0000

01DAB DA CC 40 DE 40 DE E2 D6   ..@.@...   1101 1010 1100 1100 0100 0000 1101 1110 0100 0000 1101 1110 1110 0010 1101 0110

01DB3 D4 D0 D4 DA D4 CC D4 DC   ........   1101 0100 1101 0000 1101 0100 1101 1010 1101 0100 1100 1100 1101 0100 1101 1100

01DBB D8 D0 CC DC DA D8 D4 D4   ........   1101 1000 1101 0000 1100 1100 1101 1100 1101 1010 1101 1000 1101 0100 1101 0100

01DC3 40 AC 40 AC 40 F8 1A 14   @.@.@...   0100 0000 1010 1100 0100 0000 1010 1100 0100 0000 1111 1000 0001 1010 0001 0100

01DCB 5E 60 6C 62 56 40 F6 E4   ^`lbV@..   0101 1110 0110 0000 0110 1100 0110 0010 0101 0110 0100 0000 1111 0110 1110 0100

01DD3 DC 40 CE E2 D0 D8 CC D6   .@......   1101 1100 0100 0000 1100 1110 1110 0010 1101 0000 1101 1000 1100 1100 1101 0110

01DDB CE DA D2 CC D4 DC DA DA   ........   1100 1110 1101 1010 1101 0010 1100 1100 1101 0100 1101 1100 1101 1010 1101 1010

01DE3 CC DA CE D0 40 DE E2 CC   ....@...   1100 1100 1101 1010 1100 1110 1101 0000 0100 0000 1101 1110 1110 0010 1100 1100

01DEB D4 DC D6 D6 D8 D0 DC D4   ........   1101 0100 1101 1100 1101 0110 1101 0110 1101 1000 1101 0000 1101 1100 1101 0100

Open Design Specification for .dwg files

148



01DF3 CC DE CE D2 DA D2 DE CC   ........   1100 1100 1101 1110 1100 1110 1101 0010 1101 1010 1101 0010 1101 1110 1100 1100

01DFB 40 DE 40 F8 1A 15 63 F6   @.@...c.   0100 0000 1101 1110 0100 0000 1111 1000 0001 1010 0001 0101 0110 0011 1111 0110

01E03 D9 E9 E9 B1 A1 02 00 50   .......P   1101 1001 1110 1001 1110 1001 1011 0001 1010 0001 0000 0010 0000 0000 0101 0000

01E0B B8 18 C3 37 F9 FA 7F 20   ...7...    1011 1000 0001 1000 1100 0011 0011 0111 1111 1001 1111 1010 0111 1111 0010 0000

01E13 9A 98 28 87 80            ..(..      1001 1010 1001 1000 0010 1000 1000 0111 1000 0000

01E18 07 33                     crc
OBJECT: 3d solid (26H), len 334H (820), handle: 01 04

01E1A 34 03                     4.         0011 0100 0000 0011

01E1C 49 80 80 41 24 30 C8 00   I..A$0..   0100 1001 1000 0000 1000 0000 0100 0001 0010 0100 0011 0000 1100 1000 0000 0000

01E24 05 7B 28 0B E4 DC DE D2   .{(.....   0000 0101 0111 1011 0010 1000 0000 1011 1110 0100 1101 1100 1101 1110 1101 0010

01E2C 40 D4 40 DC 40 DE 40 40   @.@.@.@@   0100 0000 1101 0100 0100 0000 1101 1100 0100 0000 1101 1110 0100 0000 0100 0000

01E34 40 40 40 40 40 40 40 40   @@@@@@@@   0100 0000 0100 0000 0100 0000 0100 0000 0100 0000 0100 0000 0100 0000 0100 0000

01E3C 40 1A 14 7A 60 76 4C 40   @..z`vL@   0100 0000 0001 1010 0001 0100 0111 1010 0110 0000 0111 0110 0100 1100 0100 0000

01E44 F6 E4 DC 40 F6 DC 40 F6   ...@..@.   1111 0110 1110 0100 1101 1100 0100 0000 1111 0110 1101 1100 0100 0000 1111 0110

01E4C E4 DC 40 F6 E4 DC 40 F8   ..@...@.   1110 0100 1101 1100 0100 0000 1111 0110 1110 0100 1101 1100 0100 0000 1111 1000

01E54 1A 14 66 54 64 5E 40 F6   ..fTd^@.   0001 1010 0001 0100 0110 0110 0101 0100 0110 0100 0101 1110 0100 0000 1111 0110

01E5C E4 DC 40 F6 E4 DC 40 F6   ..@...@.   1110 0100 1101 1100 0100 0000 1111 0110 1110 0100 1101 1100 0100 0000 1111 0110

01E64 DA 40 F6 DE 40 F8 1A 14   .@..@...   1101 1010 0100 0000 1111 0110 1101 1110 0100 0000 1111 1000 0001 1010 0001 0100

01E6C 58 6E 74 66 66 40 F6 E4   Xntff@..   0101 1000 0110 1110 0111 0100 0110 0110 0110 0110 0100 0000 1111 0110 1110 0100

01E74 DC 40 F6 E4 DC 40 F6 E4   .@...@..   1101 1100 0100 0000 1111 0110 1110 0100 1101 1100 0100 0000 1111 0110 1110 0100

01E7C DC 40 F6 D8 40 F6 DC 40   .@..@..@   1101 1100 0100 0000 1111 0110 1101 1000 0100 0000 1111 0110 1101 1100 0100 0000

01E84 F8 1A 14 72 7C 78 74 40   ...r|xt@   1111 1000 0001 1010 0001 0100 0111 0010 0111 1100 0111 1000 0111 0100 0100 0000

01E8C F6 E4 DC 40 F6 E4 DC 40   ...@...@   1111 0110 1110 0100 1101 1100 0100 0000 1111 0110 1110 0100 1101 1100 0100 0000

01E94 F6 E4 DC 40 F6 DA 40 F6   ...@..@.   1111 0110 1110 0100 1101 1100 0100 0000 1111 0110 1101 1010 0100 0000 1111 0110

01E9C E4 DC 40 F6 D6 40 72 60   ..@..@r`   1110 0100 1101 1100 0100 0000 1111 0110 1101 0110 0100 0000 0111 0010 0110 0000

01EA4 5A 50 7C 5A 76 40 58 6C   ZP|Zv@Xl   0101 1010 0101 0000 0111 1100 0101 1010 0111 0110 0100 0000 0101 1000 0110 1100

01EAC 62 70 66 74 40 F8 1A 14   bpft@...   0110 0010 0111 0000 0110 0110 0111 0100 0100 0000 1111 1000 0001 1010 0001 0100

01EB4 58 5E 6E 74 5A 74 E4 58   X^ntZt.X   0101 1000 0101 1110 0110 1110 0111 0100 0101 1010 0111 0100 1110 0100 0101 1000

01EBC 54 5A 72 7C 78 74 40 F6   TZr|xt@.   0101 0100 0101 1010 0111 0010 0111 1100 0111 1000 0111 0100 0100 0000 1111 0110

01EC4 E4 DC 40 DC DE E2 DA D2   ..@.....   1110 0100 1101 1100 0100 0000 1101 1100 1101 1110 1110 0010 1101 1010 1101 0010

01ECC DA D4 DE D8 D8 D6 D8 CC   ........   1101 1010 1101 0100 1101 1110 1101 1000 1101 1000 1101 0110 1101 1000 1100 1100

01ED4 CE D8 DC DA D8 40 CE E2   .....@..   1100 1110 1101 1000 1101 1100 1101 1010 1101 1000 0100 0000 1100 1110 1110 0010

Open Design Specification for .dwg files

149



01EDC D6 D6 D2 DC CE D6 DE D6   ........   1101 0110 1101 0110 1101 0010 1101 1100 1100 1110 1101 0110 1101 1110 1101 0110

01EE4 CC D0 DE CC D4 CC D0 40   .......@   1100 1100 1101 0000 1101 1110 1100 1100 1101 0100 1100 1100 1101 0000 0100 0000

01EEC DE 40 DE E2 CE D6 D8 DE   .@......   1101 1110 0100 0000 1101 1110 1110 0010 1100 1110 1101 0110 1101 1000 1101 1110

01EF4 D4 D4 D2 D4 CE D4 DC DE   ........   1101 0100 1101 0100 1101 0010 1101 0100 1100 1110 1101 0100 1101 1100 1101 1110

01EFC DC CC CC CC DA 40 DC 40   .....@.@   1101 1100 1100 1100 1100 1100 1100 1100 1101 1010 0100 0000 1101 1100 0100 0000

01F04 DE 40 DE 40 DE 40 DE 40   .@.@.@.@   1101 1110 0100 0000 1101 1110 0100 0000 1101 1110 0100 0000 1101 1110 0100 0000

01F0C DC 40 DE 40 AC 40 AC 40   .@.@.@.@   1101 1100 0100 0000 1101 1110 0100 0000 1010 1100 0100 0000 1010 1100 0100 0000

01F14 AC 40 AC 40 F8 1A 15 60   .@.@...`   1010 1100 0100 0000 1010 1100 0100 0000 1111 1000 0001 1010 0001 0101 0110 0000

01F1C 77 FC D6 B3 34 31 22 01   w...41".   0111 0111 1111 1100 1101 0110 1011 0011 0011 0100 0011 0001 0010 0010 0000 0001

01F24 8D FE B4 78 E5 C8 40 81   ...x..@.   1000 1101 1111 1110 1011 0100 0111 1000 1110 0101 1100 1000 0100 0000 1000 0001

01F2C 20 94 1C 0C FF FF FF FF    .......   0010 0000 1001 0100 0001 1100 0000 1100 1111 1111 1111 1111 1111 1111 1111 1111

01F34 CF FF FF FF F4 0C 0E FF   ........   1100 1111 1111 1111 1111 1111 1111 1111 1111 0100 0000 1100 0000 1110 1111 1111

01F3C 9A D6 66 86 24 40 32 3F   ..f.$@2?   1001 1010 1101 0110 0110 0110 1000 0110 0010 0100 0100 0000 0011 0010 0011 1111

01F44 D6 8F 1C B9 08 10 02 84   ........   1101 0110 1000 1111 0001 1100 1011 1001 0000 1000 0001 0000 0000 0010 1000 0100

01F4C A4 0D C4 FF AE AB F0 33   .......3   1010 0100 0000 1101 1100 0100 1111 1111 1010 1110 1010 1011 1111 0000 0011 0011

01F54 FE 6B 59 9A 18 91 00 47   .kY....G   1111 1110 0110 1011 0101 1001 1001 1010 0001 1000 1001 0001 0000 0000 0100 0111

01F5C F6 2D 7D 9A 69 1E 40 80   .-}.i.@.   1111 0110 0010 1101 0111 1101 1001 1010 0110 1001 0001 1110 0100 0000 1000 0000

01F64 EF F9 AD 66 68 62 44 03   ...fhbD.   1110 1111 1111 1001 1010 1101 0110 0110 0110 1000 0110 0010 0100 0100 0000 0011

01F6C 23 FD 68 F1 CB 90 81 00   #.h.....   0010 0011 1111 1101 0110 1000 1111 0001 1100 1011 1001 0000 1000 0001 0000 0000

01F74 28 4A 40 DC 4F FA EA 3F   (J@.O..?   0010 1000 0100 1010 0100 0000 1101 1100 0100 1111 1111 1010 1110 1010 0011 1111

01F7C 01 9F FF FF FF F9 FF FF   ........   0000 0001 1001 1111 1111 1111 1111 1111 1111 1111 1111 1001 1111 1111 1111 1111

01F84 FF FE 81 81 9F F3 5A CC   ......Z.   1111 1111 1111 1110 1000 0001 1000 0001 1001 1111 1111 0011 0101 1010 1100 1100

01F8C D0 C4 88 06 37 FA D1 E3   ....7...   1101 0000 1100 0100 1000 1000 0000 0110 0011 0111 1111 1010 1101 0001 1110 0011

01F94 97 21 02 00 60 94 81 B8   .!..`...   1001 0111 0010 0001 0000 0010 0000 0000 0110 0000 1001 0100 1000 0001 1011 1000

01F9C 9F F5 D5 7E 58 81 AF EA   ...~X...   1001 1111 1111 0101 1101 0101 0111 1110 0101 1000 1000 0001 1010 1111 1110 1010

01FA4 05 9B 13 20 18 DF EB 47   ... ...G   0000 0101 1001 1011 0001 0011 0010 0000 0001 1000 1101 1111 1110 1011 0100 0111

01FAC 8E 5C 84 08 10 19 FF 35   .\.....5   1000 1110 0101 1100 1000 0100 0000 1000 0001 0000 0001 1001 1111 1111 0011 0101

01FB4 AC CD 0C 48 80 63 7F AD   ...H.c..   1010 1100 1100 1101 0000 1100 0100 1000 1000 0000 0110 0011 0111 1111 1010 1101

01FBC 1E 39 72 10 20 06 09 48   .9r. ..H   0001 1110 0011 1001 0111 0010 0001 0000 0010 0000 0000 0110 0000 1001 0100 1000

01FC4 1B 89 FF 5D 47 E0 33 FF   ...]G.3.   0001 1011 1000 1001 1111 1111 0101 1101 0100 0111 1110 0000 0011 0011 1111 1111

01FCC FF FF FF 3F FF FF FF D0   ...?....   1111 1111 1111 1111 1111 1111 0011 1111 1111 1111 1111 1111 1111 1111 1101 0000

01FD4 30 3B FE 6B 59 9A 18 91   0;.kY...   0011 0000 0011 1011 1111 1110 0110 1011 0101 1001 1001 1010 0001 1000 1001 0001

Open Design Specification for .dwg files

150



01FDC 00 C4 FF 5A 3C 72 E4 20   ...Z<r.    0000 0000 1100 0100 1111 1111 0101 1010 0011 1100 0111 0010 1110 0100 0010 0000

01FE4 40 0C 12 90 37 13 FE BA   @...7...   0100 0000 0000 1100 0001 0010 1001 0000 0011 0111 0001 0011 1111 1110 1011 1010

01FEC AF C0 CF F9 AD 66 68 62   .....fhb   1010 1111 1100 0000 1100 1111 1111 1001 1010 1101 0110 0110 0110 1000 0110 0010

01FF4 44 01 A4 10 7C E8 5E 50   D...|.^P   0100 0100 0000 0001 1010 0100 0001 0000 0111 1100 1110 1000 0101 1110 0101 0000

01FFC 89 02 03 BF E6 B5 99 A1   ........   1000 1001 0000 0010 0000 0011 1011 1111 1110 0110 1011 0101 1001 1001 1010 0001

02004 89 10 0C 4F F5 A3 C7 2E   ...O....   1000 1001 0001 0000 0000 1100 0100 1111 1111 0101 1010 0011 1100 0111 0010 1110

0200C 42 04 00 C1 29 03 71 3F   B...).q?   0100 0010 0000 0100 0000 0000 1100 0001 0010 1001 0000 0011 0111 0001 0011 1111

02014 EB A8 FC 06 7F FF FF FF   ........   1110 1011 1010 1000 1111 1100 0000 0110 0111 1111 1111 1111 1111 1111 1111 1111

0201C E7 FF FF FF FA 06 08 7F   ........   1110 0111 1111 1111 1111 1111 1111 1111 1111 1010 0000 0110 0000 1000 0111 1111

02024 CD 6B 33 43 12 20 18 DF   .k3C. ..   1100 1101 0110 1011 0011 0011 0100 0011 0001 0010 0010 0000 0001 1000 1101 1111

0202C EB 47 8E 5C 84 08 01 82   .G.\....   1110 1011 0100 0111 1000 1110 0101 1100 1000 0100 0000 1000 0000 0001 1000 0010

02034 52 06 E2 7F D7 55 F8 D7   R....U..   0101 0010 0000 0110 1110 0010 0111 1111 1101 0111 0101 0101 1111 1000 1101 0111

0203C F5 AD B1 83 AC 44 80 61   .....D.a   1111 0101 1010 1101 1011 0001 1000 0011 1010 1100 0100 0100 1000 0000 0110 0001

02044 FF AD 1E 39 72 10 20 40   ...9r. @   1111 1111 1010 1101 0001 1110 0011 1001 0111 0010 0001 0000 0010 0000 0100 0000

0204C 87 FC D6 B3 34 31 22 01   ....41".   1000 0111 1111 1100 1101 0110 1011 0011 0011 0100 0011 0001 0010 0010 0000 0001

02054 8D FE B4 78 E5 C8 40 80   ...x..@.   1000 1101 1111 1110 1011 0100 0111 1000 1110 0101 1100 1000 0100 0000 1000 0000

0205C 18 25 20 6E 27 FD 75 1F   .% n'.u.   0001 1000 0010 0101 0010 0000 0110 1110 0010 0111 1111 1101 0111 0101 0001 1111

02064 80 8F FF FF FF FC FF FF   ........   1000 0000 1000 1111 1111 1111 1111 1111 1111 1111 1111 1100 1111 1111 1111 1111

0206C FF FF 40 CA A3 08 AD 62   ..@....b   1111 1111 1111 1111 0100 0000 1100 1010 1010 0011 0000 1000 1010 1101 0110 0010

02074 E5 52 34 03 23 FD 68 F1   .R4.#.h.   1110 0101 0101 0010 0011 0100 0000 0011 0010 0011 1111 1101 0110 1000 1111 0001

0207C CB 90 81 00 5B E6 0C 01   ....[...   1100 1011 1001 0000 1000 0001 0000 0000 0101 1011 1110 0110 0000 1100 0000 0001

02084 80 13 E3 BF 37 25 E4 B5   ....7%..   1000 0000 0001 0011 1110 0011 1011 1111 0011 0111 0010 0101 1110 0100 1011 0101

0208C B2 BB 48 D0 0F 62 D3 7F   ..H..b..   1011 0010 1011 1011 0100 1000 1101 0000 0000 1111 0110 0010 1101 0011 0111 1111

02094 FC 5E C2 14 01 6F 98 30   .^...o.0   1111 1100 0101 1110 1100 0010 0001 0100 0000 0001 0110 1111 1001 1000 0011 0000

0209C 06 00 4F 8E FC DC 97 92   ..O.....   0000 0110 0000 0000 0100 1111 1000 1110 1111 1100 1101 1100 1001 0111 1001 0010

020A4 D6 CA ED 23 40 0B 28 FF   ...#@.(.   1101 0110 1100 1010 1110 1101 0010 0011 0100 0000 0000 1011 0010 1000 1111 1111

020AC 7C 8F 2E 07 D0 05 BE 60   |......`   0111 1100 1000 1111 0010 1110 0000 0111 1101 0000 0000 0101 1011 1110 0110 0000

020B4 C0 18 01 3E 3B F0 11 FF   ...>;...   1100 0000 0001 1000 0000 0001 0011 1110 0011 1011 1111 0000 0001 0001 1111 1111

020BC FF FF FF 9F FF FF FF E8   ........   1111 1111 1111 1111 1111 1111 1001 1111 1111 1111 1111 1111 1111 1111 1110 1000

020C4 18 D7 F5 AD B1 83 AC 44   .......D   0001 1000 1101 0111 1111 0101 1010 1101 1011 0001 1000 0011 1010 1100 0100 0100

020CC 80 64 FF AD 1E 39 72 10   .d...9r.   1000 0000 0110 0100 1111 1111 1010 1101 0001 1110 0011 1001 0111 0010 0001 0000

020D4 20 45 EF E5 C2 BC A5 71    E.....q   0010 0000 0100 0101 1110 1111 1110 0101 1100 0010 1011 1100 1010 0101 0111 0001

Open Design Specification for .dwg files

151



020DC 1A 00 8B 93 7D CC 84 B4   ....}...   0001 1010 0000 0000 1000 1011 1001 0011 0111 1101 1100 1100 1000 0100 1011 0100

020E4 44 81 17 9F 97 0A F2 95   D.......   0100 0100 1000 0001 0001 0111 1001 1111 1001 0111 0000 1010 1111 0010 1001 0101

020EC C4 68 04 73 67 71 1A 1E   .h.sgq..   1100 0100 0110 1000 0000 0100 0111 0011 0110 0111 0111 0001 0001 1010 0001 1110

020F4 E8 F2 04 02 3F FF FF FF   ....?...   1110 1000 1111 0010 0000 0100 0000 0010 0011 1111 1111 1111 1111 1111 1111 1111

020FC F3 FF FF FF FD 03 2A 8C   ......*.   1111 0011 1111 1111 1111 1111 1111 1111 1111 1101 0000 0011 0010 1010 1000 1100

02104 22 B5 8B 95 48 D0 0C 8F   "...H...   0010 0010 1011 0101 1000 1011 1001 0101 0100 1000 1101 0000 0000 1100 1000 1111

0210C F5 A3 C7 2E 42 04 01 6F   ....B..o   1111 0101 1010 0011 1100 0111 0010 1110 0100 0010 0000 0100 0000 0001 0110 1111

02114 98 30 06 00 4F 8C FC DC   .0..O...   1001 1000 0011 0000 0000 0110 0000 0000 0100 1111 1000 1100 1111 1100 1101 1100

0211C 97 92 D6 CA ED 23 40 3D   .....#@=   1001 0111 1001 0010 1101 0110 1100 1010 1110 1101 0010 0011 0100 0000 0011 1101

02124 8B 4D FF F1 7B 08 50 05   .M..{.P.   1000 1011 0100 1101 1111 1111 1111 0001 0111 1011 0000 1000 0101 0000 0000 0101

0212C BE 60 C0 18 01 3E 33 F3   .`...>3.   1011 1110 0110 0000 1100 0000 0001 1000 0000 0001 0011 1110 0011 0011 1111 0011

02134 72 5E 4B 5B 2B B4 8D 00   r^K[+...   0111 0010 0101 1110 0100 1011 0101 1011 0010 1011 1011 0100 1000 1101 0000 0000

0213C 2C A3 FD F2 3C B8 1F 40   ,...<..@   0010 1100 1010 0011 1111 1101 1111 0010 0011 1100 1011 1000 0001 1111 0100 0000

02144 16 F9 83 00 60 04 F8 CF   ....`...   0001 0110 1111 1001 1000 0011 0000 0000 0110 0000 0000 0100 1111 1000 1100 1111

0214C D4 C1 44 3E               ..D>       1101 0100 1100 0001 0100 0100 0011 1110

02150 5A C5                     crc
#### 20.4.42 RAY (40)

Common Entity Data

Point
3BD
10

Vector
3BD
11

Common Entity Handle Data

CRC
X
---
##### 20.4.42.1 Example:
OBJECT: ray (28H), len 2FH (47), handle: 01 06

02185 2F 00                     /.         0010 1111 0000 0000

02187 4A 00 80 41 A2 E8 08 00   J..A....   0100 1010 0000 0000 1000 0000 0100 0001 1010 0010 1110 1000 0000 1000 0000 0000

0218F 05 7B 12 4C 98 47 CA EF   .{.L.G..   0000 0101 0111 1011 0001 0010 0100 1100 1001 1000 0100 0111 1100 1010 1110 1111

02197 C4 A8 00 84 0B FC 98 72   .......r   1100 0100 1010 1000 0000 0000 1000 0100 0000 1011 1111 1100 1001 1000 0111 0010

0219F 3F F9 FC 0F 91 CC D7 E5   ?.......   0011 1111 1111 1001 1111 1100 0000 1111 1001 0001 1100 1100 1101 0111 1110 0101

021A7 CD 71 5F 99 7D 7E 4D 05   .q_.}~M.   1100 1101 0111 0001 0101 1111 1001 1001 0111 1101 0111 1110 0100 1101 0000 0101

021AF C1 3D 47 F1 82 88 78      .=G...x    1100 0001 0011 1101 0100 0111 1111 0001 1000 0010 1000 1000 0111 1000

021B6 AD CF                     crc

Open Design Specification for .dwg files

152


#### 20.4.43 XLINE (41)
Same as RAY (40) — except for type code.
##### 20.4.43.1 Example:
OBJECT: const line (29H), len 2FH (47), handle: 01 05
02152 2F 00                     /.         0010 1111 0000 0000
02154 4A 40 80 41 62 E8 08 00   J@.Ab...   0100 1010 0100 0000 1000 0000 0100 0001 0110 0010 1110 1000 0000 1000 0000 0000
0215C 05 7B 09 95 83 71 C8 B2   .{...q..   0000 0101 0111 1011 0000 1001 1001 0101 1000 0011 0111 0001 1100 1000 1011 0010
02164 03 E8 03 C1 22 6C 91 8A   ...."l..   0000 0011 1110 1000 0000 0011 1100 0001 0010 0010 0110 1100 1001 0001 1000 1010
0216C 28 4A 04 28 B1 0A 5D F6   (J.(..].   0010 1000 0100 1010 0000 0100 0010 1000 1011 0001 0000 1010 0101 1101 1111 0110
02174 48 76 1F 8D E0 E8 59 D8   Hv....Y.   0100 1000 0111 0110 0001 1111 1000 1101 1110 0000 1110 1000 0101 1001 1101 1000
0217C 7A FB 87 F1 82 88 78      z.....x    0111 1010 1111 1011 1000 0111 1111 0001 1000 0010 1000 1000 0111 1000
02183 FE 9C                     crc
#### 20.4.44 DICTIONARY (42)
Basically a list of pairs of string/objhandle that constitute the dictionary entries.

Length
MS
---
Entity length (not counting itself or CRC).

Type
S
0
42 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
S

number of reactors in this object
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Numitems
L

number of dictonary items
R14 Only:

Unknown R14
RC

Unknown R14 byte, has always been 0
R2000+:

Cloning flag
BS
281

Hard Owner flag
RC
280
Common:

Text
TV

string name of dictionary entry, numitems entries

Handle refs
H

parenthandle (soft relative pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)

Open Design Specification for .dwg files

153






itemhandles (soft owner)
20.4.44.1
Example:
OBJECT: dictionary (2AH), len 2CH (44), handle: 0C

0254B 2C 00                     ,.         0010 1100 0000 0000

0254D 4A 80 43 22 C0 10 00 09   J.C"....   0100 1010 1000 0000 0100 0011 0010 0010 1100 0000 0001 0000 0000 0000 0000 1001

02555 02 00 42 90 50 D0 51 17   ..B.P.Q.   0000 0010 0000 0000 0100 0010 1001 0000 0101 0000 1101 0000 0101 0001 0001 0111

0255D D1 D4 93 D5 54 10 F4 14   ....T...   1101 0001 1101 0100 1001 0011 1101 0101 0101 0100 0001 0000 1111 0100 0001 0100

02565 34 14 45 F4 D4 C4 94 E4   4.E.....   0011 0100 0001 0100 0100 0101 1111 0100 1101 0100 1100 0100 1001 0100 1110 0100

0256D 55 35 45 94 C4 54 03 02   U5E..T..   0101 0101 0011 0101 0100 0101 1001 0100 1100 0100 0101 0100 0000 0011 0000 0010

02575 10 D2 10 EC               ....       0001 0000 1101 0010 0001 0000 1110 1100

02579 D2 36                     crc
#### 20.4.45 DICTIONARYWDFLT

Same as the DICTIONARY object with the following additional fields:



H
7
Default entry (hard pointer)


#### 20.4.46 MTEXT (44)

Common Entity (Handle) Data


Insertion pt3
BD
10
First picked point. (Location relative to text
depends on attachment point (71).)

Extrusion
3BD
210
Undocumented; appears in DXF and entget, but ACAD
doesn't even bother to adjust it to unit length.

X-axis dir
3BD
11
Apparently the text x-axis vector.  (Why not just a
rotation?)  ACAD maintains it as a unit vector.
Common:

Rect width
BD
41
Reference rectangle width (width picked by the
user).
R2007+:

Rect height
BD
46
Reference rectangle height.
Common:

Text height
BD
40
Undocumented

Attachment
BS
71
Similar to justification; see DXF doc

Drawing dir
BS
72
Left to right, etc.; see DXF doc

Extents
ht
BD
---
Undocumented and not present in DXF or entget

Extents wid
BD
---
Undocumented and not present in DXF or entget

Open Design Specification for .dwg files

154






The extents rectangle, when rotated the same as the
text, fits the actual text image on the screen
(altough we've seen it include an extra row of text
in height).

Text
TV
1
All text in one long string (without '\n's



3
for line wrapping).  ACAD seems to add braces ({ })
and backslash-P's to indicate paragraphs based on
the "\r\n"'s found in the imported file.  But, all
the text is in this one long string -- not broken
into 1- and 3-groups as in DXF and entget.




ACAD's entget breaks this string into 250-char
pieces (not 255 as doc'd) – even if it's mid-word.
The 1-group always gets the tag end; therefore, the
3's are always 250 chars long.


H
7
STYLE (hard pointer)
R2000+:

Linespacing Style
BS
73

Linespacing Factor
BD
44

Unknown bit
B
R2004+:

Background flags
BL
90
0 = no background, 1 = background fill, 2 =
background fill with drawing fill color, 0x10 = text
frame (R2018+)
IF background flags has bit 0x01 set, or in case of R2018 bit 0x10:

Background scale factor


BL
45
default = 1.5

Background color
CMC
63


Background transparency


BL
441

END IF background flags 0x01/0x10
R2018+

Is NOT annotative
B
IF MTEXT is not annotative

Version
BS

Default 0

Default flag
B

Default true
BEGIN REDUNDANT FIELDS (see above for descriptions)

Registered application H

Hard pointer

Attachment point
BL

X-axis dir
3BD
10

Insertion point
3BD
11

Rect width
BD
40

Rect height
BD
41

Extents width
BD
42

Extents height
BD
43
END REDUNDANT FIELDS

Open Design Specification for .dwg files

155



Column type
BS
71
0 = No columns, 1 = static columns, 2 = dynamic
columns
IF Has Columns data (column type is not 0)

Column height count
BL
72

Columnn width
BD
44

Gutter
BD
45

Auto height?
B
73

Flow reversed?
B
74
IF not auto height and column type is dynamic columns
REPEAT Column heights

Column height
BD
46
END REPEAT
END IF (has column heights)
END IF (has columns data)
END IF (not annotative)
Common:

CRC
X
---
##### 20.4.46.1 Example:
OBJECT: mtext (2CH), len 4DH (77), handle: CE

00515 4D 00                     M.         0100 1101 0000 0000

00517 4B 00 73 A0 C8 10 00 01   K.s.....   0100 1011 0000 0000 0111 0011 1010 0000 1100 1000 0001 0000 0000 0000 0000 0001

0051F 33 0F AE 2B 5E AE E0 84   3..+^...   0011 0011 0000 1111 1010 1110 0010 1011 0101 1110 1010 1110 1110 0000 1000 0100

00527 48 04 88 93 FD FD 9A 00   H.......   0100 1000 0000 0100 1000 1000 1001 0011 1111 1101 1111 1101 1001 1010 0000 0000

0052F FA 05 4B 50 15 AF 46 E0   ..KP..F.   1111 1010 0000 0101 0100 1011 0101 0000 0001 0101 1010 1111 0100 0110 1110 0000

00537 7A 15 8E 7E 82 A0 20 6E   z..~.. n   0111 1010 0001 0101 1000 1110 0111 1110 1000 0010 1010 0000 0010 0000 0110 1110

0053F BD 1B 81 E8 56 39 F9 9B   ....V9..   1011 1101 0001 1011 1000 0001 1110 1000 0101 0110 0011 1001 1111 1001 1001 1011

00547 99 99 99 99 99 E0 7E 85   ......~.   1001 1001 1001 1001 1001 1001 1001 1001 1001 1001 1110 0000 0111 1110 1000 0101

0054F AE 20 98 9D A9 18 17 1B   . ......   1010 1110 0010 0000 1001 1000 1001 1101 1010 1001 0001 1000 0001 0111 0001 1011

00557 1B 19 1B 60 82 18 28 87   ...`..(.   0001 1011 0001 1001 0001 1011 0110 0000 1000 0010 0001 1000 0010 1000 1000 0111

0055F A8 89 A8 88 00            .....      1010 1000 1000 1001 1010 1000 1000 1000 0000 0000

00564 6F F0                     crc
#### 20.4.47 LEADER (45)

Common Entity Data


Unknown bit
B
---
Always seems to be 0.

Annot type
BS
---
Annotation type (NOT bit-coded):




Value 0 : MTEXT

Open Design Specification for .dwg files

156






Value 1 : TOLERANCE




Value 2 : INSERT




Value 3 : None

path type
BS
---

numpts
BL
---
number of points

point
3BD
10
As many as counter above specifies.

Origin
3BD
---
The leader plane origin (by default it’s the first
point).

Extrusion
3BD
210

x direction
3BD
211

offsettoblockinspt
3BD
212
Used when the BLOCK option is used.  Seems to be an
unused feature.
R14+:

Endptproj
3BD
---
A non-planar leader gives a point that projects the
endpoint back to the annotation.  It's the offset
from the endpoint of the leader to the annotation,
taking into account the extrusion direction.
R13-R14 Only:

DIMGAP
BD
---
The value of DIMGAP in the associated DIMSTYLE at
the time of creation, multiplied by the dimscale in
that dimstyle.
Common:

Box height
BD
40
MTEXT extents height.  (A text box is slightly
taller, probably by some DIMvar amount.)

Box width
BD
41
MTEXT extents width.  (A text box is slightly wider,
probably by some DIMvar amount.)

Hooklineonxdir
B

hook line is on x direction if 1

Arrowheadon
B

arrowhead on indicator
R13-R14 Only:

Arrowheadtype
BS

arrowhead type

Dimasz
BD

DIMASZ at the time of creation, multiplied by
DIMSCALE

Unknown
B

Unknown
B

Unknown
BS

Byblockcolor
BS

Unknown
B

Unknown
B
R2000+:

Unknown
BS

Unknown
B

Unknown
B
Common:

Common Entity Handle Data

Open Design Specification for .dwg files

157




H
340
Associated annotation




activated in R14. (hard pointer)


H
2
DIMSTYLE (hard pointer)

CRC
X
---
##### 20.4.47.1 Example:
OBJECT: leader (2DH), len 80H (128), handle: 01 09

02213 80 00                     ..         1000 0000 0000 0000

02215 4B 40 80 42 65 20 18 00   K@.Be ..   0100 1011 0100 0000 1000 0000 0100 0010 0110 0101 0010 0000 0001 1000 0000 0000

0221D 05 5B 29 03 25 AD 59 2D   .[).%.Y-   0000 0101 0101 1011 0010 1001 0000 0011 0010 0101 1010 1101 0101 1001 0010 1101

02225 08 7D C9 50 04 41 FF AB   .}.P.A..   0000 1000 0111 1101 1100 1001 0101 0000 0000 0100 0100 0001 1111 1111 1010 1011

0222D AF A2 81 04 08 2E E6 9D   ........   1010 1111 1010 0010 1000 0001 0000 0100 0000 1000 0010 1110 1110 0110 1001 1101

02235 29 5D 0C 21 40 1C 3C C0   )].!@.<.   0010 1001 0101 1101 0000 1100 0010 0001 0100 0000 0001 1100 0011 1100 1100 0000

0223D 0F B5 ED 05 D0 20 50 04   ..... P.   0000 1111 1011 0101 1110 1101 0000 0101 1101 0000 0010 0000 0101 0000 0000 0100

02245 84 77 1E 34 65 00 78 56   .w.4e.xV   1000 0100 0111 0111 0001 1110 0011 0100 0110 0101 0000 0000 0111 1000 0101 0110

0224D 18 21 BF AB 15 40 89 6B   .!...@.k   0001 1000 0010 0001 1011 1111 1010 1011 0001 0101 0100 0000 1000 1001 0110 1011

02255 56 4B 42 1F 72 54 01 10   VKB.rT..   0101 0110 0100 1011 0100 0010 0001 1111 0111 0010 0101 0100 0000 0001 0001 0000

0225D 7F EA EB E8 A0 41 02 A5   .....A..   0111 1111 1110 1010 1110 1011 1110 1000 1010 0000 0100 0001 0000 0010 1010 0101

02265 AA AA 02 B5 E8 DC 0F 42   .......B   1010 1010 1010 1010 0000 0010 1011 0101 1110 1000 1101 1100 0000 1111 0100 0010

0226D AD CF C0 AD 7A 37 03 D0   ....z7..   1010 1101 1100 1111 1100 0000 1010 1101 0111 1010 0011 0111 0000 0011 1101 0000

02275 AC 73 F3 0B D4 A1 72 3F   .s....r?   1010 1100 0111 0011 1111 0011 0000 1011 1101 0100 1010 0001 0111 0010 0011 1111

0227D 0B B4 FF 80 AD 7A 37 03   .....z7.   0000 1011 1011 0100 1111 1111 1000 0000 1010 1101 0111 1010 0011 0111 0000 0011

02285 D0 AC 73 F2 C3 05 10 FC   ..s.....   1101 0000 1010 1100 0111 0011 1111 0010 1100 0011 0000 0101 0001 0000 1111 1100

0228D 10 26 05 20 10 A5 11 D6   .&. ....   0001 0000 0010 0110 0000 0101 0010 0000 0001 0000 1010 0101 0001 0001 1101 0110

02295 6E AB                     crc
#### 20.4.48 MLEADER
This entity was introduced in version 21. A significant portion (content block/text and leaders) of the
multileader entity is stored in the MLeaderAnnotContext object (see paragraph 20.4.86), which is
embedded into this object (stream).
Version
Field
type
DXF
group
code
Description

…

Common entity data.
R2010+




BS
270
Version (expected to be 2).

Open Design Specification for .dwg files

158


Common




…

MLeaderAnnotContext fields (see paragraph 20.4.86). This contains the
mleader content (block/text) and the leaders.

H
340
Leader style handle (hard pointer)

BL
90
Override flags:
1 << 0 = Leader line type,
1 << 1 = Leader line color,
1 << 2 = Leader line type handle,
1 << 3 = Leader line weight,
1 << 4 = Enabled landing,
1 << 5 = Landing gap,
1 << 6 = Enabled dog-leg,
1 << 7 = Dog-leg length,
1 << 8 = Arrow symbol handle,
1 << 9 = Arrow size,
1 << 10 = Conent type,
1 << 11 = Text style handle,
1 << 12 = Text left attachment type (of MTEXT),
1 << 13 = Text angle type (of MTEXT),
1 << 14 = Text alignment type (of MTEXT),
1 << 15 = Text color (of MTEXT),
1 << 16 = Text height (of MTEXT),
1 << 17 = Enable text frame,
1 << 18 = Enable use of default MTEXT (from MLEADERSTYLE),
1 << 19 = Content block handle,
1 << 20 = Block content color,
1 << 21 = Block content scale,
1 << 22 = Block content rotation,
1 << 23 = Block connection type,
1 << 24 = Scale,
1 << 25 = Text right attachment type (of MTEXT),
1 << 26 = Text switch alignment type (of MTEXT),
1 << 27 = Text attachment direction (of MTEXT),
1 << 28 = Text top attachment type (of MTEXT),
1 << 29 = Text bottom attachment type (of MTEXT)

BS
170
Leader type (0 = inivisible leader, 1 = straight line leader, 2 = spline leader).

CMC
91
Leader color

H
341
Leader line type handle (hard pointer)

BL
171
Line weight

B
290
Landing enabled

B
291
Dog-leg enabled

BD
41
Landing distance

H
342
Arrow head handle (hard pointer)

BD
42
Default arrow head size

BS
172
Style content type:

Open Design Specification for .dwg files

159


0 = None,
1 = Block content,
2 = MTEXT content,
3 = TOLERANCE content

H
343
Style text style handle (hard pointer)

BS
173
Style left text attachment type. Values 0-8 are used for the left/right attachment
point (attachment direction is horizontal), values 9-10 are used for the
top/bottom attachment points (attachment direction is vertical). Attachment
point is:

0 = top of top text line,

1 = middle of top text line,

2 = middle of text,

3 = middle of bottom text line,

4 = bottom of bottom text line,

5 = bottom text line,

6 = bottom of top text line. Underline bottom line

7 = bottom of top text line. Underline top line,

8 = bottom of top text line. Underline all content,

9 = center of text (y-coordinate only),

10 = center of text (y-coordinate only), and overline top/underline
bottom content.

BS
95
Style right text attachment type. See also style left text attachment type.

BS
174
Style text angle type:
0 = text angle is equal to last leader line segment angle,
1 = text is horizontal,
2 = text angle is equal to last leader line segment angle, but potentially rotated
by 180 degrees so the right side is up for readability.

BS
175
Unknown

CMC
92
Style text color

B
292
Style text frame enabled

H
[344]
Style block handle (hard pointer) (DXF group is optional)

CMC
93
Style block color

3BD
10
Style block scale vector

BD
43
Style block rotation (radians)

BS
176
Style attachment type (0 = center extents, 1 = insertion point)

B
293
Is annotative
-R2007




BL
-
Number of arrow heads



BEGIN REPEAT arrow heads

B
94
Is default?

H
345
Arrow head handle (hard pointer)



END REPEAT arrow heads

BL
-
Number of block labels



BEGIN REPEAT block labels

Open Design Specification for .dwg files

160



H
330
Attribute definition (ATTDEF) handle (soft pointer)

TV
302
Label text

BS
177
UI index (sequential index of the label in the collection)



BD
44
Width



END REPEAT block labels

B
294
Is text direction negative

BS
178
IPE align (meaning unknown)

BS
179
Justification (1 = left, 2 = center, 3 = righ)

BD
45
Scale factor
R2010+




BS
271
Attachment direction (0 = horizontal, 1 = vertical). This defines whether the
leaders attach to the left/right of the content block/text, or attach to the
top/bottom.

BS
273
Style top text attachment. See also style left text attachment type.

BS
272
Style bottom text attachment type. See also style left text attachment type.
R2013+
B
295
Leader extended to text
#### 20.4.49 TOLERANCE (46)

Common Entity Data

R13-R14 Only:

Unknown short
S

Height
BD
--

Dimgap(?)
BD

dimgap at time of creation, * dimscale
Common:

Ins pt
3BD
10

X direction
3BD
11

Extrusion
3BD
210
etc.

Text string
BS
1

Common Entity Handle Data


H

DIMSTYLE (hard pointer)
##### 20.4.49.1 Example:
OBJECT: tolerance (2EH), len 65H (101), handle: 01 0C

022EB 65 00                     e.         0110 0101 0000 0000

022ED 4B 80 80 43 27 18 10 00   K..C'...   0100 1011 1000 0000 1000 0000 0100 0011 0010 0111 0001 1000 0001 0000 0000 0000

022F5 05 5B 40 56 BD 1B 81 E8   .[@V....   0000 0101 0101 1011 0100 0000 0101 0110 1011 1101 0001 1011 1000 0001 1110 1000

022FD 56 39 F8 15 AF 46 E0 7A   V9...F.z   0101 0110 0011 1001 1111 1000 0001 0101 1010 1111 0100 0110 1110 0000 0111 1010

02305 15 6E 7E 51 19 A0 47 00   .n~Q..G.   0001 0101 0110 1110 0111 1110 0101 0001 0001 1001 1010 0000 0100 0111 0000 0000

0230D C7 13 A0 18 09 38 21 8A   .....8!.   1100 0111 0001 0011 1010 0000 0001 1000 0000 1001 0011 1000 0010 0001 1000 1010

02315 5E A1 48 13 54 A5 CF 6B   ^.H.T..k   0101 1110 1010 0001 0100 1000 0001 0011 0101 0100 1010 0101 1100 1111 0110 1011

Open Design Specification for .dwg files

161



0231D 88 CC EC 8E 87 6D 4F A4   .....mO.   1000 1000 1100 1100 1110 1100 1000 1110 1000 0111 0110 1101 0100 1111 1010 0100

02325 A4 AE CF 6B 88 CC EC 8E   ...k....   1010 0100 1010 1110 1100 1111 0110 1011 1000 1000 1100 1100 1110 1100 1000 1110

0232D 87 6D CF AC 2E 6C 8C CF   .m...l..   1000 0111 0110 1101 1100 1111 1010 1100 0010 1110 0110 1100 1000 1100 1100 1111

02335 6B 88 CC EC 8E 87 6D AF   k.....m.   0110 1011 1000 1000 1100 1100 1110 1100 1000 1110 1000 0111 0110 1101 1010 1111

0233D A4 A4 AE C4 A4 AE C4 A4   ........   1010 0100 1010 0100 1010 1110 1100 0100 1010 0100 1010 1110 1100 0100 1010 0100

02345 AE C4 A4 AE C6 0A 21 F8   ......!.   1010 1110 1100 0100 1010 0100 1010 1110 1100 0110 0000 1010 0010 0001 1111 1000

0234D 20 4C 0A 23 B4             L.#.      0010 0000 0100 1100 0000 1010 0010 0011 1011 0100

02352 45 2F                     crc
#### 20.4.50 MLINE (47)

Common Entity Data


Scale
BD
40

Just
EC

top (0), bottom(2), or center(1)

Base point
3BD
10

Extrusion
3BD
210
etc.

Openclosed
BS

open (1), closed(3)

Linesinstyle
RC
73

Numverts
BS
72

do numverts times {

vertex    3BD

vertex direction 3BD

miter direction  3BD

do lineinstyle times {

numsegparms    BS

do numsegparms times {

segparm         BD    segment parameter

}

numareafillparms BS

do num area fill parms times {

areafillparm   BD    area fill parameter

}

}

}


Common Entity Handle Data


H

mline style oject handle (hard pointer)

Open Design Specification for .dwg files

162


##### 20.4.50.1 Example:
OBJECT: mline (2FH), len E4H (228), handle: 01 0D

02354 E4 00                     ..         1110 0100 0000 0000

02356 4B C0 80 43 66 C8 30 00   K..Cf.0.   0100 1011 1100 0000 1000 0000 0100 0011 0110 0110 1100 1000 0011 0000 0000 0000

0235E 05 5B 20 04 61 AD 1E F2   .[ .a...   0000 0101 0101 1011 0010 0000 0000 0100 0110 0001 1010 1101 0001 1110 1111 0010

02366 13 A8 8A 01 81 93 3C 67   ......<g   0001 0011 1010 1000 1000 1010 0000 0001 1000 0001 1001 0011 0011 1100 0110 0111

0236E D4 2B C0 7F 52 80 81 20   .+..R..    1101 0100 0010 1011 1100 0000 0111 1111 0101 0010 1000 0000 1000 0001 0010 0000

02376 64 61 AD 1E F2 13 A8 8A   da......   0110 0100 0110 0001 1010 1101 0001 1110 1111 0010 0001 0011 1010 1000 1000 1010

0237E 01 81 93 3C 67 D4 2B C0   ...<g.+.   0000 0001 1000 0001 1001 0011 0011 1100 0110 0111 1101 0100 0010 1011 1100 0000

02386 7F 13 E9 CF 70 DE 47 3C   ....p.G<   0111 1111 0001 0011 1110 1001 1100 1111 0111 0000 1101 1110 0100 0111 0011 1100

0238E C7 E4 F8 6A 7B 9C 00 2F   ...j{../   1100 0111 1110 0100 1111 1000 0110 1010 0111 1011 1001 1100 0000 0000 0010 1111

02396 39 FC 4E 86 A7 B9 C0 02   9.N.....   0011 1001 1111 1100 0100 1110 1000 0110 1010 0111 1011 1001 1100 0000 0000 0010

0239E F3 DF 93 E9 CF 70 DE 47   .....p.G   1111 0011 1101 1111 1001 0011 1110 1001 1100 1111 0111 0000 1101 1110 0100 0111

023A6 3C C7 F2 05 52 04 00 00   <...R...   0011 1100 1100 0111 1111 0010 0000 0101 0101 0010 0000 0100 0000 0000 0000 0000

023AE 00 00 00 00 78 5F D0 38   ....x_.8   0000 0000 0000 0000 0000 0000 0000 0000 0111 1000 0101 1111 1101 0000 0011 1000

023B6 DD 69 B0 78 DE 38 80 44   .i.x.8.D   1101 1101 0110 1001 1011 0000 0111 1000 1101 1110 0011 1000 1000 0000 0100 0100

023BE 0A 1C 33 BD E1 05 20 40   ..3... @   0000 1010 0001 1100 0011 0011 1011 1101 1110 0001 0000 0101 0010 0000 0100 0000

023C6 62 C6 53 15 C9 57 71 F9   b.S..Wq.   0110 0010 1100 0110 0101 0011 0001 0101 1100 1001 0101 0111 0111 0001 1111 1001

023CE FB 6C F0 9B 58 B3 AB 7F   .l..X...   1111 1011 0110 1100 1111 0000 1001 1011 0101 1000 1011 0011 1010 1011 0111 1111

023D6 05 47 3C F4 7B 0B 79 B7   .G<.{.y.   0000 0101 0100 0111 0011 1100 1111 0100 0111 1011 0000 1011 0111 1001 1011 0111

023DE E0 8F 92 1D DC D1 2F 79   ....../y   1110 0000 1000 1111 1001 0010 0001 1101 1101 1100 1101 0001 0010 1111 0111 1001

023E6 FC 81 54 81 18 D6 BA 82   ..T.....   1111 1100 1000 0001 0101 0100 1000 0001 0001 1000 1101 0110 1011 1010 1000 0010

023EE C0 20 DE 77 F4 27 50 A1   . .w.'P.   1100 0000 0010 0000 1101 1110 0111 0111 1111 0100 0010 0111 0101 0000 1010 0001

023F6 65 46 02 92 A0 13 16 15   eF......   0110 0101 0100 0110 0000 0010 1001 0010 1010 0000 0001 0011 0001 0110 0001 0101

023FE 43 DA 24 00 28 10 1C B1   C.$.(...   0100 0011 1101 1010 0010 0100 0000 0000 0010 1000 0001 0000 0001 1100 1011 0001

02406 94 C5 72 55 DC 7E 7F 5B   ..rU.~.[   1001 0100 1100 0101 0111 0010 0101 0101 1101 1100 0111 1110 0111 1111 0101 1011

0240E 3C 26 D6 2C EA DF C7 65   <&.,...e   0011 1100 0010 0110 1101 0110 0010 1100 1110 1010 1101 1111 1100 0111 0110 0101

02416 B3 C2 6D 62 CE A9 F8 20   ..mb...    1011 0011 1100 0010 0110 1101 0110 0010 1100 1110 1010 1001 1111 1000 0010 0000

0241E B1 94 C5 72 55 DC 7F 20   ...rU..    1011 0001 1001 0100 1100 0101 0111 0010 0101 0101 1101 1100 0111 1111 0010 0000

02426 55 20 40 00 00 00 00 00   U @.....   0101 0101 0010 0000 0100 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

0242E 07 85 FD 18 28 87 C0 50   ....(..P   0000 0111 1000 0101 1111 1101 0001 1000 0010 1000 1000 0111 1100 0000 0101 0000

02436 87 28 8E 4C               .(.L       1000 0111 0010 1000 1000 1110 0100 1100


Open Design Specification for .dwg files

163


0243A 91 88                     crc
#### 20.4.51 BLOCK CONTROL (48)

Length
MS
---
Object length (not counting itself or CRC).

Type
BS
0&2
48 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Owner handle (soft pointer) of root object (0).

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
L

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Numentries
BL
70
Doesn't count *MODEL_SPACE and *PAPER_SPACE.

Handle refs
H

NULL (soft pointer)




xdicobjhandle (hard owner)




numentries handles of blockheaders in the file (soft
owner), then *MODEL_SPACE and *PAPER_SPACE (hard
owner).

CRC
X
---
##### 20.4.51.1 Example:
OBJECT: blk ctrl (30H), len 20H (32), handle: 01

00464 20 00                      .         0010 0000 0000 0000

00466 4C 00 40 64 80 00 00 09   L.@d....   0100 1100 0000 0000 0100 0000 0110 0100 1000 0000 0000 0000 0000 0000 0000 1001

0046E 08 40 30 21 93 21 9F 21   .@0!.!.!   0000 1000 0100 0000 0011 0000 0010 0001 1001 0011 0010 0001 1001 1111 0010 0001

00476 AD 21 BB 21 CA 21 D6 21   .!.!.!.!   1010 1101 0010 0001 1011 1011 0010 0001 1100 1010 0010 0001 1101 0110 0010 0001

0047E F4 22 01 13 31 19 31 16   ."..1.1.   1111 0100 0010 0010 0000 0001 0001 0011 0011 0001 0001 1001 0011 0001 0001 0110

00486 C1 3A                     crc
#### 20.4.52 BLOCK HEADER (49)

Length
MS
---
Object length (not counting itself or CRC).

Type
BS
0&2
49 (internal DWG type code).
R2000+:

Open Design Specification for .dwg files

164



Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
code 0, length followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
L

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Entry name
TV
2

64-flag
B
70
The 64-bit of the 70 group.

xrefindex+1
BS
70
subtract one from this value when read.  After that,
-1 indicates that this reference did not come from
an xref, otherwise this value indicates the index of
the blockheader for the xref from which this came.

Xdep
B
70
block is dependent on an xref. (16 bit)

Anonymous
B
1
if this is an anonymous block  (1 bit)

Hasatts
B
1
if block contains attdefs    (2 bit)

Blkisxref
B
1
if block is xref             (4 bit)

Xrefoverlaid
B
1
if an overlaid xref          (8 bit)
R2000+:

Loaded Bit
B

0 indicates loaded for an xref
R2004+:

Owned Object Count
BL

Number of objects owned by this object.
Common:

Base pt
3BD
10
Base point of block.

Xref pname
TV
1
Xref pathname.  That's right: DXF 1 AND 3!



3
1 appears in a tblnext/search elist; 3 appears in an
entget.
R2000+:

Insert Count
RC

A sequence of zero or more non-zero RC’s, followed
by a terminating 0 RC.  The total number of these
indicates how many insert handles will be present.

Block Description
TV
4
Block description.

Size of preview data
BL

Indicates number of bytes of data following.

Binary Preview Data N*RC
310

R2007+:

Insert units
BS
70

Explodable
B
280

Open Design Specification for .dwg files

165



Block scaling
RC
281
Common:

Handle refs
H

Block control handle (soft pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)




NULL (hard pointer)




BLOCK entity. (hard owner)
R13-R2000:




if (!blkisxref && !xrefisoverlaid) {




first entity in the def. (soft pointer)




last entity in the def. (soft pointer)




}
R2004+:


H

[ENTITY (hard owner)] Repeats “Owned Object Count”
times.
Common:




ENDBLK entity. (hard owner)
R2000+:

Insert Handles
H

N insert handles, where N corresponds to the number
of insert count entries above (soft pointer).

Layout Handle
H

(hard pointer)
Common:

CRC
X
---
##### 20.4.52.1 Example:
OBJECT: blk hdr (31H), len 19H (25), handle: CA

00488 19 00                     ..         0001 1001 0000 0000

0048A 4C 40 72 A6 80 00 00 09   L@r.....   0100 1100 0100 0000 0111 0010 1010 0110 1000 0000 0000 0000 0000 0000 0000 1001

00492 02 2A 44 C8 AA 41 01 30   .*D..A.0   0000 0010 0010 1010 0100 0100 1100 1000 1010 1010 0100 0001 0000 0001 0011 0000

0049A 50 31 CB 41 CC 41 D3 31   P1.A.A.1   0101 0000 0011 0001 1100 1011 0100 0001 1100 1100 0100 0001 1101 0011 0011 0001

004A2 D4                        .          1101 0100

004A3 E5 AA                     crc
#### 20.4.53 LAYER CONTROL (50) (UNDOCUMENTED)

Length
MS
---
Object length (not counting itself or CRC).

Type
BS
0&2
50 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Owner handle (soft pointer) of root object (0).

Open Design Specification for .dwg files

166



EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Numentries
BL
70
Counts layer "0", too.

Handle refs
H

NULL (soft pointer)




xdicobjhandle(hard owner)




layer objhandles (soft owner)

CRC
X
---
##### 20.4.53.1 Example:
OBJECT: layer ctrl (32H), len FH (15), handle: 02

024B1 0F 00                     ..         0000 1111 0000 0000

024B3 4C 80 40 A4 80 00 00 09   L.@.....   0100 1100 1000 0000 0100 0000 1010 0100 1000 0000 0000 0000 0000 0000 0000 1001

024BB 02 40 30 21 0F 21 99      .@0!.!.    0000 0010 0100 0000 0011 0000 0010 0001 0000 1111 0010 0001 1001 1001

024C2 C3 1D                     crc
#### 20.4.54 LAYER (51)

Length
MS
---
Object length (not counting itself or CRC).

Type
BS
0&2
51 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
code 0, length followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Entry name
TV
2

Open Design Specification for .dwg files

167



64-flag
B
70
The 64-bit of the 70 group.

xrefindex+1
BS
70
subtract one from this value when read.  After that,
-1 indicates that this reference did not come from
an xref, otherwise this value indicates the index of
the blockheader for the xref from which this came.

Xdep
B
70
dependent on an xref.  (16 bit)
R13-R14 Only:

Frozen
B
70
if frozen  (1 bit)

On
B

if on.  Normal Autodesk (and Open Design Toolkit)
policy is not to report this per se, but rather to
negate the color if the layer is off.

Frz in new
B
70
if frozen by default in new viewports (2 bit)

Locked
B
70
if locked (4 bit)
R2000+:

Values
BS 70,290,370 contains frozen (1 bit), on (2 bit), frozen by
default in new viewports (4 bit), locked (8 bit),
plotting flag (16 bit), and lineweight (mask with
0x03E0)
Common:

Color
CMC
62

Handle refs
H

Layer control (soft pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)




External reference block handle (hard pointer)
R2000+:


H
390
Plotstyle (hard pointer), by default points to
PLACEHOLDER with handle 0x0f.
R2007+:


H
347
Material
Common:


H
6
linetype (hard pointer)


H

Unknown handle (hard pointer). Always seems to be
NULL.

CRC
X
---
##### 20.4.54.1 Example:
OBJECT: layer (33H), len 1BH (27), handle: 99

02F91 1B 00                     ..         0001 1011 0000 0000

02F93 4C C0 66 6A 20 00 00 09   L.fj ...   0100 1100 1100 0000 0110 0110 0110 1010 0010 0000 0000 0000 0000 0000 0000 1001

02F9B 09 44 45 46 50 4F 49 4E   .DEFPOIN   0000 1001 0100 0100 0100 0101 0100 0110 0101 0000 0100 1111 0100 1001 0100 1110

02FA3 54 53 C0 41 D0 40 8C 14   TS.A.@..   0101 0100 0101 0011 1100 0000 0100 0001 1101 0000 0100 0000 1000 1100 0001 0100

02FAB 14 45 48                  .EH        0001 0100 0100 0101 0100 1000


Open Design Specification for .dwg files

168


02FAE 34 8F                     crc
#### 20.4.55 SHAPEFILE CONTROL (52) (UNDOCUMENTED)

Length
MS
---
Object length (not counting itself or CRC).

Type
BS
0&2
52 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Owner handle (soft pointer) of root object (0).

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Numentries
BL
70
number of style handles in refs section.

Handle refs
H

NULL (soft pointer)




xdicobjhandle (hard owner)




shapefile objhandles (soft owner)

CRC
X
---
##### 20.4.55.1 Example:
OBJECT: shpfile ctrl (34H), len FH (15), handle: 03

024C4 0F 00                     ..         0000 1111 0000 0000

024C6 4D 00 40 E4 80 00 00 09   M.@.....   0100 1101 0000 0000 0100 0000 1110 0100 1000 0000 0000 0000 0000 0000 0000 1001

024CE 02 40 30 21 10 21 F3      .@0!.!.    0000 0010 0100 0000 0011 0000 0010 0001 0001 0000 0010 0001 1111 0011

024D5 33 8B                     crc
#### 20.4.56 SHAPEFILE (53)
This contains a text style for the TEXT or MTEXT entity. Mostly the font information is stored in fields
Font name and Big font name, but sometimes (for reasons unknown) some true type font information is
contained in the table record’s extended data (see paragraph 28). The true type descriptor is stored as
follows in the extended data:
Group code (Value type)
Value
1001 (String)
Font file name
1002 (Bracket)
‘{‘ (optional)
1071 (Int32)
Flags:

Open Design Specification for .dwg files

169


Bold = 0x02000000,
Italic = 0x01000000,
Pitch (bitmask) = 0x00000003,
Font family (bitmask) = 0x000000f0,
Character set (bitmask) = 0x0000ff00
1002 (Bracket)
‘}’ (optional)

Length
MS
---
Object length (not counting itself or CRC).

Type
BS
0&2
53 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
code 0, length followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Entry name
TV
2

64-flag
B
70
The 64-bit of the 70 group.

xrefindex+1
BS
70
subtract one from this value when read.  After that,
-1 indicates that this reference did not come from
an xref, otherwise this value indicates the index of
the blockheader for the xref from which this came.

Xdep
B
70
dependent on an xref.  (16 bit)

Vertical
B
1
if vertical (1 bit of flag)

shape file
B
1
if a shape file rather than a font (4 bit)

Fixed height
BD
40

Width factor
BD
41

Oblique ang
BD
50

Generation
RC
71
Generation flags (not bit-pair coded).

Last height
BD
42

Font name
TV
3

Bigfont name
TV
4

Handle refs
H

Shapefile control (soft pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)




External reference block handle (hard pointer)

Open Design Specification for .dwg files

170



CRC
X
---
##### 20.4.56.1 Example:
OBJECT: shpfile (35H), len 25H (37), handle: 10

02FB0 25 00                     %.         0010 0101 0000 0000

02FB2 4D 40 44 20 20 10 00 09   M@D  ...   0100 1101 0100 0000 0100 0100 0010 0000 0010 0000 0001 0000 0000 0000 0000 1001

02FBA 08 53 54 41 4E 44 41 52   .STANDAR   0000 1000 0101 0011 0101 0100 0100 0001 0100 1110 0100 0100 0100 0001 0101 0010

02FC2 44 C2 60 02 6A 66 66 66   D.`.jfff   0100 0100 1100 0010 0110 0000 0000 0010 0110 1010 0110 0110 0110 0110 0110 0110

02FCA 66 67 24 FD 03 74 78 74   fg$..txt   0110 0110 0110 0111 0010 0100 1111 1101 0000 0011 0111 0100 0111 1000 0111 0100

02FD2 90 40 CC 14 28            .@..(      1001 0000 0100 0000 1100 1100 0001 0100 0010 1000

02FD7 EC 6E                     crc
#### 20.4.57 LINETYPE CONTROL (56) (UNDOCUMENTED)

Length
MS
---
Object length (not counting itself or CRC).

Type
BS
0&2
56 (internal DWG type code).
R2000 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Owner handle (soft pointer) of root object (0).

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Numentries
BL
70
Doesn't count BYBLOCK and BYLAYER even though they
both have entries.  Counts the soft owner ones.

Handle refs
H

NULL (soft pointer)




xdicobjhandle (hard owner)




the linetypes, ending with BYLAYER and BYBLOCK.




all are soft owner references except BYLAYER and
BYBLOCK, which are hard owner references.

CRC
X
---
20.4.57.1
Example:
OBJECT: ltype ctrl (38H), len 11H (17), handle: 05

Open Design Specification for .dwg files

171



024D7 11 00                     ..         0001 0001 0000 0000

024D9 4E 00 41 64 80 00 00 09   N.Ad....   0100 1110 0000 0000 0100 0001 0110 0100 1000 0000 0000 0000 0000 0000 0000 1001

024E1 01 40 30 21 15 31 13 31   .@0!.1.1   0000 0001 0100 0000 0011 0000 0010 0001 0001 0101 0011 0001 0001 0011 0011 0001

024E9 14                        .          0001 0100

024EA 82 54                     crc
#### 20.4.58 LTYPE (57)

Length
MS
---
Object length (not counting itself or CRC).

Type
BS
0&2
57 (internal DWG type code).
R2000 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
code 0, length followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Entry name
TV
2

64-flag
B
70
The 64-bit of the 70 group.

xrefindex+1
BS
70
subtract one from this value when read.  After that,
-1 indicates that this reference did not come from
an xref, otherwise this value indicates the index of
the blockheader for the xref from which this came.

Xdep
B
70
dependent on an xref.  (16 bit)

Description
TV
3

Pattern Len
BD
40

Alignment
RC
72
Always 'A'.

Numdashes
RC
73
The number of repetitions of the 49...74 data.
repeat numdashes times {

Dash length
BD
49
Dash or dot specifier.

Complex shapecode
BS
75
Shape number if shapeflag is 2, or index into the
string area if shapeflag is 4.

X-offset
RD
44
(0.0 for a simple dash.)

Y-offset
RD
45
(0.0 for a simple dash.)

Scale
BD
46
(1.0 for a simple dash.)

Open Design Specification for .dwg files

172



Rotation
BD
50
(0.0 for a simple dash.)

Shapeflag
BS
74
bit coded:




if (shapeflag & 1), text is rotated 0 degrees,




otherwise it follows the segment




if (shapeflag & 2), complexshapecode holds the




index of the shape to be drawn




if (shapeflag & 4), complexshapecode holds the index
into the text area of the string to be drawn.
NOTE:  Teigha Classic for .dwg files Toolkit does not present the data this way. It uses a separate
variable called stroffset which indicates the offets into the text string area. This is done in order to attempt
to make the data easier to understand.
}
R2004 and earlier:
Strings area
X
9
256 bytes of text area.  The complex dashes that
have text use this area via the 75-group indices.
It's basically a pile of 0-terminated strings. First
byte is always 0 for R13 and data starts at byte 1.
In R14 it is not a valid data start from byte 0.




(The 9-group is undocumented.)
R2007+:


X
9
512 bytes of text area, if the 0x02 bit is set on
any ShapeFlag (DXF 74) value above.  Otherwise no
data is present.
Common:

Handle refs
H

Ltype control (soft pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)




External reference block handle (hard pointer)



340
shapefile for dash/shape (1 each) (hard pointer)

CRC
X
---

#### 20.4.59 VIEW CONTROL (60) (UNDOCUMENTED)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0&2
60 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Owner handle (soft pointer) of root object (0).

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles

Open Design Specification for .dwg files

173


Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Numentries
BL
70

Handle refs
H

NULL (soft pointer)




xdicobjhandle (hard owner)




the views (soft owner)

CRC
X
---
##### 20.4.59.1 Example:
OBJECT: view ctrl (3CH), len DH (13), handle: 06

00A04 0D 00                     ..         0000 1101 0000 0000

00A06 4F 00 41 A4 80 00 00 09   O.A.....   0100 1111 0000 0000 0100 0001 1010 0100 1000 0000 0000 0000 0000 0000 0000 1001

00A0E 01 40 30 21 3F            .@0!?      0000 0001 0100 0000 0011 0000 0010 0001 0011 1111

00A13 E1 20                     crc
#### 20.4.60 VIEW (61)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
61 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Entry name
TV
2

64-flag
B
70
The 64-bit of the 70 group.

xrefindex+1
BS
70
subtract one from this value when read.  After that,
-1 indicates that this reference did not come from

Open Design Specification for .dwg files

174


an xref, otherwise this value indicates the index of
the blockheader for the xref from which this came.

Xdep
B
70
dependent on an xref.  (16 bit)

View height
BD
40

View width
BD
41

View center
2RD
10
(Not bit-pair coded.)

Target
3BD
12

View dir
3BD
11
DXF doc suggests from target toward camera.

Twist angle
BD
50
Radians

Lens length
BD
42

Front clip
BD
43

Back clip
BD
44

View mode
X
71
4 bits: 0123




0 : 71's bit 0 (1)




1 : 71's bit 1 (2)




2 : 71's bit 2 (4)




3 : OPPOSITE of 71's bit 4 (16)




Note that only bits 0, 1, 2, and 4 of the 71 can be
specified -- not bit 3 (8).
R2000+:

Render Mode
RC
281
R2007+:

Use default lights
B
?
Default value is true

Default lighting
RC
?
Default value is 1

Type

Brightness
BD
?
Default value is 0

Contrast
BD
?
Default value is 0

Abient color
CMC
?
Default value is AutoCAD indexed color 250
Common:

Pspace flag
B
70
Bit 0 (1) of the 70-group.
R2000+:

Associated UCS
B
72

Origin
3BD
10
This and next 4 R2000 items are present only if 72
value is 1.

X-direction
3BD
11

Y-direction
3BD
12

Elevation
BD
146

OrthographicViewType
BS
79

R2007+:

Camera plottable
B
73
Common:

Open Design Specification for .dwg files

175



Handle refs
H

view control object (soft pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)




External reference block handle (hard pointer)
R2007:

Background handle
H
332
soft pointer

Visual style
H
348
hard pointer

Sun
H
361
hard owner
R2000+:

Base UCS Handle
H
346
hard pointer

Named UCS Handle
H
345
hard pointer
R2007+:

Live section
H
334
soft pointer
Common:

CRC
X
---
##### 20.4.60.1 Example:
OBJECT: view (3DH), len 40H (64), handle: 3F

01409 40 00                     @.         0100 0000 0000 0000

0140B 4F 40 4F ED 90 10 00 09   O@O.....   0100 1111 0100 0000 0100 1111 1110 1101 1001 0000 0001 0000 0000 0000 0000 1001

01413 06 4D 59 56 49 45 57 C2   .MYVIEW.   0000 0110 0100 1101 0101 1001 0101 0110 0100 1001 0100 0101 0101 0111 1100 0010

0141B F1 38 4A E7 EB B4 A9 00   .8J.....   1111 0001 0011 1000 0100 1010 1110 0111 1110 1011 1011 0100 1010 1001 0000 0000

01423 9E EA 45 5D 73 27 34 40   ..E]s'4@   1001 1110 1110 1010 0100 0101 0101 1101 0111 0011 0010 0111 0011 0100 0100 0000

0142B 9D EA 45 5D 73 27 24 40   ..E]s'$@   1001 1101 1110 1010 0100 0101 0101 1101 0111 0011 0010 0111 0010 0100 0100 0000

01433 BC 4E 12 B9 FA ED 1A 40   .N.....@   1011 1100 0100 1110 0001 0010 1011 1001 1111 1010 1110 1101 0001 1010 0100 0000

0143B AA 98 00 00 00 00 00 00   ........   1010 1010 1001 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

01443 49 40 A1 20 83 18 28 00   I@. ..(.   0100 1001 0100 0000 1010 0001 0010 0000 1000 0011 0001 1000 0010 1000 0000 0000

0144B 0C 90                     crc
#### 20.4.61 UCS CONTROL (62) (UNDOCUMENTED)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0&2
62 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Owner handle (soft pointer) of root object (0).

EED
X
-3
See EED section.
R13-R14 Only:

Open Design Specification for .dwg files

176



Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Numentries
BL
70

Handle refs
H

NULL (soft pointer)




xdicobjhandle (hard owner)




the ucs’s (soft owner)

CRC
X
---
##### 20.4.61.1 Example:
OBJECT: ucs ctrl (3EH), len DH (13), handle: 07

0350B 0D 00                     ..         0000 1101 0000 0000

0350D 4F 80 41 E4 80 00 00 09   O.A.....   0100 1111 1000 0000 0100 0001 1110 0100 1000 0000 0000 0000 0000 0000 0000 1001

03515 01 40 30 21 4C            .@0!L      0000 0001 0100 0000 0011 0000 0010 0001 0100 1100

0351A A0 6F                     crc
#### 20.4.62 UCS (63)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
63 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Entry name
TV
2

64-flag
B
70
The 64-bit of the 70 group.

Open Design Specification for .dwg files

177



xrefindex+1
BS
70
subtract one from this value when read.  After that,
-1 indicates that this reference did not come from
an xref, otherwise this value indicates the index of
the blockheader for the xref from which this came.

Xdep
B
70
dependent on an xref.  (16 bit)

Origin
3BD
10

X-direction
3BD
11

Y-direction
3BD
12
R2000+:

Elevation
BD
146

OrthographicViewType
BS
79

OrthographicType
BS
71
Common:

Handle refs
H

ucs control object (soft pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)




External reference block handle (hard pointer)
R2000+:

Base UCS Handle
H
346
hard pointer

Named UCS Handle
H
-
hard pointer, not present in DXF
Common:

CRC
X
---
##### 20.4.62.1 Example:
OBJECT: ucs (3FH), len 45H (69), handle: 4C

03EB1 45 00                     E.         0100 0101 0000 0000

03EB3 4F C0 53 20 60 20 00 09   O.S ` ..   0100 1111 1100 0000 0101 0011 0010 0000 0110 0000 0010 0000 0000 0000 0000 1001

03EBB 05 4D 59 55 43 53 CA 8F   .MYUCS..   0000 0101 0100 1101 0101 1001 0101 0101 0100 0011 0101 0011 1100 1010 1000 1111

03EC3 DF FF FF FF FF FE 73 F2   ......s.   1101 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111 1110 0111 0011 1111 0010

03ECB 14 E5 08 BB 73 23 90 FC   ....s#..   0001 0100 1110 0101 0000 1000 1011 1011 0111 0011 0010 0011 1001 0000 1111 1100

03ED3 EC FF FF FF FF FF BF BF   ........   1110 1100 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111 1011 1111 1011 1111

03EDB 2B D3 16 3A 1E AD B6 EF   +..:....   0010 1011 1101 0011 0001 0110 0011 1010 0001 1110 1010 1101 1011 0110 1110 1111

03EE3 CF 8F FF FF FF FF FE 33   .......3   1100 1111 1000 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111 1110 0011 0011

03EEB F2 18 E5 08 BB 73 23 90   .....s#.   1111 0010 0001 1000 1110 0101 0000 1000 1011 1011 0111 0011 0010 0011 1001 0000

03EF3 FD 04 1C C1 40            ....@      1111 1101 0000 0100 0001 1100 1100 0001 0100 0000

03EF8 BE 62                     crc
#### 20.4.63 TABLE (VPORT) (64) (UNDOCUMENTED)

Length
MS
---
Entity length (not counting itself or CRC).

Open Design Specification for .dwg files

178



Type
BS
0&2
64 (internal DWG type code).
R2000:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Owner handle (soft pointer) of root object (0).

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Numentries
BL
70
Counts all 0010.refs -- even the null ones
(0010.0000).  The actual 70-group value from an
entget doesn't count the null ones.

Handle refs
H

NULL (soft pointer)




xdicobjhandle (hard owner)




the vports (soft owner)

CRC
X
---
##### 20.4.63.1 Example:
OBJECT: vport ctrl (40H), len 12H (18), handle: 08

0351C 12 00                     ..         0001 0010 0000 0000

0351E 50 00 42 24 80 00 00 09   P.B$....   0101 0000 0000 0000 0100 0010 0010 0100 1000 0000 0000 0000 0000 0000 0000 1001

03526 04 40 30 20 21 4E 21 4F   .@0 !N!O   0000 0100 0100 0000 0011 0000 0010 0000 0010 0001 0100 1110 0010 0001 0100 1111

0352E 21 50                     !P         0010 0001 0101 0000

03530 9E 1F                     crc
#### 20.4.64 VPORT (65)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
65 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles

Open Design Specification for .dwg files

179


Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Entry name
TV
2

64-flag
B
70
The 64-bit of the 70 group.

xrefindex+1
BS
70
subtract one from this value when read.  After that,
-1 indicates that this reference did not come from
an xref, otherwise this value indicates the index of
the blockheader for the xref from which this came.

Xdep
B
70
dependent on an xref.  (16 bit)

View height
BD
40

Aspect ratio
BD
41
The number stored here is actually the aspect ratio
times the view height (40), so this number must be
divided by the 40-value to produce the aspect ratio
that entget gives.  (R13 quirk; R12 has just the
aspect ratio.)

View Center
2RD
12
DCS.  (If it's plan view, add the view target (17)
to get the WCS coordinates.  Careful! Sometimes you
have to SAVE/OPEN to update the .dwg file.)  Note
that it's WSC in R12.

View target
3BD
17

View dir
3BD
16

View twist
BD
51

Lens length
BD
42

Front clip
BD
43

Back clip
BD
44

View mode
X
71
4 bits: 0123




0 : 71's bit 0 (1)




1 : 71's bit 1 (2)




2 : 71's bit 2 (4)




3 : OPPOSITE of 71's bit 4 (16)




Note that only bits 0, 1, 2, and 4 are given here;
see UCSFOLLOW below for bit 3 (8) of the 71.
R2000+:

Render Mode
RC
281
R2007+:

Use default lights
B
292

Default lighting type RC
282

Brightness
BD
141

Constrast
BD
142

Ambient Color
CMC
63

Open Design Specification for .dwg files

180


Common:

Lower left
2RD
10
In fractions of screen width and height.

Upper right
2RD
11
In fractions of screen width and height.

UCSFOLLOW
B
71
UCSFOLLOW.  Bit 3 (8) of the 71-group.

Circle zoom
BS
72
Circle zoom percent.

Fast zoom
B
73

UCSICON
X
74
2 bits: 01




0 : 74's bit 0 (1)




1 : 74's bit 1 (2)

Grid on/off
B
76

Grd spacing
2RD
15

Snap on/off
B
75

Snap style
B
77

Snap isopair
BS
78

Snap rot
BD
50

Snap base
2RD
13

Snp spacing
2RD
14
R2000+:

Unknown
B

UCS per Viewport
B
71

UCS Origin
3BD
110

UCS X Axis
3BD
111

UCS Y Axis
3BD
112

UCS Elevation
BD
146

UCS Orthographic type BS
79
R2007+:

Grid flags
BS
60

Grid major
BS
61
Common:

Handle refs
H

Vport control (soft pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)




External reference block handle (hard pointer)
R2007+:

Background handle
H
332
soft pointer

Visual Style handle
H
348
hard pointer

Sun handle
H
361
hard owner
R2000+:

Named UCS Handle
H
345
hard pointer

Base UCS Handle
H
346
hard pointer

Open Design Specification for .dwg files

181


Common:

CRC
X
---
##### 20.4.64.1 Example:
OBJECT: vport (41H), len 93H (147), handle: 4E

03EFA 93 00                     ..         1001 0011 0000 0000

03EFC 50 40 53 A7 50 40 00 09   P@S.P@..   0101 0000 0100 0000 0101 0011 1010 0111 0101 0000 0100 0000 0000 0000 0000 1001

03F04 07 2A 41 43 54 49 56 45   .*ACTIVE   0000 0111 0010 1010 0100 0001 0100 0011 0101 0100 0100 1001 0101 0110 0100 0101

03F0C C2 1E 94 3B 21 CD A4 CD   ...;!...   1100 0010 0001 1110 1001 0100 0011 1011 0010 0001 1100 1101 1010 0100 1100 1101

03F14 00 A5 86 68 4A 2C 0E 2D   ...hJ,.-   0000 0000 1010 0101 1000 0110 0110 1000 0100 1010 0010 1100 0000 1110 0010 1101

03F1C 40 A5 86 68 4A 2C 0E 1D   @..hJ,..   0100 0000 1010 0101 1000 0110 0110 1000 0100 1010 0010 1100 0000 1110 0001 1101

03F24 40 87 A5 0E C8 73 69 23   @....si#   0100 0000 1000 0111 1010 0101 0000 1110 1100 1000 0111 0011 0110 1001 0010 0011

03F2C 40 AA 98 00 00 00 00 00   @.......   0100 0000 1010 1010 1001 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

03F34 00 49 40 A1 00 00 00 00   .I@.....   0000 0000 0100 1001 0100 0000 1010 0001 0000 0000 0000 0000 0000 0000 0000 0000

03F3C 00 00 E0 3F 00 00 00 00   ...?....   0000 0000 0000 0000 1110 0000 0011 1111 0000 0000 0000 0000 0000 0000 0000 0000

03F44 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

03F4C 00 00 F0 3F 00 00 00 00   ...?....   0000 0000 0000 0000 1111 0000 0011 1111 0000 0000 0000 0000 0000 0000 0000 0000

03F54 00 00 F0 3F 2C 98 00 00   ...?,...   0000 0000 0000 0000 1111 0000 0011 1111 0010 1100 1001 1000 0000 0000 0000 0000

03F5C 00 00 00 01 C0 7E 00 00   .....~..   0000 0000 0000 0000 0000 0000 0000 0001 1100 0000 0111 1110 0000 0000 0000 0000

03F64 00 00 00 01 C0 7E 50 00   .....~P.   0000 0000 0000 0000 0000 0000 0000 0001 1100 0000 0111 1110 0101 0000 0000 0000

03F6C 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

03F74 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

03F7C 00 00 00 00 07 01 F8 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0111 0000 0001 1111 1000 0000 0000

03F84 00 00 00 00 07 01 FA 08   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0111 0000 0001 1111 1010 0000 1000

03F8C 41 82 80                  A..        0100 0001 1000 0010 1000 0000

03F8F 7D 31                     crc
#### 20.4.65 TABLE (APPID) (66) (UNDOCUMENTED)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0&2
66 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Owner handle (soft pointer) of root object (0).

EED
X
-3
See EED section.

Open Design Specification for .dwg files

182


R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Numentries
BL
70

Handle refs
H

NULL (soft pointer)




xdicobjhandle (hard owner)




the apps (soft owner)

CRC
X
---
##### 20.4.65.1 Example:
OBJECT: regapp ctrl (42H), len FH (15), handle: 09

03532 0F 00                     ..         0000 1111 0000 0000

03534 50 80 42 64 80 00 00 09   P.Bd....   0101 0000 1000 0000 0100 0010 0110 0100 1000 0000 0000 0000 0000 0000 0000 1001

0353C 02 40 30 21 11 21 86      .@0!.!.    0000 0010 0100 0000 0011 0000 0010 0001 0001 0001 0010 0001 1000 0110

03543 FA D9                     crc
#### 20.4.66 APPID (67)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
67 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Entry name
TV
2

64-flag
B
70
The 64-bit of the 70 group.

Open Design Specification for .dwg files

183



xrefindex+1
BS
70
subtract one from this value when read.  After that,
-1 indicates that this reference did not come from
an xref, otherwise this value indicates the index of
the blockheader for the xref from which this came.

Xdep
B
70
dependent on an xref.  (16 bit)

Unknown
RC
71
Undoc'd 71-group; doesn't even appear in DXF or an
entget if it's 0.

Handle refs
H

The app control (soft pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)




External reference block handle (hard pointer)

CRC
X
---
##### 20.4.66.1 Example:
OBJECT: regapp (43H), len 13H (19), handle: 11

040BF 13 00                     ..         0001 0011 0000 0000

040C1 50 C0 44 67 40 00 00 09   P.Dg@...   0101 0000 1100 0000 0100 0100 0110 0111 0100 0000 0000 0000 0000 0000 0000 1001

040C9 04 41 43 41 44 C0 0C 10   .ACAD...   0000 0100 0100 0001 0100 0011 0100 0001 0100 0100 1100 0000 0000 1100 0001 0000

040D1 83 05 0A                  ...        1000 0011 0000 0101 0000 1010

040D4 8C E9                     crc
#### 20.4.67 DIMSTYLE CONTROL (68) (UNDOCUMENTED)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0&2
68 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Owner handle (soft pointer) of root object (0).

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Numentries
BL
70

Handle refs
H

NULL (soft pointer)




xdicobjhandle (hard owner)

Open Design Specification for .dwg files

184






the dimstyles (soft owner)

CRC
X
---
##### 20.4.67.1 Example:
OBJECT: dimstyle ctrl (44H), len 10H (16), handle: 0A

03545 10 00                     ..         0001 0000 0000 0000

03547 51 00 42 A4 80 00 00 09   Q.B.....   0101 0001 0000 0000 0100 0010 1010 0100 1000 0000 0000 0000 0000 0000 0000 1001

0354F 03 40 30 21 1D 21 4D 20   .@0!.!M    0000 0011 0100 0000 0011 0000 0010 0001 0001 1101 0010 0001 0100 1101 0010 0000

03557 BA 14                     crc
#### 20.4.68 DIMSTYLE (69)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
69 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Entry name
TV
2

64-flag
B
70
The 64-bit of the 70 group.

xrefindex+1
BS
70
subtract one from this value when read.  After that,
-1 indicates that this reference did not come from
an xref, otherwise this value indicates the index of
the blockheader for the xref from which this came.

Xdep
B
70
dependent on an xref.  (16 bit)
R13 & R14 Only:

DIMTOL
B
71

DIMLIM
B
72

DIMTIH
B
73

DIMTOH
B
74

DIMSE1
B
75

DIMSE2
B
76

Open Design Specification for .dwg files

185



DIMALT
B
170

DIMTOFL
B
172

DIMSAH
B
173

DIMTIX
B
174

DIMSOXD
B
175

DIMALTD
RC
171

DIMZIN
RC
78

DIMSD1
B
281

DIMSD2
B
282

DIMTOLJ
RC
283

DIMJUST
RC
280

DIMFIT
RC
287

DIMUPT
B
288

DIMTZIN
RC
284

DIMALTZ
RC
285

DIMALTTZ
RC
286

DIMTAD
RC
77

DIMUNIT
BS
270

DIMAUNIT
BS
275

DIMDEC
BS
271

DIMTDEC
BS
272

DIMALTU
BS
273

DIMALTTD
BS
274

DIMSCALE
BD
40

DIMASZ
BD
41

DIMEXO
BD
42

DIMDLI
BD
43

DIMEXE
BD
44

DIMRND
BD
45

DIMDLE
BD
46

DIMTP
BD
47

DIMTM
BD
48

DIMTXT
BD
140

DIMCEN
BD
141

DIMTSZ
BD
142

DIMALTF
BD
143

DIMLFAC
BD
144

DIMTVP
BD
145

DIMTFAC
BD
146

DIMGAP
BD
147

Open Design Specification for .dwg files

186



DIMPOST
T
3

DIMAPOST
T
4

DIMBLK
T
5

DIMBLK1
T
6

DIMBLK2
T
7

DIMCLRD
BS
176

DIMCLRE
BS
177

DIMCLRT
BS
178
R2000+:

DIMPOST
TV
3

DIMAPOST
TV
4

DIMSCALE
BD
40

DIMASZ
BD
41

DIMEXO
BD
42

DIMDLI
BD
43

DIMEXE
BD
44

DIMRND
BD
45

DIMDLE
BD
46

DIMTP
BD
47

DIMTM
BD
48
R2007+:

DIMFXL
BD
49

DIMJOGANG
BD
50

DIMTFILL
BS
69

DIMTFILLCLR
CMC
70
R2000+:

DIMTOL
B
71

DIMLIM
B
72

DIMTIH
B
73

DIMTOH
B
74

DIMSE1
B
75

DIMSE2
B
76

DIMTAD
BS
77

DIMZIN
BS
78

DIMAZIN
BS
79
R2007+:

DIMARCSYM
BS
90
R2000+:

DIMTXT
BD
140

DIMCEN
BD
141

Open Design Specification for .dwg files

187



DIMTSZ
BD
142

DIMALTF
BD
143

DIMLFAC
BD
144

DIMTVP
BD
145

DIMTFAC
BD
146

DIMGAP
BD
147

DIMALTRND
BD
148

DIMALT
B
170

DIMALTD
BS
171

DIMTOFL
B
172

DIMSAH
B
173

DIMTIX
B
174

DIMSOXD
B
175

DIMCLRD
BS
176

DIMCLRE
BS
177

DIMCLRT
BS
178

DIMADEC
BS
179

DIMDEC
BS
271

DIMTDEC
BS
272

DIMALTU
BS
273

DIMALTTD
BS
274

DIMAUNIT
BS
275

DIMFRAC
BS
276

DIMLUNIT
BS
277

DIMDSEP
BS
278

DIMTMOVE
BS
279

DIMJUST
BS
280

DIMSD1
B
281

DIMSD2
B
282

DIMTOLJ
BS
283

DIMTZIN
BS
284

DIMALTZ
BS
285

DIMALTTZ
BS
286

DIMUPT
B
288

DIMFIT
BS
287
R2007+:

DIMFXLON
B
290
R2010+:

DIMTXTDIRECTION
B
295

DIMALTMZF
BD
?

Open Design Specification for .dwg files

188



DIMALTMZS
T
?
DIMMZF
BD
?

DIMMZS
T
?
R2000+:

DIMLWD
BS
371

DIMLWE
BS
372
Common:

Unknown
B
70
Seems to set the 0-bit (1) of the 70-group.

Handle refs
H

Dimstyle control (soft pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)




External reference block handle (hard pointer)
340
shapefile (DIMTXSTY) (hard pointer)
R2000+:
341
leader block (DIMLDRBLK) (hard pointer)
342
dimblk (DIMBLK) (hard pointer)
343
dimblk1 (DIMBLK1) (hard pointer)
344
dimblk2 (DIMBLK2) (hard pointer)
R2007+:
345
dimltype (hard pointer)
346
dimltex1 (hard pointer)
347
dimltex2 (hard pointer)
Common:

CRC
X
---
20.4.68.1
Example:
OBJECT: dimstyle (45H), len 70H (112), handle: 1D

040F0 70 00                     p.         0111 0000 0000 0000

040F2 51 40 47 64 90 30 00 09   Q@Gd.0..   0101 0001 0100 0000 0100 0111 0110 0100 1001 0000 0011 0000 0000 0000 0000 1001

040FA 08 53 54 41 4E 44 41 52   .STANDAR   0000 1000 0101 0011 0101 0100 0100 0001 0100 1110 0100 0100 0100 0001 0101 0010

04102 44 C3 00 04 00 00 80 01   D.......   0100 0100 1100 0011 0000 0000 0000 0100 0000 0000 0000 0000 1000 0000 0000 0001

0410A 80 00 00 00 10 29 04 41   .....).A   1000 0000 0000 0000 0000 0000 0000 0000 0001 0000 0010 1001 0000 0100 0100 0001

04112 10 24 09 02 B5 E8 DC 0F   .$......   0001 0000 0010 0100 0000 1001 0000 0010 1011 0101 1110 1000 1101 1100 0000 1111

0411A 42 B1 CF C0 00 00 00 00   B.......   0100 0010 1011 0001 1100 1111 1100 0000 0000 0000 0000 0000 0000 0000 0000 0000

04122 00 0B 03 F1 4A E0 7A 17   ....J.z.   0000 0000 0000 1011 0000 0011 1111 0001 0100 1010 1110 0000 0111 1010 0001 0111

0412A AD 47 60 FC 0A D7 A3 70   .G`....p   1010 1101 0100 0111 0110 0000 1111 1100 0000 1010 1101 0111 1010 0011 0111 0000

04132 3D 0A C7 3F AA 02 B5 E8   =..?....   0011 1101 0000 1010 1100 0111 0011 1111 1010 1010 0000 0010 1011 0101 1110 1000


Open Design Specification for .dwg files

189


0413A DC 0F 42 B1 CF C0 AD 7A   ..B....z   1101 1100 0000 1111 0100 0010 1011 0001 1100 1111 1100 0000 1010 1101 0111 1010

04142 37 03 D0 AB 73 F8 66 66   7...s.ff   0011 0111 0000 0011 1101 0000 1010 1011 0111 0011 1111 1000 0110 0110 0110 0110

0414A 66 66 66 66 39 40 64 0A   ffff9@d.   0110 0110 0110 0110 0110 0110 0110 0110 0011 1001 0100 0000 0110 0100 0000 1010

04152 D7 A3 70 3D 0A B7 3F AA   ..p=..?.   1101 0111 1010 0011 0111 0000 0011 1101 0000 1010 1011 0111 0011 1111 1010 1010

0415A AA 20 85 18 28 28 88 00   . ..((..   1010 1010 0010 0000 1000 0101 0001 1000 0010 1000 0010 1000 1000 1000 0000 0000

04162 CC 33                     crc
#### 20.4.69 VIEWPORT ENTITY CONTROL (70) (UNDOCUMENTED)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0&2
70 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Owner handle (soft pointer) of root object (0).

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
B
L
Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Numentries
BL
70

Handle refs
H

NULL (soft pointer)




xdicobjhandle (hard owner)




the viewport entity headers (soft owner)

CRC
X
---
20.4.69.1
Example:
OBJECT: vpent ctrl (46H), len 17H (23), handle: 0B

03559 17 00                     ..         0001 0111 0000 0000

0355B 51 80 42 E4 80 00 00 09   Q.B.....   0101 0001 1000 0000 0100 0010 1110 0100 1000 0000 0000 0000 0000 0000 0000 1001

03563 06 40 30 21 51 21 52 21   .@0!Q!R!   0000 0110 0100 0000 0011 0000 0010 0001 0101 0001 0010 0001 0101 0010 0010 0001

0356B 54 21 56 21 58 21 5A      T!V!X!Z    0101 0100 0010 0001 0101 0110 0010 0001 0101 1000 0010 0001 0101 1010

03572 9E 84                     crc

Open Design Specification for .dwg files

190


#### 20.4.70 VIEWPORT ENTITY HEADER (71)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
71 (internal DWG type code).
R2000:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Entry name
TV
2

64-flag
B
70
The 64-bit of the 70 group.

xrefindex+1
BS
70
subtract one from this value when read.  After that,
-1 indicates that this reference did not come from
an xref, otherwise this value indicates the index of
the blockheader for the xref from which this came.

Xdep
B
70
dependent on an xref.  (16 bit)

1 flag
B

The 1 bit of the 70 group

Handle refs
H

viewport entity control (soft pointer)




xdicobjhandle (hard owner)




External reference block handle (hard pointer)




the corresponding viewport entity (soft owner)
objhandle of previous vport ent header in chain
(hard pointer) sometimes points to self; I change
those to NULL.  NULL indicates end of chain.

CRC
X
---
##### 20.4.70.1 Example:
OBJECT: vpent hdr (47H), len 11H (17), handle: 58

03574 11 00                     ..         0001 0001 0000 0000

03576 51 C0 56 24 50 00 00 0A   Q.V$P...   0101 0001 1100 0000 0101 0110 0010 0100 0101 0000 0000 0000 0000 0000 0000 1010

0357E CA 08 59 82 82 0A CA 8A   ..Y.....   1100 1010 0000 1000 0101 1001 1000 0010 1000 0010 0000 1010 1100 1010 1000 1010

03586 B4                        .          1011 0100

03587 2F 9E                     crc

Open Design Specification for .dwg files

191


#### 20.4.71 AcDbAnnotScaleObjectContextData
This class inherits from class AcDbObjectContextData (see paragraph 20.4.89).
Version
Field
type
DXF
group
code
Description

…

Common AcDbObjectContextData data (see paragraph 20.4.89).

H
340
Handle to scale (AcDbScale) object (hard pointer). See paragraph 20.4.92.
#### 20.4.72 GROUP (72):  Group of ACAD entities

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
72 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Str
TV

name of group

Unnamed
BS
1
if group has no name

Selectable
BS
1
if group selectable

Numhandles
BL

# objhandles in this group

Handle refs
H

parenthandle (soft pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)




the entries in the group (hard pointer)
20.4.72.1
Example:
OBJECT: group (48H), len 27H (39), handle: 7B

0431E 27 00                     '.         0010 0111 0000 0000

04320 52 00 5E ED E0 00 00 04   R.^.....   0101 0010 0000 0000 0101 1110 1110 1101 1110 0000 0000 0000 0000 0000 0000 0100

04328 05 0F 74 68 69 73 20 69   ..this i   0000 0101 0000 1111 0111 0100 0110 1000 0110 1001 0111 0011 0010 0000 0110 1001

04330 73 20 6D 79 67 72 6F 75   s mygrou   0111 0011 0010 0000 0110 1101 0111 1001 0110 0111 0111 0010 0110 1111 0111 0101

Open Design Specification for .dwg files

192



04338 70 90 14 0D 04 35 04 34   p....5.4   0111 0000 1001 0000 0001 0100 0000 1101 0000 0100 0011 0101 0000 0100 0011 0100

04340 C1 45 E9 45 B5 45 A1      .E.E.E.    1100 0001 0100 0101 1110 1001 0100 0101 1011 0101 0100 0101 1010 0001

04347 35 69                     crc
#### 20.4.73 MLINESTYLE (73):

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
73 (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Name
TV

Name of this style

Desc
TV

Description of this style

Flags
BS

A short which reconstitutes the mlinestyle flags as
defined in DXF.  Here are the bits as they relate to
DXF:




DWG bit     goes with     DXF bit




1                         2




2                         1




16                        16




32                        64




64                        32




256                       256




512                      1024




1024                       512

fillcolor
CMC

Fill color for this style

startang
BD

Start angle

endang
BD

End angle

linesinstyle
RC

Number of lines in this style

REPEAT 'linesinstyle' times:

Open Design Specification for .dwg files

193



Offset
BD

Offset of this segment

Color
CMC

Color of this segment
Before R2018:

Ltindex
BS

Linetype index (yes, index)
R2018+:

Line type handle
H

Line type handle (hard pointer)
END REPEAT

Common:

Handle refs
H

parenthandle (soft pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)
##### 20.4.73.1 Example:
OBJECT: mlstyle (49H), len 55H (85), handle: 74

0439B 55 00                     U.         0101 0101 0000 0000

0439D 52 40 5D 27 C0 20 00 04   R@]'. ..   0101 0010 0100 0000 0101 1101 0010 0111 1100 0000 0010 0000 0000 0000 0000 0100

043A5 05 09 4D 59 4D 4C 53 54   ..MYMLST   0000 0101 0000 1001 0100 1101 0101 1001 0100 1101 0100 1100 0101 0011 0101 0100

043AD 59 4C 45 44 9B 5E 48 1B   YLED.^H.   0101 1001 0100 1100 0100 0101 0100 0100 1001 1011 0101 1110 0100 1000 0001 1011

043B5 5D 5B 1D 1A 5B 1A 5B 99   ][..[.[.   0101 1101 0101 1011 0001 1101 0001 1010 0101 1011 0001 1010 0101 1011 1001 1001

043BD 48 1C DD 1E 5B 19 68 18   H...[.h.   0100 1000 0001 1100 1101 1101 0001 1110 0101 1011 0001 1001 0110 1000 0001 1000

043C5 2D 44 54 FB 21 F9 3F 06   -DT.!.?.   0010 1101 0100 0100 0101 0100 1111 1011 0010 0001 1111 1001 0011 1111 0000 0110

043CD 0B 51 15 3E C8 7E 4F C0   .Q.>.~O.   0000 1011 0101 0001 0001 0101 0011 1110 1100 1000 0111 1110 0100 1111 1100 0000

043D5 C0 00 00 00 00 00 0E 03   ........   1100 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 1110 0000 0011

043DD FD 01 90 44 08 00 00 00   ...D....   1111 1101 0000 0001 1001 0000 0100 0100 0000 1000 0000 0000 0000 0000 0000 0000

043E5 00 00 00 E0 BF 40 90 34   .....@.4   0000 0000 0000 0000 0000 0000 1110 0000 1011 1111 0100 0000 1001 0000 0011 0100

043ED 10 E4 10 E3 00            .....      0001 0000 1110 0100 0001 0000 1110 0011 0000 0000

043F2 8F AA                     crc
NOTE:  OBJECTS LISTED AFTER THIS POINT DO NOT HAVE FIXED TYPES.  THEIR TYPES
ARE DETERMINED BY FINDING THE CLASS ENTRY WHOSE POSITION IN THE CLASS LIST
+ 500 EQUALS THE TYPE OF THIS OBJECT
#### 20.4.74 DICTIONARYVAR (varies)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
typecode (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles

Open Design Specification for .dwg files

194


Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Intval
RC

an integer value

Str
BS

a string

Handle refs
H

parenthandle (soft pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)
##### 20.4.74.1 Example:
OBJECT: proxy (1F9H), len 12H (18), handle: 01 EA

0CDB4 12 00                     ..         0001 0010 0000 0000

0CDB6 3E 40 40 80 7A A7 00 00   >@@.z...   0011 1110 0100 0000 0100 0000 1000 0000 0111 1010 1010 0111 0000 0000 0000 0000

0CDBE 00 04 04 01 01 33 40 41   .....3@A   0000 0000 0000 0100 0000 0100 0000 0001 0000 0001 0011 0011 0100 0000 0100 0001

0CDC6 A2 30                     .0         1010 0010 0011 0000

0CDC8 AC DA                     crc
#### 20.4.75 HATCH (varies)

Common Entity Data
R2004+:

Is Gradient Fill
BL
450
Non-zero indicates a gradient fill is used.

Reserved
BL
451


Gradient Angle
BD
460

Gradient Shift
BD
461

Single Color Grad.
BL
452

Gradient Tint
BD
462

# of Gradient Colors
BL
453

Repeats # of Gradient Colors time:

Unknown double
BD
463


Unknown short
BS

RGB Color
BL 63,421

Open Design Specification for .dwg files

195



Ignored color byte
RC
End Repeat

Gradient Name
TV
470
Common:



Z coord
BD
30
X, Y always 0.0

Extrusion
3BD
210

Name
TV
2
name of hatch

Solidfill
B
70
1 if solidfill, else 0

Associative
B
71
1 if associative, else 0

Numpaths
BL
91
Number of paths enclosing the hatch

/* definitions of the hatch boundaries */

Repeat numpaths times:
Pathflag     BL  92  Path flag
if (!(pathflag & 2)) {
Numpathsegs   BL  93  number of segments in this path
Repeat numpathsegs times:
pathtypestatus   RC  72  type of path
if (pathtypestatus==1) {    /* LINE */
pt0              2RD  10  first endpoint
pt1              2RD  11  second endpoint
}
else if (pathtypestatus==2) {  /* CIRCULAR ARC */
pt0              2RD  10  center
radius            BD  40  radius
startangle        BD  50  start angle
endangle          BD  51  endangle
isccw             B   73  1 if counter clockwise, otherwise 0
}
else if (pathtypestatus==3) {  /* ELLIPTICAL ARC */
pt0              2RD  10  center
endpoint         2RD  11  endpoint of major axis
minormajoratio    BD  40  ratio of minor to major axis
startangle        BD  50  start angle
endangle          BD  51  endangle
isccw              B  73  1 if counter clockwise, otherwise 0
}
else if (pathtypestatus==4) {  /* SPLINE */
degree            BL  94  degree of the spline

Open Design Specification for .dwg files

196


isrational         B  73  1 if rational (has weights), else 0
isperiodic         B  74  1 if periodic, else 0
numknots          BL  95  number of knots
numctlpts         BL  96  number of control points
Repeat numknots times:
knot               BD  40  knot value
End repeat
Repeat numctlpts times:
pt0                2RD  10  control point
if (isrational)
weight            BD  40  weight
endif
End repeat
R24:
Numfitpoints          BL  97  number of fit points
Begin repeat numfitpoints times:
Fitpoint           2RD  11
End repeat
Start tangent        2RD  12
End tangent          2RD  13
Common:
}
End repeat (numpathsegs)
} /* (!(pathflag & 2)) */
else {  /* POLYLINE PATH */
bulgespresent         B  72  bulges are present if 1
closed                B  73  1 if closed
numpathsegs          BL  91  number of path segments
Repeat numpathsegs times:
pt0                 2RD  10  point on polyline
if (bulgespresent) {
bulge                BD  42  bulge
}
End repeat
}  /* pathflag & 2 */
numboundaryobjhandles     BL  97  Number of boundary object handles for this path
End repeat (numpaths)

/* below this point is the definition of the hatch itself */

Open Design Specification for .dwg files

197



style
BS
75
style of hatch  0==odd parity, 1==outermost,
2==whole area

patterntype
BS
76
pattern type  0==user-defined, 1==predefined,
2==custom
if (!solidfill) {
angle          BD  52  hatch angle
scaleorspacing BD  41  scale or spacing (pattern fill only)
doublehatch     B  77  1 for double hatch
numdeflines    BS  78  number of definition lines
Repeat numdeflines times:
angle           BD  53  line angle
pt0            2BD  43/44  pattern through this point (X,Y)
offset         2BD  45/56  pattern line offset
numdashes       BS  79  number of dash length items
Repeat numdashes times:
dashlength      BD  49  dash length
End repeat
End repeat
}
if (ANY of the pathflags & 4) {
pixelsize        BD  47  pixel size
}
numseedpoints      BL  98  number of seed points
Repeat numseedpoints times:
pt0               2RD  10  seed point
End repeat


Common Entity Handle Data
Repeat totalbounditems (sum of all "numboundaryitems") times
boundaryhandle    H  330  boundary handle (soft pointer)
End repeat


CRC
X
---
##### 20.4.75.1 Example:
OBJECT: proxy (1F5H), len E2H (226), handle: 68

069C4 E2 00                     ..         1110 0010 0000 0000

069C6 3D 40 40 5A 26 70 30 00   =@@Z&p0.   0011 1101 0100 0000 0100 0000 0101 1010 0010 0110 0111 0000 0011 0000 0000 0000

069CE 02 80 DB 54 A0 C8 29 CA   ...T..).   0000 0010 1000 0000 1101 1011 0101 0100 1010 0000 1100 1000 0010 1001 1100 1010

069D6 69 26 66 22 02 80 A0 80   i&f"....   0110 1001 0010 0110 0110 0110 0010 0010 0000 0010 1000 0000 1010 0000 1000 0000

Open Design Specification for .dwg files

198



069DE 28 03 02 5A E2 89 80 68   (..Z...h   0010 1000 0000 0011 0000 0010 0101 1010 1110 0010 1000 1001 1000 0000 0110 1000

069E6 0D 0F 09 03 C3 C3 C0 88   ........   0000 1101 0000 1111 0000 1001 0000 0011 1100 0011 1100 0011 1100 0000 1000 1000

069EE 1C 12 5E 96 B9 91 BC A7   ..^.....   0001 1100 0001 0010 0101 1110 1001 0110 1011 1001 1001 0001 1011 1100 1010 0111

069F6 F6 1A C1 03 D6 06 A0 88   ........   1111 0110 0001 1010 1100 0001 0000 0011 1101 0110 0000 0110 1010 0000 1000 1000

069FE 00 3C 12 5E 96 B9 91 BC   .<.^....   0000 0000 0011 1100 0001 0010 0101 1110 1001 0110 1011 1001 1001 0001 1011 1100

06A06 A7 F6 1A C1 03 D6 06 A0   ........   1010 0111 1111 0110 0001 1010 1100 0001 0000 0011 1101 0110 0000 0110 1010 0000

06A0E 88 1A 0F A5 B5 4C A8 1F   .....L..   1000 1000 0001 1010 0000 1111 1010 0101 1011 0101 0100 1100 1010 1000 0001 1111

06A16 47 EC 11 0B 35 26 AC 5D   G...5&.]   0100 0111 1110 1100 0001 0001 0000 1011 0011 0101 0010 0110 1010 1100 0101 1101

06A1E C7 E0 3A 0F A5 B5 4C A8   ..:...L.   1100 0111 1110 0000 0011 1010 0000 1111 1010 0101 1011 0101 0100 1100 1010 1000

06A26 1F 47 EC 11 0B 35 26 AC   .G...5&.   0001 1111 0100 0111 1110 1100 0001 0001 0000 1011 0011 0101 0010 0110 1010 1100

06A2E 5D C7 EA 06 B5 C1 81 D1   ].......   0101 1101 1100 0111 1110 1010 0000 0110 1011 0101 1100 0001 1000 0001 1101 0001

06A36 80 28 10 04 08 44 05 F1   .(...D..   1000 0000 0010 1000 0001 0000 0000 0100 0000 1000 0100 0100 0000 0101 1111 0001

06A3E 1E 87 E0 2A 06 B5 C1 81   ...*....   0001 1110 1000 0111 1110 0000 0010 1010 0000 0110 1011 0101 1100 0001 1000 0001

06A46 D1 80 28 10 04 08 44 05   ..(...D.   1101 0001 1000 0000 0010 1000 0001 0000 0000 0100 0000 1000 0100 0100 0000 0101

06A4E F1 1E 87 E8 03 02 5A E2   ......Z.   1111 0001 0001 1110 1000 0111 1110 1000 0000 0011 0000 0010 0101 1010 1110 0010

06A56 89 80 68 0D 0F 09 03 C3   ..h.....   1000 1001 1000 0000 0110 1000 0000 1101 0000 1111 0000 1001 0000 0011 1100 0011

06A5E C3 C0 88 14 80 83 05 A8   ........   1100 0011 1100 0000 1000 1000 0001 0100 1000 0000 1000 0011 0000 0101 1010 1000

06A66 8A 9F 64 3F 27 E4 D4 CC   ..d?'...   1000 1010 1001 1111 0110 0100 0011 1111 0010 0111 1110 0100 1101 0100 1100 1100

06A6E CC CC CC CD C9 F9 01 34   .......4   1100 1100 1100 1100 1100 1100 1100 1101 1100 1001 1111 1001 0000 0001 0011 0100

06A76 88 4C DF DF 36 40 90 28   .L..6@.(   1000 1000 0100 1100 1101 1111 1101 1111 0011 0110 0100 0000 1001 0000 0010 1000

06A7E 0B 63 FF 51 18 1A 82 BF   .c.Q....   0000 1011 0110 0011 1111 1111 0101 0001 0001 1000 0001 1010 1000 0010 1011 1111

06A86 02 98 FF D4 46 06 A0 AF   ....F...   0000 0010 1001 1000 1111 1111 1101 0100 0100 0110 0000 0110 1010 0000 1010 1111

06A8E E4 04 00 00 00 00 00 00   ........   1110 0100 0000 0100 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

06A96 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

06A9E 00 01 05 EC C1 44 3E 02   .....D>.   0000 0000 0000 0001 0000 0101 1110 1100 1100 0001 0100 0100 0011 1110 0000 0010

06AA6 84 17                     ..         1000 0100 0001 0111

06AA8 C2 EA                     crc

The proxy flags for the class are 0x480.

Open Design Specification for .dwg files

199


#### 20.4.76 FIELD
Class properties:
App name
ObjectDBX Classes
Class number
Dynamic (>= 500)
DWG version
R18
Maintenance version
0
Class proxy flags
0x480
C++ class name
AcDbField
DXF name
FIELD
Fields are referenced from the field list of a drawing (paragraph 20.4.77).

Version
Field
type
DXF
group
code
Description

…

Common object data (paragraph 20.1).

TV
1
Evaluator ID

TV
2,3
Field code (in DXF strings longer than 255 characters are written in chunks of
255 characters in one 2 group and one or more 3 groups).

BL
90
Number of child fields



Begin repeat child fields

H
360
Child field handle (hard owner)



End repeat child fields

BL
97
Number of field objects



Begin repeat field objects

H
331
Field object handle (soft pointer)



End repeat field objects
-R2004
TV
4
Format string. After R2004 the format became part of the value object.
Common
BL
91
Evaluation option flags:
Never = 0,
On open = 1,
On save = 2,
On plot = 4,
When packed for eTransmit = 8,
On regeneration = 16,
On demand = 32

BL
92
Filing option flags:
None = 0,
Don’t file field result = 1

BL
94
Field state flags:
Unknown = 0,
Initialized = 1,
Compiled = 2,
Modified = 4,

Open Design Specification for .dwg files

200


Evaluated = 8,
Cached = 16

BL
95
Evaluation status flags:
Not evaluated = 1,
Success = 2,
Evaluator not found = 4,
Syntax error = 8,
Invalid code = 16,
Invalid context = 32,
Other error = 64

BL
96
Evaluation error code

TV
300
Evaluation error message

…
…
The field value, see paragraph 20.4.99.

TV
301, 9
Value string (DXF: written in 255 character chunks)

TV
98
Value string length

BL
93
Number of child fields



Begin repeat child fields

TV
6
Child field key

…
…
The field value, see paragraph 20.4.99.



End repeat child fields

#### 20.4.77 FIELDLIST
Class properties:
App name
ObjectDBX Classes
Class number
Dynamic (>= 500)
DWG version
R18
Maintenance version
0
Class proxy flags
0x480
C++ class name
AcDbFieldList, inherits AcDbIdSet
DXF name
FIELDLIST
Fields (paragraph 20.4.76) are referenced from the field list of a drawing. The field list is stored in the
root dictionary entry ACAD_FIELDLIST.

Version
Field
type
DXF
group
code
Description

…

Common object data (paragraph 20.1).

BL

Number of fields

B

Unknown



Begin repeat fields

Open Design Specification for .dwg files

201



H
330
Field handle (soft pointer)



End repeat fields
#### 20.4.78 GEODATA
Class properties:
App name
ObjectDBX Classes
Class number
Dynamic (>= 500)
DWG version
R21
Maintenance version
45
Class proxy flags
0xFFF
C++ class name
AcDbGeoData
DXF name
GEODATA
The geo data object was introduced in AutoCAD 2009. The format changed considerably in AutoCAD
2010. The objectVersion field discerns between the formats (1 = AutoCAD 2009, 2 = AutoCAD 2010, 3
= AutoCAD 2013, but the format is the same as 2010).

Version
Field
type
DXF
group
code
Description

…

Common object data (paragraph 20.1).

BL

Object version formats (1 = AutoCAD 2009, 2 = AutoCAD 2010, 3 =
AutoCAD 2013, but the format is the same as 2010)

H

Soft pointer to host block (model space layout owner block)

BS

Design coordinate type (0 = unknown, local grid = 1, projected grid = 2,
geographic (defined by latitude/longitude) = 3)



If version is AutoCAD 2010 or later

3BD

Design point

3BD

Reference point

BD

Unit scale factor horizontal

BL

Units value horizontal
Undefined = 0,
Inches = 1,
Feet = 2,
Miles = 3,
Millimeters = 4,
Centimeters = 5,
Meters = 6,
Kilometers = 7,
Micro inches = 8,
Mils = 9,
Yards = 10,
Angstroms = 11,
Nanometers = 12,

Open Design Specification for .dwg files

202


Microns = 13,
Decimeters = 14,
Dekameters = 15,
Hectometers = 16,
Gigameters = 17,
Astronomical = 18,
Light years = 19,
Parsecs = 20

BD

Unit scale factor vertical

BL

Units value vertical (same enumeration  as for the units value horizontal)

3BD

Up direction

3RD

North direction

BL

Scale estimation method:
None = 1,
User specified scale factor = 2,
Grid scale at reference point = 3,
Prismodial = 4

BD

User specified scale factor

B

Do sea level correction

BD

Sea level elevation

BD

Coordinate projection radius

VT

Coordinate system definition . In AutoCAD 2010 this is a map guide XML
string.

VT

Geo RSS tag.



Else (version is earlier than AutoCAD 2010)

3BD

Reference point

BL

Units value horizontal (see above for enum definition).

3BD

Design point

3BD

Obsolete, ODA writes (0, 0, 0)

3BD

Up direction

BD

Angle of north direction (radians, angle measured clockwise from the (0, 1)
vector).

3BD

Obsolete, ODA writes (1, 1, 1)

VT

Coordinate system definition. In AutoCAD 2009 this is a “Well known text”
(WKT) string containing a projected coordinate system (PROJCS).

VT

Geo RSS tag

BD

Unit scale factor horizontal

VT

Obsolete, coordinate system datum name

VT

Obsolete: coordinate system WKT



End if version is AutoCAD 2010 or later

VT

Observation from tag

VT

Observation to tag

VT

Observation coverage tag

BL

Number of geo mesh points

Open Design Specification for .dwg files

203





Repeat for each geo mesh point

2RD

Source point

2RD

Destination point



End repeat geo mesh points

BL

Number of geo mesh faces



Repeat for each geo mesh face

BL

Face index 1

BL

Face index 2

BL

Face index 3



End repeat geo mesh faces



If  DWG version is R21 or lower



Below is CIVIL data. AutoCAD 2010 always writes civil data.

B

Has civil data? (true)

B

False

RD

Reference point Y

RD

Reference point X

RD

Reference point Y

RD

Reference point X

BL

0

BL

0

2RD

(0, 0)

2RD

(0, 0)

B

false

BD

North direction angle (degrees)

BD

North direction angle (radians)

BL

Scale estimation method

BD

User specified scale factor

B

Do sea level correction

BD

Sea level elevation

BD

Coordinate projection radius



End if

#### 20.4.79 IDBUFFER (varies)
(holds list of references to an xref)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
typecode (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.

Open Design Specification for .dwg files

204


R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Unknown
RC

always 0?

Numobjids
BL

number of object ids

Handle refs
H

parenthandle (soft pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)



330
objids (soft pointer)
##### 20.4.79.1 Example:
OBJECT: proxy (1FAH), len 12H (18), handle: 8B

04437 12 00                     ..         0001 0010 0000 0000

04439 3E 80 40 62 E6 00 00 00   >.@b....   0011 1110 1000 0000 0100 0000 0110 0010 1110 0110 0000 0000 0000 0000 0000 0000

04441 04 04 01 01 80 41 8A 30   .....A.0   0000 0100 0000 0100 0000 0001 0000 0001 1000 0000 0100 0001 1000 1010 0011 0000

04449 41 89                     A.         0100 0001 1000 1001

0444B C9 64                     crc
#### 20.4.80 IMAGE (varies)

Common Entity Data

Classversion
BL
90
class version

pt0
3BD
10
insertion point

uvec
3BD
11
u direction vector

vvec
3BD
12
v direction vector

size
2RD
13
size of image

displayprops
BS
70
display properties (bit coded), 1==show image,
2==show image when not aligned with screen, 4==use
clipping boundary, 8==transparency on

clipping
B
280
1 if on

brightness
RC
281
brightness value (0—100, default 50)

contrast
RC
282
contrast value (0—100, default 50)

fade
RC
283
fade value (0—100, default 0)
R2010+:

Clip mode
B
290
0 = outside, 1 = inside
Common:

Open Design Specification for .dwg files

205



clipbndtype
BS
71
type of clipping boundary, 1==rect, 2==polygon
if (clipbndtype==1) {

pt0
2RD
14
first corner of clip boundary

pt1
2RD
14
second corner of clip boundary
}
else {

numclipverts
BL
91
number of vertices in clipping polygon
Repeat numclipverts times:

pt0
2RD
14
a point on the polygon
End repeat
}


Common Entity Handle Data


H

imagedef (hard pointer)


H

imagedefreactor (hard owner)

CRC
X
---
##### 20.4.80.1 Example:
OBJECT: proxy (1F9H), len 109H (265), handle: 6D

02D3E 09 01                     ..         0000 1001 0000 0001

02D40 3E 40 40 5B 6C 60 00 00   >@@[l`..   0011 1110 0100 0000 0100 0000 0101 1011 0110 1100 0110 0000 0000 0000 0000 0000

02D48 04 60 00 00 00 08 00 00   .`......   0000 0100 0110 0000 0000 0000 0000 0000 0000 0000 0000 1000 0000 0000 0000 0000

02D50 04 20 00 00 00 30 00 00   . ...0..   0000 0100 0010 0000 0000 0000 0000 0000 0000 0000 0011 0000 0000 0000 0000 0000

02D58 00 28 00 00 06 B5 6E 62   .(....nb   0000 0000 0010 1000 0000 0000 0000 0000 0000 0110 1011 0101 0110 1110 0110 0010

02D60 0B AA E1 02 00 03 72 C5   ......r.   0000 1011 1010 1010 1110 0001 0000 0010 0000 0000 0000 0011 0111 0010 1100 0101

02D68 63 F8 D8 AA 00 00 00 00   c.......   0110 0011 1111 1000 1101 1000 1010 1010 0000 0000 0000 0000 0000 0000 0000 0000

02D70 00 00 00 00 06 B5 6E 62   ......nb   0000 0000 0000 0000 0000 0000 0000 0000 0000 0110 1011 0101 0110 1110 0110 0010

02D78 0B AA E1 02 00 03 72 C5   ......r.   0000 1011 1010 1010 1110 0001 0000 0010 0000 0000 0000 0011 0111 0010 1100 0101

02D80 63 F8 D8 CA 00 00 00 00   c.......   0110 0011 1111 1000 1101 1000 1100 1010 0000 0000 0000 0000 0000 0000 0000 0000

02D88 00 00 00 00 06 B5 6E 62   ......nb   0000 0000 0000 0000 0000 0000 0000 0000 0000 0110 1011 0101 0110 1110 0110 0010

02D90 0B AA E1 12 00 03 72 C5   ......r.   0000 1011 1010 1010 1110 0001 0001 0010 0000 0000 0000 0011 0111 0010 1100 0101

02D98 63 F8 D8 CA 00 00 00 00   c.......   0110 0011 1111 1000 1101 1000 1100 1010 0000 0000 0000 0000 0000 0000 0000 0000

02DA0 00 00 00 00 06 B5 6E 62   ......nb   0000 0000 0000 0000 0000 0000 0000 0000 0000 0110 1011 0101 0110 1110 0110 0010

02DA8 0B AA E1 12 00 03 72 C5   ......r.   0000 1011 1010 1010 1110 0001 0001 0010 0000 0000 0000 0011 0111 0010 1100 0101

02DB0 63 F8 D8 AA 00 00 00 00   c.......   0110 0011 1111 1000 1101 1000 1010 1010 0000 0000 0000 0000 0000 0000 0000 0000

Open Design Specification for .dwg files

206



02DB8 00 00 00 00 06 B5 6E 62   ......nb   0000 0000 0000 0000 0000 0000 0000 0000 0000 0110 1011 0101 0110 1110 0110 0010

02DC0 0B AA E1 02 00 03 72 C5   ......r.   0000 1011 1010 1010 1110 0001 0000 0010 0000 0000 0000 0011 0111 0010 1100 0101

02DC8 63 F8 D8 AA 00 00 00 00   c.......   0110 0011 1111 1000 1101 1000 1010 1010 0000 0000 0000 0000 0000 0000 0000 0000

02DD0 00 00 00 00 06 D0 38 00   ......8.   0000 0000 0000 0000 0000 0000 0000 0000 0000 0110 1101 0000 0011 1000 0000 0000

02DD8 02 80 DB 46 B5 6E 62 0B   ...F.nb.   0000 0010 1000 0000 1101 1011 0100 0110 1011 0101 0110 1110 0110 0010 0000 1011

02DE0 AA E1 02 00 00 DC B1 58   .......X   1010 1010 1110 0001 0000 0010 0000 0000 0000 0000 1101 1100 1011 0001 0101 1000

02DE8 FE 36 2A 81 00 00 00 00   .6*.....   1111 1110 0011 0110 0010 1010 1000 0001 0000 0000 0000 0000 0000 0000 0000 0000

02DF0 00 00 10 07 F4 00 00 00   ........   0000 0000 0000 0000 0001 0000 0000 0111 1111 0100 0000 0000 0000 0000 0000 0000

02DF8 00 00 53 10 9E 00 00 00   ..S.....   0000 0000 0000 0000 0101 0011 0001 0000 1001 1110 0000 0000 0000 0000 0000 0000

02E00 00 00 00 10 07 F0 00 00   ........   0000 0000 0000 0000 0000 0000 0001 0000 0000 0111 1111 0000 0000 0000 0000 0000

02E08 00 00 00 03 02 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0011 0000 0010 0000 0000 0000 0000 0000 0000

02E10 00 00 00 03 02 02 0E 32   .......2   0000 0000 0000 0000 0000 0000 0000 0011 0000 0010 0000 0010 0000 1110 0011 0010

02E18 32 00 40 40 00 00 00 00   2.@@....   0011 0010 0000 0000 0100 0000 0100 0000 0000 0000 0000 0000 0000 0000 0000 0000

02E20 00 38 2F C0 00 00 00 00   .8/.....   0000 0000 0011 1000 0010 1111 1100 0000 0000 0000 0000 0000 0000 0000 0000 0000

02E28 00 38 2F C0 00 00 00 00   .8/.....   0000 0000 0011 1000 0010 1111 1100 0000 0000 0000 0000 0000 0000 0000 0000 0000

02E30 38 17 D0 00 00 00 00 00   8.......   0011 1000 0001 0111 1101 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

02E38 38 17 D0 10 5E CC 14 43   8...^..C   0011 1000 0001 0111 1101 0000 0001 0000 0101 1110 1100 1100 0001 0100 0100 0011

02E40 F0 41 68 43 54 5A CC 5B   .AhCTZ.[   1111 0000 0100 0001 0110 1000 0100 0011 0101 0100 0101 1010 1100 1100 0101 1011

02E48 3F                        ?          0011 1111

02E49 0D 2A                     crc
#### 20.4.81 IMAGEDEF (varies)
(used in conjunction with IMAGE entities)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
typecode (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj

Open Design Specification for .dwg files

207


R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Clsver
BL
0
class version

Imgsize
2RD
10
size of image in pixels

Filepath
TV
1
path to file

Isloaded
B
280
0==no, 1==yes

Resunits
RC
281
0==none, 2==centimeters, 5==inches

Pixelsize
2RD
11
size of one pixel in AutoCAD units

Handle refs
H

parenthandle (hard owner)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)
##### 20.4.81.1 Example:
OBJECT: proxy (1F7H), len 4EH (78), handle: 6B

04349 4E 00                     N.         0100 1110 0000 0000

0434B 3D C0 40 5A E3 B0 20 00   =.@Z.. .   0011 1101 1100 0000 0100 0000 0101 1010 1110 0011 1011 0000 0010 0000 0000 0000

04353 04 0A 00 00 00 00 00 00   ........   0000 0100 0000 1010 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

0435B 60 40 00 00 00 00 00 00   `@......   0110 0000 0100 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

04363 60 40 46 D0 CE 97 15 D2   `@F.....   0110 0000 0100 0000 0100 0110 1101 0000 1100 1110 1001 0111 0001 0101 1101 0010

0436B 53 93 95 17 11 99 58 5D   S.....X]   0101 0011 1001 0011 1001 0101 0001 0111 0001 0001 1001 1001 0101 1000 0101 1101

04373 1A 19 5C 95 19 5E 1D 1D   ..\..^..   0001 1010 0001 1001 0101 1100 1001 0101 0001 1001 0101 1110 0001 1101 0001 1101

0437B 5C 99 4B 98 9B 5C 20 5E   \.K..\ ^   0101 1100 1001 1001 0100 1011 1001 1000 1001 1011 0101 1100 0010 0000 0101 1110

04383 25 D4 EB 07 52 BA C7 FE   %...R...   0010 0101 1101 0100 1110 1011 0000 0111 0101 0010 1011 1010 1100 0111 1111 1110

0438B 25 D4 EB 07 52 BA C7 F0   %...R...   0010 0101 1101 0100 1110 1011 0000 0111 0101 0010 1011 1010 1100 0111 1111 0000

04393 08 2D 48 2D 86 11         .-H-..     0000 1000 0010 1101 0100 1000 0010 1101 1000 0110 0001 0001

04399 E8 23                     crc
#### 20.4.82 IMAGEDEFREACTOR (varies)
(used in conjunction with IMAGE entities)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
typecode (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

Open Design Specification for .dwg files

208



EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Classver
BL
90
class version

Handle refs
H

parenthandle (soft pointer)




[Reactors (soft pointer])




xdicobjhandle (hard owner)
##### 20.4.82.1 Example:
OBJECT: proxy (1F8H), len CH (12), handle: 6C



02E4B 0C 00                     ..         0000 1100 0000 0000



02E4D 3E 00 40 5B 25 00 00 00   >.@[%...   0011 1110 0000 0000 0100 0000 0101 1011 0010 0101 0000 0000 0000 0000 0000 0000

02E55 09 02 60 30               ..`0       0000 1001 0000 0010 0110 0000 0011 0000

02E59 A1 13                     crc
#### 20.4.83 LAYER_INDEX

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
typecode (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.

Open Design Specification for .dwg files

209


Common:

timestamp1
BL
40

timestamp2
BL
40

numentries
BL

the number of entries
Repeat numentries times:

Indexlong
BL

a long

Indexstr
TV
8
a layer name
End repeat


Handle refs
H

parenthandle (soft pointer)




[Reactors (soft pointer])




xdicobjhandle (hard owner)




entry handles, 1 per entry
20.4.83.1
Example:
OBJECT: proxy (1FFH), len 59H (89), handle: 01 F8




0D1CD 59 00                     Y.         0101 1001 0000 0000

0D1CF 3F C0 40 80 7E 20 C0 20   ?.@.~ .    0011 1111 1100 0000 0100 0000 1000 0000 0111 1110 0010 0000 1100 0000 0010 0000

0D1D7 00 04 04 61 65 25 00 3B   ...ae%.;   0000 0000 0000 0100 0000 0100 0110 0001 0110 0101 0010 0101 0000 0000 0011 1011

0D1DF 3A 89 80 90 64 DD 01 30   :...d..0   0011 1010 1000 1001 1000 0000 1001 0000 0110 0100 1101 1101 0000 0001 0011 0000

0D1E7 42 50 64 15 34 84 14 44   BPd.4..D   0100 0010 0101 0000 0110 0100 0001 0101 0011 0100 1000 0100 0001 0100 0100 0100

0D1EF 54 05 08 55 52 4C 4C 41   T..URLLA   0101 0100 0000 0101 0000 1000 0101 0101 0101 0010 0100 1100 0100 1100 0100 0001

0D1F7 59 45 52 90 94 44 54 65   YER..DTe   0101 1001 0100 0101 0101 0010 1001 0000 1001 0100 0100 0100 0101 0100 0110 0101

0D1FF 04 F4 94 E5 45 34 1D 03   ....E4..   0000 0100 1111 0100 1001 0100 1110 0101 0100 0101 0011 0100 0001 1101 0000 0011

0D207 52 45 44 41 10 44 24 C5   REDA.D$.   0101 0010 0100 0101 0100 0100 0100 0001 0001 0000 0100 0100 0010 0100 1100 0101

0D20F 54 58 04 20 1F 73 03 20   TX. .s.    0101 0100 0101 1000 0000 0100 0010 0000 0001 1111 0111 0011 0000 0011 0010 0000

0D217 1F A3 20 1F B3 20 1F C3   .. .. ..   0001 1111 1010 0011 0010 0000 0001 1111 1011 0011 0010 0000 0001 1111 1100 0011

0D21F 20 1F D3 20 1F E3 20 1F    .. .. .   0010 0000 0001 1111 1101 0011 0010 0000 0001 1111 1110 0011 0010 0000 0001 1111

0D227 FE                        .          1111 1110

0D228 46 E8                     crc
#### 20.4.84 LAYOUT (varies)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
typecode (internal DWG type code).
R2000+:

Open Design Specification for .dwg files

210



Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Page setup name
TV
1
plotsettings page setup name

Printer/Config
TV
2
plotsettings printer or configuration file

Plot layout flags
BS
70
plotsettings plot layout flag

Left Margin
BD
40
plotsettings left margin in millimeters

Bottom Margin
BD
41
plotsettings bottom margin in millimeters

Right Margin
BD
42
plotsettings right margin in millimeters

Top Margin
BD
43
plotsettings top margin in millimeters

Paper Width
BD
44
plotsettings paper width in millimeters

Paper Height
BD
45
plotsettings paper height in millimeters

Paper Size
TV
4
plotsettings paper size

Plot origin
2BD
46,47
plotsettings origin offset in millimeters

Paper units
BS
72
plotsettings plot paper units

Plot rotation
BS
73
plotsettings plot rotation

Plot type
BS
74
plotsettings plot type

Window min
2BD
48,49
plotsettings plot window area lower left

Window max
2BD 140,141
plotsettings plot window area upper right
R13-R2000 Only:

Plot view name
T
6
plotsettings plot view name
Common:

Real world units
BD
142
plotsettings numerator of custom print scale

Drawing units
BD
143
plotsettings denominator of custom print scale

Current style sheet
TV
7
plotsettings current style sheet

Scale type
BS
75
plotsettings standard scale type

Scale factor
BD
147
plotsettings scale factor

Paper image origin
2BD 148,149
plotsettings paper image origin
R2004+:

Shade plot mode
BS
76

Shade plot res. Level BS
77

Open Design Specification for .dwg files

211



Shade plot custom DPI BS
78
Common:

Layout name
TV
1
layout name

Tab order
BL
71
layout tab order

Flag
BS
70
layout flags

Ucs origin
3BD
13
layout ucs origin

Limmin
2RD
10
layout minimum limits

Limmax
2RD
11
layout maximum limits

Inspoint
3BD
12
layout insertion base point

Ucs x axis
3BD
16
layout ucs x axis direction

Ucs y axis
3BD
17
layout ucs y axis direction

Elevation
BD
146
layout elevation

Orthoview type
BS
76
layout orthographic view type of UCS

Extmin
3BD
14
layout extent min

Extmax
3BD
15
layout extent max
R2004+:

Viewport count
RL

# of viewports in this layout
Common:

Handle refs
H

parenthandle (soft pointer)




[Reactors (soft pointer])




xdicobjhandle (hard owner)
R2004+:



6
plot view handle (hard pointer)
R2007+:




Visual Style handle (soft pointer)
Common:



330
associated paperspace block record handle (soft
pointer)



331
last active viewport handle (soft pointer)



346
base ucs handle (hard pointer)



345
named ucs handle (hard pointer)
R2004+:




Viewport handle (repeats Viewport count times) (soft
pointer)
#### 20.4.85 LWPLINE (varies)

Common Entity Data

Flag
BS
70
if (flag & 4) {

constwidth
BD
43
Constant width for this lwpline
}

Open Design Specification for .dwg files

212


if (flag & 8) {

elevation
BD
38
Elevation of this lwpline
}
if (flag & 2) {

thickness
BD
39
thickness of this lwpline
}
if (flag & 1) {

normal
3BD
210
extrusion direction
}

numpoints
BL
90
number of verts
if (flag & 16) {

numbulges
BL

number of bulges (when present, always same as
number of verts in all examples so fa)r
}
R2010+:
If (flag & 1024) {

vertexIdCount
BL

number of vertex identifiers (when present, always
the same as number of vertes).
}
if (flag & 32) {

numwidths
BL

number of width entries (when present, always same
as number of verts in all examples so far.
}
R13-R14 Only:
repeat numpoints times

pt0
2RD
10
vertex location
end repeat
R2000+:

pt0
2RD
10
first vertex
repeat numpoints-1 times

x
DD
10
use previous point x value for default

y
DD
20
use previous point y value for default
end repeat
Common:
repeat numbulges times

bulge
BD
42
bulge value
end repeat
repeat vertexIdCount times

vertex id
BL
91
The vertex identifier
end repeat
repeat numwidths times

Open Design Specification for .dwg files

213



widths
2BD
40/41
start, end widths
end repeat

Common Entity Handle Data
##### 20.4.85.1 Example:
OBJECT: proxy (1FBH), len C8H (200), handle: 01 0F

03E52 C8 00                     ..         1100 1000 0000 0000

03E54 3E C0 40 80 43 D0 35 20   >.@.C.5    0011 1110 1100 0000 0100 0000 1000 0000 0100 0011 1101 0000 0011 0101 0010 0000

03E5C 10 94 60 10 08 2A 0C 00   ..`..*..   0001 0000 1001 0100 0110 0000 0001 0000 0000 1000 0010 1010 0000 1100 0000 0000

03E64 00 5E A0 20 80 12 14 85   .^. ....   0000 0000 0101 1110 1010 0000 0010 0000 1000 0000 0001 0010 0001 0100 1000 0101

03E6C 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

03E74 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

03E7C 00 00 00 00 00 00 14 A0   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001 0100 1010 0000

03E84 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

03E8C 00 00 00 00 00 00 14 A0   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001 0100 1010 0000

03E94 00 00 00 00 00 00 78 1F   ......x.   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0111 1000 0001 1111

03E9C 80 00 00 00 00 40 23 20   .....@#    1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0100 0000 0010 0011 0010 0000

03EA4 00 00 00 00 00 00 78 1F   ......x.   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0111 1000 0001 1111

03EAC 80 00 00 00 00 40 23 20   .....@#    1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0100 0000 0010 0011 0010 0000

03EB4 00 00 00 00 00 00 00 20   .......    0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0010 0000

03EBC 00 00 00 00 00 40 23 20   .....@#    0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0100 0000 0010 0011 0010 0000

03EC4 00 00 00 00 00 00 1E 20   .......    0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001 1110 0010 0000

03ECC 00 00 00 00 00 40 23 20   .....@#    0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0100 0000 0010 0011 0010 0000

03ED4 00 00 00 00 00 00 1E A0   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001 1110 1010 0000

03EDC 00 00 00 00 00 00 14 A0   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001 0100 1010 0000

03EE4 00 00 00 00 00 00 1E A0   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001 1110 1010 0000

03EEC 00 00 00 00 00 00 14 A0   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001 0100 1010 0000

03EF4 00 00 00 00 00 00 1F 20   .......    0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001 1111 0010 0000

03EFC 00 00 00 00 00 00 00 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

03F04 00 00 00 00 00 00 1F 20   .......    0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001 1111 0010 0000

03F0C 55 1F FF FF FF FF FF FD   U.......   0101 0101 0001 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111 1101

03F14 F7 F5 56 08 19 82 88 7A   ..V....z   1111 0111 1111 0101 0101 0110 0000 1000 0001 1001 1000 0010 1000 1000 0111 1010

03F1C 85 93                     crc

Open Design Specification for .dwg files

214


#### 20.4.86 MLeaderAnnotContext
This is a helper class for the multileader entity (see paragraph 20.4.48), that inherits from class
AcDbAnnotScaleObjectContextData (see paragraph 20.4.71).
This object mainly contains a content object, which is either a block or multiline text. To the content
object one or two leader roots are attached. They are either attached to the left/right or top/bottom
depending on the multileaders attachment direction (horizontal/vertical). Each leader root can contain one
more leader lines.
Version
Field
type
DXF
group
code
Description

…

Common AcDbAnnotScaleObjectContextData data (see paragraph 20.4.71).


300
DXF: “CONTEXT_DATA{“

BL
-
Number of leader roots



Begin repeat leader root


302
DXF: “LEADER{“

B
290
Is content valid (ODA writes true)

B
291
Unknown (ODA writes true)

3BD
10
Connection point

3BD
11
Direction

BL

Number of break start/end point pairs



Begin repeat break start/end point pairs

3BD
12
Break start point

3BD
13
Break end point



End repeat break start/end point pairs

BL
90
Leader index

BD
40
Landing distance

BL

Number of leader lines



Begin repeat leader lines


304
DXF: “LEADER_LINE{“

BL
-
Number of points



Begin repeat points

3BD
10
Point



End repeat points

BL

Break info count

BL
90
Segment index

BL

Start/end point pair count



Begin repeat start/end point pairs

3BD
11
Start Point

3BD
12
End point



End repeat start/end point pairs

BL
91
Leader line index.
R2010




Open Design Specification for .dwg files

215



BS
170
Leader type (0 = invisible leader, 1 = straight leader, 2 = spline leader)

CMC
92
Line color

H
340
Line type handle (hard pointer)

BL
171
Line weight

BD
40
Arrow size

H
341
Arrow symbol handle (hard pointer)

BL
93
Override flags (1 = leader type, 2 = line color, 4 = line type, 8 = line weight, 16
= arrow size, 32 = arrow symbol (handle)
Common




-
305
DXF: “}”



End repeat leader lines
R2010




BS
271
Attachment direction  (0 = horizontal, 1 = vertical, default is 0)

-
303
DXF: “}”



End repeat leader root
Common




BD
40
Overall scale

3BD
10
Content base point

BD
41
Text height

BD
140
Arrow head size

BD
145
Landing gap

BS
174
Style left text attachment type. See also MLEADER style left text attachment
type for values. Relevant if mleader attachment direction is horizontal.

BS
175
Style right text attachment type. See also MLEADER style left text attachment
type for values. Relevant if mleader attachment direction is horizontal.

BS
176
Text align type (0 = left, 1 = center, 2 = right)

BS
177
Attachment type (0 = content extents, 1 = insertion point).

B
290
Has text contents



IF Has text contents

TV
304
Text label

3BD
11
Normal vector

H
340
Text style handle (hard pointer)

3BD
12
Location

3BD
13
Direction

BD
42
Rotation (radians)

BD
43
Boundary width

BD
44
Boundary height

BD
45
Line spacing factor

BS
170
Line spacing style (1 = at least, 2 = exactly)

CMC
90
Text color

BS
171
Alignment (1 = left, 2 = center, 3 = right)

BS
172
Flow direction (1 = horizontal, 3 = vertical, 6 = by style)

CMC
91
Background fill color

BD
141
Background scale factor

Open Design Specification for .dwg files

216



BL
92
Background transparency

B
291
Is background fill enabled

B
292
Is background mask fill on

BS
173
Column type (ODA writes 0), *TODO: what meaning for values?

B
293
Is text height automatic?

BD
142
Column width

BD
143
Column gutter

B
294
Column flow reversed

BL

Column sizes count



Begin repeat column sizes

BD
144
Column size



End repeat column sizes

B
295
Word break

B

Unknown



ELSE (Has text contents)

B
296
Has contents block



IF Has contents block

H
341
AcDbBlockTableRecord handle (soft pointer)

3BD
14
Normal vector

3BD
15
Location

3BD
16
Scale vector

BD
46
Rotation (radians)

CMC
93
Block color

BD (16)
47
16 doubles containg the complete transformation matrix. Order of
transformation is:

Rotation,

OCS to WCS (using normal vector),

Scaling (using scale vector),

Translation (using location)



END IF Has contents block



END IF Has text contents

3BD
110
Base point

3BD
111
Base direction

3BD
112
Base vertical

B
297
Is normal reversed?
R2010




BS
273
Style top attachment. See also MLEADER style left text attachment type for
values. Relevant if mleader attachment direction is vertical.

BS
272
Style bottom attachment. See also MLEADER style left text attachment type
for values. Relevant if mleader attachment direction is vertical.

-
301
DXF: “}”

Open Design Specification for .dwg files

217


#### 20.4.87 MLEADERSTYLE (AcDbMLeaderStyle)
This class inherits from AcDbObject. The provides a style for the MLEADER entity (see
paragraph 20.4.48).
The value of IsNewFormat is true in case the version is R2010 or later, or if the object has extended data
for APPID “ACAD_MLEADERVER”.
Version
Field
type
DXF
group
code
Description

…

Common object data (paragraph 20.1).
R2010




BS
179
Version (expected to have value 2)
Common




BS
170
Content type (see paragraph on LEADER for more details).

BS
171
Draw multi-leader order (0 = draw content first, 1 = draw leader first)

BS
172
Draw leader order (0 = draw leader head first, 1 = draw leader tail first)

BL
90
Maximum number of points for leader

BD
40
First segment angle (radians)

BD
41
Second segment angle (radians)

BS
173
Leader type (see paragraph on LEADER for more details).

CMC
91
Leader line color

H
340
Leader line type handle (hard pointer)

BL
92
Leader line weight

B
290
Is landing enabled?

BD
42
Landing gap

B
291
Auto include landing (is dog-leg enabled?)

BD
43
Landing distance

TV
3
Style description

H
341
Arrow head block handle (hard pointer)

BD
44
Arrow head size

TV
300
Text default

H
342
Text style handle (hard pointer)

BS
174
Left attachment (see paragraph on LEADER for more details).

BS
178
Right attachment (see paragraph on LEADER for more details).



IF IsNewFormat OR DXF file

BS
175
Text angle type (see paragraph on LEADER for more details).



END IF IsNewFormat OR DXF file

BS
176
Text alignment type

CMC
93
Text color

BD
45
Text height

B
292
Text frame enabled



IF IsNewFormat OR DXF file

B
297
Always align text left

Open Design Specification for .dwg files

218





END IF IsNewFormat OR DXF file

BD
46
Align space

H
343
Block handle (hard pointer)

CMC
94
Block color

3BD
47,
49,
140
Block scale vector

B
293
Is block scale enabled

BD
141
Block rotation (radians)

B
294
Is block rotation enabled

BS
177
Block connection type (0 = MLeader connects to the block extents, 1 =
MLeader connects to the block base point)

BD
142
Scale factor

B
295
Property changed, meaning not totally clear, might be set to true if something
changed after loading, or might be used to trigger updates in dependent
MLeaders.

B
296
Is annotative?

BD
143
Break size
R2010+




BS
271
Attachment direction (see paragraph on LEADER for more details).

BS
273
Top attachment (see paragraph on LEADER for more details).

BS
272
Bottom attachment (see paragraph on LEADER for more details).
#### 20.4.88 OLE2FRAME (varies)

Common Entity Data

Flags
BS
70
R2000+:

Mode
BS
Common:

Data Length
BL
--
Bit-pair-coded long giving the length of the data
section that follows.

Unknown data
-
--
The OLE2 data.
R2000+:

Unknown
RC
Common:

Common Entity Handle Data

CRC
X
---
##### 20.4.88.1 <<No example>>
#### 20.4.89 AcDbObjectContextData
This class inherits from AcDbObject. The object provides contextual data for another object/entity.

Open Design Specification for .dwg files

219


Version
Field
type
DXF
group
code
Description

…

Common object data (paragraph 20.1).
R2010




BS
70
Version (default value is 3).

B
-
Has file to extension dictionary (default value is true).

B
290
Default flag (default value is false).

#### 20.4.90 PROXY (varies):

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
typecode (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
R2000+:

Class ID
BL
91
Before R2018:

Object Drawing Format BL
95
This is a bitwise OR of the version and the
maintenance version, shifted 16 bits to the left.
R2018+:

Version
BL
71
The AutoCAD version of the object.

Maintenance version
BL
97
The AutoCAD maintenance version of the object.
R2000+:

Original Data Format
B
70
0 for dwg, 1 for dxf
Common:

Databits
X

databits, however many there are to the handles

Handle refs
H

parenthandle (soft pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)

Open Design Specification for .dwg files

220






objid object handles, as many as we can read until
we run out of data.  These are TYPEDOBJHANDLEs.
##### 20.4.90.1 <<No example>>
#### 20.4.91 RASTERVARIABLES (varies)
(used in conjunction with IMAGE entities)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
typecode (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Classver
BL
90
classversion

Dispfrm
BS
70
displayframe

Dispqual
BS
71
display quality

Units
BS
72
units

Handle refs
H

parenthandle (soft pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)
##### 20.4.91.1 Example:
OBJECT: proxy (1F5H), len 11H (17), handle: 5A

0CD78 11 00                     ..         0001 0001 0000 0000

0CD7A 3D 40 40 56 A6 60 00 00   =@@V.`..   0011 1101 0100 0000 0100 0000 0101 0110 1010 0110 0110 0000 0000 0000 0000 0000

0CD82 04 06 40 50 19 01 04 30   ..@P...0   0000 0100 0000 0110 0100 0000 0101 0000 0001 1001 0000 0001 0000 0100 0011 0000

0CD8A C0                        .          1100 0000

0CD8B DC D2                     crc

Open Design Specification for .dwg files

221


#### 20.4.92 SCALE (AcDbScale)
This class inherits from AcDbObject. This represents a ratio of paper units to drawing units, where the
drawing units are divided by 10 when using the same distance units (e.g. mm). E.g. a scale of 1 mm to 10
mm is stored as paper units = 1, drawing units = 1. A scale of 1 mm to 1000 mm (= 1 m) is stored as
paper units = 1, drawing units = 100.

Version
Field
type
DXF
group
code
Description

…

Common object data (see paragraph 20.1.

BS
70
Unknown (ODA writes 0).

TV
300
Name

BD
140
Paper units (numerator)

BD
141
Drawing units (denominator, divided by 10).

B
290
Has unit scale

#### 20.4.93 SORTENTSTABLE (varies)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
typecode (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Numentries
BL

number of entries

Sorthandle
H

Sort handle (numentries of these, CODE 0, i.e. part
of the main bit stream, not of the handle bit
stream!). The sort handle does not have to point to
an entity (but it can). This is just the handle used
for determining the drawing order of the entity
specified by the entity handle in the handle bit
stream. When the sortentstable doesn’t have a

Open Design Specification for .dwg files

222


mapping from entity handle to sort handle, then the
entity’s own handle is used for sorting.

Handle refs
H

parenthandle (soft pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)




owner handle (soft pointer)




handles of entities (numentries of these, soft
pointer)
##### 20.4.93.1 Example:
OBJECT: proxy (1FAH), len 59H (89), handle: A5

0D015 59 00                     Y.         0101 1001 0000 0000

0D017 3E 80 40 69 67 80 10 00   >.@ig...   0011 1110 1000 0000 0100 0000 0110 1001 0110 0111 1000 0000 0001 0000 0000 0000

0D01F 04 05 12 01 6E 01 68 01   ....n.h.   0000 0100 0000 0101 0001 0010 0000 0001 0110 1110 0000 0001 0110 1000 0000 0001

0D027 6C 01 5E 01 53 01 6A 01   l.^.S.j.   0110 1100 0000 0001 0101 1110 0000 0001 0101 0011 0000 0001 0110 1010 0000 0001

0D02F 60 01 95 01 58 01 A6 01   `...X...   0110 0000 0000 0001 1001 0101 0000 0001 0101 1000 0000 0001 1010 0110 0000 0001

0D037 6F 01 6D 01 54 01 6B 01   o.m.T.k.   0110 1111 0000 0001 0110 1101 0000 0001 0101 0100 0000 0001 0110 1011 0000 0001

0D03F 56 01 69 01 76 01 55 40   V.i.v.U@   0101 0110 0000 0001 0110 1001 0000 0001 0111 0110 0000 0001 0101 0101 0100 0000

0D047 41 A4 30 41 19 41 6D 41   A.0A.AmA   0100 0001 1010 0100 0011 0000 0100 0001 0001 1001 0100 0001 0110 1101 0100 0001

0D04F 60 41 6B 41 56 41 A6 41   `AkAVA.A   0110 0000 0100 0001 0110 1011 0100 0001 0101 0110 0100 0001 1010 0110 0100 0001

0D057 69 41 58 41 76 41 54 41   iAXAvATA   0110 1001 0100 0001 0101 1000 0100 0001 0111 0110 0100 0001 0101 0100 0100 0001

0D05F 95 41 6E 41 6C 41 55 41   .AnAlAUA   1001 0101 0100 0001 0110 1110 0100 0001 0110 1100 0100 0001 0101 0101 0100 0001

0D067 6A 41 53 41 68 41 6F 41   jASAhAoA   0110 1010 0100 0001 0101 0011 0100 0001 0110 1000 0100 0001 0110 1111 0100 0001

0D06F 5E                        ^          0101 1110

0D070 D3 A5                     crc
#### 20.4.94 SPATIAL_FILTER (varies)
(used to clip external references)

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
typecode (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Open Design Specification for .dwg files

223



Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Numpts
BS
70
number of points  /* really long? */

Repeat numpts times:

pt0
2RD
10
a point on the clip boundary
End repeat


Extrusion
3BD
210
extrusion

Clipbdorg
3BD
10
clip bound origin

Dispbound
BS
71
display boundary

Frontclipon
BS
72
1 if front clip on

Frontdist
BD
40
front clip dist (present if frontclipon==1)

Backclipon
BS
73
1 if back clip on

Backdist
BD
41
back clip dist (present if backclipon==1)

Invblktr
12BD
40
inverse block transformation matrix




(double [4][3], column major order)

clipbdtr
12BD
40
clip bound transformation matrix




(double [4][3], column major order)

Handle refs
H

parenthandle (soft pointer)




[Reactors (soft pointer)]




xdicobjhandle (hard owner)
##### 20.4.94.1 Example:
OBJECT: proxy (1FDH), len 7BH (123), handle: 02 15

0D68A 7B 00                     {.         0111 1011 0000 0000

0D68C 3F 40 40 80 85 6A A0 30   ?@@..j.0   0011 1111 0100 0000 0100 0000 1000 0000 1000 0101 0110 1010 1010 0000 0011 0000

0D694 00 04 05 05 96 EA 02 5E   .......^   0000 0000 0000 0100 0000 0101 0000 0101 1001 0110 1110 1010 0000 0010 0101 1110

0D69C 66 70 2E 40 3A AF B1 4B   fp.@:..K   0110 0110 0111 0000 0010 1110 0100 0000 0011 1010 1010 1111 1011 0001 0100 1011

0D6A4 54 7F 16 40 27 E0 D7 48   T..@'..H   0101 0100 0111 1111 0001 0110 0100 0000 0010 0111 1110 0000 1101 0111 0100 1000

0D6AC 12 9C 30 40 4A F2 5C DF   ..0@J.\.   0001 0010 1001 1100 0011 0000 0100 0000 0100 1010 1111 0010 0101 1100 1101 1111

0D6B4 87 03 14 40 B5 AB 90 F2   ...@....   1000 0111 0000 0011 0001 0100 0100 0000 1011 0101 1010 1011 1001 0000 1111 0010

0D6BC 93 F6 31 40 82 75 1C 3F   ..1@.u.?   1001 0011 1111 0110 0011 0001 0100 0000 1000 0010 0111 0101 0001 1100 0011 1111

0D6C4 54 3A 17 40 75 79 73 B8   T:.@uys.   0101 0100 0011 1010 0001 0111 0100 0000 0111 0101 0111 1001 0111 0011 1011 1000


Open Design Specification for .dwg files

224


0D6CC 56 D7 32 40 EF 3D 5C 72   V.2@.=\r   0101 0110 1101 0111 0011 0010 0100 0000 1110 1111 0011 1101 0101 1100 0111 0010

0D6D4 DC 11 20 40 74 94 83 D9   .. @t...   1101 1100 0001 0001 0010 0000 0100 0000 0111 0100 1001 0100 1000 0011 1101 1001

0D6DC 04 00 2E 40 E7 DF 2E FB   ...@....   0000 0100 0000 0000 0010 1110 0100 0000 1110 0111 1101 1111 0010 1110 1111 1011

0D6E4 75 A7 20 40 A6 A4 06 9A   u. @....   0111 0101 1010 0111 0010 0000 0100 0000 1010 0110 1010 0100 0000 0110 1001 1010

0D6EC 0F 88 C4 46 B0 5D 8A 70   ...F.].p   0000 1111 1000 1000 1100 0100 0100 0110 1011 0000 0101 1101 1000 1010 0111 0000

0D6F4 26 06 E1 49 2C DE A1 C0   &..I,...   0010 0110 0000 0110 1110 0001 0100 1001 0010 1100 1101 1110 1010 0001 1100 0000

0D6FC 70 29 9A A6 A9 90 10 80   p)......   0111 0000 0010 1001 1001 1010 1010 0110 1010 1001 1001 0000 0001 0000 1000 0000

0D704 85 0C 10                  ...        1000 0101 0000 1100 0001 0000

0D707 07 5E                     crc
#### 20.4.95 SPATIAL_INDEX (varies):

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
typecode (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

timestamp1
BL

timestamp2
BL

unknown
X

rest of bits to handles

Handle refs
H

parenthandle (hard owner)




[Reactors (soft pointer)]




xdictionary (hard owner)
##### 20.4.95.1 Example:
OBJECT: proxy (200H), len 406H (1030), handle: 01 F9

0D280 06 04                     ..         0000 0110 0000 0100

0D282 00 00 80 80 7E 63 A1 F0   ....~c..   0000 0000 0000 0000 1000 0000 1000 0000 0111 1110 0110 0011 1010 0001 1111 0000


Open Design Specification for .dwg files

225


0D28A 00 04 04 61 65 25 00 3B   ...ae%.;   0000 0000 0000 0100 0000 0100 0110 0001 0110 0101 0010 0101 0000 0000 0011 1011

0D292 3A 89 80 88 F8 D8 33 54   :.....3T   0011 1010 1000 1001 1000 0000 1000 1000 1111 1000 1101 1000 0011 0011 0101 0100

0D29A 4E 3A 94 10 02 D6 3C 73   N:....<s   0100 1110 0011 1010 1001 0100 0001 0000 0000 0010 1101 0110 0011 1100 0111 0011

0D2A2 98 D3 04 FC 1F CD 85 40   .......@   1001 1000 1101 0011 0000 0100 1111 1100 0001 1111 1100 1101 1000 0101 0100 0000

0D2AA 69 D4 B2 41 18 08 F6 18   i..A....   0110 1001 1101 0100 1011 0010 0100 0001 0001 1000 0000 1000 1111 0110 0001 1000

0D2B2 FB 39 79 2F C4 29 C3 30   .9y/.).0   1111 1011 0011 1001 0111 1001 0010 1111 1100 0100 0010 1001 1100 0011 0011 0000

0D2BA E2 0C 6C 84 10 00 00 89   ..l.....   1110 0010 0000 1100 0110 1100 1000 0100 0001 0000 0000 0000 0000 0000 1000 1001

0D2C2 17 FE A4 92 FC 25 03 00   .....%..   0001 0111 1111 1110 1010 0100 1001 0010 1111 1100 0010 0101 0000 0011 0000 0000

0D2CA 00 01 00 00 00 FF FF 00   ........   0000 0000 0000 0001 0000 0000 0000 0000 0000 0000 1111 1111 1111 1111 0000 0000

0D2D2 00 FF FF 00 00 FF FF 01   ........   0000 0000 1111 1111 1111 1111 0000 0000 0000 0000 1111 1111 1111 1111 0000 0001

0D2DA 00 00 04 58 00 D4 08 00   ...X....   0000 0000 0000 0000 0000 0100 0101 1000 0000 0000 1101 0100 0000 1000 0000 0000

0D2E2 00 01 08 00 00 FE 8F 00   ........   0000 0000 0000 0001 0000 1000 0000 0000 0000 0000 1111 1110 1000 1111 0000 0000

0D2EA 00 FE 8F 00 00 FE 8F 00   ........   0000 0000 1111 1110 1000 1111 0000 0000 0000 0000 1111 1110 1000 1111 0000 0000

0D2F2 00 01 08 00 00 FE 50 00   ......P.   0000 0000 0000 0001 0000 1000 0000 0000 0000 0000 1111 1110 0101 0000 0000 0000

0D2FA 00 FE 50 00 00 FE 50 03   ..P...P.   0000 0000 1111 1110 0101 0000 0000 0000 0000 0000 1111 1110 0101 0000 0000 0011

0D302 00 00 09 56 00 8B 01 00   ...V....   0000 0000 0000 0000 0000 1001 0101 0110 0000 0000 1000 1011 0000 0001 0000 0000

0D30A 36 00 00 08 00 00 02 01   6.......   0011 0110 0000 0000 0000 0000 0000 1000 0000 0000 0000 0000 0000 0010 0000 0001

0D312 09 00 3F FE 8F 00 00 FE   ..?.....   0000 1001 0000 0000 0011 1111 1111 1110 1000 1111 0000 0000 0000 0000 1111 1110

0D31A 50 00 00 FE 50 02 00 00   P...P...   0101 0000 0000 0000 0000 0000 1111 1110 0101 0000 0000 0010 0000 0000 0000 0000

0D322 07 E2 01 00 33 00 36 00   ....3.6.   0000 0111 1110 0010 0000 0001 0000 0000 0011 0011 0000 0000 0011 0110 0000 0000

0D32A 00 00 02 01 0A 00 00 FE   ........   0000 0000 0000 0000 0000 0010 0000 0001 0000 1010 0000 0000 0000 0000 1111 1110

0D332 50 00 3F FE 8F 00 00 FE   P.?.....   0101 0000 0000 0000 0011 1111 1111 1110 1000 1111 0000 0000 0000 0000 1111 1110

0D33A 50 03 00 00 09 DE 01 00   P.......   0101 0000 0000 0011 0000 0000 0000 0000 0000 1001 1101 1110 0000 0001 0000 0000

0D342 13 00 22 00 00 00 00 00   ..".....   0001 0011 0000 0000 0010 0010 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

0D34A 02 01 0B 00 3F FE 8F 00   ....?...   0000 0010 0000 0001 0000 1011 0000 0000 0011 1111 1111 1110 1000 1111 0000 0000

0D352 3F FE 8F 00 00 FE 50 04   ?.....P.   0011 1111 1111 1110 1000 1111 0000 0000 0000 0000 1111 1110 0101 0000 0000 0100

0D35A 00 00 0B CF 01 00 01 00   ........   0000 0000 0000 0000 0000 1011 1100 1111 0000 0001 0000 0000 0000 0001 0000 0000

0D362 01 00 34 00 00 10 00 00   ..4.....   0000 0001 0000 0000 0011 0100 0000 0000 0000 0000 0001 0000 0000 0000 0000 0000

0D36A 02 01 1A 00 00 FE 8F 00   ........   0000 0010 0000 0001 0001 1010 0000 0000 0000 0000 1111 1110 1000 1111 0000 0000

0D372 3F FE 8F 00 00 FE 50 01   ?.....P.   0011 1111 1111 1110 1000 1111 0000 0000 0000 0000 1111 1110 0101 0000 0000 0001

0D37A 00 00 05 CD 01 00 01 00   ........   0000 0000 0000 0000 0000 0101 1100 1101 0000 0001 0000 0000 0000 0001 0000 0000

0D382 00 00 02 02 01 09 00 70   .......p   0000 0000 0000 0000 0000 0010 0000 0010 0000 0001 0000 1001 0000 0000 0111 0000


Open Design Specification for .dwg files

226


0D38A FF FF 00 00 FE 8F 00 00   ........   1111 1111 1111 1111 0000 0000 0000 0000 1111 1110 1000 1111 0000 0000 0000 0000

0D392 FE 8F 00 00 01 08 00 70   .......p   1111 1110 1000 1111 0000 0000 0000 0000 0000 0001 0000 1000 0000 0000 0111 0000

0D39A FE C0 00 00 FE 50 00 00   .....P..   1111 1110 1100 0000 0000 0000 0000 0000 1111 1110 0101 0000 0000 0000 0000 0000

0D3A2 FE 50 02 00 00 07 BD 01   .P......   1111 1110 0101 0000 0000 0010 0000 0000 0000 0000 0000 0111 1011 1101 0000 0001

0D3AA 00 22 00 00 00 00 00 02   ."......   0000 0000 0010 0010 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0010

0D3B2 01 09 00 AF FF FF 00 00   ........   0000 0001 0000 1001 0000 0000 1010 1111 1111 1111 1111 1111 0000 0000 0000 0000

0D3BA FE 50 00 00 FE 50 00 00   .P...P..   1111 1110 0101 0000 0000 0000 0000 0000 1111 1110 0101 0000 0000 0000 0000 0000

0D3C2 02 01 0A 00 70 FE C0 00   ....p...   0000 0010 0000 0001 0000 1010 0000 0000 0111 0000 1111 1110 1100 0000 0000 0000

0D3CA 3F FE 8F 00 00 FE 50 01   ?.....P.   0011 1111 1111 1110 1000 1111 0000 0000 0000 0000 1111 1110 0101 0000 0000 0001

0D3D2 00 00 05 E0 01 00 22 00   ......".   0000 0000 0000 0000 0000 0101 1110 0000 0000 0001 0000 0000 0010 0010 0000 0000

0D3DA 00 00 02 01 0B 00 AF FF   ........   0000 0000 0000 0000 0000 0010 0000 0001 0000 1011 0000 0000 1010 1111 1111 1111

0D3E2 FF 00 3F FE 8F 00 00 FE   ..?.....   1111 1111 0000 0000 0011 1111 1111 1110 1000 1111 0000 0000 0000 0000 1111 1110

0D3EA 50 00 00 02 02 01 0A 00   P.......   0101 0000 0000 0000 0000 0000 0000 0010 0000 0010 0000 0001 0000 1010 0000 0000

0D3F2 00 FE 8F 00 70 FF FF 00   ....p...   0000 0000 1111 1110 1000 1111 0000 0000 0111 0000 1111 1111 1111 1111 0000 0000

0D3FA 00 FE 8F 00 00 01 08 00   ........   0000 0000 1111 1110 1000 1111 0000 0000 0000 0000 0000 0001 0000 1000 0000 0000

0D402 00 FE 50 00 70 FE C0 00   ..P.p...   0000 0000 1111 1110 0101 0000 0000 0000 0111 0000 1111 1110 1100 0000 0000 0000

0D40A 00 FE 50 07 00 00 12 95   ..P.....   0000 0000 1111 1110 0101 0000 0000 0111 0000 0000 0000 0000 0001 0010 1001 0101

0D412 01 00 14 00 34 00 25 00   ....4.%.   0000 0001 0000 0000 0001 0100 0000 0000 0011 0100 0000 0000 0010 0101 0000 0000

0D41A 01 00 15 00 C7 01 00 57   .......W   0000 0001 0000 0000 0001 0101 0000 0000 1100 0111 0000 0001 0000 0000 0101 0111

0D422 02 00 00 02 01 09 00 3F   .......?   0000 0010 0000 0000 0000 0000 0000 0010 0000 0001 0000 1001 0000 0000 0011 1111

0D42A FE 8F 00 70 FE C0 00 00   ...p....   1111 1110 1000 1111 0000 0000 0111 0000 1111 1110 1100 0000 0000 0000 0000 0000

0D432 FE 50 03 00 00 09 81 02   .P......   1111 1110 0101 0000 0000 0011 0000 0000 0000 0000 0000 1001 1000 0001 0000 0010

0D43A 00 18 00 01 00 25 00 00   .....%..   0000 0000 0001 1000 0000 0000 0000 0001 0000 0000 0010 0101 0000 0000 0000 0000

0D442 00 02 01 0A 00 00 FE 50   .......P   0000 0000 0000 0010 0000 0001 0000 1010 0000 0000 0000 0000 1111 1110 0101 0000

0D44A 00 AF FF FF 00 00 FE 50   .......P   0000 0000 1010 1111 1111 1111 1111 1111 0000 0000 0000 0000 1111 1110 0101 0000

0D452 0F 00 00 21 D3 01 00 01   ...!....   0000 1111 0000 0000 0000 0000 0010 0001 1101 0011 0000 0001 0000 0000 0000 0001

0D45A 00 01 00 01 00 01 00 29   .......)   0000 0000 0000 0001 0000 0000 0000 0001 0000 0000 0000 0001 0000 0000 0010 1001

0D462 00 76 00 01 00 01 00 01   .v......   0000 0000 0111 0110 0000 0000 0000 0001 0000 0000 0000 0001 0000 0000 0000 0001

0D46A 00 01 00 01 00 01 00 01   ........   0000 0000 0000 0001 0000 0000 0000 0001 0000 0000 0000 0001 0000 0000 0000 0001

0D472 00 5A 00 D0 9A 00 00 02   .Z......   0000 0000 0101 1010 0000 0000 1101 0000 1001 1010 0000 0000 0000 0000 0000 0010

0D47A 01 0B 00 3F FE 8F 00 AF   ...?....   0000 0001 0000 1011 0000 0000 0011 1111 1111 1110 1000 1111 0000 0000 1010 1111

0D482 FF FF 00 00 FE 50 00 00   .....P..   1111 1111 1111 1111 0000 0000 0000 0000 1111 1110 0101 0000 0000 0000 0000 0000


Open Design Specification for .dwg files

227


0D48A 02 01 18 00 00 FE 8F 00   ........   0000 0010 0000 0001 0001 1000 0000 0000 0000 0000 1111 1110 1000 1111 0000 0000

0D492 70 FE C0 00 00 FE 50 01   p.....P.   0111 0000 1111 1110 1100 0000 0000 0000 0000 0000 1111 1110 0101 0000 0000 0001

0D49A 00 00 04 54 00 00 00 00   ...T....   0000 0000 0000 0000 0000 0100 0101 0100 0000 0000 0000 0000 0000 0000 0000 0000

0D4A2 00 02 02 01 0B 00 70 FF   ......p.   0000 0000 0000 0010 0000 0010 0000 0001 0000 1011 0000 0000 0111 0000 1111 1111

0D4AA FF 00 70 FF FF 00 00 FE   ..p.....   1111 1111 0000 0000 0111 0000 1111 1111 1111 1111 0000 0000 0000 0000 1111 1110

0D4B2 8F 00 00 01 08 00 70 FE   ......p.   1000 1111 0000 0000 0000 0000 0000 0001 0000 1000 0000 0000 0111 0000 1111 1110

0D4BA C0 00 70 FE C0 00 00 FE   ..p.....   1100 0000 0000 0000 0111 0000 1111 1110 1100 0000 0000 0000 0000 0000 1111 1110

0D4C2 50 01 00 00 05 84 02 00   P.......   0101 0000 0000 0001 0000 0000 0000 0000 0000 0101 1000 0100 0000 0010 0000 0000

0D4CA 78 00 00 00 02 01 09 00   x.......   0111 1000 0000 0000 0000 0000 0000 0000 0000 0010 0000 0001 0000 1001 0000 0000

0D4D2 AF FF FF 00 70 FE C0 00   ....p...   1010 1111 1111 1111 1111 1111 0000 0000 0111 0000 1111 1110 1100 0000 0000 0000

0D4DA 00 FE 50 07 00 00 11 EE   ..P.....   0000 0000 1111 1110 0101 0000 0000 0111 0000 0000 0000 0000 0001 0001 1110 1110

0D4E2 03 00 01 00 01 00 01 00   ........   0000 0011 0000 0000 0000 0001 0000 0000 0000 0001 0000 0000 0000 0001 0000 0000

0D4EA 03 00 01 00 01 00 00 77   .......w   0000 0011 0000 0000 0000 0001 0000 0000 0000 0001 0000 0000 0000 0000 0111 0111

0D4F2 00 00 02 01 0A 00 70 FE   ......p.   0000 0000 0000 0000 0000 0010 0000 0001 0000 1010 0000 0000 0111 0000 1111 1110

0D4FA C0 00 AF FF FF 00 00 FE   ........   1100 0000 0000 0000 1010 1111 1111 1111 1111 1111 0000 0000 0000 0000 1111 1110

0D502 50 00 00 02 01 0B 00 AF   P.......   0101 0000 0000 0000 0000 0000 0000 0010 0000 0001 0000 1011 0000 0000 1010 1111

0D50A FF FF 00 AF FF FF 00 00   ........   1111 1111 1111 1111 0000 0000 1010 1111 1111 1111 1111 1111 0000 0000 0000 0000

0D512 FE 50 02 00 00 07 F2 03   .P......   1111 1110 0101 0000 0000 0010 0000 0000 0000 0000 0000 0111 1111 0010 0000 0011

0D51A 00 01 00 FA FC 00 00 02   ........   0000 0000 0000 0001 0000 0000 1111 1010 1111 1100 0000 0000 0000 0000 0000 0010

0D522 02 01 18 00 00 FF FF 00   ........   0000 0010 0000 0001 0001 1000 0000 0000 0000 0000 1111 1111 1111 1111 0000 0000

0D52A 00 FE 8F 00 00 FE 8F 00   ........   0000 0000 1111 1110 1000 1111 0000 0000 0000 0000 1111 1110 1000 1111 0000 0000

0D532 00 01 18 00 00 FF FF 00   ........   0000 0000 0000 0001 0001 1000 0000 0000 0000 0000 1111 1111 1111 1111 0000 0000

0D53A 00 FE 50 00 00 FE 50 01   ..P...P.   0000 0000 1111 1110 0101 0000 0000 0000 0000 0000 1111 1110 0101 0000 0000 0001

0D542 00 00 05 EE 01 00 01 00   ........   0000 0000 0000 0000 0000 0101 1110 1110 0000 0001 0000 0000 0000 0001 0000 0000

0D54A 00 00 02 02 01 1A 00 00   ........   0000 0000 0000 0000 0000 0010 0000 0010 0000 0001 0001 1010 0000 0000 0000 0000

0D552 FF FF 00 70 FF FF 00 00   ...p....   1111 1111 1111 1111 0000 0000 0111 0000 1111 1111 1111 1111 0000 0000 0000 0000

0D55A FE 8F 01 00 00 05 A6 01   ........   1111 1110 1000 1111 0000 0001 0000 0000 0000 0000 0000 0101 1010 0110 0000 0001

0D562 00 00 00 00 00 01 1A 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001 0001 1010 0000 0000

0D56A 00 FF FF 00 AF FF FF 00   ........   0000 0000 1111 1111 1111 1111 0000 0000 1010 1111 1111 1111 1111 1111 0000 0000

0D572 00 FE 50 01 00 00 04 5E   ..P....^   0000 0000 1111 1110 0101 0000 0000 0001 0000 0000 0000 0000 0000 0100 0101 1110

0D57A 00 00 00 00 00 02 02 01   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0010 0000 0010 0000 0001

0D582 28 00 00 FE 8F 00 00 FF   (.......   0010 1000 0000 0000 0000 0000 1111 1110 1000 1111 0000 0000 0000 0000 1111 1111


Open Design Specification for .dwg files

228


0D58A FF 00 00 FE 8F 00 00 01   ........   1111 1111 0000 0000 0000 0000 1111 1110 1000 1111 0000 0000 0000 0000 0000 0001

0D592 28 00 00 FE 50 00 00 FF   (...P...   0010 1000 0000 0000 0000 0000 1111 1110 0101 0000 0000 0000 0000 0000 1111 1111

0D59A FF 00 00 FE 50 01 00 00   ....P...   1111 1111 0000 0000 0000 0000 1111 1110 0101 0000 0000 0001 0000 0000 0000 0000

0D5A2 04 53 00 00 00 00 00 02   .S......   0000 0100 0101 0011 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0010

0D5AA 01 29 00 3F FE 8F 00 00   .).?....   0000 0001 0010 1001 0000 0000 0011 1111 1111 1110 1000 1111 0000 0000 0000 0000

0D5B2 FF FF 00 00 FE 50 01 00   .....P..   1111 1111 1111 1111 0000 0000 0000 0000 1111 1110 0101 0000 0000 0001 0000 0000

0D5BA 00 04 55 00 00 00 00 00   ..U.....   0000 0000 0000 0100 0101 0101 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

0D5C2 02 02 01 38 00 00 FE 8F   ...8....   0000 0010 0000 0010 0000 0001 0011 1000 0000 0000 0000 0000 1111 1110 1000 1111

0D5CA 00 00 FE 8F 00 00 FF FF   ........   0000 0000 0000 0000 1111 1110 1000 1111 0000 0000 0000 0000 1111 1111 1111 1111

0D5D2 00 00 01 3B 00 3F FE 8F   ...;.?..   0000 0000 0000 0000 0000 0001 0011 1011 0000 0000 0011 1111 1111 1110 1000 1111

0D5DA 00 3F FE 8F 00 00 FF FF   .?......   0000 0000 0011 1111 1111 1110 1000 1111 0000 0000 0000 0000 1111 1111 1111 1111

0D5E2 01 00 00 04 60 00 00 00   ....`...   0000 0001 0000 0000 0000 0000 0000 0100 0110 0000 0000 0000 0000 0000 0000 0000

0D5EA 00 00 02 02 02 00 42 1D   ......B.   0000 0000 0000 0000 0000 0010 0000 0010 0000 0010 0000 0000 0100 0010 0001 1101

0D5F2 FC 00 00 00 03 40 00 00   .....@..   1111 1100 0000 0000 0000 0000 0000 0000 0000 0011 0100 0000 0000 0000 0000 0000

0D5FA 34 3C 7C 40 32 6D 11 40   4<|@2m.@   0011 0100 0011 1100 0111 1100 0100 0000 0011 0010 0110 1101 0001 0001 0100 0000

0D602 3F FF FF FF F7 3C 7C 40   ?....<|@   0011 1111 1111 1111 1111 1111 1111 1111 1111 0111 0011 1100 0111 1100 0100 0000

0D60A 00 40 00 00 21 0E 21 40   .@..!.!@   0000 0000 0100 0000 0000 0000 0000 0000 0010 0001 0000 1110 0010 0001 0100 0000

0D612 A1 0E 21 40 98 00 77 C0   ..!@..w.   1010 0001 0000 1110 0010 0001 0100 0000 1001 1000 0000 0000 0111 0111 1100 0000

0D61A 06 3C BC 40 03 00 00 00   .<.@....   0000 0110 0011 1100 1011 1100 0100 0000 0000 0011 0000 0000 0000 0000 0000 0000

0D622 08 3C BC 40 05 00 00 00   .<.@....   0000 1000 0011 1100 1011 1100 0100 0000 0000 0101 0000 0000 0000 0000 0000 0000

0D62A 00 00 00 00 00 00 1E 00   ........   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001 1110 0000 0000

0D632 70 88 95 C0 81 00 00 00   p.......   0111 0000 1000 1000 1001 0101 1100 0000 1000 0001 0000 0000 0000 0000 0000 0000

0D63A 11 84 50 C0 03 3C BC 40   ..P..<.@   0001 0001 1000 0100 0101 0000 1100 0000 0000 0011 0011 1100 1011 1100 0100 0000

0D642 3C 07 E4 C2 80 00 00 00   <.......   0011 1100 0000 0111 1110 0100 1100 0010 1000 0000 0000 0000 0000 0000 0000 0000

0D64A 00 00 1E 00 7F FF C0 00   ........   0000 0000 0000 0000 0001 1110 0000 0000 0111 1111 1111 1111 1100 0000 0000 0000

0D652 00 00 00 00 3A 40 00 00   ....:@..   0000 0000 0000 0000 0000 0000 0000 0000 0011 1010 0100 0000 0000 0000 0000 0000

0D65A 14 16 AB 40 00 00 00 00   ...@....   0001 0100 0001 0110 1010 1011 0100 0000 0000 0000 0000 0000 0000 0000 0000 0000

0D662 0F FC BC 40 11 0E D0 30   ...@...0   0000 1111 1111 1100 1011 1100 0100 0000 0001 0001 0000 1110 1101 0000 0011 0000

0D66A 40 90 80 7D CC 10 80 41   @..}...A   0100 0000 1001 0000 1000 0000 0111 1101 1100 1100 0001 0000 1000 0000 0100 0001

0D672 90 80 41 D0 80 42 10 80   ..A..B..   1001 0000 1000 0000 0100 0001 1101 0000 1000 0000 0100 0010 0001 0000 1000 0000

0D67A 48 50 80 48 90 80 48 D0   HP.H..H.   0100 1000 0101 0000 1000 0000 0100 1000 1001 0000 1000 0000 0100 1000 1101 0000

0D682 80 84 90 80 87 4E         .....N     1000 0000 1000 0100 1001 0000 1000 0000 1000 0111 0100 1110


Open Design Specification for .dwg files

229


0D688 54 B0                     crc
#### 20.4.96 TABLE (varies)
The TABLE entity (entity type ACAD_TABLE) was introduced in AutoCAD 2005 (a sub
release of R18), and a large number of changes were introduced in AutoCAD 2008 (a sub release of
R21). The table entity inherits from the INSERT entity. The geometric results, consisting of table borders,
texts and such are created in an anonymous block, similarly to the mechanism in the DIMENSION entity.
The anonymous block name prefix is “*T”. For the AutoCAD 2008 changes see paragraph 20.4.96.2.
TODO: document roundtrip data with connections to AcDbTableContent and
AcDbTableGeometry.

##### 20.4.96.1 Until R21
This paragraph describes the table DWG format until R21. In R24 the format was changed to make use of
table content to contain all data (AcDbTableContent).


Common Entity Data

Ins pt
3BD
10
R13-R14 Only:

X Scale
BD
41

Y Scale
BD
42

Z Scale
BD
43
R2000+ Only:

Data flags
BB



Scale Data


Varies with Data flags:




11 - scale is (1.0, 1.0, 1.0), no data stored.




01 – 41 value is 1.0, 2 DD’s are present, each using
### 1.0 as the default value, representing the 42 and 43
values.




10 – 41 value stored as a RD, and 42 & 43 values are
not stored, assumed equal to 41 value.




00 – 41 value stored as a RD, followed by a 42 value
stored as DD (use 41 for default value), and a 43
value stored as a DD (use 41 value for default
value).
Common:

Rotation
BD
50

Extrusion
3BD
210

Has ATTRIBs
B
66
Single bit; 1 if ATTRIBs follow.
R2004+:

Open Design Specification for .dwg files

230



Owned Object Count
BL

Number of objects owned by this object.
Common:

Flag for table value
BS
90
Bit flags, 0x06 (0x02 + 0x04): has block,
0x10: table direction, 0 = up, 1 = down,
0x20: title suppressed.
Normally 0x06 is always set.

Hor. Dir. Vector
3BD
11

Number of columns
BL
92

Number of rows
BL
91

Column widths
BD
142
Repeats “# of columns” times

Row heights
BD
141
Repeats “# of rows” times
Cell data, repeats for all cells in n x m table:

Cell type
BS
171
1 = text, 2 = block.
In AutoCAD 2007 a cell can contain either 1 text
or 1 block. In AutoCAD 2008 this changed (TODO).

Cell edge flags
RC
172
Specifies which edges have property overrides in a
cell, 1 = top, 2 = right, 4 = bottom, 8 = left. Note
that if a shared edge between two cells has property
overrides, the edge overrides flag is set in both
adjacent cells, but in one of them the edge is
marked as virtual (see virtual edge flags below). So
the virtual edge flag property determines where the
override is stored: each property override is stored
only once. When a virtual edge flag is set, the
override is determined by the adjacent cell, when it
is not set it is determined by the cell itself.
Normally a property override is stored with the cell
on which the user made the modification, but
sometimes when the user makes multiple changes in
both adjacent cells, e.g. a color modification in
cell A, and a line weight modification in cell B
(adjacent to cell A), then for the shared edge, the
property overrides for both color and line weight
are stored in the same cell (either A or B). The
reason for this is that the virtual edge flag
doesn’t allow to discriminate between individual
properties, only on the edge level.

Cell merged value
B
173
Determines whether this cell is merged with another
cell.

Autofit flag
B
174

Merged width flag
BL
175
Represents the horizontal number of merged cells.

Merged height flag
BL
176
Represents the vertical number of merged cells.

Rotation value
BD
145
If cell type == 1 (text cell):

Text string
TV
1
Present only if 344 value below is 0
If cell type == 2 (block cell):

Block scale
BD
144

Has attributes flag
B



If has attributes flag == 1:

Attr. Def. count
BS
179

Open Design Specification for .dwg files

231



Attr. Def. index
BS

Not present in dxf

Attr. Def. text
TV
300
Common to both text and block cells:

has override flag
B


If has override flag == 1:

Cell flag override
BL
177

Virtual edge flag
RC
178
Determines which edges are virtual, see also the
explanation on the cell edge flags above. When an
edge is virtual, that edge has no border overrides.
1 = top, 2 = right, 4 = bottom, 8 = left.

Cell alignment
RS
170
Present only if bit 0x01 is set in cell flag
override.
Top left = 1, top center = 2, top right = 3, middle
left = 4, middle center = 5, middle right = 6,
bottom left = 7, bottom center = 8, bottom right =
9.

Background fill none
B
283
Present only if bit 0x02 is set in cell flag
override

Background color
CMC
63
Present only if bit 0x04 is set in cell flag
override

Content color
CMC
64
Present only if bit 0x08 is set in cell flag
override

Text style
H
7
Present only if bit 0x10 is set in cell flag
override (hard pointer)

Text height
BD
140
Present only if bit 0x20 is set in cell flag
override

Top grid color
CMC
69
Present only if bit 0x00040 is set in cell flag
override

Top grid lineweight
BS
279
Present only if bit 0x00400 is set in cell flag
override

Top visibility
BS
289
Present only if bit 0x04000 is set in cell flag
override (1 = visible).

Right grid color
CMC
65
Present only if bit 0x00080 is set in cell flag
override

Right grid lineweight BS
275
Present only if bit 0x00800 is set in cell flag
override

Right visibility
BS
285
Present only if bit 0x08000 is set in cell flag
override (1 = visible).

Bottom grid color
CMC
66
Present only if bit 0x00100 is set in cell flag
override

Bottom grid lineweight BS
276
Present only if bit 0x01000 is set in cell flag
override

Bottom visibility
BS
286
Present only if bit 0x10000 is set in cell flag
override (1 = visible).

Left grid color
CMC
68
Present only if bit 0x00200 is set in cell flag
override

Left grid lineweight
BS
278
Present only if bit 0x02000 is set in cell flag
override

Open Design Specification for .dwg files

232



Left visibility
BS
288
Present only if bit 0x20000 is set in cell flag
override (1 = visible).
R2007+:

Unknown
BL

Value fields
…

See paragraph 20.4.98.


Common:
End Cell Data (remaining data applies to entire table)

Has table overrides
B


If has table overrides == 1:

Table flag override
BL
93

Title suppressed
B
280
Present only if bit 0x0001 is set in table overrides
flag

Header suppresed
--
281
Always true (do not read any data for this)

Flow direction
BS
70
Present only if bit 0x0004 is set in table overrides
flag (0 = down, 1 = up).

Horz. Cell margin
BD
40
Present only if bit 0x0008 is set in table overrides
flag

Vert. cell margin
BD
41
Present only if bit 0x0010 is set in table overrides
flag

Title row color
CMC
64
Present only if bit 0x0020 is set in table overrides
flag

Header row color
CMC
64
Present only if bit 0x0040 is set in table overrides
flag

Data row color
CMC
64
Present only if bit 0x0080 is set in table overrides
flag

Title row fill none
B
283
Present only if bit 0x0100 is set in table overrides
flag

Header row fill none
B
283
Present only if bit 0x0200 is set in table overrides
flag

Data row fill none
B
283
Present only if bit 0x0400 is set in table overrides
flag

Title row fill color CMC
63
Present only if bit 0x0800 is set in table overrides
flag

Header row fill clr. CMC
63
Present only if bit 0x1000 is set in table overrides
flag

Data row fill color
CMC
63
Present only if bit 0x2000 is set in table overrides
flag

Title row align.
BS
170
Present only if bit 0x4000 is set in table overrides
flag

Header row align.
BS
170
Present only if bit 0x8000 is set in table overrides
flag

Data row align.
BS
170
Present only if bit 0x10000 is set in table
overrides flag

Title text style hnd
H
7
Present only if bit 0x20000 is set in table
overrides flag (hard pointer)

Open Design Specification for .dwg files

233



Title text style hnd
H
7
Present only if bit 0x40000 is set in table
overrides flag (hard pointer)

Title text style hnd
H
7
Present only if bit 0x80000 is set in table
overrides flag (hard pointer)

Title row height
BD
140
Present only if bit 0x100000 is set in table
overrides flag

Header row height
BD
140
Present only if bit 0x200000 is set in table
overrides flag

Data row height
BD
140
Present only if bit 0x400000 is set in table
overrides flag
End If has table overrides == 1

Has border color overrides
B


If has border color overrides == 1:

Overrides flag
BL
94
Border COLOR overrides

Title hor. Top. col. CMC
64
Present only if bit 0x01 is set in border color
overrides flag

Title hor. ins. col. CMC
65
Present only if bit 0x02 is set in border color
overrides flag

Title hor. bot. col. CMC
66
Present only if bit 0x04 is set in border color
overrides flag

Title ver. left. col. CMC
63
Present only if bit 0x08 is set in border color
overrides flag

Title ver. ins. col. CMC
68
Present only if bit 0x10 is set in border color
overrides flag

Title ver. rt. col.
CMC
69
Present only if bit 0x20 is set in border color
overrides flag

Header hor. Top. col. CMC
64
Present only if bit 0x40 is set in border color
overrides flag

Header hor. ins. col. CMC
65
Present only if bit 0x80 is set in border color
overrides flag

Header hor. bot. col. CMC
66
Present only if bit 0x100 is set in border color
overrides flag

Header ver. left. col.CMC
63
Present only if bit 0x200 is set in border color
overrides flag

Header ver. ins. col. CMC
68
Present only if bit 0x400 is set in border color
overrides flag

Header ver. rt. col. CMC
69
Present only if bit 0x800 is set in border color
overrides flag

Data hor. Top. col.
CMC
64
Present only if bit 0x1000 is set in border color
overrides flag

Data hor. ins. col.
CMC
65
Present only if bit 0x2000 is set in border color
overrides flag

Data hor. bot. col.
CMC
66
Present only if bit 0x4000 is set in border color
overrides flag

Data ver. left. col. CMC
63
Present only if bit 0x8000 is set in border color
overrides flag

Data ver. ins. col.
CMC
68
Present only if bit 0x10000 is set in border color
overrides flag

Open Design Specification for .dwg files

234



Data ver. rt. col.
CMC
69
Present only if bit 0x20000 is set in border color
overrides flag
End If has border color overrides == 1

Has border lineweight overridesB


If has border lineweight overrides == 1:

Overrides flag
BL
95
Border LINEWEIGHT overrides

Title hor. Top. lw.
BS

Present only if bit 0x01 is set in border color
overrides flag

Title hor. ins. lw.
BS

Present only if bit 0x02 is set in border color
overrides flag

Title hor. bot. lw.
BS

Present only if bit 0x04 is set in border color
overrides flag

Title ver. left. lw.
BS

Present only if bit 0x08 is set in border color
overrides flag

Title ver. ins. lw.
BS

Present only if bit 0x10 is set in border color
overrides flag

Title ver. rt. lw.
BS

Present only if bit 0x20 is set in border color
overrides flag

Header hor. Top. lw.
BS

Present only if bit 0x40 is set in border color
overrides flag

Header hor. ins. lw.
BS

Present only if bit 0x80 is set in border color
overrides flag

Header hor. bot. lw.
BS

Present only if bit 0x100 is set in border color
overrides flag

Header ver. left. lw. BS

Present only if bit 0x200 is set in border color
overrides flag

Header ver. ins. lw.
BS

Present only if bit 0x400 is set in border color
overrides flag

Header ver. rt. lw.
BS

Present only if bit 0x800 is set in border color
overrides flag

Data hor. Top. lw.
BS

Present only if bit 0x1000 is set in border color
overrides flag

Data hor. ins. lw.
BS

Present only if bit 0x2000 is set in border color
overrides flag

Data hor. bot. lw.
BS

Present only if bit 0x4000 is set in border color
overrides flag

Data ver. left. lw.
BS

Present only if bit 0x8000 is set in border color
overrides flag

Data ver. ins. lw.
BS

Present only if bit 0x10000 is set in border color
overrides flag

Data ver. rt. lw.
BS

Present only if bit 0x20000 is set in border color
overrides flag
End If has border lineweight overrides == 1

Has border visibility overridesB


If has border visibility overrides == 1:

Overrides flag
BL
96
Border visibility overrides

Title hor. Top. vsb.
BS

Present only if bit 0x01 is set in border visibility
overrides flag (0 = visible, 1 = invisible)

Open Design Specification for .dwg files

235



Title hor. ins. vsb.
BS

Present only if bit 0x02 is set in border visibility
overrides flag (0 = visible, 1 = invisible)

Title hor. bot. vsb.
BS

Present only if bit 0x04 is set in border visibility
overrides flag (0 = visible, 1 = invisible)

Title ver. left. vsb. BS

Present only if bit 0x08 is set in border visibility
overrides flag (0 = visible, 1 = invisible)

Title ver. ins. vsb.
BS

Present only if bit 0x10 is set in border visibility
overrides flag (0 = visible, 1 = invisible)

Title ver. rt. vsb.
BS

Present only if bit 0x20 is set in border visibility
overrides flag (0 = visible, 1 = invisible)

Header hor. Top. vsb. BS

Present only if bit 0x40 is set in border visibility
overrides flag (0 = visible, 1 = invisible)

Header hor. ins. vsb. BS

Present only if bit 0x80 is set in border visibility
overrides flag (0 = visible, 1 = invisible)

Header hor. bot. vsb. BS

Present only if bit 0x100 is set in border
visibility overrides flag (0 = visible, 1 =
invisible)

Header ver. left. vsb. BS

Present only if bit 0x200 is set in border
visibility overrides flag (0 = visible, 1 =
invisible)

Header ver. ins. vsb. BS

Present only if bit 0x400 is set in border  (0 =
visible, 1 = invisible)visibility overrides flag

Header ver. rt. vsb.
BS

Present only if bit 0x800 is set in border
visibility overrides flag (0 = visible, 1 =
invisible)

Data hor. Top. vsb.
BS

Present only if bit 0x1000 is set in border
visibility overrides flag (0 = visible, 1 =
invisible)

Data hor. ins. vsb.
BS

Present only if bit 0x2000 is set in border
visibility overrides flag (0 = visible, 1 =
invisible)

Data hor. bot. vsb.
BS

Present only if bit 0x4000 is set in border
visibility overrides flag (0 = visible, 1 =
invisible)

Data ver. left. vsb.
BS

Present only if bit 0x8000 is set in border
visibility overrides flag (0 = visible, 1 =
invisible)

Data ver. ins. vsb.
BS

Present only if bit 0x10000 is set in border
visibility overrides flag (0 = visible, 1 =
invisible)

Data ver. rt. vsb.
BS

Present only if bit 0x20000 is set in border
visibility overrides flag (0 = visible, 1 =
invisible)
End If has border visibility overrides == 1



Common:

Common Entity Handle Data


H
2
BLOCK HEADER (hard pointer)

Open Design Specification for .dwg files

236


R13-R200:


H

[1st ATTRIB (soft pointer)]  if 66 bit set; can be
NULL


H

[last ATTRIB](soft pointer)] if 66 bit set; can be
NULL
R2004:


H

[ATTRIB (soft pointer)] Repeats “Owned Object Count”
times.
Common:


H

[SEQEND (hard owner)]      if 66 bit set


H
342
Table Style ID (hard pointer)


H Varies
344 for text cell, 340 for block cell (hard pointer)


H
331
Attr. Def. ID (soft pointer, present only for block
cells, when additional data flag == 1, and 1 entry
per attr. def.)


H
7
Text style override (present only if bit 0x08 is set
in cell flag override), one for each applicable cell


H
7
Title row style override (present only if bit
0x20000 is set in table overrides flag


H
7
Title row style override (present only if bit
0x40000 is set in table overrides flag


H
7
Title row style override (present only if bit
0x80000 is set in table overrides flag



CRC
X
---
##### 20.4.96.2 R24 and later
In the R24 format the old table data structures were replaced with new data structures, of which the root
is the AcDbTableContent class. The old data structures are still used in the DXF format. An R24 DXF
file contains both the old and new structures, where the new structures are optionally used. If AutoCAD
can store all data just using the old structures it does not always write the new structures in DXF. In an
R24 DWG file, always the new structures are used. The table then points to a AcDbTableContent object,
which contains most of the actual data. Note that AcDbTableContent was already introduced in
AutoCAD 2008 (R21), but in R21 it was indirectly referenced through the tables extension dictionary
entry ACAD_XREC_ROUNDTRIP (TODO: describe  details on
ACAD_ROUNDTRIP_2008_TABLE_ENTITY and for 2007).
Version
Field
type
DXF
group
code
Description

…

Common entity data.
R2010+




RC

Unknown (default 0)

H

Unknown (soft pointer, default NULL)

BL

Unknown (default 0)

Open Design Specification for .dwg files

237


R2010




B

Unknown (default true)
R2013




BL

Unknown (default 0)
R2010+




…

Here the table content is present (see TABLECONTENT object), without the
common OBJECT data. See paragraph 20.4.97.

BS

Unknown (default 38)

3BD
11
Horizontal direction

BL

Has break data flag (0 = no break data, 1 = has break data)



Begin break data (optional)

BL

Option flags:
Enable breaks = 1,
Repeat top labels = 2,
Repeat bottom labels = 4,
Allow manual positions = 8,
Allow manual heights = 16

BL

Flow direction:
Right = 1,
Vertical = 2,
Left = 4

BD

Break spacing

BL

Unknown flags

BL

Unknown flags

BL

Number of manual positions (break heights)



Begin repeat manual positions (break heights)

3BD

Position

BD

Height

BL

Flags (meaning unknown)



End repeat manual positions (break heights)



End break data

BL

Number of break row ranges (there is always at least 1)



Begin repeat row ranges

3BD

Position

BL

Start row index

BL

End row index



End repeat row ranges

#### 20.4.97 TABLECONTENT
This represents the table content (AcDbTableContent) that replaces the old table data structures that were
introduced in AutoCAD 2005. Table content was introduced in AutoCAD 2008 and supports more

Open Design Specification for .dwg files

238


advanced features like e.g. multiple contents per cell. In AutoCAD 2008 the table content was written as a
separate object in DWG and referenced by roundtrip data in the table entity’s extension dictionary. In
DXF this is still the case even for R24. In a R24 DWG file, the table content is part of the table entity data
and is no longer present as a separate object. Possibly for backwards compatibility with the AutoCAD
2007 (R21) format, this separate data container was created instead of extending the ACAD_TABLE
entity.
The table content class inherits from 3 other classes, which never exist independently so they will all be
described in this paragraph. AcDbTableContent inherits from AcDbFormattedTableData, which inherits
from AcDbLinkedTableData, which inherits from AcDbLinkedData. Class AcDbLinkedTableData
contains most of the data (rows, columns, cells, cell contents).

Version
Field
type
DXF
group
code
Description

…

Common object data.



AcDbLinkedData fields

TV
1
Name

TV
300
Description



AcDbLinkedTableData fields

BL
90
Number of columns



Begin repeat columns

TV
300
Column name

BL
91
32-bit integer containing custom data

…

Custom data collection, see paragraph 20.4.100.

…

Cell style data, see paragraph 20.4.101.4, this contains cell style overrides for
the column.

BL
90
Cell style ID, points to the cell style in the table’s table style that is used as the
base cell style for the column. 0 if not present.

BD
40
Column width.



End repeat columns

BL
91
Number of rows.



Begin repeat rows.

BL
90
Number of cells in row.



Begin repeat cells

BL
90
Cell state flags:
Content locked = 0x1,
Content readonly = 0x2,
Linked = 0x4,
Content modified after update = 0x8,
Format locked = 0x10,
Format readonly = 0x20,
Format modified after update = 0x40

Open Design Specification for .dwg files

239



TV
300
Tooltip

BL
91
32-bit integer containing custom data

…

Custom data collection, see paragraph 20.4.100.

BL
92
Has linked data flags, 0 = false, 1 = true



If has linked data

H
340
Handle to data link object (hard pointer).

BL
93
Row count.

BL
94
Column count.

BL
96
Unknown.



End if has linked data

BL
95
Number of cell contents



Begin repeat cell contents

BL
90
Cell content type:
Unknown = 0,
Value = 0x1,
Field = 0x2,
Block = 0x4



If cell content type is Value

…

Write value (see paragraph 20.4.98)



Else if cell content type is Field

H
340
Handle to AcDbField object (hard pointer).



Else if cell content type is Block

H
340
Handle to block record (hard pointer).



End if cell content type is Block

BL
91
Number of attributes



Begin repeat attributes

H
330
Handle to attribute definition (ATTDEF), soft pointer.

TV
301
Attribute value.

BL
92
Index (starts at 1).



End repeat attributes

BS
170
Has content format overrides flag



If has content format overrides flag is non-zero

…

The content format overrides, see paragraph 20.4.101.3. By default the cell
content uses the cell’s cell style, this allows to override properties per content.



End if has content format overrides flag is non-zero



End repeat cell contents

…

Cell style data, see paragraph 20.4.101.4, this contains cell style overrides for
the cell.

BL
90
Cell style ID, points to the cell style in the table’s table style that is used as the
base cell style for the cell. 0 if not present.

BL
91
Unknown flag



If unknown flag is non-zero

BL
91
Unknown

BD
40
Unknown

Open Design Specification for .dwg files

240



BD
41
Unknown

BL

Geometry data flags

H

Unknown ()



If geometry data flags is non-zero

…

Cell content geometry, see paragraph 20.4.98.



Enf if geometry data flags is non-zero



End If unknown flag is non-zero



End repeat cells

BL
91
32-bit integer containing custom data

…

Custom data collection, see paragraph 20.4.100.

…

Cell style data, see paragraph 20.4.101.4, this contains cell style overrides for
the row.

BL
90
Cell style ID, points to the cell style in the table’s table style that is used as the
base cell style for the row. 0 if not present.

BD
40
Row height.



End repeat rows.

BL
-
Number of cell contents that contain a field reference.



Begin repeat field references

H
-
Handle to field (AcDbField), hard owner.



End repeat field references



AcDbFormattedTableData fields

…

The table’s cell style override fields (see paragraph 20.4.101.4). The table’s
base cell style is the table style’s overall cell style (present from R24 onwards).

BL
90
Number of merged cell ranges



Begin repeat merged cell ranges

BL
91
Top row index

BL
92
Left column index

BL
93
Bottom row index

BL
94
Right column index



End repeat merged cell ranges



AcDbTableContent fields

H
340
Handle to table style (hard pointer).
#### 20.4.98 Cell content geometry
The table below represents the cell content geometry (does not have to be written)
Version
Field
type
DXF
group
code
Description

3BD

Distance to top left

3BD

Distance to center

BD

Content width

BD

Content height

BD

Width

Open Design Specification for .dwg files

241



BD

Height

BL

Unknown flags
#### 20.4.99 Value
This is a not an entity or object, but a common value that is always part of an entity or object. Since it
appears in multiple entities/objects a separate paragraph is dedicated to it.
R2007+:

Flags
BL
93
Flags & 0x01 => type is kGeneral
Common:

Data type
BL
90


Varies by type:


Not present in case bit 1 in Flags is set

0 – Unknown
BL


1 - Long
BL

2 –Double
BD

4 –String
TV

8 –Date


BL data size N, followed by N bytes (Int64 value)

16 –Point


BL data size, followed by 2RD

32 –3D Point


BL data size, followed by 3RD

64 –Object Id
H

Read from appropriate place in handles section (soft
pointer).

128 –Buffer


Unknown.

256 –Result Buffer


Unknown.

512 –General


General, BL containing the byte count followed by a
byte array. (introduced in R2007, use Unknown before
R2007).
R2007+:

Unit type
BL
94
0 = no units, 1 = distance, 2 = angle, 4 = area, 8 =
volume

Format String
TV
300

Value String
TV
302
20.4.100
Custom data collection
Table cells, columns and rows may have a collection of custom data items (key/value pairs) associated
with them.
Version
Field
type
DXF
group
code
Description

BL
90
Number of custom data items



Begin repeat custom data items

TV
300
Item name

…

Item value (variant), see paragraph 20.4.98.

Open Design Specification for .dwg files

242





End repeat custom data items
20.4.101
TABLESTYLE
The table style object repesents the style for the table entity. Like the table entity, table style was
introduced in AutoCAD 2005. In AutoCAD 2008 new cell style data was introduced, which was stored in
a separate container object: CELLSTYLEMAP, see paragraph 20.4.102 for more details. The cellstyle
map can contain custom cell styles, whereas the TABLESTYLE only contains the Table (R24), _Title,
_Header and _Data cell style.
20.4.101.1
TABLESTYLE format until R21

Common OBJECT data, see paragraph 20.1.
Common:

Description
TV
3

Flow direction
BS
70
0 = down, 1 = up

Bit flags
BS
71
Meaning unknown.

Horizontal cell margin BD
40

Vertical cell margin
BD
41

Suppress title
B
280

Suppress header
B
281
Begin repeat 3 times (data, title and header row styles in this order)

Text style ID
H
7
Hard pointer.

Text height
BD
140

Text alignment
BS
170
Top left = 1, top center = 2, top right = 3, middle
left = 4, middle center = 5, middle right = 6,
bottom left = 7, bottom center = 8, bottom right =
9.

Text color
CMC
62

Fill color
CMC
63

Background color enabled
B
283
Begin repeat 6 times (borders: top, horizontal inside, bottom, left, vertical inside, right, in
this order)

Line weight
BS 274-279

Visible
B 284-289
0 = invisible, 1 = visible

Border color
CMC
64-69
End repeat borders
R2007+

Data type
BL
90
As defined in the ACAD_TABLE entity.

Data unit type
BL
91
As defined in the ACAD_TABLE entity.


Format string
TV
1

End repeat row styles

Open Design Specification for .dwg files

243


20.4.101.2
R24 TABLESTYLE format
Version
Field
type
DXF
group
code
Description

RC
-
Unknown

TV
3
Description

BL
-
Unknown

BL
-
Unknown

H
-
Unknown (hard owner)

…

The cell style with name “Table”, see paragraph 20.4.101.4.

BL
90
Cell style ID, 1 = title, 2 =  header, 3 = data, 4 = table (new in R24).
The cell style ID is used by cells, columns, rows to reference a cell style in the
table’s table style. Custom cell style ID’s are numbered starting at 101.

BL
91
Cell style class, 1= data, 2 = label. The default value is label.

TV
300
Cell style name

BL

The number of cell styles (should be 3), the non-custom cell styles are present
only in the CELLSTYLEMAP.



Begin repeat cell styles (for data, title, header in this order)

…

The cell style fields, see paragraph 20.4.101.4.

BL
-
Cell style ID, 1 = title, 2 =  header, 3 = data, 4 = table (new in R24).
The cell style ID is used by cells, columns, rows to reference a cell style in the
table’s table style. Custom cell style ID’s are numbered starting at 101.

BL
-
Cell style class, 1= data, 2 = label. The default value is label.

TV
-
Cell style name



End repeat cell styles
20.4.101.3
Content format
Content format data is present in the cell style map object, in the table entity and also the table content
object.
Version
Field
type
DXF
group
code
Description

BL
90
Property override flags (is used for both content format and cell style):

Content format properties:
Data type = 0x1,
Data format = 0x2,
Rotation = 0x4,
Block scale = 0x8,
Alignment = 0x10,
Content color = 0x20,
Text style = 0x40,
Text height = 0x80,
Auto scale = 0x100,

Open Design Specification for .dwg files

244



Cell style properties:
Background color = 0x200,
Margin left = 0x400,
Margin top = 0x800,
Margin right = 0x1000,
Margin bottom = 0x2000,
Content layout = 0x4000,
Margin horizontal spacing = 0x20000,
Margin vertical spacing = 0x40000,

Row/column properties:
Merge all = 0x8000
Table properties:
Flow direction bottom to top = 0x10000

BL
91
Property flags. Contains property bit values for property Auto Scale only
(0x100).

BL
92
Value data type, see also paragraph 20.4.98.

BL
93
Value unit type, see also paragraph 20.4.98.

TV
300
Value format string

BD
40
Rotation

BD
140
Block scale

BL
94
Cell alignment:
Top left = 1,
Top center = 2,
Top right = 3,
Middle left = 4,
Middle center = 5,
Middle right = 6,
Bottom left = 7,
Bottom center = 8,
Bottom right = 9

TC
62
Content color

H
340
Text style handle (hard pointer)

BD
144
Text height

20.4.101.4
Cell style
Table cell style data is present in the cell style map object, in the table entity and also the table content
object. A cell style inherits from content format. Cell style adds amongst others cell border style and
margin properties to the content style properties of content format (see paragraph 20.4.101.3).


Open Design Specification for .dwg files

245


Version
Field
type
DXF
group
code
Description

BL
90
Cell style type:
Cell = 1,
Row = 2,
Column = 3,
Formatted table data = 4,
Table = 5

BS
170
Data flags, 0 = no data, 1 = data is present



If data is present

BL
91
Property override flags. The definition is the same as the content format
propery override flags, see paragraph 20.4.101.3.

BL
92
Merge flags, but may only for bits 0x8000 and 0x10000.

TC
62
Background color

BL
93
Content layout flags:
Flow = 1,
Stacked horizontal = 2,
Stacked vertical = 4

…

Content format fields (see paragraph 20.4.101.3).

BS
171
Margin override flags, bit 1 is set if margin overrides are present



If margin overrides are present

BD
40
Vertical margin

BD
40
Horizontal margin

BD
40
Bottom margin

BD
40
Right margin

BD
40
Margin horizontal spacing

BD
40
Margin vertical spacing



End if margin overrides are present

BL
94
Number of borders present (0-6)



Begin repeat borders

BL
95
Edge flags: 1 = top, 2 = right, 4 = bottom, 8 = left, 0x10 = inside vertical, 0x20
= inside horizontal



If edge flags is non-zero

BL
90
Border property override flags:
Border types = 0x1,
Line weight = 0x2,
Line type = 0x4,
Color = 0x8,
Invisibility = 0x10,
Double line spacing = 0x20

BL
91
Border type:
Single = 1,
Double = 2

Open Design Specification for .dwg files

246



TC
62
Color

BL
92
Line weight

H
340
Line type (hard pointer)

BL
93
Invisibility: 1 = invisible, 0 = visible.

BD
40
Double line spacing



End if edge flags is non-zero



End repeat borders



End if data is present

20.4.102
CELLSTYLEMAP
The cell style map (AcDbCellStyleMap) is a helper class for TABLESTYLE containing all cell styles.
This object was introduced in AutoCAD 2008, together with the new table related classes (like
AcDbTableContent). Possibly for backwards compatibility with the AutoCAD 2007 (R21) format, this
separate data container was created instead of extending the TABLESTYLE object.
The cell style map is connected to the table style through an extension dictionary entry with name
“ACAD_ROUNDTRIP_2008_TABLESTYLE_CELLSTYLEMAP” in the table style’s extension
dictionary. The dictionary entry value points to the cell style map.

Version
Field
type
DXF
group
code
Description

…

Common AcDbObject fields, see paragraph 20.1.

BL
90
Number of cell styles



Begin repeat cell styles

…

Cell style fields, see paragraph 20.4.101.4.

BL
90
Cell style ID, 1 = title, 2 =  header, 3 = data, 4 = table (new in R24).
The cell style ID is used by cells, columns, rows to reference a cell style in the
table’s table style. Custom cell style ID’s are numbered starting at 101.

BL
91
Cell style class, 1= data, 2 = label. The default value is label.

TV
300
Cell style name



End repeat cell styles
20.4.103
TABLEGEOMETRY
This object represents a table’s geometry and was introduced in AutoCAD 2008. It does not need to be
present in a DWG file.

Version
Field
DXF
Description

Open Design Specification for .dwg files

247


type
group
code

…

Common AcDbObject fields, see paragraph 20.1.

BL
90
Row count

BL
91
Column count

BL
92
Row * column count



Begin repeat rows



Begin repeat columns

BL
93
Flags

BD
40
Width with gap

BD
41
Height with gap

H
330
Handle to unknown (soft pointer)

BL
94
Content count



Begin repeat contents

3BD
10,20,30
Distance to top left.

3BD
11,21,31
Distance to center.

BD
43
Content width.

BD
44
Content height.

BD
45
Width.

BD
46
Height.

BD
95
Unknown (0).



End repeat contents



End repeat columns



End repeat rows
20.4.104
XRECORD (varies):

Length
MS
---
Entity length (not counting itself or CRC).

Type
BS
0
typecode (internal DWG type code).
R2000+:

Obj size
RL

size of object in bits, not including end handles
Common:

Handle
H
5
Length (char) followed by the handle bytes.

EED
X
-3
See EED section.
R13-R14 Only:

Obj size
RL

size of object in bits, not including end handles
Common:

Numreactors
BL

Number of persistent reactors attached to this obj
R2004+:

XDic Missing Flag
B

If 1, no XDictionary handle is stored for this
object, otherwise XDictionary handle is stored as in
R2000 and earlier.
Common:

Numdatabytes
BL

number of databytes

Open Design Specification for .dwg files

248



Databytes
X

databytes, however many there are to the handles
R2000+:

Cloning flag
BS
280
Common:
XRECORD data is pairs of:


RS indicator number, then data.  The indicator
number indicates the DXF number of the data, then
the data follows, so for instance an indicator of 1
would be followed by the string length (RC), the
dwgcodepage (RC), and then the string, for R13-R2004
files.  For R2007+, a string contains a short length
N, and then N Unicode characters (2 bytes each).  An
indicator of 70 would mean a 2 byte short following.
An indicator of 10 indicates 3 8-byte doubles
following.  An indicator of 40 means 1 8-byte
double.  These indicator numbers all follow the
normal AutoCAD DXF convention for group codes.

Handle refs
H

parenthandle (soft pointer)




[Reactors (soft pointer)]




xdictionary (hard owner)




objid object handles, as many as you can read until
you run out of data
20.4.104.1
Example:
OBJECT: proxy (1F4H), len 65H (101), handle: 28

00AC1 65 00                     e.         0110 0101 0000 0000

00AC3 3D 00 40 4A 20 80 30 00   =.@J .0.   0011 1101 0000 0000 0100 0000 0100 1010 0010 0000 1000 0000 0011 0000 0000 0000

00ACB 04 05 56 01 00 1B 00 0C   ..V.....   0000 0100 0000 0101 0101 0110 0000 0001 0000 0000 0001 1011 0000 0000 0000 1100

00AD3 54 68 69 73 20 69 73 20   This is    0101 0100 0110 1000 0110 1001 0111 0011 0010 0000 0110 1001 0111 0011 0010 0000

00ADB 61 20 74 65 73 74 20 78   a test x   0110 0001 0010 0000 0111 0100 0110 0101 0111 0011 0111 0100 0010 0000 0111 1000

00AE3 72 65 63 6F 72 64 20 6C   record l   0111 0010 0110 0101 0110 0011 0110 1111 0111 0010 0110 0100 0010 0000 0110 1100

00AEB 69 73 74 0A 00 00 00 00   ist.....   0110 1001 0111 0011 0111 0100 0000 1010 0000 0000 0000 0000 0000 0000 0000 0000

00AF3 00 00 00 F0 3F 00 00 00   ....?...   0000 0000 0000 0000 0000 0000 1111 0000 0011 1111 0000 0000 0000 0000 0000 0000

00AFB 00 00 00 00 40 00 00 00   ....@...   0000 0000 0000 0000 0000 0000 0000 0000 0100 0000 0000 0000 0000 0000 0000 0000

00B03 00 00 00 00 00 28 00 6F   .....(.o   0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0010 1000 0000 0000 0110 1111

00B0B 86 1B F0 F9 21 09 40 32   ....!.@2   1000 0110 0001 1011 1111 0000 1111 1001 0010 0001 0000 1001 0100 0000 0011 0010

00B13 00 D7 35 33 F0 F9 21 09   ..53..!.   0000 0000 1101 0111 0011 0101 0011 0011 1111 0000 1111 1001 0010 0001 0000 1001

00B1B 40 3E 00 01 00 46 00 B4   @>...F..   0100 0000 0011 1110 0000 0000 0000 0001 0000 0000 0100 0110 0000 0000 1011 0100

00B23 00 40 41 0C 30            .@A.0      0000 0000 0100 0000 0100 0001 0000 1100 0011 0000

00B28 45 76                     crc

Open Design Specification for .dwg files

249