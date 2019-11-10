from unittest import TestCase

from ddt import ddt, data, unpack

from outlines_unleashed.tag_field_descriptor import TagFieldDescriptor

tag_matching_test_data = (
    ('[*', '*]', 'TEXT_NO_TAG', None, 'TEXT_NO_TAG'),
    ('[*-(', ')-*]', 'COMPLEX_DELIMITER NO TAG', None, 'COMPLEX_DELIMITER NO TAG'),
    ('[*', '*]', '[*TAG_NO_TEXT*]', 'TAG_NO_TEXT', ''),

    ('[*', '*]', '', None, ''),
    ('[*', '*]', '  ', None, ''),

    ('[*', '*]', '[*SIMPLE-TAG*]SIMPLE_TEXT', 'SIMPLE-TAG', 'SIMPLE_TEXT'),
    ('[*', '*]', ' [*WHITESPACE-BEFORE-TAG*]SIMPLE_TEXT', 'WHITESPACE-BEFORE-TAG', 'SIMPLE_TEXT'),
    ('[*', '*]', '[*WHITESPACE-AFTER-TAG*] SIMPLE_TEXT', 'WHITESPACE-AFTER-TAG', 'SIMPLE_TEXT'),
    ('[*', '*]', '[*    WHITESPACE-IN-TAG-LEFT*]SIMPLE_TEXT', 'WHITESPACE-IN-TAG-LEFT', 'SIMPLE_TEXT'),
    ('[*', '*]', '[*WHITESPACE-IN-TAG-RIGHT      *]SIMPLE_TEXT', 'WHITESPACE-IN-TAG-RIGHT', 'SIMPLE_TEXT'),
    ('[*', '*]', '   [*WHITESPACE-IN-TAG-BOTH-ENDS*]        SIMPLE_TEXT', 'WHITESPACE-IN-TAG-BOTH-ENDS', 'SIMPLE_TEXT'),

    ('[*', '*]', '[*SIMPLE-TAG*]TEXT WITH \nNEWLINE', 'SIMPLE-TAG', 'TEXT WITH \nNEWLINE'),
)


@ddt
class TestTagMatching(TestCase):
    @data(*tag_matching_test_data)
    @unpack
    def test_tag_parsing_valid(self, left_delim, right_delim, tag_string, tag_value, text_value):
        """
        Args:
            left_delim:
            right_delim:
            tag_string:
            tag_value:
            text_value:
        """
        tag_field_descriptor = TagFieldDescriptor((left_delim, right_delim))

        text, tag = tag_field_descriptor.parse_tag(tag_string)

        self.assertEqual(tag_value, tag)
        self.assertEqual(text_value, text)

