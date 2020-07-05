"""
Wrapper class for an Outline object which unleashes it by adding additional functionality such as wrapping
each of the nodes into UnleashedOutlineNodes.

The trick here is to put in place the wiring which allows us to deal with unleashed outline nodes instead of
outline nodes without having to repeat logic created to manage outline nodes (such as the convoluted and recursive
list_all_nodes method.
"""
import re

from outline.outline import Outline
from outlines_unleashed.unleashed_outline_node import UnleashedOutlineNode


class UnleashedOutline:
    def __init__(self, outline: Outline, default_text_tag_delimiter=None, default_note_tag_delimiter=None):
        """
        Note.  While we are wrapping the Outline object we aren't trying to hide it.  Access to standard methods
        of the Outline object which aren't changed by the wrapper class are accessed by simply accessing the inner
        Outline object and calling the method.

        :param outline:
        :param default_text_tag_delimiter: text tag delimiter to use when extracting data nodes, unless overridden.
        :param default_note_tag_delimiter: note tag delimiter to use when extracting data nodes, unless overridden.
        """
        self.default_text_tag_delimiter = default_text_tag_delimiter
        self.default_note_tag_delimiter = default_note_tag_delimiter
        self.outline = outline

    def iter_unleashed_nodes(self):
        return UnleashedOutlineNode(self.outline.top_outline_node,
                                    tag_regex_text=self.default_text_tag_delimiter,
                                    tag_regex_note=self.default_note_tag_delimiter).iter_unleashed_nodes()

    def list_unleashed_nodes(self):
        return list(self.iter_unleashed_nodes())

    def get_node(self, node_number):
        top_level_outline_node = self.outline.top_outline_node
        unleashed_top_level_node = UnleashedOutlineNode(top_level_outline_node,
                                                        tag_regex_text=self.default_text_tag_delimiter,
                                                        tag_regex_note=self.default_note_tag_delimiter)
        return unleashed_top_level_node.get_node(node_number)

    def extract_data_nodes(self):
        """
        Extract nodes within the outline which have been tagged as data nodes.  A data node is a root node where the
        sub-tree held under it represents data records in a structured form suitable for extraction using a
        data node specifier.

        Data Nodes are identified by a JSON string in the note of a node which contains a 'data_node' field name
        followed by the name of the data node record.

        :return:
        """
        data_nodes = []
        for node_sequence_number, node in \
                enumerate([ancestry_record.node() for ancestry_record in self.list_unleashed_nodes()]):
            note_text = node.note

            # For now, just look for curly braces beginning and end.  Later use more sophisticated JSON decoding.
            data_node_regex = r"\{data_node: (\w+)\}"
            match = re.search(data_node_regex, note_text)

            if match is not None:
                data_node_name = match.group(1)
                data_nodes.append({
                    'data_node_name': data_node_name,
                    'data_node_list_index': node_sequence_number
                })

        return data_nodes
