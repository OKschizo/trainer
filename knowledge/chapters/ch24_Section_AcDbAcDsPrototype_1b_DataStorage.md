# Chapter 24: Section AcDb:AcDsPrototype_1b (DataStorage)

24 Section AcDb:AcDsPrototype_1b (DataStorage)
At this moment (December 2012), this sections contains information about Acis data (regions, solids).
The data is stored in a byte stream, not a bit stream like e.g. the objects section.
The data store contains several data segments, and index segments that contain lookup information for
finding the data segments and objects within these data segments. The file header contains the stream
position of the segment index file segment and the segment indexes for the schema index/data
index/search file segments. The segment index file segment is a lookup table for finding the stream
position of a file segment by its segment index.
In paragraph 24.3 the default contents of this section is shown when empty.
### 24.1 File header
Version
Field
type
DXF
group
code
Description

UInt32

File signature

Int32

File header size

Int32

Unknown 1 (always 2?)

Int32

Version (always 2?)

Int32

Unknown 2 (always 0?)

Int32

Data storage revision

Int32

Segment index offset (the stream off set from the data store’s stream start
position). See paragraph 24.2.2.1 for the segment index file segment.

Int32

Segment index unknown

Int32

Segment index entry count

Int32

Schema index segment index. This is the index into the segment index entry
array (see paragraph 24.2.2.1) for the schema index file segment (see
paragraph 24.2.2.4).

Int32

Data index segment index. This is the index into the segment index entry array
(see paragraph 24.2.2.1) for the data index file segment (see paragraph
24.2.2.2).

Int32

Search segment index

Int32

Previous save index

Int32

File size
### 24.2 File segment
A file segment is a segment containing data. There are several types of file segments containing
different types of data.

Open Design Specification for .dwg files

253


At the beginning of each segment there is a header. Then there are a number of data bytes specific
for the type of file segment. At the end there are padding bytes so the total segment size including
the header is a multiple of 0x40 bytes (AutoCAD writes a multiple of 0x80 bytes). The padding
consists of an array of 0x70 values.
#### 24.2.1 Header
Version
Field
type
DXF
group
code
Description

Int16

Signature (always 0xd5ac?)

byte[6]

Name (6 bytes). Names for the several file segments are:

Segment index: “segidx”

Data index: “datidx”

Data: “_data_”

Schema index: “schidx”

Schema data: “schdat”

Search: “search”

Blob01: “blob01”

Int32

Segment index

Int32

Unknown 1 (0 or 1? 1 in blob01 segment).

Int32

Segment size (multiple of 0x40 bytes (AutoCAD uses 0x80), padded with
0x70 values).

Int32

Unknown 2 (always 0?)

Int32

Data storage revision

Int32

Unknown 3 (always 0?)

Int32

System data alignment offset (calculate the stream position by shifting left 4
bits and adding to the file segment’s stream start position). This offset is used
for schema index and schema data segments. So the name “system data” seems
to refer to schema index/schema data.

Int32

Object data alignment offset (calculate the stream position by shifting left 4
bits and adding to the file segment’s stream start position). This offset is used
for the data segment.

byte[8]

8 alignment bytes (always 8 x 0x55?).
#### 24.2.2 Sub types
In the following sub paragraphs all file segment sub types are described. Their data directly follows upon
the file segment header.
##### 24.2.2.1 Segment index file segment
This file segment contains information about each file segment’s offset and size in the stream.
The segment is looked up by the index in the array.
Version
Field
type
DXF
group
Description

Open Design Specification for .dwg files

254


code



Begin repeat segment index entry count (as present in the file header, see
paragraph 24.1)

UInt64

Offset. This is the offset from the data store’s stream start position.

UInt32

Size



End repeat segment index entry count

##### 24.2.2.2 Data index file segment
This file segment contains index entries for objects within the data file segment (see paragraph
24.2.2.3).
Version
Field
type
DXF
group
code
Description

Int32

Entry count

Int32

Unknown (always 0?)



Begin repeat of entries (entry count)

