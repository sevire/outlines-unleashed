"""
Enables matching of nodes of an outline with supplied criteria before then extracting data into data object.
"""
from typing import Tuple

from opml.outline import Outline
from opml.outline_node import OutlineNode


class UnleashedOutline:
    """This is one of the core elements of functionality which drives the
    unleashing of an outline. Being able to match nodes which match key criteria
    in order to then extract the data from the nodes is in many ways the USP of
    the application.
    """

    def __init__(self, outline: Outline) -> None:
        """Accepts an outline and then makes available various methods which
        allow unleashing of the outline.

        Args:
            outline (Outline):
        """
        self.outline = outline

    def match_nodes(self, criteria) -> [OutlineNode, Tuple]:
        """Supplied with a matching criteria (defined by a user) locate nodes
        within the outline which meet those criteria.

        Args:
            criteria:
        """