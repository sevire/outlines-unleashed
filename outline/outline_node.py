import copy

from xml.etree.ElementTree import Element, ElementTree
from outline import outline_utilities as outil
from outline.node_ancestry_item import NodeAncestryItem
from outline.node_ancestry_record import NodeAncestryRecord
from outline.opml_exceptions import MalformedOutline


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
    _max_len_for_short = 15

    def __init__(self, outline_node: Element):
        """
        Do some checking that we have been passed in the right type of object (should be an xml.etree.Element
        object with tag of outline and a few other things.

        ToDo: Re-factor signature of OutlineNode to remove tags and notes

        Everything else is done through methods which expose the properties to the user from the node.

        :param outline_node: Element with tag <outline> which the OutlineNode will wrap.
        """

        if outil.is_valid_tag(outline_node):
            outil.get_valid_attribute(outline_node, 'text')
            self._node = outline_node
        else:
            raise (MalformedOutline(f'Invalid element <{outline_node.tag}> in outline'))

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

    @classmethod
    def create_outline_node(cls, outline_text=None, outline_note=None, children_data=None):
        try:
            assert outline_text is None or isinstance(outline_text, str), f"outline_text must be a string not a {type(outline_text)}"
            assert outline_note is None or isinstance(outline_note, str), f"outline_text must be a string not a {type(outline_note)}"
        except AssertionError as err:
            raise ValueError(f"Node text and note fields must be of type str. {err}")

        attrib = {}
        if outline_text is not None:
            attrib['text'] = outline_text
        else:
            attrib['text'] = ''

        if outline_note is not None:
            attrib['_note'] = outline_note

        element = Element('outline', attrib)
        if children_data is not None:
            for child_data in children_data:
                child_node = cls.create_outline_node(outline_text=child_data['text'], outline_note=child_data['note'])
                element.append(child_node)

        node = OutlineNode(element)

        return node

    def add_node(self, text, note):
        # ToDo: Remove hard-coding around creation of new Outline Node (should be with other outline utilities)
        attributes = {'text': text, '_note': note}
        self._node.append(Element('outline', attributes))

    def validate(self, full_validation_flag):
        """
        Carry out validation on a given outline node.  This will involve things like checking that obligatory elements
        are present and that no unexpected elements are present.

        :param full_validation_flag:
        :return:
        """

        if full_validation_flag:
            #  Parse this and all sub-nodes and check all elements and all attributes are valide
            node_list = self.list_nodes()

            for node_entry in node_list:
                outline_node = node_entry.node()
                node_element = outline_node._node
                outil.validate_attributes(node_element)
            return True
        else:
            return True

    def iter_nodes(self, ancestry: NodeAncestryRecord = None):
        """
        Recursive generator which traverses the outline node tree in document order (depth first) and returns, for
        each node, a NodeAncestryRecord object which includes a reference to the node, and a tuple representing its
        child_number_ancestry (ie the list of child_numbers from root to the node, which uniquely determines the node's
        position in the tree.

        Note that the yield happens at the beginning of the function.  This means that we are yielding what we have
        been passed, not what we are generating in the function.

        (This took a while for me to get my head round and is important to the understanding of the convoluted nature
        of the recursion in the generator).

        When the generator reaches the leaf node of a given path, when the for loop is encountered, it will just fall
        straight through, and return to the last call, having already yielded the value for this call.

        On the first call, there is nothing to be passed in, so the generator creates a first node (bootstrapping
        itself, so to speak).

        :param ancestry:
        :return:
        """
        if ancestry is None:
            ancestry_record = NodeAncestryRecord([NodeAncestryItem(None, self)])
        else:
            ancestry_record = ancestry
            # node_ancestry_item_list = ancestry_record
        yield ancestry_record
        for child_number, a_child in enumerate(self):
            next_gen_ancestry = copy.copy(ancestry_record)
            next_gen_ancestry.append_node_to_ancestry(NodeAncestryItem(child_number + 1, a_child))
            yield from a_child.iter_nodes(next_gen_ancestry)

    def list_nodes(self):
        return list(self.iter_nodes())

    def get_node(self, node_number):
        """
        Gets the nth node of the outline when taken in depth first sequence (that is the order in which nodes appear
        in the opml file).

        Quite a brute force approach, just iterate through the nodes and stop when we get to the right one.  But still
        more efficient than listing all the nodes then accessing through a list[index].

        :param node_number:
        :return:
        """
        for index, record in enumerate(self.iter_nodes()):
            if index == node_number:
                return record

    def total_sub_nodes(self):
        count = len(self) + 1
        for node in self:
            count += node.total_sub_nodes() - 1  # Need to compensate for adding 1 as it only applies to top node
        return count

    @property
    def text(self):
        """
        Access to the text attribute of an outline node. If a tag regex string has been defined then look for a tag
        and if there is one extract the tag before returning the remainder

        :return: The text attribute of self.node
        """
        field_text = outil.get_valid_attribute(self._node, 'text')
        return field_text

    @property
    def note(self):
        """
        Access to the text attribute of an outline node.

        :return: The _note attribute of self.node
        """
        field_note = outil.get_valid_attribute(self._node, '_note')
        return field_note

    def iter(self):
        return self.iter_nodes()

    def __str__(self):
        text_display_string = self._process_string_for_display(self.text)
        note_display_string = self._process_string_for_display(self.note)
        return 'OutlineNode: children: {}, text: \'{}\', note: \'{}\''.format(len(self),
                                                                              text_display_string, note_display_string)

    def __repr__(self):
        text_display_string = self._process_string_for_display(self.text)
        note_display_string = self._process_string_for_display(self.note)

        return f'OutlineNode.create_outline_node(text: \'{text_display_string}\', note: \'{note_display_string}\')'

    @staticmethod
    def _process_string_for_display(long_string):
        # Remove leading and trailing whitespace and line breaks
        string_stripped = long_string.strip().replace('\n', ' ').replace('\r', '')

        ellipsis_str = '...'

        is_truncated = True if len(string_stripped) > OutlineNode._max_len_for_short else False
        length = min(len(string_stripped), OutlineNode._max_len_for_short - len(ellipsis_str))

        ellipsis_string = ellipsis_str if is_truncated else ''
        display_string = string_stripped[:length]
        return_string = display_string + ellipsis_string

        return return_string

    @property
    def short_text(self):
        return self._process_string_for_display(self.text)

    @property
    def short_note(self):
        return self._process_string_for_display(self.note)
