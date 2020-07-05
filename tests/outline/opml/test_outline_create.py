import os
from unittest import TestCase

from ddt import ddt

from outline.outline import Outline
from outline.outline_node import OutlineNode
from tests.test_utilities.test_config import output_files_root

relative_folder = os.path.join("outline", "opml")

test_opml_output_file_01 = "test_opml_creation_01.opml"

outline_expected_node_results = [
    (1, 0, 1, "Created node 1: Level 1", "Created node note 1"),
    (2, 1, 2, "Created node 2: Level 2", "Created node note 2"),
    (3, 0, 1, "Created node 3: Level 1", "Created node note 3"),
    (4, 0, 1, "Created node 4: Level 1", "Created node note 4"),
]


def generate_outline_from_test_data(outline):
    for record in outline_expected_node_results:
        node_sequence_number, parent_node_number, level, text, note = record

        outline.


@ddt
class TestOutlineCreate(TestCase):
    """
    Creates an outline from scratch, then writes it out as an opml file and checks that when an outline is created
    from the .opml file it matches what was intended.
    """
    def test_outline_create_01(self):
        output_opml_path = os.path.join(output_files_root, relative_folder, test_opml_output_file_01)

        second_level_nodes = [
            OutlineNode.create_outline_node(outline_text="Child 1:1 text", outline_note="Child 1:1 note"),
            OutlineNode.create_outline_node(outline_text="Child 1:2 text", outline_note="Child 1:2 note"),
            OutlineNode.create_outline_node(outline_text="Child 1:3 text", outline_note="Child 1:3 note"),
        ]

        new_outline = Outline.from_scratch(second_level_nodes)

        new_outline.write_opml(output_opml_path)