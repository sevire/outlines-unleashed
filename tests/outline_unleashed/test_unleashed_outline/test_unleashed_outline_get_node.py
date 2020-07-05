import os
from unittest import TestCase

from ddt import ddt, data, unpack

from outline.outline import Outline
from outlines_unleashed.unleashed_outline import UnleashedOutline
from tests.test_utilities.test_config import input_files_root

relative_folder_name = os.path.join("outline_unleashed", "unleashed_outline")
input_file_name = "unleashed_outline-test-get-node-01.opml"
input_file_path = os.path.join(input_files_root, relative_folder_name, input_file_name)

test_data_driver = [
    (2, "H2: Heading B", "Notes for Heading C", "TAG-TEXT-H2B", None),
    (15, "H5: Heading O", "Level 5 Note 3", None, "TAG-NOTE-H5O")
]

@ddt
class TestUnleashedOutline(TestCase):
    @data(*test_data_driver)
    @unpack
    def test_unleashed_outline(self, node_number, text, note, text_tag, note_tag):
        outline = Outline.from_opml(input_file_path)
        unleashed_outline = UnleashedOutline(outline, ['(-', '-)'], ['(-', '-)'])

        node_record = unleashed_outline.get_node(node_number)
        node_item = node_record[-1]
        node = node_item.node

        self.assertEqual(text, node.text)
        self.assertEqual(note, node.note)
        self.assertEqual(text_tag, node.text_tag)
        self.assertEqual(note_tag, node.note_tag)




