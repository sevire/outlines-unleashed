import copy
from typing import Tuple

import opml.opml_exceptions as ex
from xml.etree import ElementTree
from opml import outline_utilities as outil
from opml.outline_node import OutlineNode


class Outline:
    """
        Provides the functionality to read, create and process an OPML document or outline from other supported formats.

        It is a wrapper to an xml.etree.ElementTree object, working in conjunction with
        OutlineNode so that a user doesn't need to worry about the ins and outs of general XML handling, just getting
        at the data within the outline an understanding the structure.

        While central use case is for an outline stored as an OPML file, I want to allow other options to drive more
        flexible use cases later on - such as creating an outline from indented text.  So the class is implemented with
        that in mind.

        Formats supported are:
        - Now...
            - OPML object (in .opml file)
            - OPML file (in ElementTree xml object)
        - Later...
            - OPML file (in text string)
            - Indented Text (in .txt file)
            - Indented Text (in text string)
            - List of Lists (included to support testing but may have other applications

        The approach taken is to extract all the outline specific information (version, expansion state etc) and
        hold it as data fields, so there is no need to provide access directly to the opml or _head elements to the
        user.  I think this is helpful because the structure for OPML files is quite simple and without the need to
        access _head and opml there is only one node type - the outline node.

        So the outline object gives access to the outline level data, and to the top level outline node.  Access
        to other nodes is implemented recursively through the OutlineNode class which wraps the Element class in
        the ElementTree implementation.

        This may change if I decide to implement outline editing and writing, but that's not for now.
    """
    def __init__(self, outline, head, root, full_validate=False,
                 tag_regex_delim_text: Tuple[str, str] = None, tag_regex_delim_note: Tuple[str, str] = None):
        """
        :param outline: An outline object from one of the factory methods implementing supported formats.  In the form
                        of an ElementTree object.
        :param full_validate: Indicates whether to validate the supplied outline as valid based on the OPML 2.0 spec.
                              Note this library does not support OPML 1.0
        """

        # We are creating an outline from a passed in ElementTree object (but this may have been generated from somethin
        # else originally.
        self._root = root
        self._head = head

        self.tag_regex_text = tag_regex_delim_text
        self.tag_regex_note = tag_regex_delim_note

        self.outline = OutlineNode(outline, self.tag_regex_text, self.tag_regex_note)

        self.version = outil.get_valid_attribute(self._root, 'version')
        self.title = outil.get_valid_element_value(self._head, 'title')
        self.dateCreated = outil.get_valid_element_value(self._head, 'dateCreated')
        self.dateModified = outil.get_valid_element_value(self._head, 'dateModified')
        self.ownerName = outil.get_valid_element_value(self._head, 'ownerName')
        self.ownerEmail = outil.get_valid_element_value(self._head, 'ownerEmail')
        self.ownerId = outil.get_valid_element_value(self._head, 'ownerId')
        self.docs = outil.get_valid_element_value(self._head, 'docs')
        self.expansionState = outil.get_valid_element_value(self._head, 'expansionState')
        self.verticalScrollState = outil.get_valid_element_value(self._head, 'verticalScrollState')
        self.windowTop = outil.get_valid_element_value(self._head, 'windowTop')
        self.windowLeft = outil.get_valid_element_value(self._head, 'windowLeft')
        self.windowBottom = outil.get_valid_element_value(self._head, 'windowBottom')
        self.windowRight = outil.get_valid_element_value(self._head, 'windowRight')

        if full_validate is True:
            pass  # Put more here later
        else:
            # Minimum validation.  Version is 2.0
            if self.version != '2.0':
                raise ex.MalformedOutline(f'Version is {self.version} must be 2.0')

    # =================================================================================================================
    # Methods used during initialisation of an outline.  Includes factory methods for creating an outline from
    # different sources and also for any immediate initialisation required.
    # =================================================================================================================

    @staticmethod
    def initialise_opml_tree(tree):
        # Takes a full tree extracted from an OPML file and extracts _head and places all the outline elements from
        # the body under an outline element (this ensures that all nodes in the tree are outline elements and makes
        # for easier processing).

        root = tree.getroot()

        should_be_body = root.findall('body')
        body = outil.validate_matched_node(should_be_body, 'body')
        if body is None:
            raise ex.MalformedOutline('Should be only one body element but {} were found'.format(len(should_be_body)))
        else:
            top_outline = ElementTree.Element('outline')
            top_outline.set('text', '')  # All outline elements must have text attribute so need to add for top element

            for outline in body:
                top_outline.append(outline)

            should_be_head = root.findall('head')
            if len(should_be_head) == 1 and should_be_head[0].tag == 'head':
                head = should_be_head[0]
            else:
                head = None

            return top_outline, head, root

    @classmethod
    def from_opml(
            cls,
            opml_path: str,
            tag_text_delimiter: Tuple[str, str] = None,
            tag_note_delimiter: Tuple[str, str] = None
    ):
        outline = ElementTree.parse(opml_path)

        return cls(*Outline.initialise_opml_tree(outline), tag_regex_delim_text=tag_text_delimiter, tag_regex_delim_note=tag_note_delimiter)

    @classmethod
    def from_etree(cls, e_tree):
        outline = e_tree

        # Deep copy to de-couple from the external structure that was passed in.
        outline_copy = copy.deepcopy(outline)

        return cls(*Outline.initialise_opml_tree(outline_copy))

    def total_sub_nodes(self):
        return self.outline.total_sub_nodes()

    def list_all_nodes(self):
        return self.outline.list_all_nodes()

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

