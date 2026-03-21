# Chapter 14: Data section AcDb:Preview

14 Data section AcDb:Preview
### 14.1 PRE-R13C3
Section property
Value
Name
AcDb:Preview
Compressed
1
Encrypted
0 if not encrypted, 1 if encrypted.
Page size
If a thumbnail image is present, then header + image data size + sentinels and size
info (0x40 bytes) + section alignment padding
If no thumbnail image is present, the value is 0x400.


The BMP (or, sometimes, WMF) image of this file, if any. Only stored here for pre-R13C3 files. Later
files place the data at the end. The format of this data is discussed in the section illustrating where R13C4
and beyond store it.
### 14.2 R13C3 AND LATER
Start sentinel
{0x1F,0x25,0x6D,0x07,0xD4,0x36,0x28,0x28,0x9D,0x57,0xCA,0x3F,0x9D,0x44,0x10,0x2B }

overall size
RL

overall size of image area

imagespresent
RC

counter indicating what is present here
Repeat imagespresent times {

Code
RC

code indicating what follows
if (code==1) {

header data start
RL

start of header data

header data size
RL

size of header data
}
if (code == 2) {

start of bmp
RL

start of bmp data

size of bmp
RL

size of bmp data
}
if (code == 3) {

Open Design Specification for .dwg files

94



start of wmf
RL

start of wmf data

size of wmf
RL

size of wmf data
}
}
if (bmpdata is present) {

bmp data
RC

(there are “size of bmp” bytes of data)
}
if (wmfdata is present) {

wmf data
RC

(there are “size of wmf” bytes of data)
}
end sentinel
0xE0,0xDA,0x92,0xF8,0x2B,0xc9,0xD7,0xD7,0x62,0xA8,0x35,0xC0,0x62,0xBB,0xEF,0xD4 };


Open Design Specification for .dwg files

95