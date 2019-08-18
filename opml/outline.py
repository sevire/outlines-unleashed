import copy
import opml.opml_exceptions as ex
from xml.etree import ElementTree
from opml.outline_node_definition import outline_node_structures as ods


class Outline:
    """
        Provides the functionality to read, create and process an OPML document or outline from other supported formats.

        Formats supported are:
        - OPML object (in .opml file)
        - OPML file (in text string)
        - OPML file (in ElementTree xml object)
        - Indented Text (in .txt file)
        - Indented Text (in text string)
        - List of Lists (included to support testing but may have other applications
    """
    def __init__(self, outline, full_validate=False):
        """
        :param outline: An outline object from one of the factory methods implementing supported formats.  In the form
                        of an ElementTree object.
        :param full_validate: Indicates whether to validate the supplied outline as valid based on the OPML 2.0 spec. Note
                              this library does not support OPML 1.0
        """

        # We are creating an outline from a passed in ElementTree object.
        self.root = outline.getroot()

        self.head = Outline.get_valid_element(self.root, 'head')

        self.version = Outline.get_valid_attribute(self.root, 'version')
        self.title = Outline.get_valid_element_value(self.head, 'title')
        self.dateCreated = Outline.get_valid_element_value(self.head, 'dateCreated')
        self.dateModified = Outline.get_valid_element_value(self.head, 'dateModified')
        self.ownerName = Outline.get_valid_element_value(self.head, 'ownerName')
        self.ownerEmail = Outline.get_valid_element_value(self.head, 'ownerEmail')
        self.ownerId = Outline.get_valid_element_value(self.head, 'ownerId')
        self.docs = Outline.get_valid_element_value(self.head, 'docs')
        self.expansionState = Outline.get_valid_element_value(self.head, 'expansionState')
        self.verticalScrollState = Outline.get_valid_element_value(self.head, 'verticalScrollState')
        self.windowTop = Outline.get_valid_element_value(self.head, 'windowTop')
        self.windowLeft = Outline.get_valid_element_value(self.head, 'windowLeft')
        self.windowBottom = Outline.get_valid_element_value(self.head, 'windowBottom')
        self.windowRight = Outline.get_valid_element_value(self.head, 'windowRight')

    # =================================================================================================================
    # Methods used during initialisation of an outline.  Includes factory methods for creating an outline from
    # different sources and also for any immediate initialisation required.
    # =================================================================================================================

    @staticmethod
    def initialise_opml_tree(tree):
        # Takes a full tree extracted from an OPML file and extracts head and places all the outline elements from
        # the body under an outline element (this ensures that all nodes in the tree are outline elements and makes
        # for easier processing).

        root = tree.getroot()

        should_be_body = root.findall('body')
        body = Outline.validate_matched_node(should_be_body, 'body')
        if body is None:
            top_outline = ElementTree.Element('outline')
        else:
            raise ex.MalformedOutline('Should be only one body element but {} were found'.format(len(should_be_body)))

        for outline in body:
            top_outline.append(outline)

        should_be_head = root.findall('head')
        if len(should_be_head) == 1 and should_be_head[0].tag == 'head':
            head = should_be_head[0]
        else:
            head = None

        return top_outline, head

    @classmethod
    def from_opml(cls, opml_path):
        outline = ElementTree.parse(opml_path)

        return cls(outline)

    @classmethod
    def from_etree(cls, e_tree):
        outline = e_tree
        top_outline, head = Outline.initialise_opml_tree(outline)

        # Deep copy to de-couple from the external structure that was passed in.
        outline_copy = copy.deepcopy(outline)

        return cls(outline_copy)

    # =================================================================================================================
    # Utility functions for accessing data from an outline in robust way.
    #
    # =================================================================================================================

    @staticmethod
    def get_attribute(element, attribute_name):
        """
        Low level method to extract an attribute from a node allowing for various cases.

        Expected cases:
        - No attributes for this node                 --> None
        - Attributes exist but requested one doesn't. --> None
        - Requested attribute does exist.             --> Value (as string).

        :param element: ElementTree Element
        :param attribute_name: name of attribute to extract from element.
        :return: - Value of element if it exists.
                 - None otherwise.
        """
        attributes = getattr(element, 'attrib', {})
        if attribute_name not in attributes:
            return None
        else:
            return attributes[attribute_name]

    @staticmethod
    def is_valid_tag(element):
        """
        Checks whether a supplied node is valid as part of an outline.

        Raise an exception if not. May change this later but initially I am takin the view that we may as well stop
        straight away if there is a badly formed outline.

        :param element:
        :return:
        """

        if element.tag not in ods:
            raise ex.MalformedOutline('{} tag not allowed in an outline'.format(element.tag))
        else:
            return True

    @staticmethod
    def get_attribute_specifier(element, attribute_name):
        """
        Provided with an element and an attribute name, check whether it is valid for that attribute to exist within
        an outline for that element's tag.  If it is then return the specifier information for that attribute (i.e.
        whether it is required and what the default value is.

        Otherwise return None

        :param element:
        :param attribute_name:
        :return:
        """
        if Outline.is_valid_tag(element):
            if attribute_name in ods[element.tag]['attributes']:
                return ods[element.tag]['attributes'][attribute_name]
            else:
                return None

    @staticmethod
    def get_valid_attribute(element, attribute_name):
        """
        Provided with an element (Element) and an attribute name, perform some validation first to check whether the
        supplied node is a valid outline node and that the requested attribute is allowed/expected for that node,
        and then extract the value of the attribute (as a string) and return it.

        It will detect the following errors:
        - tag name of supplied node is not an allowed element within an outline.
        - attribute of supplied name is not allowed for node of supplied type.
        - attribute is mandatory but not supplied.

        :param element:
        :param attribute_name:
        :return:
        """
        if Outline.is_valid_tag(element):
            attribute_value = Outline.get_attribute(element, attribute_name)
            if attribute_value is None:
                required, default = Outline.get_attribute_specifier(element, attribute_name)
                if required:
                    raise ex.MalformedOutline('Missing attribute ({}) for element ({})'.format(attribute_name, element))
                else:
                    return default
            else:
                return attribute_value

    @staticmethod
    def get_element_definition(element_name, child_element_name):
        """
        To help in decoding and validating an element from an outline, this function finds the appropriate entry in
        the outline node definition structure and returns the entry.

        It could be argued that this should be recursive in case outlines become more complex in their structure.  I'm
        taking the YAGNI (you ain't gonna need it) approach :-)

        :param element_name:
        :param child_element_name:
        :return:
        """
        if element_name not in ods:
            raise ex.MalformedOutline('Attempt to access invalid element ({}) from ({})'.
                                      format(child_element_name, element_name))
        else:
            child_elements = ods[element_name]['child_elements']
            if child_element_name not in child_elements:
                raise ex.MalformedOutline('Attempt to access non-existant element ({}) in ({})'.
                                          format(child_element_name, element_name))
            else:
                return child_elements[child_element_name]

    @staticmethod
    def validate_matched_node(matched_nodes, tag):
        """
        Takes the output from a Element.findall() (A list of elements) and checks that there is only one matched
        node and that it is of the specified type

        :param matched_nodes: List of zero, one or more nodes - anything other than one is an error.
        :param tag:
        :return:
        """
        if len(matched_nodes) == 1 and matched_nodes[0].tag == tag:
            return matched_nodes[0]
        else:
            return None

    @staticmethod
    def get_valid_element(element, tag_name):
        matched_nodes = element.findall(tag_name)
        return Outline.validate_matched_node(matched_nodes, tag_name)

    @staticmethod
    def get_valid_element_value(element, tag_name):
        element = Outline.get_valid_element(element, tag_name)
        if element is None:
            return None
        else:
            element_specifier = Outline.get_attribute_specifier(element, tag_name)
            return element_specifier.value_parser(element.text)