UInt32

Segment index (0 means stub entry and can be ignored).

UInt32

Local offset. This is a local offset in the stream, relative to the file segment’s
stream start position. This points to a data file segment, see paragraph 24.2.2.3.

UInt32

Schema index



End repeat of entries

##### 24.2.2.3 Data file segment
The data file segment basically contains a byte array, of which the storage type depends on the size:

data records, where each data record is a byte array. Relatively small amounts of data are stored
directly in the data file segment (up to 0x40000 bytes).

A data blob references, where each blob reference references one or more other blob file segments.
These other file segments represent the pages of the blob (paragraph 24.2.2.3.1). Large byte arrays
are stored into multiple of these pages (more than 0x40000 bytes, max 0xfffb0 bytes per page).
For each entity’s binary data stored in the data file segment entries have to be created in the schema
search data. See paragraph 24.2.2.7.1. When reading the schema search data can be ignored.
For each ACIS entity (REGION, 3DSOLID), a data record is created with the SAB stream of the object.
More detailed description of the ACIS/SAB data falls outside the scope of this document. The SAB
stream bytes are prefixed with the ASCII encoded bytes of the string “ACIS BinaryFile”. When for an
ACIS entity a SAB stream is created from SAT, then if the version >= 21800, the bytes are post fixed
with the ASCII encoded bytes of the string “End-of-ASM-data”, otherwise “End-of-ACIS-data”.

Open Design Specification for .dwg files

255



Version
Field
type
DXF
group
code
Description



Begin repeat (data record) headers. Repeats number of local offsets times (this
is read earlier from the data index, see paragraph 24.2.2.2). For a particular
data file segment, find all data index entries with the segment’s segment index
and take the local offsets.



Move the stream position according to the current header local offset, which is
relative to this data file segments stream start position.

UInt32

Entry size

UInt32

Unknown (ODA writes 1)

UInt64

Handle

UInt32

Local offset, a stream offset relative to the data start marker (just after this list
of data record headers).



End repeat (data record) header offsets



Data start marker, this is the beginning of all data records.



Begin repeat header entries (that were read above)



Each data record starts at the data start marker position + local offset. The
maxRecordSize of the record is the difference between two consecutive stream
offsets. For the last data record the size is the file segment header’s (object
data alignment offset << 4) + segment size - the record’s stream offset (i.e. the
file segment end position – the record start position).

UInt32

dataSize



If ((dataSize + 4) <= maxRecordSize)

Byte[]

Data record’s bytes of length dataSize



Else If (dataSize == 0xbb106bb1)



Data blob reference record, see paragraph 24.2.2.3.1



End If



End repeat header entries
24.2.2.3.1
Data blob reference record
A data blob reference references one or more other file segments. These other file segments represent the
pages of the blob. Each page is stored in a Blob01 file segment, see paragraph 24.2.2.4.
Version
Field
type
DXF
group
code
Description

UInt64

Total data size

UInt32

Page count

UInt32

