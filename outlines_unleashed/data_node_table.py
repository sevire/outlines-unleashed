class DataNodeTable:
    """
    Generic representation of fields extracted from an outline into a set of data records with fields as
    defined within the Data Node Descriptor.

    This will almost always be the format in which the data for a node is extracted before being transformed
    into a format for output.  There may be some exceptions, for example where the output format is also a
    hierarchical format and the translation to a table and then back to hierarchical is un-natural and
    not appropriate.

    Current thinking is that, for example, with a Skeleton PowerPoint outline for which the outline structure
    is quite natural, even here there will be an interim Data Node Table format because this will allow
    multiple use cases to define PPT slide decks in different ways but all go through a common intermediate
    format to allow driving of the PPT output.  So it may be that all use cases will employ the DNT as
    the extraction format.
    """