import functools
import os
from unittest import TestCase
import tests.test_config as tcfg
from opml.opml_exceptions import MalformedOutline
from opml.outline import Outline
from ddt import ddt, data, unpack


@ddt
class TestOutlineNodeWalkInvalid(TestCase):

    @data('opml-test-invalid-04.opml',
          # 'opml-test-invalid-05.opml', (It's not an error to have additional attributes according to OPML spec)
          'opml-test-invalid-06.opml')
    def test_invalid_node_01(self, filename):
        """Tests that if there is a node which is invalid it generates and
        exception and aborts the walk. :return:

        Args:
            filename:
        """

        outline = Outline.from_opml(os.path.join(tcfg.test_resources_root, filename))
        #node_list = list(outline.list_all_nodes())

        func = functools.partial(list, outline.list_all_nodes())
        self.assertRaises(MalformedOutline, func)
