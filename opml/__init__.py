"""
OPML is a way of representing an outline, which is a hierarchical (mostly) textual tree structure used by outliners,
some mind mapping tools and various other applications.

See http://dev.opml.org/ for details of the OPML spec.
See https://docs.python.org/3.6/library/xml.etree.elementtree.html for details of ElementTree and associated objects.

This implementation is intended to be a fair implementation of the OPML language, but with one eye on the
requirements of Outlines Unleashed.  Initially it isn't intended to be a full and comprehensive implementation
of OPML but just enough to support the functionality of Outlines Unleashed.  It is envisaged however that over time
this will become a robust and complete implementation of the OPML language.

Because OPML is an XML language, the Outline class (and related classes such as OutlineNode) builds on existing
XML parsing capability, and in this case that is in the form of xml.etree.ElementTree (part of Python Standard Library)
as the method to store and manipulate the xml tree which forms the outline.

The Outline class within this library will support the reading in of a file of supplied pathname which is expected to
be in OPML format.

In general it isn't expected that the file will be fully validated as OPML as, depending upon the
size of the file, may take some time, and particularly if OPML files are being processed from many users at a time
(which is the intention with the web app implementation of Outlines Unleashed, when it is launched) this may be a
significant burden.

Rather, if a problem occurs while parsing or processing the data in the file, it will be raised at the time of
discovery.

However, there will be the ability to override this default behaviour and validate on reading if required.

While this library implements the ability to parse a text file formatted as OPML, an outline (i.e. a
hierarchy of textual nodes) could theoretically be represented in a number of different ways (e.g. indented text,
indented bullets from an MS Word document and many others). So in order to support the needs of Outlines Unleashed,
this library will include the ability to create an internal outline structure which is identical to one created from
an OPML document, but which was in fact created using one of a number of supported formats, with that number growing
over time based on imagination and demand.

The main classes defined within this library are:

OutlineNode: A wrapper class which takes an <outline> XML Element and overlays functionality specific to OPML,
             such as the ability to include a note field.

Outline: A representation of an object which is derived from OPML, an XML markup language. This class will read in
         an XML file in OPML format (or from other sources) and provide overlayed functionality to process it as an
         OPML structured document.
"""