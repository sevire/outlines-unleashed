"""
Tests that a valid outline can be parsed and accessed correctly.
"""
import os
from unittest import TestCase
from ddt import ddt, data, unpack
from opml.outline import Outline
from xml.etree import ElementTree
import tests.test_config as tcfg

test_data_head = (
    ('version', '2.0'),
    ('title', 'Untitled 2'),
    ('dateCreated', None),
    ('dateModified', None),
    ('ownerName', None),
    ('ownerEmail', None),
    ('ownerId', None),
    ('docs', None),
    ('expansionState', ['16', '17', '31']),
    ('verticalScrollState', None),
    ('windowTop', 192),
    ('windowLeft', 0),
    ('windowBottom', 872),
    ('windowRight', 711)
)


@ddt
class TestOutline(TestCase):

    @unpack
    @data(*test_data_head)
    def test_head_data_from_opml(self, field_name, expected_value):
        """
        Args:
            field_name:
            expected_value:
        """
        outline = Outline.from_opml(os.path.join(tcfg.test_resources_root, 'opml-test-valid-01.opml'))

        # Access field by attribute name to allow data driven approach for test
        value = getattr(outline, field_name)
        self.assertEqual(expected_value, value)

    def test_version(self):
        """Just check that version number is correct (at top level of
        outline).
        """
        outline = Outline.from_opml(os.path.join(tcfg.test_resources_root, 'opml-test-valid-01.opml'))
        version = outline.version

        self.assertEqual('2.0', version)

    @unpack
    @data(*test_data_head)
    def test_head_data_from_tree(self, field_name, expected_value):
        """
        Args:
            field_name:
            expected_value:
        """
        tree = ElementTree.parse(os.path.join(tcfg.test_resources_root, 'opml-test-valid-01.opml'))

        outline = Outline.from_etree(tree)

        # Access field by attribute name to allow data driven approach for test
        value = getattr(outline, field_name)
        self.assertEqual(expected_value, value)
