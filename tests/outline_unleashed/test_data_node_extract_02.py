from unittest import TestCase
from opml.outline import Outline
import os
import tests.test_config as tcfg
from ddt import ddt, unpack, data

from resources.test.expected_results_data import extracted_data_values_01, extracted_data_values_02, \
    extracted_data_values_06, extracted_data_values_07
from resources.test.data_node_test_specifiers import test_data_node_specifier_ppt_01, test_data_node_specifier_03x, \
    test_data_node_specifier_05x, test_data_node_specifier_06x, test_data_node_specifier_07, \
    test_data_node_specifier_freeform_notes

# Potential shorter form data structure to define field specifiers
xxx = {
    '(field_name)': {
        'pk':  'yes',
        'type': 'string',
        'field_value_specifier': 'text_value'
    }

}


def data_value_generator(data_values_to_generate):
    """
    Args:
        data_values_to_generate:
    """
    for expected_record in data_values_to_generate:
        yield expected_record

@ddt
class TestDataNodeExtract02(TestCase):
    def test_data_node_extract_01(self):
        outline = Outline.from_opml(
            os.path.join(tcfg.test_resources_root, 'opml_data_extraction_test_02.opml'))

        outline_node_list = list(outline.list_all_nodes())
        data_node = outline_node_list[1].node()

        extracted_data_records = data_node.extract_data_node(test_data_node_specifier_ppt_01)

        expected_num_records = 21

        self.assertEqual(expected_num_records, len(extracted_data_records))

    @data(*extracted_data_values_01)
    @unpack
    def test_data_node_extract_02(self, index, section, slide, bullet):
        """
        Args:
            index:
            section:
            slide:
            bullet:
        """
        data_node_index = 1

        outline = Outline.from_opml(
            os.path.join(tcfg.test_resources_root, 'opml_data_extraction_test_02.opml'))

        outline_node_list = list(outline.list_all_nodes())
        data_node = outline_node_list[data_node_index].node()

        extracted_data_records = data_node.extract_data_node(test_data_node_specifier_ppt_01)

        test_record = extracted_data_records[index]
        self.assertEqual(section, test_record['section_name'])
        self.assertEqual(slide, test_record['slide_name'])
        self.assertEqual(bullet, test_record['bullet'])

    def test_data_node_extract_03(self):
        data_node_index = 31

        outline = Outline.from_opml(
            os.path.join(tcfg.test_resources_root, 'opml_data_extraction_test_02.opml'))

        outline_node_list = list(outline.list_all_nodes())
        data_node = outline_node_list[data_node_index].node()

        extracted_data_records = data_node.extract_data_node(test_data_node_specifier_03x)

        self.assertEqual(3, len(extracted_data_records))

    @data(*extracted_data_values_02)
    @unpack
    def test_data_node_extract_04(self, index,
                                  key1,
                                  key2,
                                  non_key1,
                                  non_key2,
                                  non_key3):
        """
        Args:
            index:
            key1:
            key2:
            non_key1:
            non_key2:
            non_key3:
        """
        data_node_index = 31

        outline = Outline.from_opml(
            os.path.join(tcfg.test_resources_root, 'opml_data_extraction_test_02.opml'))

        outline_node_list = list(outline.list_all_nodes())
        data_node = outline_node_list[data_node_index].node()

        extracted_data_records = data_node.extract_data_node(test_data_node_specifier_03x)
        test_record = extracted_data_records[index]

        self.assertEqual(key1, test_record['key_field_1'])
        self.assertEqual(key2, test_record['key_field_2'])
        self.assertEqual(non_key1, test_record['data_field_1'])
        self.assertEqual(non_key2, test_record['data_field_2'])
        self.assertEqual(non_key3, test_record['data_field_3'])

    def test_data_node_extract_05(self):
        data_node_index = 46

        outline = Outline.from_opml(
            os.path.join(tcfg.test_resources_root, 'opml_data_extraction_test_02.opml'),
            tag_text_delimiter=('', ':'))

        outline_node_list = list(outline.list_all_nodes())
        data_node = outline_node_list[data_node_index].node()

        extracted_data_records = data_node.extract_data_node(test_data_node_specifier_05x)

        pass

    @data(*extracted_data_values_06)
    @unpack
    def test_data_node_extract_06(self, index, category, note, date):
        """
        Args:
            index:
            category:
            note:
            date:
        """
        data_node_index = 1

        outline = Outline.from_opml(
            os.path.join(tcfg.test_resources_root, 'OutlinesUnleashed-Examples.opml'),
            tag_text_delimiter=('', ':'))

        outline_node_list = list(outline.list_all_nodes())
        data_node = outline_node_list[data_node_index].node()

        extracted_data_records = data_node.extract_data_node(test_data_node_specifier_06x)

        if category is None:  # Signals end of list and that the test is just to check number of records
            self.assertEqual(index, len(extracted_data_records), "Wrong number of records")
        else:
            test_record = extracted_data_records[index]
            self.assertEqual(category, test_record['category'])
            self.assertEqual(note, test_record['item'])
            self.assertEqual(date, test_record['date_due'])

    @data(*extracted_data_values_07)
    @unpack
    def test_data_node_extract_07(self, index, category, note, date):
        """
        Args:
            index:
            category:
            note:
            date:
        """
        data_node_index = 1

        outline = Outline.from_opml(
            os.path.join(tcfg.test_resources_root, 'OutlinesUnleashed-Examples.opml'),
            tag_text_delimiter=('', ':'))

        outline_node_list = list(outline.list_all_nodes())
        data_node = outline_node_list[data_node_index].node()

        extracted_data_records = data_node.extract_data_node(test_data_node_specifier_07)
        if category is None:  # Signals end of list and that the test is just to check number of records
            self.assertEqual(index, len(extracted_data_records), "Wrong number of records")
        else:
            test_record = extracted_data_records[index]
            self.assertEqual(category, test_record['category'])
            self.assertEqual(note, test_record['item'])
            self.assertEqual(date, test_record['date_due'])

    def test_data_node_freeform_notes(self):
        data_node_index = 1

        outline = Outline.from_opml(
            os.path.join(tcfg.test_resources_root, 'FreeFormNotesExample.opml'),
            tag_text_delimiter=('', ':'))

        outline_node_list = list(outline.list_all_nodes())
        data_node = outline_node_list[data_node_index].node()

        extracted_data_records = data_node.extract_data_node(test_data_node_specifier_freeform_notes)
        pass
