import copy
from typing import Tuple

import outline.opml_exceptions as ex
from xml.etree import ElementTree
from outline import outline_utilities as outil
from outline.outline_node import OutlineNode
from outline.outline_utilities import is_valid_tag


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
        hold it as data fields, so there is no need to provide access directly to the outline or _head elements to the
        user.  I think this is helpful because the structure for OPML files is quite simple and without the need to
        access _head and outline there is only one node type - the outline node.

        So the outline object gives access to the outline level data, and to the top level outline node.  Access
        to other nodes is implemented recursively through the OutlineNode class which wraps the Element class in
        the ElementTree implementation.

        This may change if I decide to implement outline editing and writing, but that's not for now.
    """
    def __init__(self, outline, head, root, full_validate=False):
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

        self.top_outline_node = OutlineNode(outline)

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

        self.validate(full_validate)

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

            outline_count = 0
            for node in body:
                is_valid_tag(node)
                outline_count += 1
                top_outline.append(node)
            if outline_count == 0:
                # There has to be at least one <outline> element so abort.
                raise ex.MalformedOutline(f'No <outline> node under <body> element.')

            should_be_head = root.findall('head')
            if len(should_be_head) == 1 and should_be_head[0].tag == 'head':
                head = should_be_head[0]
            else:
                head = None

            return top_outline, head, root

    @classmethod
    def from_opml(cls, opml_path: str, full_validate=False):
        outline = ElementTree.parse(opml_path)

        return cls(*Outline.initialise_opml_tree(outline), full_validate=full_validate)

    @classmethod
    def from_etree(cls, e_tree, full_validate=False):
        outline = e_tree

        # Deep copy to de-couple from the external structure that was passed in.
        outline_copy = copy.deepcopy(outline)

        return cls(*Outline.initialise_opml_tree(outline_copy), full_validate=full_validate)

    def total_sub_nodes(self):
        return self.top_outline_node.total_sub_nodes()

    def iter_nodes(self):
        """
        Iterates through nodes in a depth first traversal of the tree.  Essentially the nodes are presented
        in the same order as they appear textually in the outline file.

        :return:
        """
        return self.top_outline_node.iter_nodes()

    def list_nodes(self):
        """
        Returns a List of all nodes in depth first traversal order.

        :return:
        """
        return self.top_outline_node.list_nodes()

    def validate(self, full_validation_flag):
        # Minimum validation.
        if self.version != '2.0':
            raise ex.InvalidOpmlVersion(f'Version is {self.version} must be 2.0')
        if full_validation_flag is True:
            return self.top_outline_node.validate(full_validation_flag=full_validation_flag)
        return True