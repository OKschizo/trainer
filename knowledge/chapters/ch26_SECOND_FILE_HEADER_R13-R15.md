# Chapter 26: SECOND FILE HEADER (R13-R15)

26 SECOND FILE HEADER (R13-R15)
### 26.1 Beginning sentinel
{0xD4,0x7B,0x21,0xCE,0x28,0x93,0x9F,0xBF,0x53,0x24,0x40,0x09,0x12,0x3C,0xAA,0x01 };

RL : size of this section

L : Location of this header (long, loc of start of sentinel).

RC : "AC1012" or "AC1014" for R13 or R14 respectively

RC : 6 0's

B : 4 bits of 0

RC : 0x18,0x78,0x01,0x04 for R13, 0x18,0x78,0x01,0x05 for R14


RC : 0

L : header address

L : header size

RC : 1

L : class address

L : class data size

RC : 2

L : Object map address (natural table)

L : Object map size

RC : 3

L : Address of unknown section 3

L : size of that section


S : 14 (# of handle records following)


RC : size of (valid chars in) handseed

RC : 0

RC : "size" characters of the handle


RC : size of (valid chars in) block control objhandle

RC : 1

RC : "size" characters of the handle


RC : size of (valid chars in) layer control objhandle

RC : 2

RC : "size" characters of the handle

Open Design Specification for .dwg files

265




RC : size of (valid chars in) shapefile control objhandle

RC : 3

RC : "size" characters of the handle


RC : size of (valid chars in) linetype control objhandle

RC : 4

RC : "size" characters of the handle


RC : size of (valid chars in) view control objhandle

RC : 5

RC : "size" characters of the handle


RC : size of (valid chars in) ucs control objhandle

RC : 6

RC : "size" characters of the handle


RC : size of (valid chars in) vport control objhandle

RC : 7

RC : "size" characters of the handle


RC : size of (valid chars in) reg app control objhandle

RC : 8

RC : "size" characters of the handle


RC : size of (valid chars in) dimstyle control objhandle

RC : 9

RC : "size" characters of the handle


RC : size of (valid chars in) viewport entity header objhandle

RC : 10

RC : "size" characters of the handle


RC : size of (valid chars in) dictionary objhandle

RC : 11

RC : "size" characters of the handle


RC : size of (valid chars in) default multi-line style objhandle

RC : 12

RC : "size" characters of the handle

Open Design Specification for .dwg files

266




RC : size of (valid chars in) group dictionary objhandle

RC : 13

RC : "size" characters of the handle


CRC


RC : 8 bytes of junk (R14 only).  Note that the junk is counted in the size of this
section at the start.

Ending sentinel
{0x2B,0x84,0xDE,0x31,0xD7,0x6C,0x60,0x40,0xAC,0xDB,0xBF,0xF6,0xED,0xC3,0x55,0xFE}

Open Design Specification for .dwg files

267