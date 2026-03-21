# Chapter 28: Extended Entity Data (Extended Object Data)

28 Extended Entity Data
(Extended Object Data)
EED directly follows the entity handle.
Each application's data is structured as follows:
|Length|Application handle|Data items|
Length is a bitshort indicating the length of the data for an app, not including itself, the bit-pair, or the app
table handle. The above format repeats until a length of zero is found.
The application handle is a standard table handle reference: 0101|4-bit length|handle bytes|
Each data item has a 1-byte code (DXF group code minus 1000) followed by the value.  It looks like
there's no bit-pair coding within the data; that would throw off the length value (it would need to count
bits, too).  The form of the value is listed below for each type:
0 (1000)   String.
R13-R2004:  1st byte of value is the length N; this is followed by a 2-byte short
indicating the codepage, followed by N single-byte characters.
R2007+: 2-byte length N, followed by N Unicode characters (2 bytes each).

1 (1001)   This one seems to be invalid; can't even use as a string inside braces.  This
would be a registered application that this data relates to, but we've already had that above, so
it would be redundant or irrelevant here.

2 (1002)   A '{' or '}'; 1 byte; ASCII 0 means '{', ASCII 1 means '}'

3 (1003)   A layer table reference.  The value is the handle of the layer; it's 8 bytes --
even if the leading ones are 0.  It's not a string; read it as hex, as usual for handles.
(There's no length specifier this time.) Even layer 0 is referred to by handle here.

4 (1004)   Binary chunk.  The first byte of the value is a char giving the length; the bytes
follow.

5 (1005)   An entity handle reference.  The value is given as 8 bytes -- even if the leading
ones are 0. It's not a string; read it as hex, as usual for handles.  (There's no length
specifier this time.)

10 - 13 (1010 - 1013)
Points; 24 bytes (XYZ) -- 3 doubles

40 - 42 (1040 - 1042)
Reals; 8 bytes (double)

70 (1070)  A short int; 2 bytes
71 (1071)  A long  int; 4 bytes

Open Design Specification for .dwg files

270