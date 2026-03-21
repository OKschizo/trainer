# Chapter 29: PROXY ENTITY GRAPHICS

29 PROXY ENTITY GRAPHICS
Proxy entities (zombies prior to R14) can have associated graphics data.  The presence or absence of this
data is indicated by the single bit which we call the “graphic present flag”, which mostly occurs on entity-
type proxies, and very few other entities.  Entity type proxies are proxies where the related class’s
itemclassid field is equal to 0x1F2.
If that bit is 1, then following it, and preceding the RL which indicates the number of bits in the object, is
an RL which indicates the number of bytes of proxy entity graphic data to follow.
Graphics data is padded to 4 byte boundaries!  So, for instance, strings which are too short are padded out
to the next 4 byte boundary.  Similarly for lists of shorts.
In addition to the data definitions from chapter 2 there are a few additional data types:
PS
: Padded string. This is a string, terminated with a zero byte. The file’s text encoding (code page)
is used to encode/decode the bytes into a string.
PUS
: Padded Unicode string. The bytes are encoded using Unicode encoding. The bytes consist of
byte pairs and the string is terminated by 2 zero bytes.
We use the following defines to discriminate sub-item presence:
#define adHasPrimTraits(a)         (a & 0xFFFFL)
#define adPrimsHaveColors(a)       (a & 0x0001L)
#define adPrimsHaveLayers(a)       (a & 0x0002L)
#define adPrimsHaveLinetypes(a)    (a & 0x0004L)
#define adPrimsHaveMarkers(a)      (a & 0x0020L)
#define adPrimsHaveVisibilities(a) (a & 0x0040L)
#define adPrimsHaveNormals(a)      (a & 0x0080L)
#define adPrimsHaveOrientation(a)  (a & 0x0400L)
The graphics data comes in chunks with the following format:

RL : size

RL : type
type-specific data

valid types are:
Extents 1

3 RD : extext min

3 RD : extent max
CIRCLE 2

3 RD : center of circle

Open Design Specification for .dwg files

271



RD : radius

3 RD : normal
CIRCLE3PT 3  (3 point circle)

3 RD : first point

3 RD : second point

3 RD : third point
CIRCULARARC 4

3 RD : center

RD : radius

3 RD : normal

3 RD : start vector direction

RD : sweep angle

RL : arc type
CIRCULARARC3PT 5

3 RD : first point

3 RD : second point

3 RD : third point

RL : arc type
POLYLINE 6

RL : number of points

3 RD : a point (repeat "number of points" times)
POLYGON 7

RL : number of points

3 RD : a point (repeat "number of points" times)
MESH 8
RL:number of rows
RL:number of columns
Repeat "rows" times:
Repeat "cols" times
3 RD: vertex
Endrep
Endrep

RL:edge primitive flags

Open Design Specification for .dwg files

272


