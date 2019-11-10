"""
Collection of utility functions used by both Outline and OutlineNode classes.  Help with checking and accessing
elements of an outline.
"""
from opml.outline_node_definition import outline_node_structures as ods
import opml.opml_exceptions as ex


def get_attribute(element, attribute_name):
    """Low level method to extract an attribute from a node allowing for various
    cases.

    Expected cases: - No attributes for this node --> None - Attributes exist
    but requested one doesn't. --> None - Requested attribute does exist. -->
    Value (as string).

    Args:
        element: ElementTree Element
        attribute_name: name of attribute to extract from element.

    Returns:
        - Value of element if it exists.
        - None otherwise.
    """
    attributes = getattr(element, 'attrib', {})
    if attribute_name not in attributes:
        return None
    else:
        return attributes[attribute_name]


def is_valid_tag(element):
    """Checks whether a supplied node is valid as part of an outline.

    Raise an exception if not. May change this later but initially I am takin
    the view that we may as well stop straight away if there is a badly formed
    outline.

    Args:
        element:
    """

    if element.tag not in ods:
        raise ex.MalformedOutline('{} tag not allowed in an outline'.format(element.tag))
    else:
        return True


def get_valid_attribute(element, attribute_name):
    """Provided with an element (Element) and an attribute name, perform some
    validation first to check whether the supplied node is a valid outline node
    and that the requested attribute is allowed/expected for that node, and then
    extract the value of the attribute (as a string) and return it.

    It will detect the following errors: - tag name of supplied node is not
    an allowed element within an outline. - attribute of supplied name is not
    allowed for node of supplied type. - attribute is mandatory but not
    supplied.

    Args:
        element:
        attribute_name:
    """
    if not is_valid_tag(element):
        raise ex.MalformedOutline('Attempt to create OutlineNode with non <outline> element')
    else:
        attribute_value = get_attribute(element, attribute_name)
        if attribute_value is None:
            field_specifier = get_field_specifier(element, attribute_name)
            if field_specifier.required:
                raise ex.MalformedOutline('Missing attribute ({}) for element ({})'.format(attribute_name, element))
            else:
                return field_specifier.default
        else:
            return attribute_value


def get_field_specifier(element, field_name, element_flag=False):
    """Provided with an element and a field name which is either an attribute or
    an element, check whether it is valid for the element to have an attribute
    or child element with that name.

    If it is, get the field specifier which will state whether the field is
    mandatory or not, and if not, what the default value is (if any).

    Then extract the value and process according to the field specifier,
    returning the value.

    Args:
        element: Element for which we are extracting an attribute or child
            element.
        field_name: Name of attribute or child element
        element_flag: If true then the field is an element, otherwise an
            attribute
    """
    if is_valid_tag(element):
        if element_flag is False and field_name in ods[element.tag]['attributes']:
            return ods[element.tag]['attributes'][field_name]
        elif element_flag is True and field_name in ods[element.tag]['child_elements']:
            return ods[element.tag]['child_elements'][field_name]
        else:
            return None


def validate_matched_node(matched_nodes, tag):
    """Takes the output from a Element.findall() (A list of elements) and checks
    that there is only one matched node and that it is of the specified type

    Args:
        matched_nodes: List of zero, one or more nodes - anything other than one
            is an error.
        tag:
    """
    if len(matched_nodes) == 1 and matched_nodes[0].tag == tag:
        return matched_nodes[0]
    else:
        return None


def get_valid_element(element, tag_name):
    """
    Args:
        element:
        tag_name:
    """
    matched_nodes = element.findall(tag_name)
    return validate_matched_node(matched_nodes, tag_name)


def get_valid_element_value(element, tag_name):
    """
    Args:
        element:
        tag_name:
    """
    child_element = get_valid_element(element, tag_name)
    if child_element is None:
        return None
    else:
        element_specifier = get_field_specifier(element, tag_name, element_flag=True)
        return element_specifier.value_parser(child_element.text)
