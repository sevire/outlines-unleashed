import copy

import outline.opml_exceptions as ex
from xml.etree import ElementTree
from outline import outline_utilities as outil
from outline.outline_node import OutlineNode
from outline.outline_node_definition import outline_identity, outline_int, outline_list
from outline.outline_utilities import is_valid_tag, value_serialize


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
        self.vertScrollState = outil.get_valid_element_value(self._head, 'vertScrollState')
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

    @classmethod
    def from_scratch(cls, top_level_outline_nodes=None):
        """
        Create basic Outline object from scratch.  The Outline will be a valid one and include all the elements required
        for it to be compliant with the OPML spec (v2.0)

        There must be at least one outline node under the body of an OPML file, so the Outline object requires at least
        one OutlineNode object as the second level after the root (which is a body element in the OPML spec).

        So, you can supply the OutlineNodes which are to sit under the body node, or supply nothing, and the method
        will create a single OutlineNode beneath the body node.

        :param top_level_outline_nodes: List of of OutlineNode objects to sit under the body element of the outline.
        :return:
        """
        if top_level_outline_nodes is None:
            # Top level nodes not provide, so create single node as OutlineNode under the body element.

            top_level_outline_nodes = [OutlineNode.create_outline_node(outline_text="text", outline_note="note")]

        opml = ElementTree.Element('opml', {"version": "2.0"})

        body = ElementTree.Element('body')
        body.extend(top_level_outline_nodes)

        head = ElementTree.Element('head')

        opml.extend([head, body])

        root = ElementTree.ElementTree(opml)
        return cls(*Outline.initialise_opml_tree(root))

    def create_opml_tree_structure(self):
        """
        Does the opposite of initialise_opml_tree.  Creates the top opml node with a head and body underneath.

        :return:
        """
        head_sub_elements = {
            "title": outline_identity(self.title, "from"),
            "dateCreated": outline_identity(self.dateCreated, "from"),
            "dateModified": outline_identity(self.dateModified, "from"),
            "ownerName": outline_identity(self.ownerName, "from"),
            "ownerEmail": outline_identity(self.ownerEmail, "from"),
            "ownerId": outline_identity(self.ownerId, "from"),
            "docs": outline_identity(self.docs, "from"),
            "expansionState": outline_list(self.expansionState, "from"),
            "vertScrollState": outline_int(self.vertScrollState, "from"),
            "windowTop": outline_int(self.windowTop, "from"),
            "windowLeft": outline_int(self.windowLeft, "from"),
            "windowBottom": outline_int(self.windowBottom, "from"),
            "windowRight": outline_int(self.windowRight, "from"),
        }
        opml = ElementTree.Element("opml", {"version": "2.0"})

        head = ElementTree.Element("head")
        for sub_element in head_sub_elements:
            if head_sub_elements[sub_element] is not None:
                sub = ElementTree.Element(sub_element)
                sub.text = head_sub_elements[sub_element]
                head.append(sub)

        body = ElementTree.Element("body")
        for outline_node in self.top_outline_node:
            body.append(outline_node._node)
        opml.append(head)
        opml.append(body)

        return opml

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

    def get_node(self, node_number):
        return self.top_outline_node.get_node(node_number)

    def validate(self, full_validation_flag):
        # Minimum validation.
        if self.version != '2.0':
            raise ex.InvalidOpmlVersion(f'Version is {self.version} must be 2.0')
        if full_validation_flag is True:
            return self.top_outline_node.validate(full_validation_flag=full_validation_flag)
        return True

    def __str__(self):
        return f"Outline - nodes: {self.top_outline_node.total_sub_nodes()}"

    def __repr__(self):
        return self.__str__()

    def write_opml(self, pathname):
        """
        Re-creates an OPML structure from the encapsulated outline, then writes it out to an opml file.

        :param pathname:
        :return:
        """
        opml = self.create_opml_tree_structure()

        tree = ElementTree.ElementTree()
        tree._setroot(opml)

        tree.write(pathname)