if (adHasPrimTraits(edgeprimflag)) {
compute nummeshedges as (rows-1)*cols + (cols-1) * rows
if (adPrimsHaveColors(edgeprimflag) {
RL: color for each edge
}
if (adPrimsHaveLayers(edgeprimflag)) {
RL: layer ids, 1 for each edge
}
if (adPrimsHaveLinetypes(edgeprimflag)) {
RL: linetype ids, 1 for each edge
}
if (adPrimsHaveMarkers(edgeprimflag)) {
RL: marker indices, 1 for each edge
}
if (adPrimsHaveVisibilities(edgeprimflag)) {
RL: visibility indicator, 1 for each edge
}
}

RL: face primitive flags
if (adHasPrimTraits(faceprimflag)) {
compute nummeshfaces as (rows-1)*(cols-1)
if (adPrimsHaveColors(faceprimflag) {
RL: color for each face
}
if (adPrimsHaveLayers(faceprimflag)) {
RL: layer ids, 1 for each face
}
if (adPrimsHaveMarkers(faceprimflag)) {
RL: marker indices, 1 for each face
}
if (adPrimsHaveNormals(faceprimflag)) {
3 RD: normal, 1 for each face
}
if (adPrimsHaveVisibilities(faceprimflag)) {
RL: visibility indicator, 1 for each face
}
}

RL: vertex primitive flags

Open Design Specification for .dwg files

273


if (adHasPrimTraits(vertprimflag)) {
compute numvertices as rows * cols
if (adPrimsHaveNormals(vertprimflag)) {
3 RD: normal, 1 for each vertex
}
if (adPrimsHaveOrientation(vertprimflag)) {
RL: orientation indicator, 1 ONLY
}
}
SHELL 9

RL : number of points

3 RD : vertex, 1 set of 3 for each vertex

RL : number of face entries

RL : face entries, "number of face entries" of these indicates a face for the shell.
negative entry indicates the number of entries to follow.  then follow the
entries, which indicate the vertices, read above, that make up that face.  So for
instance entries

-3,2,3,4 would mean a 3 sided face of vertices 2,3 and 4.

We scan this list and get the number of faces and edges.
RL: edge primitive flags
if (adHasPrimTraits(edgeprimflag)) {
if (adPrimsHaveColors(edgeprimflag) {
RL: color for each edge
}
if (adPrimsHaveLayers(edgeprimflag)) {
RL: layer ids, 1 for each edge
}
if (adPrimsHaveLinetypes(edgeprimflag)) {
RL: linetype ids, 1 for each edge
}
if (adPrimsHaveMarkers(edgeprimflag)) {
RL: marker indices, 1 for each edge
}
if (adPrimsHaveVisibilities(edgeprimflag)) {
RL: visibility indicator, 1 for each edge
}
}

RL: face primitive flags
if (adHasPrimTraits(faceprimflag)) {
if (adPrimsHaveColors(faceprimflag) {
RL: color for each face
}
if (adPrimsHaveLayers(faceprimflag)) {
RL: layer ids, 1 for each face
}
if (adPrimsHaveMarkers(faceprimflag)) {
RL: marker indices, 1 for each face
}
if (adPrimsHaveNormals(faceprimflag)) {
3 RD: normal, 1 for each face
}

Open Design Specification for .dwg files

274


if (adPrimsHaveVisibilities(faceprimflag)) {
RL: visibility indicator, 1 for each face
}
}

RL: vertex primitive flags
if (adHasPrimTraits(vertprimflag)) {
compute numvertices as rows * cols
if (adPrimsHaveNormals(vertprimflag)) {
3 RD: normal, 1 for each vertex
}
if (adPrimsHaveOrientation(vertprimflag)) {
RL: orientation indicator, 1 ONLY
}
}
TEXT 10

3 RD : start point

3 RD : normal

3 RD : text direction

RD : height

RD : widthfactor

RD : oblique angle

PS : string, zero terminated and padded to 4 byte boundary
TEXT2 11

3 RD : start point

3 RD : normal

3 RD : text direction

PS : string, padded to 4 byte boundary

RL : length of string, -1 if zero terminated

RL : "raw"; 0 if raw, 1 if not.  raw means don't interpret %% stuff

RD : height

RD : widthfactor

RD : oblique angle

RD : Tracking percentage

RL : Is backwards (0/1)

RL : Is upside down (0/1)

RL : Is vertical (0/1)

RL : Is underlined (0/1)

RL : Is overlined (0/1)

PS : Font filename

PS : Big font filename
XLINE 12

3 RD : a point on the construction line

Open Design Specification for .dwg files

275



3 RD : another point
RAY 13

3 RD : a point on the construction line

3 RD : another point
These "SUBENT" items indicate changes for subsequently drawn items.
SUBENT_COLOR 14

RL : color
SUBENT_LAYER 16

RL : layer index
SUBENT_LINETYPE 18

RL : linetype index, 0xFFFFFFFF for bylayer, 0xFFFFFFFE for byblock
SUBENT_MARKER 19

RL : marker index
SUBENT_FILLON 20

RL : fill on if 1, off if 0
SUBENT_TRUECOLOR 22

RC : red

RC : green

RC : blue
SUBENT_LNWEIGHT 23

RL : line weight
SUBENT_ LTSCALE 24

RD : linetype scale
SUBENT_ THICKNESS 25

RD : thickness
SUBENT_ PLSTNAME 26

RL : type, BYLAYER == 0, BYBLOCK == 1, DICT_DEFAULT == 2, PLOTSTYLE_BY_ID == 3

RL : plot style index

Open Design Specification for .dwg files

276


PUSH_CLIP 27

3 RD : extrusion

3 RD : clip boundary origin

RL : number of points

2 RD : 2D point, repeated number of points times

16 RD : clip boundary transformation matrix

16 RD : inverse block transformation matrix

RL : front clip on

RL : back clip on

RD : front clip

RD : back clip

RL : draw boundary (0/1)
POP_CLIP 28

empty
PUSH_MODELXFORM 29

16 RD : transformation matrix
PUSH_MODELXFORM2 30

16 RD : transformation matrix

? : unknown data
POP_MODELXFORM 31

empty
Polyline with normal 32

RL : number of points

3 RD : a point (repeat "number of points" times)

RD : normal vector

LWPOLYLINE 33

RL : number of bytes containing the LWPOLYLINE entity data

B : bytes containing the LWPOLYLINE entity data. This excludes the common entity data.
More specifically: it starts at the LWPOLYLINE flags (BS), and ends with the width
array (BD).

RC : Unknown byte

RC : Unknown byte

RC : Unknown byte


Open Design Specification for .dwg files

277


Sub entity material 34

H: Material handle

Sub entity mapper 35

RL : dummy value 1

RL : dummy value 2

RL : projection

RL : U-tiling

RL : V-tiling

RL : Auto transform

RL : dummy value 3

Unicode text 36
Identical to text (10), but with the text string type being encoded in unicode.

Unknown 37

Empty
Unicode text 2
Identical to text 2 (11), but with the text string type being encoded in unicode and some minor
additions:

3 RD : start point

3 RD : normal

3 RD : text direction

PUS : string, padded to 4 byte boundary

RL : length of string, -1 if zero terminated

RL : "raw"; 0 if raw, 1 if not.  raw means don't interpret %% stuff

RD : height

RD : widthfactor

RD : oblique angle

RD : Tracking percentage

RL : Is backwards (0/1)

RL : Is upside down (0/1)

RL : Is vertical (0/1)

RL : Is underlined (0/1)

RL : Is overlined (0/1)
True type font descriptor fields {

RL : Is bold (0/1)

Open Design Specification for .dwg files

278



RL : Is italic (0/1)

RL : Charset (contains 1 byte)

RL : Pitch and family (contains 1 byte)

PUS : Type face

PUS : Font filename
}

PUS : Big font filename



Open Design Specification for .dwg files

279


- END OF DOCUMENT -