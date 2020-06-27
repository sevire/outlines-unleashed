import os
from unittest import TestCase
import json

from ddt import unpack, data, ddt

import tests.test_utilities.test_config as tcfg
from outline.outline import Outline
from outlines_unleashed.data_node_specifier import DataNodeSpecifier
from outlines_unleashed.unleashed_outline import UnleashedOutline

from tests.python_test_data.data_node_specifier_data.expected_results_data import extracted_data_values_02
from resources.test.json_serialized import serialized_json_01, serialized_json_specifier_03x
from tests.python_test_data.data_node_specifier_data.data_node_test_specifiers import test_data_node_specifier_03x
from tests.python_test_data.data_node_specifier_data.json_serialize_test_descriptors import test_json_descriptor_01

test_root = os.path.join(tcfg.input_files_root, 'data_node_descriptor')


@ddt
class TestSerializeDescriptor(TestCase):
    def test_serialise_descriptor_01(self):
        """
        This was a step in the journey to developing the to_json functionality.  It doesn't directly test any
        outline or unleashed outline functionality but may be useful in the future to help understand what's happened
        of the to_json functionality stops working.  It simply uses json.dumps to
        functionality
        :return:
        """
        self.maxDiff = None
        serialized_descriptor = json.dumps(test_data_node_specifier_03x, default=lambda o: o.__dict__, indent=4)
        self.assertEqual(serialized_json_specifier_03x, serialized_descriptor)

    def test_opml_to_json(self):
        self.maxDiff = None
        serialized_descriptor = DataNodeSpecifier.to_json(test_json_descriptor_01)
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
        """
        Data driven test to check that a data node specifier record imported from JSON can be used correctly to
        parse a data node and get correct results.  The intention isn't to do a full test of data node extract
        functionality but to use sufficiently complex data to provide confidence that the from_json functionality
        is working.

        :param index:     Index of the node under the data node where the data is to be checked.
        :param key1:      First key field expected to be in the extracted data
        :param key2:      Second key field expected to be in the extracted data
        :param non_key1:  Expected data
        :param non_key2:  Expected data
        :param non_key3:  Expected data
        :return:
        """
        descriptor = DataNodeSpecifier.from_json(serialized_json_specifier_03x)
        # tag_text_delimiter = tuple(descriptor.dns_structure['header']['tag_delimiters']['text_delimiters'])
        # tag_note_delimiter = tuple(descriptor.dns_structure['header']['tag_delimiters']['note_delimiters'])

        # Use descriptor to process a node and check that output results are correct.
        data_node_index = 31

        outline = Outline.from_opml(
            os.path.join(test_root, 'opml_data_extraction_test_02.opml'),
        )

        unleashed_outline = UnleashedOutline(outline)

        outline_node_list = unleashed_outline.list_unleashed_nodes()
        data_node = outline_node_list[data_node_index].node()

        extracted_data_records = descriptor.extract_data_node_dispatch(data_node)
        test_record = extracted_data_records[index]

        self.assertEqual(key1, test_record['key_field_1'])
        self.assertEqual(key2, test_record['key_field_2'])
        self.assertEqual(non_key1, test_record['data_field_1'])
        self.assertEqual(non_key2, test_record['data_field_2'])
        self.assertEqual(non_key3, test_record['data_field_3'])

