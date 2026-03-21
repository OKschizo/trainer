# Chapter 7: R2013 DWG FILE FORMAT ORGANIZATION

7 R2013 DWG FILE FORMAT ORGANIZATION
The 2013 format is based mostly on the 2010 format. The file header, summary info, page map, section
map, compression are the same as in R2004. The bit coding is the same as in R2010. Like the R2007
format, the data, strings and handles are separated in header and objects sections. The changes in the
Header section are minor (only 2 added fields).
A new data section was introduced, the data storage section (AcDb:AcDsPrototype_1b). At this moment
(December 2012), this sections contains information about Acis data (regions, solids). See chapter 24 for
more details about this section.
Note that at the point of writing (22 March 2013) known valid values for acad maintenance version are 6
and 8. The ODA currently writes value 8.


Open Design Specification for .dwg files

71