Record size (the size of  this data blob reference record

UInt32

Page size

UInt32

Last page size

UInt32

Unknown 1 (ODA writes 0)

Open Design Specification for .dwg files

256



UInt32

Unknown 2 (ODA writes 0)



Begin repeat page count

UInt32

Segment index. The page’s blob01 file segment stream position can be found
by a lookup in the segment index file segment using the segment index, see
paragraph 24.2.2.1.

UInt32

Size



End repeat page count
##### 24.2.2.4 Blob01 file segment
Version
Field
type
DXF
group
code
Description

UInt64

Total data size

UInt64

Page start offset

Int32

Page index

Int32

Page count

UInt64

Page data size

byte[]

Binary data (byte array) of size Page data size
##### 24.2.2.5 Schema index file segment
The schema index contains references to objects within the schema data file segment, see
paragraph 24.2.2.6.
Version
Field
type
DXF
group
code
Description

UInt32

Unknown property count

UInt32

Unknown (0)



Begin repeat schema unknown property count

UInt32

Index (starting at 0)

UInt32

Segment index into the segment index file segment entry table (paragraph
24.2.2.1) of the schema data file segment (paragraph 24.2.2.6)

UInt32

Local offset of the unknown schema property. This is a local offset in the
stream, relative to the schema data file segment’s stream start position.



End repeat schema unknown property count

Int64

Unknown (0x0af10c)

UInt32

Property entry count

UInt32

Unknown (0)



Begin repeat property entry count

UInt32

Segment index into the segment index file segment entry table (paragraph
24.2.2.1) of the schema data file segment (paragraph 24.2.2.6).

UInt32

Local offset of the schema property. This is a local offset in the stream, relative
to the schema data file segment’s stream start position.

UInt32

Index



End repeat property entry count

Open Design Specification for .dwg files

257


##### 24.2.2.6 Schema data file segment
The schema data file segment contains unknown properties and schemas. The stream offsets of
these objects from the start of this file segment are found in the schema index, see paragraph
24.2.2.5.
Version
Field type
DXF
group
code
Description



Begin repeat schema unknown properties in the associated schema index file
segment (paragraph 24.2.2.4), where the property’s segment index is equal to
this file segment’s segment index (found in the header).

UInt32

Data size

UInt32

Unknown flags



End repeat schema unknown properties



Begin repeat schema entries in the associated schema index file segment
(paragraph 24.2.2.4), where the property’s segment index is equal to this file
segment’s segment index (found in the header).



A schema, see paragraph 24.2.2.6.1. The stream position is the file segment’s
start position + the schema entry’s local offset.



End repeat schema entries

Uint32

Property name count



Begin repeat property name count

AnsiString

Property name (zero byte delimited). These names are referred to by the
schema’s schema property’s name index (paragraph 24.2.2.6.1.1). Name
strings can be shared between multiple schema properties this way. See
paragraph 24.2.2.6.1 for details about the schema.



End repeat property name count
24.2.2.6.1
Schema
A schema is a collection of name value pairs, where the value can have a number of types.
Version
Field
type
DXF
group
code
Description

UInt16

Index count



Begin repeat index count

UInt64

Index



End repeat index count

UInt16

Property count



Begin repeat property count



Schema property, see paragraph 24.2.2.6.1.1.



End repeat property count
####### 24.2.2.6.1.1 Schema property

Open Design Specification for .dwg files

258


This is a schema (see 24.2.2.6.1) property, having a name and a value of a certain type.
Version
Field
type
DXF
group
code
Description

UInt32
91
Property flags:

1 = Unknown 1 (if set then all other bits are cleared).

2 = Has no type.

8 = Unknown 2 (if set then all other bits are cleared).

UInt32
2
Name index. Index into a property names array in the schema data file segment
(see paragraph 24.2.2.6). In a DXF file the name is directly written instead of
indirectly through a table lookup.



If property flags bit 2 is NOT set

UInt32
280
Type (0-15)



If type == 0xe

UInt32

Custom type size



Else



The typeSize is looked up in the following array with the type being the index:
0, 0, 2, 1, 2, 4, 8, 1, 2, 4, 8, 4, 8, 0, 0, 0



End if type == 0xe



End If property flags bit 2 is NOT set



If property flags == 1

UInt32

Unknown1



Else if property flags == 8

UInt32

Unknown2



End if property flags == 8

UInt16

Property value count



If (typeSize != 0)

Byte[]

Property value, represented by a byte array of size typeSize.



End if (typeSize != 0)
##### 24.2.2.7 Search file segment
Version
Field
type
DXF
group
code
Description

UInt32

Schema count



Begin repeat schema count



Schema search data, see paragraph 24.2.2.7.1.



End repeat schema count
24.2.2.7.1
Schema search data
The purpose of this segment is unknown. It seems to contain redundant data coupling a (sort) index to the
objects in the data segment. When reading the schema search data can be ignored.

Open Design Specification for .dwg files

259


For each object stored in the data segment there has to be one item in the sorted index table (just start
numbering at 0 and increase by one for every next object). Also in the 2D index array one array has to be
present containing one entry for every object stored in the data segment. The object handle is stored,
together with the index that was also used in the sorted index table. When the schema search data is not
created, AutoCAD will ignore the entity.

Version
Field
type
DXF
group
code
Description

UInt32

Schema name index

UInt64

Sorted index count



Begin sorted index count

UInt64

Sorted index



End sorted index count



For clarity: below a 2D jagged array is described of an ID entry object,
containing itself a handle and an array of indexes.

UInt32

ID indexes count (for the set of ID indexes).



If ID indexes count > 0

UInt32

Unknown (0)



Begin repeat ID indexes count

UInt32

ID index count



Begin repeat ID index count (in this loop the ID entry object is serialized)

UInt64

Handle of the object present in the data segment (see paragraph 24.2.2.3).

UInt64

Index count



Begin repeat index count

UInt64

Index (same as Sorted index value above). The ODA only writes one index per
handle.



End repeat index count



End repeat ID index count



End repeat ID indexes count



End If ID indexes count > 0
### 24.3 Default contents
Below is a dump of the default contents (i.e. when there is no data in the Data Storage section).

schemas {
item {
index: 0
name: "AcDb3DSolid_ASM_Data"
indexes {
item: 0,
item: 1,
}

Open Design Specification for .dwg files

260


propertyDescriptors {
}
properties {
item {
flags: 0
nameIndex: 4294967295
type: 10
customTypeSize: 0
typeSize: 8
unknown1: 0
unknown2: 0
propertyValues {
item: {02, 00, 00, 00, 00, 00, 00, 00},
item: {03, 00, 00, 00, 00, 00, 00, 00},
}
name: "AcDbDs::ID"
},
item {
flags: 0
nameIndex: 4294967295
type: 15
customTypeSize: 0
typeSize: 0
unknown1: 0
unknown2: 0
propertyValues {
}
name: "ASM_Data"
},
}
},
item {
index: 1
name: "AcDbDs::TreatedAsObjectDataSchema"
indexes {
}
propertyDescriptors {
}
properties {
item {
flags: 0
nameIndex: 4294967295
type: 1
customTypeSize: 0
typeSize: 0
unknown1: 0
unknown2: 0
propertyValues {
}
name: "AcDbDs::TreatedAsObjectData"
},
}
},
item {
index: 2
name: "AcDbDs::LegacySchema"
indexes {
}
propertyDescriptors {
}
properties {

Open Design Specification for .dwg files

261


item {
flags: 0
nameIndex: 4294967295
type: 1
customTypeSize: 0
typeSize: 0
unknown1: 0
unknown2: 0
propertyValues {
}
name: "AcDbDs::Legacy"
},
}
},
item {
index: 3
name: "AcDbDs::IndexedPropertySchema"
indexes {
}
propertyDescriptors {
}
properties {
item {
flags: 0
nameIndex: 4294967295
type: 1
customTypeSize: 0
typeSize: 0
unknown1: 0
unknown2: 0
propertyValues {
}
name: "AcDs:Indexable"
},
}
},
item {
index: 4
name: "AcDbDs::HandleAttributeSchema"
indexes {
}
propertyDescriptors {
}
properties {
item {
flags: 8
nameIndex: 4294967295
type: 7
customTypeSize: 0
typeSize: 1
unknown1: 0
unknown2: 1
propertyValues {
item: {00},
}
name: "AcDbDs::HandleAttribute"
},
}
},
}
schemaUnknownProperties {

Open Design Specification for .dwg files

262


item {
dataSize: 8
unknownFlags: 1
},
item {
dataSize: 8
unknownFlags: 1
},
item {
dataSize: 8
unknownFlags: 1
},
item {
dataSize: 8
unknownFlags: 0
},
}
schemaSearchDataList {
item {
schemaNameIndex: 0
sortedIndexes {
}
idIndexesSet {
item[] {
}
}
},
}
handleToDataRecord {
}


Open Design Specification for .dwg files

263