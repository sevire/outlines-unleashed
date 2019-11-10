import os
from unittest import TestCase
import tests.test_config as tcfg
from opml.node_ancestry_item import NodeAncestryItem
from opml.node_ancestry_record import NodeAncestryRecord
from opml.outline import Outline


class TestNodeAncestryRecord(TestCase):
    def setUp(self) -> None:
        self.outline = Outline.from_opml(os.path.join(tcfg.test_resources_root, 'opml-test-valid-01.opml'))

    def test_ancestry_01(self):
        node_list = list(self.outline.list_all_nodes())
        ancestry_item_01 = node_list[1][-1]
        ancestry_item_02 = node_list[2][-1]
        ancestry_item_03 = node_list[3][-1]
        ancestry_item_04 = node_list[4][-1]

        expected_ancestry = NodeAncestryRecord(
            [
                NodeAncestryItem(None, self.outline.outline),
                NodeAncestryItem(1, ancestry_item_01.node),
                NodeAncestryItem(1, ancestry_item_02.node),
                NodeAncestryItem(1, ancestry_item_03.node),
                NodeAncestryItem(1, ancestry_item_04.node)
            ]
        )

        self.assertEqual(expected_ancestry, node_list[4])
