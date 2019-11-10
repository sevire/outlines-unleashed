"""
Tests functionality which walks an outline returning each node in the tree.
"""
import os
from unittest import TestCase
from ddt import ddt, data, unpack
import tests.test_config as tcfg
from opml.outline import Outline

test_node_text_values = (
    (0, ''),
    (1, 'H1:He'),
    (5, 'H5: H'),
    (47, 'H2: Heading AT'),
    (22, ''),
)

test_node_note_values = (
    (0, ''),
    (1, 'Notes for Heading A'),
    (5, 'Level 5 Note 1'),
    (47, ''),
    (22, 'Empty text'),
)

ancestry_test_values = (
    (0, ()),
    (1, (1,)),
    (5, (1,1,1,1,1)),
    (20, (2,1,1,1)),
    (46, (3,2,2,1,1))
)


@ddt
class TestOutlineNodeWalk(TestCase):
    def setUp(self) -> None:
        self.outline = Outline.from_opml(os.path.join(tcfg.test_resources_root, 'opml-test-valid-01.opml'))

    def test_all_nodes_covered_01(self):
        size_of_outline = self.outline.total_sub_nodes()

        self.assertEqual(48, size_of_outline)
        pass

    def test_all_nodes_covered_02(self):
        count = 0
        node_list = list(self.outline.list_all_nodes())
        self.assertEqual(48, len(node_list))

    @unpack
    @data(*test_node_text_values)
    def test_node_order_and_text_contents(self, index, text_value):
        """Don't test every row but use data driven check on what is at each
        position to allow future expansion. :return:

        Args:
            index:
            text_value:
        """
        node_list = list(self.outline.list_all_nodes())
        length = len(text_value)
        if length > 0 :
            text = node_list[index].node().text[:length]  # Truncate to length of test string
        else:
            text = node_list[index].node().text  # Don't want to truncate if testing for empty string
        self.assertEqual(text_value, text)

    @unpack
    @data(*test_node_note_values)
    def test_node_order_and_note_contents(self, index, note_value):
        """Don't test every row but use data driven check on what is at each
        position to allow future expansion. :return:

        Args:
            index:
            note_value:
        """
        node_list = list(self.outline.list_all_nodes())
        length = len(note_value)
        if length > 0 :
            note = node_list[index].node().note[:length]  # Truncate to length of test string
        else:
            note = node_list[index].node().note  # Don't want to truncate if testing for empty string
        self.assertEqual(note_value, note)

    @unpack
    @data(*ancestry_test_values)
    def test_ancestry(self, index, child_ancestry):

        """
        Args:
            index:
            child_ancestry:
        """
        node_list = list(self.outline.list_all_nodes())

        matching_ancestry = node_list[index].child_ancestry()
        self.assertEqual(child_ancestry, matching_ancestry)


