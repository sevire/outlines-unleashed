from typing import List


class NodeAncestryRecord:
    """Stores the sequence of nodes from root node to get to current node, along
    with the child number of this node.

    This will allow sophisticated matching criteria which specify any
    property of a node within the ancestry as a match criteria. So it will be
    possible to say...

        'Find all the nodes which have a text value of 'XXX' at level 2 and a
        tag of "YYY" in the node itself.'
    """
    def __init__(self, node_ancestry_item_list: List):
        """

        :param node_ancestry_item_list: (List): List of NodeAncestryItems each of which
               include the child_number of the node at that generation, and the
               node itself.
        """
        """Stores

        Args:
            node_ancestry_item_list 
        """
        self.node_ancestry_item_list = node_ancestry_item_list

    @property
    def depth(self):
        return len(self.node_ancestry_item_list) - 1  # Depth starts from zero for the root node.

    def __len__(self):
        return len(self.node_ancestry_item_list)

    def __getitem__(self, item):
        """
        Args:
            item:
        """
        return self.node_ancestry_item_list[item]

    def __eq__(self, other):
        if not isinstance(other, NodeAncestryRecord):
            return NotImplemented
        else:
            # Check that depth is same for both otherwise can't be equal
            if self.depth != other.depth:
                return False
            else:
                generation_pairs = zip(self, other)
            for generation_pair in generation_pairs:
                this_generation, other_generation = generation_pair
                if this_generation.child_number == other_generation.child_number and this_generation.node == other_generation.node:
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

        new_node_ancestry_list = []
        for item in self.node_ancestry_item_list:
            new_node_ancestry_list.append(item)
        return NodeAncestryRecord(new_node_ancestry_list)

    def append_node_to_ancestry(self, node_ancestry_item):
        """
        Args:
            node_ancestry_item:
        """
        self.node_ancestry_item_list.append(node_ancestry_item)

    def node(self):
        """Extracts the node for which this ancestry is the ancestry of and
        returns it.
        """
        if len(self.node_ancestry_item_list) == 0:
            return None
        else:
            return self[-1].node

    def child_ancestry(self):
        child_ancestry = [item.child_number for item in self.node_ancestry_item_list]

        # Don't include the root node in the child_ancestry
        return tuple(child_ancestry[1:])

    def __str__(self):
        return f"Depth: {self.depth}, Text: {str(self.node().text)}, Note: {str(self.node().note)}"
