# Chapter 8: R2018 DWG FILE FORMAT ORGANIZATION

8 R2018 DWG FILE FORMAT ORGANIZATION
The AutoCAD 2018 format is almost identical to the 2013 format. Structurally they are identical.
Below is a summary of the changes:
 Three shorts (int16) with value zero have been added to end of the auxiliary file header
(see chapter 27).
 In the AcDb:Header nothing changed, but note that the unknown 32-bit int at the start,
directly following the section size that was present for R2010/R2013 for acad
maintenance version greater than 3, is also present for R2018 (see chapter 9).
 Additions/changes in the following entities:
o ACAD_PROXY_ENTITY (paragraph 20.4.90),
o ATTRIB (paragraph 20.4.4),
o ATTDEF (paragraph 20.4.5),
o MTEXT (see paragraph 20.4.46).
 Object MLINESTYLE (paragraph 20.4.73) references line types in its element by their
handle rather than by index.

Open Design Specification for .dwg files

72