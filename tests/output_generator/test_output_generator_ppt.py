"""
Checks properties of a .PPT file to aid in testing against expected after creating from an outline.
"""
import os
from unittest import TestCase
from ddt import ddt, data, unpack
import tests.test_utilities.test_config as tcfg
from outline.outline import Outline
from outlines_unleashed.unleashed_outline import UnleashedOutline
from output_generators.ppt_output_generators import PowerPointGenerator
from tests.test_utilities.ppt_utilities import get_slide_data

test_file_folder_relative = os.path.join('output_generator')

opml_filename = "opml_output_generator_test_01.opml"

test_data = [
    (opml_filename, 0, 'slide_01_pres_title', 0, "Data Node 1"),
    (opml_filename, 1, "slide_01_pres_subtitle", 0, "Slide Deck"),
    (opml_filename, 2, "slide_02_section_title", 0, "Section 1"),
    (opml_filename, 3, "slide_02_section_subtitle", 0, ""),
    (opml_filename, 4, "slide_03_slide_title", 0, "Slide 1"),
    (opml_filename, 5, "slide_03_slide_01_bullet_01", 0, "Bullet A"),
    (opml_filename, 6, "slide_03_slide_01_bullet_02", 0, "Bullet B"),
    (opml_filename, 7, "slide_03_slide_01_bullet_03", 0, "Bullet C"),
    (opml_filename, 8, "slide_04_slide_title", 0, "Slide 2"),
    (opml_filename, 9, "slide_04_slide_02_bullet_01", 0, "Bullet D"),
    (opml_filename, 10, "slide_04_slide_02_bullet_02", 0, "Bullet E"),
    (opml_filename, 11, "slide_04_slide_02_bullet_03", 1, "Bullet F"),
    (opml_filename, 12, "slide_04_slide_02_bullet_04", 0, "Bullet G"),
    # (0, 'NAME', 0, ''),
    # (0, 'NAME', 0, 'Section 1'),
    # (0, 'NAME', 0, 'Slide 1'),
    # (0, 'NAME', 0, ''),
    # (0, 'NAME', 0, 'Bullet A'),
    # (1, 'NAME', 0, 'Bullet B (indented)'),
    # (0, 'NAME', 0, 'Bullet C'),
    # (0, 'NAME', 0, 'Slide 2'),
    # (0, 'NAME', 0, ''),
    # (0, 'NAME', 0, 'Bullet D'),
    # (0, 'NAME', 0, 'Bullet E'),
    # (0, 'NAME', 0, 'Bullet F'),
    # (0, 'NAME', 0, 'Bullet G'),
    # (0, 'NAME', 0, 'Slide 3'),
    # (0, 'NAME', 0, ''),
    # (0, 'NAME', 0, ''),
    # (0, 'NAME', 0, 'Section 2'),
    # (0, 'NAME', 0, 'Slide 4'),
    # (0, 'NAME', 0, ''),
    # (0, 'NAME', 0, 'Bullet H'),
    # (0, 'NAME', 0, 'Bullet I'),
    # (0, 'NAME', 0, 'Bullet J'),
    # (0, 'NAME', 0, 'Slide 5'),
    # (0, 'NAME', 0, ''),
    # (0, 'NAME', 0, 'Bullet K'),
    # (0, 'NAME', 0, 'Bullet L'),
    # (0, 'NAME', 0, 'Bullet M'),
    # (0, 'NAME', 0, 'Bullet N'),
    # (0, 'NAME', 0, 'Slide 6'),
    # (0, 'NAME', 0, ''),
    # (0, 'NAME', 0, ''),
    # (0, 'NAME', 0, 'Section 3'),
    # (0, 'NAME', 0, ''),
    # (0, 'NAME', 0, 'Section 4'),
    # (0, 'NAME', 0, 'Slide 7'),
    # (0, 'NAME', 0, ''),
    # (0, 'NAME', 0, 'Slide 8'),
    # (0, 'NAME', 0, ''),
    # (0, 'NAME', 0, 'Bullet O'),
    # (0, 'NAME', 0, 'Bullet P'),
    # (0, 'NAME', 0, 'Bullet Q'),
]


@ddt
class TestOutputGeneratorPpt(TestCase):
    @data(*test_data)
    @unpack
    def test_output_generator_ppt_01(self, filename, record_num, record_name, expected_level, expected_text):
        test_data_file = os.path.join(tcfg.input_files_root,
                                      test_file_folder_relative,
                                      filename)

        test_ppt_template = os.path.join(tcfg.input_files_root,
                                         test_file_folder_relative,
                                         "ppt_template_01.pptx")

        test_ppt_output_path = os.path.join(tcfg.output_files_root,
                                            test_file_folder_relative,
                                            "ppt_output_01.pptx")
        outline = Outline.from_opml(test_data_file)
        unleashed_outline = UnleashedOutline(outline, default_text_tag_delimiter=['', ':'])

        data_node_generators = unleashed_outline.extract_data_nodes()
        data_node_name = data_node_generators[0]['data_node_name']

        self.assertEqual('data_node_01', data_node_name)

        data_node_list_index = data_node_generators[0]['data_node_list_index']

        data_node = unleashed_outline.list_unleashed_nodes()[data_node_list_index].node()

        generator = PowerPointGenerator()
        generator.create_power_point_skeleton(data_node, test_ppt_template, test_ppt_output_path)

        ppt_records = list(get_slide_data(test_ppt_output_path))

        test_level, test_text = ppt_records[record_num]

        self.assertEqual(expected_level, test_level, f"Failed on {record_name}")
        self.assertEqual(expected_text, test_text)
