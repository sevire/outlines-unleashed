import os
from unittest import TestCase
from opml.outline import Outline
from opml.outline_node import OutlineNode
import tests.test_config as tcfg


class TestOutlineNode(TestCase):
    def test_child_access(self):
        outline = Outline.from_opml(os.path.join(tcfg.test_resources_root, 'opml-test-valid-01.opml'))

        top_level_node = outline.outline

        num_child_nodes = len(top_level_node)
        self.assertEqual(3, num_child_nodes)

        child_outline_nodes = list(top_level_node)
        self.assertEqual(3, len(child_outline_nodes))

        for index, child in enumerate(top_level_node):
            self.assertIsInstance(child, OutlineNode)
            self.assertIsInstance(child_outline_nodes[index], OutlineNode)
            self.assertEqual(child, child_outline_nodes[index])

    def test_field_access(self):
        outline = Outline.from_opml(
            os.path.join(tcfg.test_resources_root, 'opml-test-valid-01.opml'),
            ('(-', '-)'),
            ('[*', '*]')
        )

        top_level_node = outline.outline  # Access the top level OutlineNode object

        # Check that accessing child node gets the right one
        node_01 = top_level_node[0]
        self.assertEqual('H1:Heading A', node_01.text)
        self.assertEqual('Notes for Heading A', node_01.note)

        # Check that accessing sub-nodes from top level works ok.
        node_01_01 = top_level_node[0][0]
        self.assertEqual('H2: Heading B', node_01_01.text)
        self.assertEqual('Notes for Heading C', node_01_01.note)

        # Check that two ways of getting to the same node reveal the same one.
        node_01_01_01a = node_01_01[0]
        node_01_01_01b = top_level_node[0][0][0]

        self.assertEqual(node_01_01_01a, node_01_01_01b)

    def test_confirm_identity(self):
        """Note this test will not pass until re-factoring is complete to ensure
        that same OutlineNode object is returned for same outline element. Some
        thinking to do before we can do this. :return:
        """
        outline = Outline.from_opml(os.path.join(tcfg.test_resources_root, 'opml-test-valid-01.opml'))

        top_level_node = outline.outline  # Access the top level OutlineNode object

        node_01_01 = top_level_node[0][0]
        node_01_01_01a = node_01_01[0]

        node_01_01_01b = top_level_node[0][0][0]

        # self.assertIs(node_01_01_01a, node_01_01_01b, "Outline Node wrapping same Element not identical")
        # ToDo: Decide whether I should be testing for identity of OutlineNodes with same Element instance


