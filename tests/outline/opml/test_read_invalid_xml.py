import os
from xml.etree.ElementTree import ParseError
from unittest import TestCase
from ddt import ddt, data, unpack
from outline.outline import Outline
from tests.test_utilities.test_config import input_files_root
from tests.test_utilities.test_utilities import test_string_segment


@ddt
class TestInvalidXml(TestCase):
    """
    I haven't been able to work out how to get at the definitions of the expat error codes to test against them.
    So have just hard coded the first part of the error message.
    """
    test_data = [
        ('opml_test_invalid_xml_01.opml', 'no element found'),
        ('opml_test_invalid_xml_02.opml', 'not well-formed (invalid token)'),
        ('opml_test_invalid_xml_03.opml', 'duplicate attribute'),
        ('opml_test_invalid_xml_04.opml', 'junk after document element'),
    ]

    local_path = os.path.join('outline', 'opml')

    @unpack
    @data(*test_data)
    def test_read_invalid_xml_01(self, filename, expected_error_msg):
        full_pathname = os.path.join(input_files_root, self.local_path, filename)
        try:
            Outline.from_opml(full_pathname)
        except ParseError as err:
            self.assertTrue(test_string_segment(expected_error_msg, err.msg))
        except Exception as gen_err:
            self.fail(f"Unexpected exception raised {gen_err}")
        else:
            self.fail(f'Exception expected but wasn\'t raised. Msg {expected_error_msg}')
