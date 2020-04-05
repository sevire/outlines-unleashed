"""
Tests that the reading and parsing of an OPML file works correctly.  This includes reading the underlying XML
file and then the OPML structure which sits on top of that.

Test cases include:
- Badly formed file (not xml)
- Un-paired tags
"""