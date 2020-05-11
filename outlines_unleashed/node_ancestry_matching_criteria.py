from outline.node_ancestry_item import NodeAncestryItem


class NodeAncestryMatchingCriteria:
    """Used to identify the nodes in the outline which match a given set of
    criteria, so that node can be used as an extracted field for further
    processing or output.

    Stores a set of criteria against which a given node can be matched, and
    the method to determine whether a supplied outline node matches it.

    Where one of the supplied criterion is None this is a wild card which
    means don't test this value - always match that criterion.
    """
    def __init__(self, child_number=None, text=None, note=None, text_tag=None, note_tag=None):
        """
        Args:
            child_number: The sequence number of this child within all the
                children of the parent node.
            text: The value of the text attribute to match with (after
                separating out the tag_text value).
            note: The value of the note attribute to match with (after
                separating out the tag_note value).
            text_tag: The value of the text_tag, embedded within the node text
                value, to match with.
            note_tag: The value of the note_tag, embedded within the node note
                value, to match with.
        """
        #self.level = level
        self.child_number = child_number
        self.text = text
        self.note = note
        self.text_tag = text_tag
        self.note_tag = note_tag

    def matches_criteria(self, node_list_item: NodeAncestryItem):
        """tests whether a specific generation within the ancestry for a node
        (the node list item) matches with the criteria represented within this
        object.

        Args:
            node_list_item (NodeAncestryItem):
        """
        outline_node = node_list_item.node

        # Go through each of the supplied matching criteria and where it isn't None, check whether the supplied
        # node matches on that criterion.  Start by assuming there is a match then look for criteria which negate
        # the assumption.  As soon as a mismatch is found we can stop checking.

        match = True
        # if self.level is not None and self.level != outline_node.level:
        #     match = False
        if self.child_number is not None and self.child_number != node_list_item.child_number:
            match = False
        elif self.text is not None and self.text != outline_node.text:
            match = False
        elif self.note is not None and self.note != outline_node.note:
            match = False
        elif self.text_tag is not None and self.text_tag != outline_node.text_tag:
            match = False
        elif self.note_tag is not None and self.note_tag != outline_node.note_tag:
            match = False

        return match
