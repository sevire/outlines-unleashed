import os
from unittest import TestCase

from opml.outline import Outline
from tests.test_utilities.test_config import input_files_root


class TestJsonDescVersionNumber(TestCase):
    def test_json_desc_version_number(self):
        """
        Tests ability to parse a file with heading levels mapped directly to outline level.

        So Outine Level 1 is Heading Level 1 etc.

        Also uses JSON syntax which doesn't specify all matching criteria - these should be assigned None
        in the JSON translation.
        :return:
        """
        json_descriptor_generic_levels = os.path.join(input_files_root, "custom_json_test_descriptors_generic_levels.json")
        opml_file_name = os.path.join(input_files_root, "custom_json_test_descriptors.outline")
        root_node_index = 1
        expected_number_of_rows = 32

        # Read json file into a string (later this will be done within the outline engine).
        with open(json_descriptor_generic_levels, 'r') as f:
            json_descriptor_string = f.read()

        # Read opml file into an outline
        outline = Outline.from_opml(opml_file_name)
        node_list = list(outline.iter_nodes())
        root_node = node_list[root_node_index].node()

        descriptor = root_node.from_json(json_descriptor_string)

        extracted_data_nodes = root_node.extract_data_node(descriptor)

        self.assertEqual(expected_number_of_rows, len(extracted_data_nodes))