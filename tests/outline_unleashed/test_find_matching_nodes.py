"""
Tests functionality to extract nodes which match users (or template's) criteria.
"""
import os
from unittest import TestCase
from ddt import ddt, unpack, data

from opml.node_matching_criteria import NodeAncestryMatchingCriteria
from opml.outline import Outline
import tests.test_config as tcfg
from opml.outline_node import OutlineNode

ancestry_node_criteria = (
    (
        3, [
            NodeAncestryMatchingCriteria(),  # No criteria for root node
            NodeAncestryMatchingCriteria(child_number=1),
            NodeAncestryMatchingCriteria(child_number=1),
            NodeAncestryMatchingCriteria(child_number=1)
        ]
    ),
    (
        3, [
            NodeAncestryMatchingCriteria(),  # No criteria for root node
            NodeAncestryMatchingCriteria(1),
            NodeAncestryMatchingCriteria(1, text_tag='TAG-TEXT-H2B'),
            NodeAncestryMatchingCriteria(1, text='H3: Heading C')
        ]
    ),
    (
        20, [
            NodeAncestryMatchingCriteria(),  # No criteria for root node
            NodeAncestryMatchingCriteria(2),
            NodeAncestryMatchingCriteria(1),
            NodeAncestryMatchingCriteria(1),
            NodeAncestryMatchingCriteria(1)
        ]
    )
)

# Matching Criteria for Data Node 1
node_match_criteria_00 = NodeAncestryMatchingCriteria()  # Null criteria for root node
node_match_criteria_01 = NodeAncestryMatchingCriteria(text='Risks')
node_match_criteria_01a = NodeAncestryMatchingCriteria()
node_match_criteria_02 = NodeAncestryMatchingCriteria(child_number=1, text='Attributes')
node_match_criteria_03 = NodeAncestryMatchingCriteria(text_tag='L')
node_match_criteria_04 = NodeAncestryMatchingCriteria(text_tag='I')
node_match_criteria_05 = NodeAncestryMatchingCriteria(text_tag='M')

# Matching Criteria for Data Node 2
node_match_criteria_10 = NodeAncestryMatchingCriteria()
node_match_criteria_11 = NodeAncestryMatchingCriteria(text='Risks')
node_match_criteria_12 = NodeAncestryMatchingCriteria()
node_match_criteria_13 = NodeAncestryMatchingCriteria()
node_match_criteria_14 = NodeAncestryMatchingCriteria(child_number=1, text='Attributes')
node_match_criteria_15 = NodeAncestryMatchingCriteria(text_tag='I')
node_match_criteria_16 = NodeAncestryMatchingCriteria(text_tag='M')


data_node_specifier_test_driver = [
    {
        'risk_description': {
            'primary_key': 'yes',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                node_match_criteria_00,
                node_match_criteria_01,
                node_match_criteria_01a,
            ],
        },
        'likelihood': {
            'primary_key': 'no',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                node_match_criteria_00,
                node_match_criteria_01,
                node_match_criteria_01a,
                node_match_criteria_02,
                node_match_criteria_03,
            ],
        },
        'impact': {
            'primary_key': 'no',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                node_match_criteria_00,
                node_match_criteria_01,
                node_match_criteria_01a,
                node_match_criteria_02,
                node_match_criteria_04,
            ]
        },
        'mitigation': {
            'primary_key': 'no',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                node_match_criteria_00,
                node_match_criteria_01,
                node_match_criteria_01a,
                node_match_criteria_02,
                node_match_criteria_05,
            ]
        }
    },
    {
        'risk_description': {
            'primary_key': 'yes',  # Values: start, end, single, null
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

match_data_node_test_data = (
    (0, 1,
     [
         ('risk_description', 'There is a possibility that the world might end'),
         ('likelihood', 'Low'),
         ('impact', 'Very High'),
         ('mitigation', 'Pray every day'),
         ('risk_description', 'It may take too long to build and we don\'t have anything in the meantime'),
         ('impact', 'High'),
         ('likelihood', 'High'),
         ('risk_description', 'It may be too expensive to build'),
         ('likelihood', 'High'),
         ('impact', 'Medium')
     ]
     ),
    (1, 16,
     [
         ('likelihood', 'High'),
         ('risk_description', 'It may take too long to build and we don\'t have anything in the meantime'),
         ('impact', 'High'),
         ('risk_description', 'It may be too expensive to build'),
         ('impact', 'Medium'),
         ('likelihood', 'Low'),
         ('risk_description', 'There is a possibility that the world might end'),
         ('impact', 'Very High'),
         ('mitigation', 'Pray every day'),
     ]
     )
)

node_match_data = (
    (1, 2, 'risk_description', 'There is a possibility that the world might end'),
    (1, 4, 'likelihood', 'Low'),
    (1, 5, 'impact', 'Very High'),
    (1, 6, 'mitigation', 'Pray every day'),
    (1, 7, 'risk_description', 'It may take too long to build and we don\'t have anything in the meantime'),
    (1, 9, 'impact', 'High'),
    (1, 10, 'likelihood', 'High'),
    (1, 11, 'risk_description', 'It may be too expensive to build'),
    (1, 13, 'likelihood', 'High'),
    (1, 14, 'impact', 'Medium')
)


@ddt
class TestFindMatchingNodes(TestCase):
    def setUp(self) -> None:
        tag_delimiters_text = ('[*', '*]')

        outline = Outline.from_opml(os.path.join(tcfg.test_resources_root,
                                    'opml_data_extraction_test_01.opml'),
                                    tag_delimiters_text
                                    )

        # Create list of all nodes (plus ancestry) to allow acess to nodes by index.
        self.node_list = list(outline.list_all_nodes())

    @data(*node_match_data)
    @unpack
    def test_match_node(self, data_node_index, field_node_index, expected_field_name, expected_field_value):
        # Now extract the test data node (root node of sub-tree where field nodes are located)
        """
        Args:
            data_node_index:
            field_node_index:
            expected_field_name:
            expected_field_value:
        """
        data_node = self.node_list[data_node_index]
        data_node_list = list(data_node.node().list_all_nodes())
        field_node = data_node_list[field_node_index]

        test_matching_criteria = \
            data_node_specifier_test_driver[0][expected_field_name]['ancestry_matching_criteria']

        # Confirm that the field node matches with the appropriate criteria.
        self.assertTrue(OutlineNode.match_field(field_node, test_matching_criteria))

    @data(*node_match_data)
    @unpack
    def test_match_field_node(self, data_node_index, field_node_index, expected_field_name, expected_field_value):
        # Now extract the test data node (root node of sub-tree where field nodes are located)
        """
        Args:
            data_node_index:
            field_node_index:
            expected_field_name:
            expected_field_value:
        """
        data_node = self.node_list[data_node_index]
        data_node_list = list(data_node.node().list_all_nodes())
        field_node = data_node_list[field_node_index]

        match_data = OutlineNode.match_field_node(field_node, data_node_specifier_test_driver[0])
        self.assertIsNotNone(match_data)

        field_name, field_value = match_data
        self.assertEqual(expected_field_name, field_name)
        self.assertEqual(expected_field_value, field_value)

    @data(*match_data_node_test_data)
    @unpack
    def test_match_data_node(self, specifier_index, data_node_index, expected_field_data):
        """
        Args:
            specifier_index:
            data_node_index:
            expected_field_data:
        """
        data_node = self.node_list[data_node_index].node()

        matched_data_items = data_node.match_data_node(data_node_specifier_test_driver[specifier_index])

        self.assertEqual(match_data_node_test_data[specifier_index][2], matched_data_items)
