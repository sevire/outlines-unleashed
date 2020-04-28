import os
from unittest import TestCase
import tests.test_utilities.test_config as tcfg
from outline.node_ancestry_item import NodeAncestryItem
from outline.node_ancestry_record import NodeAncestryRecord
from outline.outline import Outline
from tests.test_utilities.test_config import input_files_root


class TestNodeAncestryRecord(TestCase):
    folder_from_resources_root = os.path.join(input_files_root, 'outline', 'node_ancestry')

    def setUp(self) -> None:
        self.outline = Outline.from_opml(os.path.join(self.folder_from_resources_root, 'opml-test-valid-opml-01.opml'))

    def test_ancestry_01(self):
        node_list = list(self.outline.iter_nodes())
        ancestry_item_01 = node_list[1][-1]
        ancestry_item_02 = node_list[2][-1]
        ancestry_item_03 = node_list[3][-1]
        ancestry_item_04 = node_list[4][-1]

        expected_ancestry = NodeAncestryRecord(
            [
                NodeAncestryItem(None, self.outline.top_outline_node),
                NodeAncestryItem(1, ancestry_item_01.node),
                NodeAncestryItem(1, ancestry_item_02.node),
                NodeAncestryItem(1, ancestry_item_03.node),
                NodeAncestryItem(1, ancestry_item_04.node)
            ]
        )

        self.assertEqual(expected_ancestry, node_list[4])
