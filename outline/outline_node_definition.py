"""
Contains data which defines valid structure of nodes which may be found in an outline.

There are four key elements and outline can contain:

- opml
- head
- body
- outline

Each one of these elements can have different attributes and other properties (such as what child nodes they can
contain).

In addition there is a whole set elements which can be contained within the head node (see data for more detail).

The data structure allows a parsing program or method to check that a parsed outline is structured correctly.

This module also includes a set of value parsing functions which will be used to decode the values of each element.

NOTE: I've tried not to go too far with this.  I don't think there is a schema for OPML but I don't want to effectively
      create an imperfect schema through this approach.  It's just to allow a check of structure which will be a very
      good indicator that the user has supplied a well-formed outline.
"""
from collections import namedtuple


# Define functions to use to decode value of elements (these will be shared by elements which contain the same type)
def outline_identity(value, direction="to"):
    """
    Converts field of a given type either from text to the type or from the type back to text (for serialization)
    This one is just text to text and doesn't do anything.

    :param value:
    :param direction: "to" - from xml text field to the type; "from" - from type to text field.
    :return:
    """
    # Just passes through the value in either direction.
    if value is None:
        return None
    else:
        return value


def outline_int(value, direction="to"):
    """
    Converts from text to value or from value to text

    :param value:
    :param direction: "to" - from xml text field to the type; "from" - from type to text field.
    :return:
    """
    if direction == "to":
        return int(value)
    elif direction == "from":
        if value is None:
            return None
        else:
            return str(value)
    else:
        raise ValueError(f"Invalid direction in converting opml field, was {direction}, should be 'to' or 'from'")


def outline_list(value, direction="to"):
    """
    Converts from text field with commas separated list items to list (expansion list) or from vice versa

    :param value:
    :param direction: "to" - from xml text field to the type; "from" - from type to text field.
    :return:
    """
    if direction == "to":
        data_list = value.split(",")

        # Remove any whitespace
        clean_list = list(map(lambda x: int(x.strip()), data_list))

        return clean_list
    elif direction == "from":
        if value is None:
            return None
        else:
            str_parts = map(lambda x: str(x[1])+", " if x[0] < len(value)-1 else str(x[1]), enumerate(value))
            field_value = ""
            for text_part in str_parts:
                field_value += text_part
            return field_value
    else:
        raise ValueError(f"Invalid direction in converting opml field, was {direction}, should be 'to' or 'from'")


# Help make specification of a particular attribute or element more readable by using named_tuple.
NodeFieldSpecifier = namedtuple('NodeFieldSpecifier', 'required default value_parser')

outline_node_structures = {
    'opml': {
        'attributes': {'version': NodeFieldSpecifier(required=True, default=None, value_parser=outline_identity)},
        'child_elements': {
            'head': NodeFieldSpecifier(required=True, default=None, value_parser=None),
            'body': NodeFieldSpecifier(required=True, default=None, value_parser=None)
        }
    },
    'head': {
        'attributes': {},
        'child_elements': {
            'title':           NodeFieldSpecifier(required=False, default='', value_parser=outline_identity),
            'dateCreated':     NodeFieldSpecifier(required=False, default=None, value_parser=outline_identity),
            'dateModified':    NodeFieldSpecifier(required=False, default=None, value_parser=outline_identity),
            'ownerName':       NodeFieldSpecifier(required=False, default=None, value_parser=outline_identity),
            'ownerEmail':      NodeFieldSpecifier(required=False, default=None, value_parser=outline_identity),
            'ownerId':         NodeFieldSpecifier(required=False, default=None, value_parser=outline_identity),
            'docs':            NodeFieldSpecifier(required=False, default=None, value_parser=outline_identity),
            'expansionState':  NodeFieldSpecifier(required=False, default=None, value_parser=outline_list),
            'vertScrollState': NodeFieldSpecifier(required=False, default=None, value_parser=outline_int),
            'windowTop':       NodeFieldSpecifier(required=False, default=None, value_parser=outline_int),
            'windowLeft':      NodeFieldSpecifier(required=False, default=None, value_parser=outline_int),
            'windowBottom':    NodeFieldSpecifier(required=False, default=None, value_parser=outline_int),
            'windowRight':     NodeFieldSpecifier(required=False, default=None, value_parser=outline_int),
        }
    },
    'body': {
        'attributes': {},
        'child_elements': {'outline'}
    },
    'outline': {
        'attributes': {
            '_note': NodeFieldSpecifier(required=False, default='', value_parser=outline_identity),
            'text': NodeFieldSpecifier(required=True, default=None, value_parser=outline_identity),
            'type': NodeFieldSpecifier(required=False,default='', value_parser=outline_identity),
        },
        'child_elements': {'outline'}
    },
    'title':           {'attributes': {}, 'child_elements': {}},
    'dateCreated':     {'attributes': {}, 'child_elements': {}},
    'dateModified':    {'attributes': {}, 'child_elements': {}},
    'ownerName':       {'attributes': {}, 'child_elements': {}},
    'ownerEmail':      {'attributes': {}, 'child_elements': {}},
    'ownerId':         {'attributes': {}, 'child_elements': {}},
    'docs':            {'attributes': {}, 'child_elements': {}},
    'expansionState':  {'attributes': {}, 'child_elements': {}},
    'vertScrollState': {'attributes': {}, 'child_elements': {}},
    'windowTop':       {'attributes': {}, 'child_elements': {}},
    'windowLeft':      {'attributes': {}, 'child_elements': {}},
    'windowBottom':    {'attributes': {}, 'child_elements': {}},
    'windowRight':     {'attributes': {}, 'child_elements': {}},
}
