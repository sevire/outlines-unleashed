import functools
import os
from unittest import TestCase

from ddt import ddt, unpack, data

from outline.outline import Outline
from outline.outline_node import OutlineNode
from tests.test_utilities.test_config import output_files_root

relative_folder = os.path.join("outline", "opml")

test_opml_output_file_01 = "test_opml_creation_01.opml"

# In this data structure, nodes must be in numerical order as the outline is being constructed on the fly so if the
# correct order isn't followed, the parent nodes may not exist or have a different sequence number.
outline_expected_node_results = [
    (1, 0, 1, "Created node 1: Level 1", "Created node note 1"),
    (2, 1, 2, "Created node 2: Level 2", "Created node note 2"),
    (3, 2, 3, "Created node 3: Level 3 - A new node", "Created node note 2"),
    (4, 0, 1, "Created node 4: Level 1", "Created node note 3"),
    (5, 0, 1, "Created node 5: Level 1", "Created node note 4"),
]

test_opml_path = os.path.join(output_files_root, relative_folder, test_opml_output_file_01)


def generate_outline_from_test_data():

    # First add all the top level nodes as they are supplied when creating the outline
    top_level_nodes = []
    for record in [item for item in outline_expected_node_results if item[1] == 0]:
        _, _, _, text, note = record
        top_level_nodes.append(OutlineNode.create_outline_node(text, note))

    # Now create the outline before adding other nodes
    new_outline = Outline.from_scratch(top_level_nodes)

    # Now add other nodes but skipping records for top level ones
    for record in [item for item in outline_expected_node_results if item[1] != 0]:
        node_sequence_number, parent_node_number, level, text, note = record

        parent_node = new_outline.get_node(parent_node_number).node()
        parent_node.add_node(text, note)

    new_outline.write_opml(test_opml_path)


@ddt
class TestOutlineCreate(TestCase):
    """
    Creates an outline from scratch, then writes it out as an opml file and checks that when an outline is created
    from the .opml file it matches what was intended.
    """
    @data(*outline_expected_node_results)
    @unpack
    def test_outline_create_01(self, node_sequence_number, parent_node_number, level, text, note):

        generate_outline_from_test_data()
        outline = Outline.from_opml(test_opml_path)

        test_record = outline.get_node(node_sequence_number)
        test_item = test_record[-1]
        test_node = test_item.node

        self.assertEqual(level, test_record.depth)
        self.assertEqual(text, test_node.text)
        self.assertEqual(note, test_node.note)
