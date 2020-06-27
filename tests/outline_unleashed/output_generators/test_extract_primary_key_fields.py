from unittest import TestCase

from outline.outline_node import OutlineNode
from outlines_unleashed.data_node_specifier import DataNodeSpecifier
from outlines_unleashed.node_ancestry_matching_criteria import NodeAncestryMatchingCriteria
from ddt import ddt

data_node_specifier_test_driver = [
    {
        'header': {
            'descriptor_version_number': "0.1"
        },
        'descriptor': {
            'risk_description': {
                'primary_key': 'yes',  # Values: start, end, single, null
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
        }
    },
    {
        'header': {
            'descriptor_version_number': "0.1"
        },
        'descriptor': {
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
        }
    }]


@ddt
class TestExtractFieldNames(TestCase):
    def test_extract_primary_key_field_names(self):
        specifier = DataNodeSpecifier(data_node_specifier_test_driver[0])
        key_field_names = specifier.extract_field_names(primary_key_only=True)

        expected_field_names = [
            'risk_description'
        ]
        self.assertEqual(expected_field_names, key_field_names)

    def test_extract_non_primary_key_field_names(self):
        specifier = DataNodeSpecifier(data_node_specifier_test_driver[0])
        key_field_names = specifier.extract_field_names(primary_key_only=False)

        expected_field_names = [
            'likelihood',
            'impact',
            'mitigation'
        ]
        self.assertEqual(expected_field_names, key_field_names)

    def test_extract_all_field_names(self):
        specifier = DataNodeSpecifier(data_node_specifier_test_driver[0])
        key_field_names = specifier.extract_field_names(primary_key_only=None)

        expected_field_names = [
            'risk_description',
            'likelihood',
            'impact',
            'mitigation'
        ]
        self.assertEqual(expected_field_names, key_field_names)
