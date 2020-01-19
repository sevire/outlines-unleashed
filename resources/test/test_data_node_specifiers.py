from opml.node_matching_criteria import NodeAncestryMatchingCriteria

test_data_node_specifier_ppt_01 = {
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
test_data_node_specifier_03x = {
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
test_data_node_specifier_05x = {
    'topic': {
        'primary_key': 'yes',
        'type': 'string',
        'field_value_specifier': 'text_value',
        'ancestry_matching_criteria': [
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria()
        ]
    },
    'speaker': {
        'primary_key': 'yes',
        'type': 'string',
        'field_value_specifier': 'text_value',
        'ancestry_matching_criteria': [
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(text_tag='Person'),
        ]
    },
    'note': {
        'primary_key': 'yes',
        'type': 'string',
        'field_value_specifier': 'text_value',
        'ancestry_matching_criteria': [
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(),
        ]
    }
}
test_data_node_specifier_06x = {
    'category': {
        'primary_key': 'yes',
        'type': 'string',
        'field_value_specifier': 'text_value',
        'ancestry_matching_criteria': [
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(text_tag='Category')
        ]
    },
    'item': {
        'primary_key': 'yes',
        'type': 'string',
        'field_value_specifier': 'text_value',
        'ancestry_matching_criteria': [
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(text_tag='Item')
        ]
    },
    'date_due': {
        'primary_key': 'yes',
        'type': 'string',
        'field_value_specifier': 'text_value',
        'ancestry_matching_criteria': [
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(text_tag='Date')
        ]
    },
}
test_data_node_specifier_07 = {
    'category': {
        'primary_key': 'yes',
        'type': 'string',
        'field_value_specifier': 'text_value',
        'ancestry_matching_criteria': [
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(text_tag='Category')
        ]
    },
    'item': {
        'primary_key': 'yes',
        'type': 'string',
        'field_value_specifier': 'text_value',
        'ancestry_matching_criteria': [
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(text_tag='Item')
        ]
    },
    'date_due': {
        'primary_key': 'no',
        'type': 'string',
        'field_value_specifier': 'text_value',
        'ancestry_matching_criteria': [
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(text_tag='Date')
        ]
    },
}
test_data_node_specifier_freeform_notes = {
    'Topic': {
        'primary_key': 'yes',
        'type': 'string',
        'field_value_specifier': 'text_value',
        'ancestry_matching_criteria': [
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(text_tag='Topic'),
        ]
    },
    'Speaker': {
        'primary_key': 'yes',
        'type': 'string',
        'field_value_specifier': 'text_value',
        'ancestry_matching_criteria': [
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(text_tag='Who'),
        ]
    },
    'Note': {
        'primary_key': 'yes',
        'type': 'string',
        'field_value_specifier': 'text_value',
        'ancestry_matching_criteria': [
            NodeAncestryMatchingCriteria(),
            NodeAncestryMatchingCriteria(),
        ]
    }
}