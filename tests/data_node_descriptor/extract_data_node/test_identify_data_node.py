import os
from unittest import TestCase

from ddt import ddt, data, unpack

import tests.test_utilities.test_config as tcfg
from outline.outline import Outline
from outlines_unleashed.unleashed_outline import UnleashedOutline

test_folder = "data_node_descriptor"

test_data_driver = [
    {
        "file_name": "opml_data_extraction_test_03.opml",
        "expected_data_nodes": {
            "data_node_01": {
                "data_node_sequence_number": 0,
                "data_node_list_index": 1
            },
            "data_node_02": {
                "data_node_sequence_number": 1,
                "data_node_list_index": 31
            },
            "data_node_03": {
                "data_node_sequence_number": 2,
                "data_node_list_index": 46
            },
            "data_node_04": {
                "data_node_sequence_number": 3,
                "data_node_list_index": 65
            },
            "data_node_05": {
                "data_node_sequence_number": 4,
                "data_node_list_index": 74
            },
        }
    }
]


def test_data_generator():
    for file in test_data_driver:
        file_path = os.path.join(tcfg.input_files_root, test_folder, file["file_name"])
        for expected_data_node in file["expected_data_nodes"]:
            expected_node_record = file["expected_data_nodes"][expected_data_node]
            yield file_path, expected_node_record['data_node_sequence_number'], 'data_node_name', expected_data_node
            yield file_path, expected_node_record['data_node_sequence_number'], 'data_node_list_index', expected_node_record['data_node_list_index']


@ddt
class TestIdentifyDataNode(TestCase):
    @data(*test_data_generator())
    @unpack
    def test_identify_data_node_01(self, file_path, expected_node_index, field_name, expected_field_value):
        outline = Outline.from_opml(file_path)
        unleashed_outline = UnleashedOutline(outline)
        data_nodes = unleashed_outline.extract_data_nodes()
        expected_node_record = data_nodes[expected_node_index]

        self.assertEqual(expected_field_value, expected_node_record[field_name])
