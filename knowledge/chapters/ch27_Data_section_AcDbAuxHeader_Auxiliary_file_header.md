# Chapter 27: Data section: AcDb:AuxHeader (Auxiliary file header)

27 Data section: AcDb:AuxHeader (Auxiliary file
header)
The auxiliary file header contains mostly redundant information and was introduced in R15.


RC : 0xff 0x77 0x01

RS : DWG version:
AC1010 = 17,
AC1011 = 18,
AC1012 = 19,
AC1013 = 20,
AC1014 = 21,
AC1015 (beta) = 22,
AC1015 = 23,
AC1018 (beta) = 24,
AC1018 = 25,
AC1021 (beta) = 26,
AC1021 = 27,
AC1024 (beta) = 28,
AC1024 = 29
AC1027 (beta) = 30,
AC1027 = 31,
AC1032 (beta) = 32,
AC1032 = 33

RS : Maintenance version

RL : Number of saves (starts at 1)

RL : -1

RS : Number of saves part 1 ( = Number of saves – number of saves part 2)

RS : Number of saves part 2 ( = Number of saves – 0x7fff if Number of saves > 0x7fff,
otherwise 0)

RL : 0

RS : DWG version string

RS : Maintenance version

RS : DWG version string

RS : Maintenance version

RS : 0x0005

RS : 0x0893

RS : 0x0005

RS : 0x0893

RS : 0x0000

RS : 0x0001

RL : 0x0000

RL : 0x0000

RL : 0x0000

Open Design Specification for .dwg files

268



RL : 0x0000

RL : 0x0000

TD : TDCREATE (creation datetime)

TD : TDUPDATE (update datetime)

RL : HANDSEED (Handle seed) if < 0x7fffffff, otherwise -1.

RL : Educational plot stamp (default value is 0)

RS : 0

RS : Number of saves part 1 – number of saves part 2

RL : 0

RL : 0

RL : 0

RL : Number of saves

RL : 0

RL : 0

RL : 0

RL : 0
R2018+

RS : 0

RS : 0

RS : 0



Open Design Specification for .dwg files

269