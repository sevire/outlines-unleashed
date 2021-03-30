from outlines_unleashed.node_ancestry_matching_criteria import NodeAncestryMatchingCriteria

data_node_specifier_csv_test_01 = {
    'header': {
        'descriptor_version_number': '0.1',
        'tag_delimiters': {
            'text_delimiters': ["[*", "*]"],
            'note_delimiters': ["[*", "*]"]
        }
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
            'default_value': '(unfilled)',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(text='Risks'),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(child_number=1, text='Attributes'),
                NodeAncestryMatchingCriteria(text_tag='M')
            ]
        }
    }
}