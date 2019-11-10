import os
from unittest import TestCase

from ddt import ddt, data, unpack
import tests.test_config as tcfg
from opml.outline import Outline

tag_extract_data=(
    (12, 'text_tag', 'TAG-TEXT-H5'),
    (12, 'text',     'H5: Heading L'),
    (15, 'note_tag', 'TAG-NOTE-H5O'),
    (15, 'note',     'Level 5 Note 3'),
    (21, 'text_tag', 'TAG-TEXT-H5U'),
    (21, 'text',     'H5: Heading U'),
    (21, 'note_tag', 'TAG-NOTE-H5U'),
    (21, 'note',     'Level 5 Note 4'),
    (28, 'note',     'Level 5 \nNote 5'),
    (31, 'note_tag', 'TAG-NOTE-WHITESPACE-H5AD'),
    (31, 'note', 'Level 5 Note 6'),
    (31, 'text', 'H5: Heading AD'),
    (37, 'note_tag', 'TAG-NOTE-WHITESPACE-H5AJ'),
    (37, 'note', 'Level 5\nNote 7 after newline'),
    (43, 'text_tag', 'TEXT-TAG-WHITESPACE-H5AP'),
    (43, 'text', 'H5: Heading AP'),
    (46, 'text_tag', 'TEXT-TAG-WHITESPACE-H5AS')
)


@ddt
class TestOutlineNodeTag(TestCase):
    """Tests functionality to extract tag and text from a node."""
    def setUp(self) -> None:
        tag_regex_delim_text = (r'[*', r'*]')
        tag_regex_delim_note = (r'(-', r'-)')

        self.outline = Outline.from_opml(os.path.join(tcfg.test_resources_root, 'opml-test-valid-01.opml'),
                                         tag_regex_delim_text,
                                         tag_regex_delim_note)

    @data(*tag_extract_data)
    @unpack
    def test_extract_tag(self, index, field_name, value):
        """Get all nodes and show that the tags are correctly identified and
        spotted from the appropriate nodes :return:

        Args:
            index:
            field_name:
            value:
        """
        node_list = list(self.outline.list_all_nodes())
        node = node_list[index].node()

        field_value = getattr(node, field_name)
        self.assertEqual(value, field_value)
