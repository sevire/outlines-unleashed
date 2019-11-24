from unittest import TestCase
from opml.node_matching_criteria import NodeAncestryMatchingCriteria
from opml.outline import Outline
import os
import tests.test_config as tcfg

test_data_node_specifier = {
    'section_name': {
        'primary_key': 'yes',  # Values: start, end, single, null
        'type': 'string',
        'field_value_specifier': 'text_value',
        'ancestry_matching_criteria': [
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(),
        ]
    },
    'slide_name': {
        'primary_key': 'yes',  # Values: start, end, single, null
        'type': 'string',
        'field_value_specifier': 'text_value',
        'ancestry_matching_criteria': [
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(),
        ]
    },
    'bullet': {
        'primary_key': 'yes',  # Values: start, end, single, null
        'type': 'string',
        'field_value_specifier': 'text_value',
        'ancestry_matching_criteria': [
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(),
        ]
    }
}


class TestDataNodeExtract02(TestCase):
    def test_data_node_extract_02_01(self):

        outline = Outline.from_opml(
            os.path.join(tcfg.test_resources_root, 'opml_data_extraction_test_01.opml'))

        outline_node_list = list(outline.list_all_nodes())
        data_node = outline_node_list[1].node()

        extracted_data_records = data_node.extract_data_node(test_data_node_specifier)

        expected_num_records = 22

        self.assertEqual(expected_num_records, len(extracted_data_records))



