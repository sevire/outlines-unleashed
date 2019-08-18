"""
Tests that a valid outline can be parsed and accessed correctly.
"""
from unittest import TestCase
from ddt import ddt, data, unpack
from opml.outline import Outline

test_data_head = (
    ('version', '2.0'),
    ('title', 'Untitled 2'),
    ('dateCreated', None),
    ('dateModified', None),
    ('ownerName', None),
    ('ownerEmail', None),
    ('ownerId', None),
    ('docs', None),
    ('expansionState', [16, 17, 31]),
    ('verticalScrollState', None),
    ('windowTop', None),
    ('windowLeft', None),
    ('windowBottom', None),
    ('windowRight', None)
)


@ddt
class TestOutline(TestCase):
    def setUp(self):
        self.outline = Outline.from_opml('../resources/opml-test-valid-01.opml')

    @unpack
    @data(*test_data_head)
    def test_head_data(self, field_name, expected_value):
        version = self.outline.version

        # Access field by attribute name to allow data driven approach for test
        value = getattr(self.outline, field_name)
        self.assertEqual(expected_value, value)
