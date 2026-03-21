# Chapter 16: Data section AcDb:AppInfo

16 Data section AcDb:AppInfo
Contains information about the application that wrote the .dwg file. This section is optional.
Section property
Value
Name
AcDb:AppInfo
Compressed
1
Encrypted
0
Page size
0x80
The AppInfo format depends on the application version (Acad version that wrote the file) in the file
header. So a R18 .dwg file might have an R21 AppInfo section.
### 16.1 R18
In R18 the app info section consists of the following fields. Strings are encoded as a 16-bit length,
followed by the character bytes (0-terminated).

Type
Length
Description
String
2 + n
App info name, ODA writes “AppInfoDataList”
UInt32
4
Unknown, ODA writes 2
String
2 + n
Unknown, ODA writes “4001”
String
2 + n
App info product XML element, e.g. ODA writes
“<ProductInformation name ="Teigha" build_version="0.0"
registry_version="3.3" install_id_string="ODA"
registry_localeID="1033"/>"
String
2 + n
App info version, e.g. ODA writes "2.7.2.0".

Open Design Specification for .dwg files

97


### 16.2 R21-27
In R21 (and also R24, R27) the app info section consists of the following fields. Strings are encoded as a
16-bit length, followed by the character bytes (0-terminated), using unicode encoding (2 bytes per
character).
Type
Length
Description
UInt32
4
Unknown (ODA writes 2)
String
2 + 2 * n +
2
App info name, ODA writes “AppInfoDataList”
UInt32
4
Unknown (ODA writes 3)
Byte[]
16
Version data (checksum, ODA writes zeroes)
String
2 + 2 * n +
2
Version
Byte[]
16
Comment data (checksum, ODA writes zeroes)
String
2 + 2 * n +
2
Comment
Byte[]
16
Product data (checksum, ODA writes zeroes)
String
2 + 2 * n +
2
Product
String
2 + n
App info version, e.g. ODA writes "2.7.2.0".


Open Design Specification for .dwg files

98