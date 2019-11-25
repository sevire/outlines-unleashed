from unittest import TestCase
from opml.node_matching_criteria import NodeAncestryMatchingCriteria
from opml.outline import Outline
import os
import tests.test_config as tcfg
from ddt import ddt, idata, unpack

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

extracted_data_values = (
    (0, 'Section 1', 'Slide 1', 'Bullet A'),
    (1, 'Section 1', 'Slide 1', 'Bullet B'),
    (2, 'Section 1', 'Slide 1', 'Bullet C'),
    (3, 'Section 1', 'Slide 2', 'Bullet D'),
    (4, 'Section 1', 'Slide 2', 'Bullet E'),
    (5, 'Section 1', 'Slide 2', 'Bullet F'),
    (6, 'Section 1', 'Slide 2', 'Bullet G'),
    (7, 'Section 1', 'Slide 3', '(unfilled)'),
    (8, 'Section 2', 'Slide 4', 'Bullet H'),
    (9, 'Section 2', 'Slide 4', 'Bullet I'),
    (10, 'Section 2', 'Slide 4', 'Bullet J'),
    (11, 'Section 2', 'Slide 5', 'Bullet K'),
    (12, 'Section 2', 'Slide 5', 'Bullet L'),
    (13, 'Section 2', 'Slide 5', 'Bullet M'),
    (14, 'Section 2', 'Slide 5', 'Bullet N'),
    (15, 'Section 2', 'Slide 6', '(unfilled)'),
    (16, 'Section 3', '(unfilled)', '(unfilled)'),
    (17, 'Section 4', 'Slide 7', '(unfilled)'),
    (18, 'Section 4', 'Slide 8', 'Bullet O'),
    (19, 'Section 4', 'Slide 8', 'Bullet P'),
    (20, 'Section 4', 'Slide 8', 'Bullet Q'),
)


def data_value_generator():
    for expected_record in extracted_data_values:
        yield expected_record[0], expected_record[1], expected_record[2], expected_record[3]


@ddt
class TestDataNodeExtract02(TestCase):
    def test_data_node_extract_num_records(self):

        outline = Outline.from_opml(
            os.path.join(tcfg.test_resources_root, 'opml_data_extraction_test_02.opml'))

        outline_node_list = list(outline.list_all_nodes())
        data_node = outline_node_list[1].node()

        extracted_data_records = data_node.extract_data_node(test_data_node_specifier)

        expected_num_records = 21

        self.assertEqual(expected_num_records, len(extracted_data_records))

    @idata(data_value_generator())
    @unpack
    def test_data_node_extract_record_values(self, index, section, slide, bullet):

        outline = Outline.from_opml(
            os.path.join(tcfg.test_resources_root, 'opml_data_extraction_test_02.opml'))

        outline_node_list = list(outline.list_all_nodes())
        data_node = outline_node_list[1].node()

        extracted_data_records = data_node.extract_data_node(test_data_node_specifier)

        test_record = extracted_data_records[index]
        self.assertEqual(section, test_record['section_name'])
        self.assertEqual(slide, test_record['slide_name'])
        self.assertEqual(bullet, test_record['bullet'])
