import os
from unittest import TestCase

from outline.outline import Outline
from tests.test_utilities.test_config import input_files_root


class TestIterNodes(TestCase):
    input_file_full_path = os.path.join(input_files_root, 'outline', 'outline',
                                        'outline-test-valid-01.opml')

    def test_iter_nodes(self):

        outline = Outline.from_opml(opml_path=self.input_file_full_path, full_validate=True)

        for index, unleashed_node in enumerate(outline.iter_nodes()):
            print(f'Node {index}: {unleashed_node.node()}')

        self.assertTrue(True)
