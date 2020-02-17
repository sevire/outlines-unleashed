from opml.node_matching_criteria import NodeAncestryMatchingCriteria

test_json_descriptor_01 = {
    'header': {
        'descriptor_version_number': '0.1',
        'tag_delimiters': {
            'note_delimiters': ['[*', '*]'],
            'text_delimiters': ['[*', '*]']
        }
    },
    'descriptor': {
        'key_field_1': {
            'primary_key': 'yes',
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
            ]
    },
        'key_field_2': {
            'primary_key': 'yes',
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
            ]
        },
        'data_field_1': {
            'primary_key': 'no',
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(child_number=1),
            ]
        },
        'data_field_2': {
            'primary_key': 'no',
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(child_number=2),
            ]
        },
        'data_field_3': {
            'primary_key': 'no',
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(child_number=3),
            ]
        }
    }
}
