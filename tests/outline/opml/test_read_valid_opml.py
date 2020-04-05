"""
Tests that a valid opml file will be read sensibly by the Outline class and result in a valid Outline
structure.
"""
import os
from unittest import TestCase

from ddt import ddt, unpack, data

from outline.outline import Outline
from tests.test_utilities.test_config import input_files_root


@ddt
class TestValidOpml(TestCase):
    """
    Data driven test for valid OPML files.  Each file should be read without error.
    """

    test_data = [
        ('opml-test-valid-opml-01.opml', ),
    ]

    local_path = os.path.join('outline', 'opml')

    @unpack
    @data(*test_data)
    def test_valid_opml_01(self, filename):
        full_pathname = os.path.join(input_files_root, self.local_path, filename)
        try:
            Outline.from_opml(full_pathname)
        except Exception as gen_err:
            self.fail(f"Unexpected exception raised {gen_err}")
