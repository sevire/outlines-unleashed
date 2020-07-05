"""
Tests that a valid outline can be parsed and accessed correctly. Note outline not opml. Validation applies to any
outline whether it originated from an OPML file or some other means.  This will become more relevant when we start
to implement different ways of representing an outline in a textual format (e.g. indented raw text, bulleted lists from
emails etc.)
"""
from xml.etree import ElementTree
import tests.test_utilities.test_config as tcfg
import os
from unittest import TestCase
from ddt import ddt, unpack, data
from outline.outline import Outline

test_data_head = (
    ('version', '2.0'),
    ('title', 'Untitled 2'),
    ('dateCreated', None),
    ('dateModified', None),
    ('ownerName', None),
    ('ownerEmail', None),
    ('ownerId', None),
    ('docs', None),
    ('expansionState', ['0', '16', '32']),
    ('vertScrollState', None),
    ('windowTop', 193),
    ('windowLeft', 400),
    ('windowBottom', 873),
    ('windowRight', 1111)
)


@ddt
class TestValidOpml(TestCase):
    """
    Data driven test for valid Outline from OPML or eTree sources.  Each file should be read without error and data
    should have been read correctly for key elements, attributes etc.
    """

    test_data_file = 'unleashed_outline-test-valid-01.opml'
    # NOTE: Don't modify the OPML file or the unit tests will fail.  See OPML file for more information.

    local_path = os.path.join('outline_unleashed', 'unleashed_outline')

    @unpack
    @data(*test_data_head)
    def test_head_data_from_opml(self, field_name, expected_value):
        """
        Args:
            field_name:
            expected_value:
        """
        outline = Outline.from_opml(os.path.join(tcfg.input_files_root, self.local_path, self.test_data_file))

        # Access field by attribute name to allow data driven approach for test
        value = getattr(outline, field_name)
        self.assertEqual(expected_value, value)

    @unpack
    @data(*test_data_head)
    def test_head_data_from_tree(self, field_name, expected_value):
        """
        Args:
            field_name:
            expected_value:
        """
        tree = ElementTree.parse(os.path.join(tcfg.input_files_root, self.local_path, self.test_data_file))

        outline = Outline.from_etree(tree)

        # Access field by attribute name to allow data driven approach for test
        value = getattr(outline, field_name)
        self.assertEqual(expected_value, value)
