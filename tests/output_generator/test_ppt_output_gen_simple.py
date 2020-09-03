from unittest import TestCase
import os

from ddt import ddt, unpack, data

from outline.outline import Outline
from outlines_unleashed.data_node_specifier import DataNodeSpecifier
from outlines_unleashed.node_ancestry_matching_criteria import NodeAncestryMatchingCriteria
from outlines_unleashed.unleashed_outline import UnleashedOutline
from output_generators.ppt_output_generator_simple import PptOutputGeneratorSimple
from tests.test_utilities.ppt_utilities import get_slide_data
from tests.test_utilities.test_config import input_files_root, output_files_root

test_file_folder_relative = "output_generator"
filename = "opml_output_generator_test_02.opml"

dns = {
    'header': {
        'descriptor_version_number': '0.1'
    },
    'descriptor': {
        'slide_deck_title': {
            'primary_key': 'yes',
            'type': 'string',
            'default_value': 'This is an auto-generated title',
            'field_value_specifier': 'text_tag',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
            ]
        },
        'slide_deck_sub_title': {
            'primary_key': 'yes',
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
            ]
        },
        'section_title': {
            'primary_key': 'yes',
            'type': 'string',
            'field_value_specifier': 'text_tag',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
            ]
        },
        'section_sub_title': {
            'primary_key': 'yes',
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
            ]
        },
        'slide_title': {
            'primary_key': 'yes',
            'type': 'string',
            'field_value_specifier': 'text_tag',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
            ]
        },
        'slide_sub_title': {
            'primary_key': 'yes',
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
            ]
        },
        'bullet-01': {
            'primary_key': 'yes',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
            ]
        },
        'bullet-02': {
            'primary_key': 'yes',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
            ]
        },
        'bullet-03': {
            'primary_key': 'yes',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
            ]
        },
        'bullet-04': {
            'primary_key': 'yes',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
            ]
        },
        'bullet-05': {
            'primary_key': 'yes',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
            ]
        },
        'bullet-06': {
            'primary_key': 'yes',  # Values: start, end, single, null
            'type': 'string',
            'field_value_specifier': 'text_value',
            'ancestry_matching_criteria': [
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
                NodeAncestryMatchingCriteria(),
            ]
        }
    }
}

test_data = [
    (filename, 0, 'slide_01_pres_title', 0, "Slide Deck Title"),
    (filename, 1, "slide_01_pres_subtitle", 0, "Slide Deck SubTitle"),
    (filename, 2, "slide_02_section_title", 0, "Section 1"),
    (filename, 3, "slide_02_section_subtitle", 0, "Thursday update"),
    (filename, 4, "slide_03_slide_title", 0, "Slide 1"),
    (filename, 5, "slide_03_slide_01_bullet_01", 0, "Bullet A"),
    (filename, 6, "slide_03_slide_01_bullet_02", 0, "Bullet B"),
    (filename, 7, "slide_03_slide_01_bullet_03", 0, "Bullet C"),
    (filename, 8, "slide_04_slide_title", 0, "Slide 2"),
    (filename, 9, "slide_04_slide_02_bullet_01", 0, "Bullet D"),
    (filename, 10, "slide_04_slide_02_bullet_02", 0, "Bullet E"),
    (filename, 11, "slide_04_slide_02_bullet_03", 1, "Bullet F"),
    (filename, 12, "slide_04_slide_02_bullet_03", 2, "Bullet F-1"),
    (filename, 13, "slide_04_slide_02_bullet_03", 3, "Bullet F-2"),
    (filename, 14, "slide_04_slide_02_bullet_03", 4, "Bullet F-3"),
    (filename, 15, "slide_04_slide_02_bullet_03", 5, "Bullet F-4"),
    (filename, 16, "slide_04_slide_02_bullet_04", 0, "Bullet G"),
]


@ddt
class TestPptOutputGenSimple(TestCase):
    @unpack
    @data(*test_data)
    def test_output_generator(self, filename, record_num, record_name, expected_level, expected_text):
        test_data_file = os.path.join(input_files_root,
                                      test_file_folder_relative,
                                      filename)

        test_ppt_template = os.path.join(input_files_root,
                                         test_file_folder_relative,
                                         "ppt_template_02.pptx")

        test_ppt_output_path = os.path.join(output_files_root,
                                            test_file_folder_relative,
                                            "ppt_output_02.pptx")

        outline = Outline.from_opml(test_data_file)
        unleashed_outline = UnleashedOutline(outline, default_text_tag_delimiter=['', ':'])

        data_nodes = unleashed_outline.extract_data_nodes()
        data_node = unleashed_outline.list_unleashed_nodes()[data_nodes[0]['data_node_list_index']].node()

        data_node_descriptor = DataNodeSpecifier(dns)
        data_node_table = data_node_descriptor.extract_data_node_dispatch(data_node)
        PptOutputGeneratorSimple.generate_ppt(data_node_table, test_ppt_output_path, test_ppt_template)

        ppt_records = list(get_slide_data(test_ppt_output_path))

        test_level, test_text = ppt_records[record_num]

        self.assertEqual(expected_level, test_level, f"Failed on {record_name}")
        self.assertEqual(expected_text, test_text)

