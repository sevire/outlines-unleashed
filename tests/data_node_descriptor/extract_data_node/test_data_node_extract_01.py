"""
Test which invokes extraction of a data node and gets a data structure of the right format back, based
on the data node provided and the data node descriptor provided.

Calls extract_data_node() method upon the root of a data node sub-tree (OutlineNode) within a parsed
outline.

Gets in return a List of Dicts where each field in the dict corresponds to the fields in the specifier.
"""
from typing import List
from unittest import TestCase

import tests.test_utilities.test_config as tcfg
import os
from ddt import ddt, data, unpack

from outline.outline import Outline
from outlines_unleashed.data_node_specifier import DataNodeSpecifier
from outlines_unleashed.outline_parser import OutlineParser
from outlines_unleashed.unleashed_outline import UnleashedOutline
from tests.python_test_data.data_node_specifier_data.data_node_test_specifiers import data_node_specifier_test_driver

data_driver_01 = (
    (1,
     0,
     [
         ('risk_description', 'text'),
         ('likelihood', 'text'),
         ('impact', 'text'),
         ('mitigation', 'text'),
     ]),
)


@ddt
class TestDataNodeExtract01(TestCase):
    def setUp(self) -> None:
        data_node_index = 1
        data_node_specifier = DataNodeSpecifier(data_node_specifier_test_driver[0])

        tag_delimiters_text = ('[*', '*]')

        outline_file_path = os.path.join(tcfg.input_files_root, 'data_node_descriptor', 'opml_data_extraction_test_01.opml')

        outline = Outline.from_opml(outline_file_path)
        unleashed_outline = UnleashedOutline(outline, default_text_tag_delimiter=tag_delimiters_text)

        data_node = unleashed_outline.list_unleashed_nodes()[data_node_index].node()

        self.extracted_data_table = data_node_specifier.extract_data_node_dispatch(data_node)

        pass

        # outline_parser = OutlineParser(outline_file_path, tag_delimiters_text)
        # self.extracted_data_table = outline_parser.extract_data_node(
        #     data_node_index=data_node_index,
        #     data_node_descriptor=data_node_specifier
        # )

    def test_data_node_extract_properties(self):
        self.assertIsInstance(self.extracted_data_table, List)

    def test_data_node_number_of_fields(self):
        test_record = self.extracted_data_table[0]  # Any record will do, but there must be at least one
        self.assertEqual(4, len(test_record))

    def test_data_node_field_type(self):
        test_record = self.extracted_data_table[0]  # Any record will do, but there must be at least one
        for field in test_record:
            value = test_record[field]
            self.assertIsInstance(value, str)

    def test_data_node_first_record(self):
        test_record = self.extracted_data_table[0]

        expected_record = {
            'risk_description': 'There is a possibility that the world might end',
            'likelihood': 'Low',
            'impact': 'Very High',
            'mitigation': 'Pray every day'
        }
        self.assertEqual(expected_record, test_record)

    def test_data_node_number_of_records(self):
        self.assertEqual(3, len(self.extracted_data_table))

    @data(
        (0, 'There is a possibility that the world might end', 'Low', 'Very High', 'Pray every day'),
        (1, 'It may take too long to build and we don\'t have anything in the meantime', 'High', 'High', '(unfilled)'),
        (2, 'It may be too expensive to build', 'High', 'Medium', '(unfilled)')
    )
    @unpack
    def test_data_node_values(self, record_number, description, likelihood, impact, mitigation):

        """
        Args:
            record_number:
            description:
            likelihood:
            impact:
            mitigation:
        """
        self.assertTrue(len(self.extracted_data_table) >= record_number + 1, 'More test records than data records')
        test_record = self.extracted_data_table[record_number]
        self.assertEqual(description, test_record['risk_description'])
        self.assertEqual(likelihood, test_record['likelihood'])
        self.assertEqual(impact, test_record['impact'])
        self.assertEqual(mitigation, test_record['mitigation'])
