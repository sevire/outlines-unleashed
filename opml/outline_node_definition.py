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


# Define functions to use to decode value of elements (these will be shared by elements which contain the same type
def outline_identity(text):
    # If there is no parsing to do just return the value un-transformed.
    return text


def outline_list(text):
    """
    Created to deal with the case of the expansion_state element but will work for any element where the data is
    represented as a comma separated list.

    :param text:
    :return:
    """
    data_list = text.split(",")

    # Remove any whitespace
    clean_list = map(lambda x: x.strip(), data_list)

    return clean_list


# Help make specification of a particular attribute or element more readable by using named_tuple.
NodeElementSpecifier = namedtuple('NodeElementSpecifier', 'required default value_parser')

outline_node_structures = {
    'opml': {
        'attributes': {'version': NodeElementSpecifier(required=True, default=None, value_parser=outline_identity)},
        'child_elements': {
            'head': NodeElementSpecifier(required=True, default=None, value_parser=None),
            'body': NodeElementSpecifier(required=True, default=None, value_parser=None)
        }
    },
    'head': {
        'attributes': {},
        'child_elements': {
            'title':           NodeElementSpecifier(required=False, default='', value_parser=None),
            'dateCreated':     NodeElementSpecifier(required=False, default=None, value_parser=outline_identity),
            'dateModified':    NodeElementSpecifier(required=False, default=None, value_parser=outline_identity),
            'ownerName':       NodeElementSpecifier(required=False, default=None, value_parser=outline_identity),
            'ownerEmail':      NodeElementSpecifier(required=False, default=None, value_parser=outline_identity),
            'ownerId':         NodeElementSpecifier(required=False, default=None, value_parser=outline_identity),
            'docs':            NodeElementSpecifier(required=False, default=None, value_parser=outline_identity),
            'expansionState':  NodeElementSpecifier(required=False, default=None, value_parser=outline_list),
            'vertScrollState': NodeElementSpecifier(required=False, default=None, value_parser=outline_identity),
            'windowTop':       NodeElementSpecifier(required=False, default=None, value_parser=outline_identity),
            'windowLeft':      NodeElementSpecifier(required=False, default=None, value_parser=outline_identity),
            'windowBottom':    NodeElementSpecifier(required=False, default=None, value_parser=outline_identity),
            'windowRight':     NodeElementSpecifier(required=False, default=None, value_parser=outline_identity),
        }
    },
    'body': {
        'attributes': {},
        'child_elements': {'outline'}
    },
    'outline': {
        'attributes': {
            '_note': NodeElementSpecifier(required=False, default='', value_parser=outline_identity),
            'text': NodeElementSpecifier(required=True, default=None, value_parser=outline_identity)
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
