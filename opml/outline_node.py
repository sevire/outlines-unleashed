class OutlineNode():
    def __init__(self, xml_node):
        """
        Wrapper class for node in an xml tree of an outline. Makes for easier handling of nodes and encapsulates some
        common functionality like get at text and notes fields.

        NOTE: This implementation favours composition over extension.  To extend Element

        What we expect to see:

        - PROPERTIES:
          - tag    = 'outline': All nodes are xml elements of type outline.
          - text              : An xml element can contain sub-elements and text.  The 'text' property contains the text
                                after the start tag (loosely).  Not relevant for outline and this shouldn't contain anything
                                but white space.
          - tail              : (see text property). The 'tail' property contains the text between the end tag and the
                                next start tag (loosely).  Not relevant for outline and this shouldn't contain anything.
          - attrib = dict     : xml attributes (see below)

        - ATTRIBUTES (within attrib dict)
          - 'text'            : The text of the outline node. NOT to be confused with the text property.
          - '_note'           : The notes property of the outline node (used by OmniOutliner - not sure about others).

            :param xml_node:
            """