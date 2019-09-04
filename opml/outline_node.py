from opml import outline_utilities as outil
from xml.etree.ElementTree import Element
from opml.opml_exceptions import MalformedOutline


class OutlineNode:
    """
    This is a wrapper class for an outline element within an OPML (XML) file read in via xml.etree.ElementTree.

    It provides a simplified way of accessing data within an outline without having to negotiate the complexities
    of generic XML handling.  For example, the 'tail' field is the text between the end of the definition of
    sub-elements and the end tag for this element.  This is meaningless for outlines.

    A user needs the following:

    - The text value for this node (in the text attribute)
    - The notes value for this node (in the _note attribute)
    - Access to the children of this node (as OutlineNode objects)

    NOTE: This implementation favours composition over extension, as the purpose of this implementation is to
    hide the complexity of generic XML nodes and just expose the simple interface required for an outline.
    """
    max_len_for_short = 15

    def __init__(self, outline_node: Element):
        """
        Do some checking that we have been passed in the right type of object (should be an xml.etree.Element
        object with tag of outline and a few other things.

        Everything else is done through methods which expose the properties to the user from the node.

        :param outline_node:
        """
        if outil.is_valid_tag(outline_node):
            outil.get_valid_attribute(outline_node, 'text')
            self._node = outline_node
        else:
            raise(MalformedOutline(f'Invalid element <{outline_node.tag}> in outline'))

    def __getitem__(self, index):
        return OutlineNode(self._node[index])
        # ToDo: Identical <outline> nodes should return identical OutlineNodes (pass the 'is' test)

    def __eq__(self, other: Element):
        if self._node is other._node:
            return True
        else:
            return False

    def __len__(self):
        """
        An important element of turning this object into an list-like object.  Implementing this and __getitem__
        allows for constructs such as:
            list(outline_node)
        and
            for child in outline_node

        :return:
        """
        return len(self._node)

    def list_all_nodes(self, ancestry=None):
        local_ancestry = [] if ancestry is None else ancestry
        yield (self, tuple(local_ancestry))
        for child_number, a_child in enumerate(self):
            child_ancestry = local_ancestry.copy()
            child_ancestry.append(child_number+1)
            yield from a_child.list_all_nodes(child_ancestry)

    def total_sub_nodes(self):
        count = len(self) + 1
        for node in self:
            count += node.total_sub_nodes() - 1  # Need to compensate for adding 1 as it only applies to top node
        return count

    @property
    def text(self):
        """
        Access to the text attribute of an outline node.

        :return: The text attribute of self.node
        """
        return outil.get_valid_attribute(self._node, 'text')

    @property
    def note(self):
        """
        Access to the text attribute of an outline node.

        :return: The _note attribute of self.node
        """
        return outil.get_valid_attribute(self._node, '_note')

    def iter(self):
        return self.list_all_nodes()

    @property
    def ancestry(self):
        ancestry = None
        return ancestry

    @classmethod
    def create_outline_node(cls, outline_text='', outline_note=None, children_data=None):
        attrib = {}
        if outline_text is not None:
            attrib['text'] = outline_text

        if outline_note is not None:
            attrib['_note'] = outline_note

        element = Element('outline', attrib)
        if children_data is not None:
            for child_data in children_data:
                child_node = cls.create_outline_node(outline_text=child_data['text'], outline_note=child_data['note'])
                element.append(child_node)

        node = OutlineNode(element)

        return node

    def __str__(self):
        text_display_string = self._process_string_for_display(self.text)
        note_display_string = self._process_string_for_display(self.note)
        return 'OutlineNode: children: {}, text: "{}", note: "{}"'.format(len(self), text_display_string, note_display_string)

    def __repr__(self):
        text_display_string = self._process_string_for_display(self.text)
        note_display_string = self._process_string_for_display(self.note)

        return 'OutlineNode(text: \'{}\', note: \'{}\')'.format(text_display_string, note_display_string)

    @staticmethod
    def _process_string_for_display(long_string):
        # Remove leading and trailing whitespace and line breaks
        string_stripped = long_string.strip().replace('\n', ' ').replace('\r', '')

        is_truncated = True if len(string_stripped) > OutlineNode.max_len_for_short else False
        length = min(len(string_stripped), OutlineNode.max_len_for_short)

        ellipsis = '...' if is_truncated else ''
        display_string = string_stripped[:length]
        return_string = display_string + ellipsis

        return return_string


