

class UnleashedNodeAncestryItem:
    def __init__(self, node_ancestry_item, text_tag_regex=None, note_tag_regex=None):
        """
        This is a mirror of NodeAncestryItem but it holds an UnleashedOutlineNode, rather than an
        OutlineNode

        :param child_number:
        :param unleashed_node:
        """

        self.node_ancestry_item = node_ancestry_item
        self.text_tag_regex = text_tag_regex
        self.note_tag_regex = note_tag_regex

    @property
    def child_number(self):
        return self.node_ancestry_item.child_number

    @property
    def node(self):
        from outlines_unleashed.unleashed_outline_node import UnleashedOutlineNode
        return UnleashedOutlineNode(self.node_ancestry_item.node,
                                    tag_regex_text=self.text_tag_regex,
                                    tag_regex_note = self.note_tag_regex)
