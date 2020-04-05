import os
from unittest import TestCase
import tests.test_utilities.test_config as tcfg
from opml.outline import Outline
from outlines_unleashed.unleashed_outline import UnleashedOutline


class TestUnleashedOutlineNode(TestCase):
    def test_unleashed_outline_node(self):
        outline = Outline.from_opml(
            os.path.join(tcfg.input_files_root, 'opml_data_extraction_test_02.opml'))

        unleashed_outline = UnleashedOutline(outline)

        unleashed_nodes = list(unleashed_outline.iter_nodes())

        node_ancestry_record = unleashed_nodes[1]

        depth = node_ancestry_record.depth

        item = node_ancestry_record[1]
        child_number = item.child_number

        pass