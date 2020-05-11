"""
Wrapper class for an Outline object which unleashes it by adding additional functionality such as wrapping
each of the nodes into UnleashedOutlineNodes.

The trick here is to put in place the wiring which allows us to deal with unleashed outline nodes instead of
outline nodes without having to repeat logic created to manage outline nodes (such as the convoluted and recursive
list_all_nodes method.
"""
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

    def match_root_nodes(self, matching_criteria):
        """
        Find the nodes within the outline which are flagged as 'unleashed' nodes (that is nodes which contain
        structured data for processing).

        At the time of writing unleashed nodes will be identified by containing the tag "DATA-OBJECT".  This is
        for convenience during development and testing and may change later.

        ToDo: Revise/Confirm approach for identifying root nodes.

        Finds all nodes which match the given criteria.  These will be the root nodes of the data objects embedded
        within the outline, which can then be processed accordingly (e.g. to extract and tabulate the data)

        :param matching_criteria:
        :return:
        """
        return [] # Empty list for now.