import os
from unittest import TestCase
from outline.outline import Outline
from outline.outline_node import OutlineNode
import tests.test_utilities.test_config as tcfg


class TestOutlineNode(TestCase):
    local_path = os.path.join('outline', 'outline_node')
    test_outline = os.path.join(tcfg.input_files_root, local_path, 'outline-test-valid-01.opml')

    def test_child_access(self):
        outline = Outline.from_opml(self.test_outline)

        top_level_node = outline.top_outline_node

        num_child_nodes = len(top_level_node)
        self.assertEqual(3, num_child_nodes)

        child_outline_nodes = list(top_level_node)
        self.assertEqual(3, len(child_outline_nodes))

        for index, child in enumerate(top_level_node):
            self.assertIsInstance(child, OutlineNode)
            self.assertIsInstance(child_outline_nodes[index], OutlineNode)
            self.assertEqual(child, child_outline_nodes[index])

    def test_field_access(self):
        outline = Outline.from_opml(self.test_outline)

        top_level_node = outline.top_outline_node  # Access the top level OutlineNode object

        # Check that accessing child node gets the right one
        node_01 = top_level_node[0]
        self.assertEqual('H1:Heading A', node_01.text)
        self.assertEqual('Notes for Heading A', node_01.note)

        # Check that accessing sub-nodes from top level works ok.
        # Note that (unleashed) tags are in the text but (correctly) not recognised by outline node.
        # Also note that white space is NOT ignored in the tag text as it isn't recognised as a tag.
        node_01_01 = top_level_node[0][0]
        self.assertEqual(' (-TAG-TEXT-H2B-)H2: Heading B', node_01_01.text)
        self.assertEqual('Notes for Heading C', node_01_01.note)

        # Check that two ways of getting to the same node reveal the same one.
        node_01_01_01a = node_01_01[0]
        node_01_01_01b = top_level_node[0][0][0]

        self.assertEqual(node_01_01_01a, node_01_01_01b)