import os
from unittest import TestCase
from ddt import ddt, data, unpack
from outline.outline import Outline
from outline.opml_exceptions import MalformedOutline, InvalidOpmlVersion, MissingOpmlAttribute, MissingOpmlElement, \
    InvalidOpmlAttribute
from functools import partial
from tests.test_utilities.test_config import input_files_root

folder_from_resources_root = os.path.join(input_files_root, 'outline', 'outline')

test_data_version_filename = (
        (os.path.join(folder_from_resources_root, 'opml-test-invalid-outline-01.opml'), InvalidOpmlVersion),
        (os.path.join(folder_from_resources_root, 'opml-test-invalid-outline-02.opml'), MissingOpmlAttribute),
        (os.path.join(folder_from_resources_root, 'opml-test-invalid-outline-03.opml'), InvalidOpmlVersion),
        (os.path.join(folder_from_resources_root, 'opml-test-invalid-outline-04.opml'), MalformedOutline),
        (os.path.join(folder_from_resources_root, 'opml-test-invalid-outline-05.opml'), MalformedOutline),
        (os.path.join(folder_from_resources_root, 'opml-test-invalid-outline-06.opml'), MissingOpmlAttribute),
        (os.path.join(folder_from_resources_root, 'opml-test-invalid-outline-07.opml'), InvalidOpmlAttribute),
)


@ddt
class TestInvalidOutline(TestCase):
    @unpack
    @data(*test_data_version_filename)
    def test_invalid_version_01(self, file, exception):
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

        partial_from_opml = partial(Outline.from_opml, file, full_validate=True)
        self.assertRaises(exception, partial_from_opml)
