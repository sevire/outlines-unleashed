import os
from unittest import TestCase
from outline.outline import Outline
from outlines_unleashed.unleashed_outline import UnleashedOutline
from tests.test_utilities.test_config import input_files_root


class TestUnleashedOutline(TestCase):
    input_file_full_path = os.path.join(input_files_root, 'outline_unleashed', 'unleashed_outline', 'unleashed_outline-test-valid-01.opml')

    def test_unleashed_outline(self):
        outline = Outline.from_opml(opml_path=self.input_file_full_path, full_validate=True)
        unleashed_outline = UnleashedOutline(outline)

        for index, unleashed_node in enumerate(unleashed_outline.iter_unleashed_nodes()):
            print(f'Node {index}: {unleashed_node}')

        self.assertTrue(True)
