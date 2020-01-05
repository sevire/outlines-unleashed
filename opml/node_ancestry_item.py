from typing import Optional


class NodeAncestryItem:
    def __init__(self, child_number: Optional[int], node):
        """
        Args:
            child_number: The sequence within the child nodes of the parent
                where this node appears. If this is the root node child_number
                will be None
            node: The node which appears at this point in the sequence of
                children from the root node to the node that this object is part
                of the ancestry for.
        """
        self.child_number = child_number
        self.node = node
