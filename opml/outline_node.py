import copy
import re
from typing import Tuple, Optional

from opml import outline_utilities as outil
from xml.etree.ElementTree import Element

from opml.node_ancestry_item import NodeAncestryItem
from opml.node_ancestry_record import NodeAncestryRecord
from opml.opml_exceptions import MalformedOutline, MalformedTagRegex
from outlines_unleashed.tag_field_descriptor import TagFieldDescriptor


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

    def __init__(self,
                 outline_node: Element,
                 tag_regex_text: Tuple[str, str] = None,
                 tag_regex_note: Tuple[str, str] = None
                 ):
        """
        Do some checking that we have been passed in the right type of object (should be an xml.etree.Element
        object with tag of outline and a few other things.

        Everything else is done through methods which expose the properties to the user from the node.

        :param outline_node: Element with tag <outline> which the OutlineNode will wrap.
        :param tag_regex_text: String containing regex to use to parse tag value in text field.
        :param tag_regex_note: String containing regex to use to parse tag value in note field.
        """

        if outil.is_valid_tag(outline_node):
            outil.get_valid_attribute(outline_node, 'text')
            self._node = outline_node
            self.tag_regex_text = tag_regex_text
            self.tag_regex_note = tag_regex_note
        else:
            raise (MalformedOutline(f'Invalid element <{outline_node.tag}> in outline'))

    def __getitem__(self, index):
        return OutlineNode(self._node[index], self.tag_regex_text, self.tag_regex_note)
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

    def list_all_nodes(self, ancestry: NodeAncestryRecord = None):
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
            # node_ancestry = ancestry_record
        yield ancestry_record
        for child_number, a_child in enumerate(self):
            next_gen_ancestry = copy.copy(ancestry_record)
            next_gen_ancestry.append_node_to_ancestry(NodeAncestryItem(child_number + 1, a_child))
            yield from a_child.list_all_nodes(next_gen_ancestry)

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
        text, tag = self._extract_tag_and_text(field_text, self.tag_regex_text)
        return text

    @property
    def note(self):
        """
        Access to the text attribute of an outline node.

        :return: The _note attribute of self.node
        """
        field_text = outil.get_valid_attribute(self._node, '_note')
        text, tag = self._extract_tag_and_text(field_text, self.tag_regex_note)
        return text

    @property
    def text_tag(self):
        field_text = outil.get_valid_attribute(self._node, 'text')
        text, tag = self._extract_tag_and_text(field_text, self.tag_regex_text)
        return tag

    @property
    def note_tag(self):
        field_text = outil.get_valid_attribute(self._node, '_note')
        text, tag = self._extract_tag_and_text(field_text, self.tag_regex_note)
        return tag

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
        return 'OutlineNode: children: {}, text: "{}", note: "{}"'.format(len(self),
                                                                          text_display_string,
                                                                          note_display_string)

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

        ellipsis_string = '...' if is_truncated else ''
        display_string = string_stripped[:length]
        return_string = display_string + ellipsis_string

        return return_string

    @staticmethod
    def _extract_tag_and_text(text: str, regex_delim: Tuple[str, str]):
        if regex_delim is None:
            return text, None
        else:
            tag_field_desciptor = TagFieldDescriptor(regex_delim)

            return tag_field_desciptor.parse_tag(text)

    @property
    def short_text(self):
        return self._process_string_for_display(self.text)

    @property
    def short_note(self):
        return self._process_string_for_display(self.note)

    def extract_data_node(self, data_node_specifier):
        """
        Parse the sub_tree with self as a root and extract all the nodes which match the criteria defined
        in the data_node_specifier.

        Based on how the primary key is defined, assemble records as the tree is parsed.  This is the
        essence of unleashing outlines, because nodes with a common parent which is a primary key node
        will share that element of the primary key, and this is how a tree structure is transformed to a
        table structure with fixed format records.

        Note: At this point we are only dealing with cases where all the key fields are closer
        to the root of the data node and all the data fields are deeper.  We don't deal with key fields
        being defined deeper than a non-key field.  I think this is almost certainly right and I haven't
        thought of any meaningful use cases yet where this may not be true, but there may be some. For now
        the logic depends upon this.

        The records are created with fields (and types) according to the field definitions within the
        data_node_specifier, and then added to a list in the order in wihch they appear in the tree.

        This is what is then returned to the caller.

        :param data_node_specifier:
        :return:
        """
        match_list = self.match_data_node(data_node_specifier)
        data_node_table = []
        primary_key_field_list = self.extract_field_names(data_node_specifier, primary_key_only=True)
        non_primary_key_field_list = self.extract_field_names(data_node_specifier, primary_key_only=False)
        empty_data_node_record = {key: None for key in primary_key_field_list + non_primary_key_field_list}

        # Initialise record for first row
        data_node_record = empty_data_node_record

        for match in match_list:
            field_name, field_value = match
            if data_node_record[field_name] is None:
                data_node_record[field_name] = field_value
            else:
                # We have already populated this field, so either it's a new primary key value (end of record)
                # or an error.
                if field_name in primary_key_field_list:
                    # A primary key field is about to be overwritten.
                    # There are a few cases to process here:
                    # - Current record must be complete now so can be written (all cases I think)
                    # - If this is not the last primary key field of the set then we have effectively
                    #   moved to a new branch and so we need to blank out any key fields in the data record
                    #   we are constructing as well as all non-key fields
                    # - Any fields which aren't populated will trigger a warning and an appropriate
                    #   default value assigned.

                    # Check whether any fields un-filled and issue warning but update with default value.
                    for field in data_node_record:
                        if data_node_record[field] is None:
                            data_node_record[field] = '(unfilled)'

                    # Append copy of record to output table so don't keep updating same pointer.
                    data_node_table.append(copy.deepcopy(data_node_record))

                    # Now update new primary key field as part of next record.
                    data_node_record[field_name] = field_value

                    # If this field isn't the last key field in the primary key, then blank out deeper
                    # elements within the current data node record as it doesn't apply to the new branch.
                    key_index = [index for index, value in enumerate(primary_key_field_list) if value == field_name]

                    assert(len(key_index) == 1)
                    if key_index[0] < len(primary_key_field_list) - 1:
                        # Key field which isn't last one has changed so need to blank out deeper key
                        # values in the data node record as they should be re-filled from next branch
                        # of node tree.

                        for index in range(key_index[0]+1, len(primary_key_field_list)):
                            data_node_record[primary_key_field_list[index]] = None

                    # Initialise record for next row.  Key fields should be maintained apart from the one which has
                    # changed. So just initialise non key fields and then update current key field.
                    for field_name in non_primary_key_field_list:
                        data_node_record[field_name] = None
                else:
                    # New value for non-primary key field.  That's an error (but only a warning to be issued)
                    # ToDo: Add logging to allow warnings to be issued which don't stop programme.
                    pass

        # All data fields have been processed, so just clean up the final record and add to the list.
        for field_name in data_node_record:
            if data_node_record[field_name] is None:
                data_node_record[field_name] = '(unfilled)'

        data_node_table.append(copy.copy(data_node_record))

        return data_node_table

    @staticmethod
    def _key_field_check(primary_key_filter, primary_key_flag):
        if primary_key_filter is None:
            return True
        elif primary_key_filter is True and primary_key_flag is 'yes':
            return True
        elif primary_key_filter is False and primary_key_flag is 'no':
            return True
        else:
            return False

    @staticmethod
    def extract_field_names(data_node_specifier, primary_key_only: Optional[bool] = None):

        fields = [
            field_name for field_name in data_node_specifier
            if OutlineNode._key_field_check(primary_key_only, data_node_specifier[field_name]['primary_key'])
        ]
        return fields

    def match_data_node(self, field_specifications):
        """
        Treat this node as the root of a data node embedded within a larger outline structure.  Using the
        field_specifications provided identify all nodes within the data_node sub-tree structure which match
        the supplied criteria, and extract the information required to fully define each extracted field

        :param field_specifications: A structure which defines the properties of a field to be extracted and
               also the criteria which define the properties of nodes which map to that field.

        :return: Information required to create a field object for each matched field and construct records
                 from the fields.
        """
        match_list = []
        for data_node_list_entry in self.list_all_nodes():
            matched_field_data = self.match_field_node(data_node_list_entry, field_specifications)
            if matched_field_data is not None:
                match_list.append(matched_field_data)

        return match_list

    @staticmethod
    def match_field_node(field_node_list_entry, field_specifications):
        """
        Checks a supplied candidate field node against all the field specifiers to look for a match. If we
        find a match then return the field value as defined within the field specifier for the matched field.

        :param field_node_list_entry:
        :param field_specifications:
        :return:
        """
        for field_name in field_specifications:
            field_specification = field_specifications[field_name]
            criteria = field_specification['ancestry_matching_criteria']

            if OutlineNode.match_field(field_node_list_entry, criteria):
                field_value = OutlineNode.extract_field(field_node_list_entry.node(), field_specification)
                return field_name, field_value

    @staticmethod
    def match_field(node_ancestry_record, field_ancestry_criteria):
        """
        Check whether an outline node (field node) from within a data node sub-tree matches the criteria
        for a specific field specifier.

        Goes through ancestry of node and tests each generation against the corresponding criteria

        :param node_ancestry_record:
        :param field_ancestry_criteria:
        :return:
        """
        # First check whether depths match.  If not then definitely not a match.
        if node_ancestry_record.depth != len(field_ancestry_criteria) - 1:
            return False
        else:
            # Depth matches so we now need to test against provided criteria.  Each criterion corresponds to
            # a generation in the ancestry, so we need to test each generation against the appropriate criterion.
            # So we walk down the ancestry from root to current generation and check for a match.  As soon as
            # we fail to get a match, we know the node doesn't match.  If we don't fail at all generations then
            # we have a match.
            match = True

            # Create list of pairs from depth 1 to depth of node we are testing against.  Note that
            # a node list entry has ancestry starting at zero to represent the root of the outline, and
            # criteria need to start there too.
            paired_gen_and_criteria = zip(node_ancestry_record, field_ancestry_criteria)
            for pair in paired_gen_and_criteria:
                generation, gen_criteria = pair
                if not gen_criteria.matches_criteria(generation):
                    match = False

        return match

    @staticmethod
    def extract_field(field_node, field_criteria):
        """
        Extracts the field value from the node according to the field_specifier for the field.  Usually will
        be called once the field has been matched to confirm it is meets the criteria for a specific field
        name.

        :param field_node:
        :param field_criteria:
        :return:
        """

        value_specifier = field_criteria['field_value_specifier']

        if value_specifier == 'text_value':
            field_value = field_node.text
        elif value_specifier == 'text_tag':
            field_value = field_node.text_tag
        elif value_specifier == 'note_value':
            field_value = field_node.note
        elif value_specifier == 'note_tag':
            field_value = field_node.note_tag
        else:
            raise ValueError(f"Unrecognised field specifier {value_specifier}")

        return field_value
