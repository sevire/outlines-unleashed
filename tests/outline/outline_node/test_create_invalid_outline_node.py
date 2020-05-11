"""
Attempt to create an Outline Node incorrectly.  Note this is not a big priority at the time of writing as functionality
to create outlines hasn't been implemented and will come later.

The tests include some valid cases to improve confidence that the code is actually testing something.
"""
from unittest import TestCase
from ddt import ddt, data, unpack

from outline.outline_node import OutlineNode

input_data = [
    (1, 'dummy note', True),
    ('dummy text', 2, True),
    (None, None, False),
    (1.234, 4.555, True),
    (('xxx', 'yyy'), None, True)
]

@ddt
class TestCreateInvalidNode(TestCase):

    @unpack
    @data(*input_data)
    def test_create_invalid_node(self, text, note, should_raise_exception):
        if should_raise_exception:
            self.assertRaises(ValueError, OutlineNode.create_outline_node, text, note)
        else:
            try:
                OutlineNode.create_outline_node(outline_text=text, outline_note=note)
            except Exception as err:
                self.fail(f"Create node shouldn't fail with values: text={text}, note={note}")
