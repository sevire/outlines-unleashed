"""
Tests functionality to extract nodes which match users (or template's) criteria.
"""
import os
from unittest import TestCase
from ddt import ddt, unpack, data

from opml.node_ancestry_record import NodeAncestryRecord
from opml.node_matching_criteria import NodeAncestryMatchingCriteria
from opml.outline import Outline
import tests.test_config as tcfg

ancestry_node_criteria = (
    (
        3, [
            NodeAncestryMatchingCriteria(child_number=1),
            NodeAncestryMatchingCriteria(child_number=1),
            NodeAncestryMatchingCriteria(child_number=1)
        ]
    ),
    (
        3, [
            NodeAncestryMatchingCriteria(1),
            NodeAncestryMatchingCriteria(1, text_tag='TAG-TEXT-H2B'),
            NodeAncestryMatchingCriteria(1, text='H3: Heading C')
        ]
    ),
    (
        20, [
            NodeAncestryMatchingCriteria(2),
            NodeAncestryMatchingCriteria(1),
            NodeAncestryMatchingCriteria(1),
            NodeAncestryMatchingCriteria(1)
        ]
    )
)

node_match_criteria_01 = NodeAncestryMatchingCriteria(text='Risks')
node_match_criteria_01a = NodeAncestryMatchingCriteria()
node_match_criteria_02 = NodeAncestryMatchingCriteria(child_number=1, text_tag='Attributes')
node_match_criteria_03 = NodeAncestryMatchingCriteria(text_tag='L')
node_match_criteria_04 = NodeAncestryMatchingCriteria(text_tag='I')
node_match_criteria_05 = NodeAncestryMatchingCriteria(text_tag='M')

data_extraction_driver_data_risks = {
    'risk_description': {
        'primary_key': 'single', # Values: start, end, single, null
        'type': 'string',
        'ancestry_matching_criteria': [
            node_match_criteria_01,
            node_match_criteria_01a,
        ],
    },
    'likelihood': {
        'primary_key': 'no',  # Values: start, end, single, null
        'type': 'string',
        'ancestry_matching_criteria': [
            node_match_criteria_01,
            node_match_criteria_01a,
            node_match_criteria_02,
            node_match_criteria_03,
        ],
        },
    'impact': {
        'primary_key': 'no',  # Values: start, end, single, null
        'type': 'string',
        'ancestry_matching_criteria': [
            node_match_criteria_01,
            node_match_criteria_01a,
            node_match_criteria_02,
            node_match_criteria_04,
        ]
    },
    'mitigation': {
        'primary_key': 'no',  # Values: start, end, single, null
        'type': 'string',
        'ancestry_matching_criteria': [
            node_match_criteria_01,
            node_match_criteria_01a,
            node_match_criteria_02,
            node_match_criteria_05,
        ]
    }
}

node_match_data = (
    (1, 'risk_description', 'There is a possibility that the world might end'),
    (3, 'likelihood', 'Low'),
    (4, 'impact', 'Very Low'),
    (5, 'mitigation', 'Pray every day')
)


@ddt
class TestFindMatchingNodes(TestCase):

    @unpack
    @data(*ancestry_node_criteria)
    def test_criteria_matching(self, index, ancestry_criteria_list):
        """
        Tests that ancestry associated with a node is calculated correctly.

        :param index: The index within the node_list where the targeted test node should be found.
        :param ancestry_criteria_list: A list of criteria to be used to test against the tested node.  The tested node
                                       should match with the supplied criteria.
        :return:
        """
        tag_delimiters_text = (r'(-', r'-)')
        tag_regex_note = (r'(-', r'-)')

        outline = Outline.from_opml(os.path.join(tcfg.test_resources_root,
                                    'opml-test-valid-01.opml'),
                                    tag_delimiters_text
                                    )

        node_list = list(outline.list_all_nodes())

        ancestry_at_test_node = node_list[index]
        depth = len(ancestry_criteria_list)

        for index in range(depth):
            level = index + 1
            ancestry_at_level = NodeAncestryRecord(ancestry_at_test_node[:level+1])
            node_at_level = list(filter(lambda x: x == ancestry_at_level, node_list))

            self.assertEqual(1, len(node_at_level))
            self.assertTrue(ancestry_criteria_list[level].matches_criteria(node_at_level[0]))

    @data(*node_match_data)
    @unpack
    def test_data_extraction(self, index, expected_field_name, expected_field_value):
        tag_delimiters_text = ('[*', '*]')
        tag_regex_note = ('[*', '*]')

        outline = Outline.from_opml(os.path.join(tcfg.test_resources_root,
                                    'data_extract_test_file_01.opml'),
                                    tag_delimiters_text
                                    )

        # Child elements accessed as though node is a list.  So
        data_node = outline.outline[0]  # This should be the node with text "Data for Parsing #1" or similar.

        match_list = data_node.match_data_node(data_extraction_driver_data_risks)

        self.assertEqual(10, len(match_list))

