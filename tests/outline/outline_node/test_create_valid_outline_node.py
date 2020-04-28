from unittest import TestCase, skip
from ddt import ddt, data, unpack
from outline.opml_exceptions import MalformedOutline
from outline.outline_node import OutlineNode


@ddt
class TestCreateOutlineNode(TestCase):

    test_well_formed_data = [
        (None, None, '', '', '', ''),
        (
            'this is text', None, 'this is text', '', 'this is text', ''
        ),
        (
            None, 'a note', '', 'a note', '', 'a note'
        ),
        (
            'B text \nhello this is text with a line break',
            'B note hello this is a note',

            'B text \nhello this is text with a line break',
            'B note hello this is a note',

            'B text  hell...',
            'B note hello...'
        )
    ]

    @data(*test_well_formed_data)
    @unpack
    def test_outline_node_well_formed(self,
                                      input_text, input_note,
                                      expected_text, expected_note,
                                      expected_short_text, expected_short_note):
        try:
            node = OutlineNode.create_outline_node(outline_text=input_text, outline_note=input_note)
        except MalformedOutline as err:
            self.fail(f'Unexpected MalformedOutline exception: {err}')
        except Exception as err:
            self.fail(f'Unexpected Exception exception: {err}')

        self.assertEqual(expected_text, node.text)
        self.assertEqual(expected_note, node.note)
        self.assertEqual(expected_short_text, node.short_text)
        self.assertEqual(expected_short_note, node.short_note)

        repr_output = f'OutlineNode.create_outline_node(text: \'{expected_short_text}\', note: \'{expected_short_note}\')'
        self.assertEqual(repr_output, node.__repr__())

        str_output = f'OutlineNode: children: {0}, text: \'{expected_short_text}\', note: \'{expected_short_note}\''
        self.assertEqual(str_output, node.__str__())