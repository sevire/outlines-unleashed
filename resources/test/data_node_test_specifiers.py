from opml.node_matching_criteria import NodeAncestryMatchingCriteria

test_data_node_specifier_ppt_01 = {
    'header': {
        'descriptor_version_number': '0.1'
    },
    'descriptor': {
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
}

test_data_node_specifier_03x = {
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

test_data_node_specifier_05x = {
    'header': {
        'descriptor_version_number': '0.1'
    },
    'descriptor': {
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
}
test_data_node_specifier_06x = {
    'header': {
        'descriptor_version_number': '0.1'
    },
    'descriptor': {
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
        }
    }
}

test_data_node_specifier_07 = {
    'header': {
        'descriptor_version_number': '0.1'
    },
    'descriptor': {
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
}

test_data_node_specifier_freeform_notes = {
    'header': {
        'descriptor_version_number': '0.1'
    },
    'descriptor': {
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
}

data_node_specifier_test_driver = [
    {
        'header': {
            'descriptor_version_number': '0.1'
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
            'descriptor_version_number': '0.1'
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