import outlinesunleashed.exceptions as ex


class OldOutlineNode:
    """
    Wrapper class for node in an xml tree of an outline. Makes for easier handling of nodes and encapsulates some
    common functionality like get at text and notes fields.

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
    """

    # List of expected properties and flag to say whether mandatory or optional
    expected_properties = {
        'attrib': True,
        'tag': True,
        'text': False,
        'tail': False
    }

    # List of expected attributes (within attrib property) and flag to say whether mandatory or optional
    # and if optional what is default value.
    expected_attributes = {
        'text': (False, ''),
        '_note': (False, '')
    }

    max_len_for_short = 15

    def __init__(self, node):

        # Check that expected things are here but don't get carried away with checking :-)
        # We need to confirm that there is a tag property and an attrib property but we don't
        # need to check whether the attributes are present in the attrib dict property as we
        # deal with missing attributes within get_attribute() robustly.

        mandatory_properties = list(filter(lambda x: OldOutlineNode.expected_properties[x] is True,
                                           OldOutlineNode.expected_properties.keys()))
        missing_properties = list(filter(lambda x: not hasattr(node, x), mandatory_properties))
        if len(missing_properties) > 0:
            missing_property_list_string = ', '.join(missing_properties)
            raise ex.MalformedOutline('Missing properties of node: {}'.format(missing_property_list_string))

        # Don't check tag is right value before checking it exists (above)!
        if node.tag != 'outline':
            raise ex.MalformedOutline('Non outline tag for outline node {} ({})'.format(node, node.tag))

        self._node = node

    def __repr__(self):
        text_display_string = self._process_string_for_display(self.text)
        note_display_string = self._process_string_for_display(self.note)

        return 'OutlineNode(text: \'{}\', note: \'{}\')'.format(text_display_string, note_display_string)

    def __str__(self):
        text_display_string = self._process_string_for_display(self.text)
        note_display_string = self._process_string_for_display(self.note)
        return 'text: "{}", note: "{}"'.format(text_display_string, note_display_string)

    def __getitem__(self, item):
        return OldOutlineNode(self._node[item])

    def __len__(self):
        return len(self._node)

    def _get_attribute(self, attribute_name):
        if attribute_name not in OldOutlineNode.expected_attributes:
            raise ValueError('get_attribute called for non-expected attribute {}'.format(attribute_name))

        mandatory, default = OldOutlineNode.expected_attributes[attribute_name]
        if attribute_name not in self._node.attrib or self._node.attrib[attribute_name] is None:
            if mandatory is True:
                raise ex.MalformedOutline('No {} field for node {}'.format(attribute_name, self._node))
            else:
                return default

        return self._node.attrib[attribute_name]

    @staticmethod
    def _process_string_for_display(long_string):
        # Remove leading and trailing whitespace and line breaks
        string_stripped = long_string.strip().replace('\n', ' ').replace('\r', '')

        is_truncated = True if len(string_stripped) > OldOutlineNode.max_len_for_short else False
        length = min(len(string_stripped), OldOutlineNode.max_len_for_short)

        ellipsis = '...' if is_truncated else ''
        display_string = string_stripped[:length]
        return_string = display_string + ellipsis

        return return_string

    @property
    def text(self):
        return self._get_attribute('text')

    @property
    def short_text(self):
        return self._process_string_for_display(self.text)

    @property
    def note(self):
        return self._get_attribute('_note')

    @property
    def short_note(self):
        return self._process_string_for_display(self.note)
