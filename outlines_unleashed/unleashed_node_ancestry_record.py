from copy import copy
from outlines_unleashed.unleashed_node_ancestry_item import UnleashedNodeAncestryItem


class UnleashedNodeAncestryRecord:
    def __init__(self, node_ancestry_record, text_tag_regex=None, note_tag_regex=None):
        self.node_ancestry_record = node_ancestry_record

        # We need to keep track of the regex for tag decoding so that we can create UnleashedOutlineNodes
        # with decodable tags.

        self.text_tag_regex = text_tag_regex
        self.note_tag_regex = note_tag_regex

    @property
    def depth(self):
        return self.node_ancestry_record.depth

    def __len__(self):
        return len(self.node_ancestry_record)

    def __getitem__(self, item):
        return UnleashedNodeAncestryItem(self.node_ancestry_record[item],
                                         text_tag_regex=self.text_tag_regex,
                                         note_tag_regex=self.note_tag_regex)

    def __eq__(self, other):
        if not isinstance(other, UnleashedNodeAncestryRecord):
            return NotImplemented
        else:
            # Check that depth is same for both otherwise can't be equal
            if self.depth != other.depth:
                return False
            else:
                generation_pairs = zip(self, other)
            for generation_pair in generation_pairs:
                this_generation, other_generation = generation_pair
                if this_generation.child_number == other_generation.child_number and \
                   this_generation.node == other_generation.node:
                    return True
                else:
                    return False

    def __copy__(self):
        """When creating a list of all nodes in an outline (for example) we need
        to be able to copy the node_ancestry_item_list at one level to pass recursively to
        the next level in the node tree. But we don't want to duplicate the
        ElementTree.Element objects as these determine when two nodes are
        identical. So deepcopy won't work.

        This will create a new NodeAncestry object with a new list of
        NodeAncestryItems which are references to the same NodeAncestryItems
        from the source object.
        """

        copied_node_ancestry_record = copy(self.node_ancestry_record)
        return UnleashedNodeAncestryRecord(copied_node_ancestry_record)

    def append_node_to_ancestry(self, node_ancestry_item):
        """
        Args:
            node_ancestry_item:
        """
        self.node_ancestry_record.append_node_to_ancestry(node_ancestry_item)

    def node(self):
        """Extracts the node for which this ancestry is the ancestry of and
        returns it.
        """
        if len(self.node_ancestry_record) == 0:
            return None
        else:
            return self[-1].node

    def child_ancestry(self):
        child_ancestry = [item.child_number for item in self.node_ancestry_record]

        # Don't include the root node in the child_ancestry
        return tuple(child_ancestry[1:])
