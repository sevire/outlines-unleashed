import os
from unittest import TestCase
from ddt import ddt, data, unpack
from opml.outline import Outline
from opml.opml_exceptions import MalformedOutline
from functools import partial
from tests.test_config import test_resources_root


test_data_version_filename = (
        (os.path.join(test_resources_root, 'opml-test-invalid-01.opml'), 'exception'),
        (os.path.join(test_resources_root, 'opml-test-invalid-02.opml'), 'exception'),
        (os.path.join(test_resources_root, 'opml-test-invalid-03.opml'), 'exception')
)


@ddt
class TestOutline(TestCase):
    @unpack
    @data(*test_data_version_filename)
    def test_invalid_version_01(self, file, fail_type):
        """As version is a mandatory field and the version of the OPML file
        drives how it is parsed, only outlines with version of '2.0' will be
        excepted, and anything else should raise an exception.

        I'm not 100% sure this is right as the version really applies to the
        OPML XML file format, so if the outline is being initialised from
        something else there is no XML. However if the version ever changes it
        may change other features which are meaningful beyond just the XML
        format (e.g. may add other elements or attributes) which is still valid
        regardless of how the outline was generated.

        Args:
            file:
            fail_type:
        """

        if fail_type == 'value':
            outline = Outline.from_opml(file)
            version = outline.version
            self.assertNotEqual('2.0', version)
        elif fail_type == 'exception':
            partial_from_opml = partial(Outline.from_opml, file)
            self.assertRaises(MalformedOutline, partial_from_opml)
