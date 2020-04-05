import os
from unittest import TestCase

from ddt import ddt, data, unpack
import tests.test_utilities.test_config as tcfg
from opml.outline import Outline

tag_extract_data=(
    (12, 'text', '[*TAG-TEXT-H5*]H5: Heading L'),
    (15, 'note', '(-TAG-NOTE-H5O-)Level 5 Note 3'),
    (21, 'text', '[*TAG-TEXT-H5U*]H5: Heading U'),
    (21, 'note', '(-TAG-NOTE-H5U-)Level 5 Note 4'),
    (28, 'note', 'Level 5 \nNote 5'),
    (31, 'note', '   (-TAG-NOTE-WHITESPACE-H5AD-)Level 5 Note 6'),
    (31, 'text', 'H5: Heading AD'),
    (37, 'note', '   (-TAG-NOTE-WHITESPACE-H5AJ  -)   Level 5\nNote 7 after newline'),
    (43, 'text', '[*TEXT-TAG-WHITESPACE-H5AP   *]H5: Heading AP'),
)


@ddt
class TestOutlineNodeTag(TestCase):
    """Tests outline with embedded tags (for unleashing) but for an unleashed outline."""
    def setUp(self) -> None:

        self.outline = Outline.from_opml(os.path.join(tcfg.input_files_root, 'opml-test-valid-01.opml'))

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
        node_list = self.outline.list_nodes()
        node = node_list[index].node()

        field_value = getattr(node, field_name)
        self.assertEqual(value, field_value)
