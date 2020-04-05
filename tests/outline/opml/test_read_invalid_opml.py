"""
Tests specifically of the OPML format
"""
import os
from unittest import TestCase

from outline.opml_exceptions import InvalidOpmlVersion, MissingOpmlElement
from outline.outline import Outline
from tests.test_utilities.test_config import input_files_root
from ddt import ddt, unpack, data
from tests.test_utilities.test_utilities import test_string_segment


@ddt
class TestInvalidOpml(TestCase):
    """
    Data driven test for invalid OPML files.  The data defines the file name, the expected exception and the
    expected error message, to allow for the fact that some slightly different errors will raise the same exception
    but make the error message more specific.
    """

    test_data = [
        ('opml-test-invalid-opml-01.opml', InvalidOpmlVersion, None),
        ('opml-test-invalid-opml-02.opml', MissingOpmlElement, None),
        ('opml-test-invalid-opml-03.opml', InvalidOpmlVersion, None),
        ('opml-test-invalid-opml-04.opml', MissingOpmlElement, None),
        ('opml-test-invalid-opml-05.opml', MissingOpmlElement, None),
        ('opml-test-invalid-opml-06.opml', MissingOpmlElement, None),
    ]

    local_path = os.path.join('outline', 'opml')

    @unpack
    @data(*test_data)
    def test_invalid_opml_01(self, filename, expected_exception, expected_error_msg):
        full_pathname = os.path.join(input_files_root, self.local_path, filename)
        try:
            Outline.from_opml(full_pathname)
        except expected_exception as err:
            # Correct exception raised, now check error message (if specified in test)
            if expected_error_msg is not None:
                self.assertTrue(test_string_segment(expected_error_msg, err.msg))
        except Exception as gen_err:
            self.fail(f"Unexpected exception raised {gen_err}")
        else:
            self.fail(f'Exception expected but not raised. Msg {expected_error_msg}')
