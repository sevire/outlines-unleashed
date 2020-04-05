import os
from unittest import TestCase
from ddt import ddt, data, unpack
from outline.outline import Outline
from outline.opml_exceptions import MalformedOutline, InvalidOpmlVersion
from functools import partial
from tests.test_utilities.test_config import input_files_root

folder_from_resources_root = os.path.join(input_files_root, 'outline', 'opml')

test_data_version_filename = (
        (os.path.join(folder_from_resources_root, 'opml-test-invalid-opml-01.opml'), 'InvalidOpmlVersion'),
        (os.path.join(folder_from_resources_root, 'opml-test-invalid-opml-02.opml'), 'MalformedOutline'),
        (os.path.join(folder_from_resources_root, 'opml-test-invalid-opml-03.opml'), 'InvalidOpmlVersion'),
        (os.path.join(folder_from_resources_root, 'opml-test-invalid-opml-05.opml'), 'MalformedOutline'),
        (os.path.join(folder_from_resources_root, 'opml-test-invalid-opml-05.opml'), 'MalformedOutline'),
        (os.path.join(folder_from_resources_root, 'opml-test-invalid-opml-06.opml'), 'MalformedOutline'),
)


@ddt
class TestInvalidOutline(TestCase):
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

        if fail_type == 'MalformedOutline':
            partial_from_opml = partial(Outline.from_opml, file)
            self.assertRaises(MalformedOutline, partial_from_opml)
        elif fail_type == 'InvalidOpmlVersion':
            partial_from_opml = partial(Outline.from_opml, file)
            self.assertRaises(InvalidOpmlVersion, partial_from_opml)

