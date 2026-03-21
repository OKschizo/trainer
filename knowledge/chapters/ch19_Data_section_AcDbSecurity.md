# Chapter 19: Data section AcDb:Security

19 Data section AcDb:Security
Section property
Value
Name
AcDb:Security
Compressed
1
Encrypted
0
Page size
0x7400
This section was introduced in R18. The AcDb:Security section is optional in the file—it is present if the
file was saved with a password.
R18: The section is present in the file if the SecurityType entry at location 0x18 in the file is greater than
0.
Strings are prefixed with a 32-bit length (not zero terminated).

Type
Length
Description
Int32
4
Unknown (ODA writes 0x0c)
Int32
4
Unknown (ODA writes 0x0)
Int32
4
Unknown (ODA writes 0xabcdabcd)
UInt32
4
Cryptographic provider ID
String32
4 + n
Croptographic provider name
UInt32
4
Algorithm ID
UInt32
4
Encryption key length
Int32
4
Buffer size of following buffer
Byte[]
n
Encrypted string "SamirBajajSamirB"
Using the indicated provider and algorithm (and password obtained from the client for this drawing), the
encryption password can be verified by decrypting the Test Encrypted Sequence. If the result is

Open Design Specification for .dwg files

102


"SamirBajajSamirB" (0x53, 0x61, 0x6d, 0x69, 0x72, 0x42, 0x61, 0x6a, 0x61, 0x6a, 0x53, 0x61, 0x6d,
0x69, 0x72, 0x42), then the password is correct.
The algorithm is RC4 (this is a symmetric encryption algorithm). The algorithm is used in DWG file
format version 2004 and 2007.
Parameters are:
- Password (provided by user).
- Provider id: e.g. 0x0d.
- Provider name: e.g. "Microsoft Base DSS and Diffie-Hellman Cryptographic Provider".
- Key length: default value is 40.
- Flags: no salt.
The password bytes (convert unicode password string to bytes, 2 bytes per character) are hashed (using
MD5). A session key is derived from the password hash (using no salt). This session key is then used for
both encryption and decryption.

Open Design Specification for .dwg files

103