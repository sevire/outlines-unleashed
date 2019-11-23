"""
Test which invokes extraction of a data node and gets a data structure of the right format back, based
on the data node provided and the data node descriptor provided.

Calls extract_data_node() method upon the root of a data node sub-tree (OutlineNode) within a parsed
outline.

Gets in return a List of Dicts where each field in the dict corresponds to the fields in the specifier.
"""
from typing import List
from unittest import TestCase

from opml.node_matching_criteria import NodeAncestryMatchingCriteria
from opml.outline import Outline
import tests.test_config as tcfg
import os
from ddt import ddt, data, unpack

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

data_node_specifier_test_driver = [
    {
        'risk_description': {
            'primary_key': 'single',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(text='Risks'),
                NodeAncestryMatchingCriteria()
            ],
        },
        'likelihood': {
            'primary_key': 'no',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(text='Risks'),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(child_number=1, text='Attributes'),
                NodeAncestryMatchingCriteria(text_tag='L')
            ],
        },
        'impact': {
            'primary_key': 'no',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(text='Risks'),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(child_number=1, text='Attributes'),
                NodeAncestryMatchingCriteria(text_tag='I')
            ]
        },
        'mitigation': {
            'primary_key': 'no',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(text='Risks'),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(child_number=1, text='Attributes'),
                NodeAncestryMatchingCriteria(text_tag='M')
            ]
        }
    },
    {
        'risk_description': {
            'primary_key': 'single',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(text='Risks'),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria()
            ],
        },
        'likelihood': {
            'primary_key': 'no',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(text='Risks'),
                NodeAncestryMatchingCriteria(),
            ]
        },
        'impact': {
            'primary_key': 'no',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(text='Risks'),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(child_number=1, text='Attributes'),
                NodeAncestryMatchingCriteria(text_tag='I')
            ],
        },
        'mitigation': {
            'primary_key': 'no',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(text='Risks'),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(child_number=1, text='Attributes'),
                NodeAncestryMatchingCriteria(text_tag='M')
            ],
        },
    }]

@ddt
class TestDataNodeExtract01(TestCase):
    def setUp(self) -> None:
        tag_delimiters_text = ('[*', '*]')

        outline = Outline.from_opml(os.path.join(tcfg.test_resources_root,
                                                 'data_extract_test_file_01.opml'),
                                    tag_delimiters_text
                                    )

        # Create list of all nodes (plus ancestry) to allow acess to nodes by index.
        self.node_list = list(outline.list_all_nodes())

    @data(*data_driver_01)
    @unpack
    def test_data_node_extract_01(self, data_node_index, data_node_descriptor_index, expected_field_data):
        test_data_node = self.node_list[data_node_index]
        extracted_data_table = test_data_node.extract_data_node(
            test_data_node,
            data_node_specifier_test_driver[data_node_descriptor_index]
        )
        self.assertIsInstance(extracted_data_table, List)
        self.assertEqual(len(expected_field_data), extracted_data_table)
        self.assertTrue(False)