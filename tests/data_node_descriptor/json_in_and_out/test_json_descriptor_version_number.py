import os
from unittest import TestCase

from outline.outline import Outline
from outlines_unleashed.data_node_specifier import DataNodeSpecifier
from outlines_unleashed.unleashed_outline import UnleashedOutline
from tests.test_utilities.test_config import input_files_root


class TestJsonDescVersionNumber(TestCase):
    test_root = os.path.join(input_files_root, 'data_node_descriptor')

    def test_json_desc_version_number(self):
        """
        Tests ability to parse a file with heading levels mapped directly to outline level.

        So Outline Level 1 is Heading Level 1 etc.

        Also uses JSON syntax which doesn't specify all matching criteria - these should be assigned None
        in the JSON translation.
        :return:
        """
        json_specifier_generic_levels = os.path.join(self.test_root, "custom_json_test_descriptors_generic_levels.json")
        opml_file_name = os.path.join(self.test_root, "custom_json_test_descriptors.opml")
        root_node_index = 1
        expected_number_of_rows = 32

        # Read json file into a string (later this will be done within the outline engine).
        with open(json_specifier_generic_levels, 'r') as f:
            json_specifier_string = f.read()

        # Read opml file into an outline
        outline = Outline.from_opml(opml_file_name)

        unleashed_outline = UnleashedOutline(outline)

        node_list = list(unleashed_outline.iter_unleashed_nodes())
        root_node = node_list[root_node_index].node()

        specifier = DataNodeSpecifier.from_json_string(json_specifier_string)

        extracted_data_nodes = specifier.extract_data_node_dispatch(root_node)

        self.assertEqual(expected_number_of_rows, len(extracted_data_nodes))