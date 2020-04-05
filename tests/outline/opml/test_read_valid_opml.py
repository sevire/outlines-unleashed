"""
Tests that a valid opml file will be read sensibly by the Outline class and result in a valid Outline
structure.
"""
from unittest import TestCase


class TestReadValidOpml(TestCase):
    def read_valid_opml_01(self):