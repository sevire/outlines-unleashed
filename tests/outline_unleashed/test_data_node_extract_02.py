from unittest import TestCase
from opml.node_matching_criteria import NodeAncestryMatchingCriteria
from opml.outline import Outline
import os
import tests.test_config as tcfg
from ddt import ddt, idata, unpack, data

test_data_node_specifier_01 = {
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

# Potential shorter form data structure to define field specifiers
xxx = {
    '(field_name)': {
        'pk':  'yes',
        'type': 'string',
        'field_value_specifier': 'text_value'
    }

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

extracted_data_values_01 = (
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

extracted_data_values_02 = (
    (0, 'Key 1: Value 1', 'Key 2: Value 2', 'Non-key 1: Value 3', 'Non-key 2: Value 4', 'Non-key 3: Value 5'),
    (1, 'Key 1: Value 1', 'Key 2: Value 11', 'Non-key 1: Value 12', 'Non-key 2: Value 13', 'Non-key 3: Value 14'),
    (2, 'Key 1: Value 6', 'Key 2: Value 7', 'Non-key 1: Value 8', 'Non-key 2: Value 9', 'Non-key 3: Value 10'),
)

extracted_data_values_06 = (
    (0, 'Category 1', 'To do list item 1', '(unfilled)'),
    (1, 'Category 1', 'To do list item 2', 'date 1'),
    (2, 'Category 1', 'To do list item 2', 'date 2'),
    (3, 'Category 2', 'To do list item 3', '(unfilled)'),
    (4, 'Category 2', 'To do list item 4', '(unfilled)'),
    (5, None, None, None)  # Last record just used to check total number of records
)

extracted_data_values_07 = (
    (0, 'Category 1', 'To do list item 1', '(unfilled)'),
    (1, 'Category 1', 'To do list item 2', 'date 1'),
    (2, 'Category 2', 'To do list item 3', '(unfilled)'),
    (3, 'Category 2', 'To do list item 4', '(unfilled)'),
    (4, None, None, None)
)


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

        extracted_data_records = data_node.extract_data_node(test_data_node_specifier_01)

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

        extracted_data_records = data_node.extract_data_node(test_data_node_specifier_01)

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
