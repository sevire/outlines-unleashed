from unittest import TestCase
import json

from resources.test.json_serialized import serialized_json_01
from resources.test.test_json_serialize_descriptors import test_json_descriptor_01


class TestSerializeDescriptor(TestCase):
    def test_serialise_descriptor_01(self):
        self.maxDiff = None
        serialized_descriptor = json.dumps(test_json_descriptor_01, default=lambda o: o.__dict__, indent=4)
        self.assertEqual(serialized_descriptor, serialized_json_01)
