import os
from unittest import TestCase
import json

from ddt import unpack, data, ddt

import tests.test_config as tcfg

from opml.outline import Outline
from opml.outline_node import OutlineNode
from resources.test.expected_results_data import extracted_data_values_02
from resources.test.json_serialized import serialized_json_01, serialized_json_specifier_03x
from resources.test.data_node_test_specifiers import test_data_node_specifier_ppt_01, test_data_node_specifier_03x
from resources.test.json_serialize_test_descriptors import test_json_descriptor_01


@ddt
class TestSerializeDescriptor(TestCase):
    def test_serialise_descriptor_01(self):
        self.maxDiff = None
        serialized_descriptor = json.dumps(test_data_node_specifier_03x, default=lambda o: o.__dict__, indent=4)
        self.assertEqual(serialized_json_01, serialized_descriptor)

    def test_opml_to_json(self):
        self.maxDiff = None
        serialized_descriptor = OutlineNode.to_json(test_json_descriptor_01)
        self.assertEqual(serialized_json_01, serialized_descriptor)

    @data(*extracted_data_values_02)
    @unpack
    def test_opml_from_json(self,
                            index,
                            key1,
                            key2,
                            non_key1,
                            non_key2,
                            non_key3):
        descriptor = OutlineNode.from_json(serialized_json_specifier_03x)

        # Use descriptor to process a node and check that output results are correct.
        data_node_index = 31

        outline = Outline.from_opml(
            os.path.join(tcfg.test_resources_root, 'opml_data_extraction_test_02.opml'))

        outline_node_list = list(outline.list_all_nodes())
        data_node = outline_node_list[data_node_index].node()

        extracted_data_records = data_node.extract_data_node(descriptor)
        test_record = extracted_data_records[index]

        self.assertEqual(key1, test_record['key_field_1'])
        self.assertEqual(key2, test_record['key_field_2'])
        self.assertEqual(non_key1, test_record['data_field_1'])
        self.assertEqual(non_key2, test_record['data_field_2'])
        self.assertEqual(non_key3, test_record['data_field_3'])

