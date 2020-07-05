import os
from unittest import TestCase

from ddt import ddt, unpack, data

from outline.node_ancestry_item import NodeAncestryItem
from outline.node_ancestry_record import NodeAncestryRecord
from outline.outline import Outline
from outline.outline_node import OutlineNode
from tests.test_utilities.test_config import input_files_root

input_file_01 = "outline-test-get_node-01.opml"
relative_folder = os.path.join("outline", "outline_node")

test_data_driver = [
    (1, 1, 1, "H1:Heading A", "Notes for Heading A"),
    (17, 1, 2, "H1:Heading Q", ""),
    (23, 2, 2, "H2: Heading V", ""),
    (44, 3, 3, "H3: Heading AQ", ""),
    (47, 2, 3, "H2: Heading AT", "")
]


def test_data_generator():
    for test_data_record in test_data_driver:
        node_number, level, child_num, text, note = test_data_record

        yield input_file_01, node_number, "level", level
        yield input_file_01, node_number, "child_number", child_num
        yield input_file_01, node_number, "text", text
        yield input_file_01, node_number, "note", note


@ddt
class TestGetNode(TestCase):
    @data(*test_data_generator())
    @unpack
    def test_get_node_01(self, file_name, node_to_get, item_to_test, expected_value):
        input_file_path = os.path.join(input_files_root, relative_folder, file_name)

        outline = Outline.from_opml(input_file_path)

        ancestry_record_to_test: NodeAncestryRecord = outline.get_node(node_to_get)
        ancestry_item_to_test: NodeAncestryItem = ancestry_record_to_test[-1]
        node_to_test: OutlineNode = ancestry_item_to_test.node

        if item_to_test == "level":
            self.assertEqual(expected_value, ancestry_record_to_test.depth)
        elif item_to_test == "child_number":
            self.assertEqual(expected_value, ancestry_item_to_test.child_number)
        elif item_to_test == "text":
            self.assertEqual(expected_value, node_to_test.text)
        elif item_to_test == "note":
            self.assertEqual(expected_value, node_to_test.note)
        else:
            self.fail(f"Unrecognised item to tes {item_to_test}")
