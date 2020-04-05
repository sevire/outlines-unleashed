from unittest import TestCase
from unittest import skip
from opml.outline_node import OutlineNode
from xml.etree import ElementTree
from opml import opml_exceptions as ex


class TestOutline(TestCase):

    def test_outline_node_simple_well_formed(self):
        # No attributes provided, everything that can be None is None.
        try:
            node = OutlineNode.create_outline_node()
        except ex.MalformedOutline:
            self.fail('Unexpected MalformedOutline exception')
        self.assertEqual('', node.text)
        self.assertEqual('', node.note)

    def test_outline_node_populated_well_formed_01(self):
        # text attribute populated.
        try:
            node = OutlineNode.create_outline_node(outline_text='hello this is text')
        except ex.MalformedOutline:
            self.fail('Unexpected MalformedOutline exception')
        self.assertEqual('hello this is text', node.text)
        self.assertEqual('', node.note)

    def test_outline_node_populated_well_formed_02(self):
        # text attribute populated.
        try:
            node = OutlineNode.create_outline_node(outline_note='hello this is a note')
        except ex.MalformedOutline:
            self.fail('Unexpected MalformedOutline exception')
        self.assertEqual('', node.text)
        self.assertEqual('hello this is a note', node.note)

    def test_outline_node_populated_well_formed_03(self):
        # text attribute populated.
        try:
            node = OutlineNode.create_outline_node(outline_note='hello this is a note B', outline_text='hello this is text B')
        except ex.MalformedOutline:
            self.fail('Unexpected MalformedOutline exception')
        except Exception:
            self.fail('Unexpected general Exception')

        self.assertEqual('hello this is text B', node.text)
        self.assertEqual('hello this is a note B', node.note)

    def test_outline_node_repr_01(self):
        try:
            node = OutlineNode.create_outline_node(outline_text='Some text longer than 15 chars', outline_note='short note')
        except ex.MalformedOutline:
            self.fail('Unexpected MalformedOutline exception')
        except Exception:
            self.fail('Unexpected general Exception')

        repr_string = node.__repr__()
        self.assertEqual('OutlineNode(text: \'Some text longe...\', note: \'short note\')', repr_string)

    def test_outline_node_repr_02(self):
        try:
            node = OutlineNode.create_outline_node(outline_text='Exactly 15 chrs', outline_note='s')
        except ex.MalformedOutline:
            self.fail('Unexpected MalformedOutline exception')
        except Exception:
            self.fail('Unexpected general Exception')

        repr_string = node.__repr__()
        self.assertEqual('OutlineNode(text: \'Exactly 15 chrs\', note: \'s\')', repr_string)

    def test_outline_node_repr_03(self):
        try:
            node = OutlineNode.create_outline_node()
        except ex.MalformedOutline:
            self.fail('Unexpected MalformedOutline exception')
        except Exception:
            self.fail('Unexpected general Exception')

        repr_string = node.__repr__()
        self.assertEqual('OutlineNode(text: \'\', note: \'\')', repr_string)

    def test_outline_node_str_01(self):
        try:
            node = OutlineNode.create_outline_node(outline_text='String for text', outline_note='String for note')
        except ex.MalformedOutline:
            self.fail('Unexpected MalformedOutline exception')
        except Exception:
            self.fail('Unexpected general Exception')

        str_string = node.__str__()
        self.assertEqual('OutlineNode: children: 0, text: "String for text", note: "String for note"', str_string)