"""
Wrapper class for an OutlineNode which adds in the additional functionality such as extract of tag, text from
the text field of a node.
"""
from typing import Tuple

from outlines_unleashed.tag_field_descriptor import TagFieldDescriptor
from outlines_unleashed.unleashed_node_ancestry_record import UnleashedNodeAncestryRecord


class UnleashedOutlineNode:
    def __init__(
        self, outline_node,
        tag_regex_text: Tuple[str, str] = None,
        tag_regex_note: Tuple[str, str] = None
    ):
        self.outline_node = outline_node
        self.tag_regex_text = tag_regex_text
        self.tag_regex_note = tag_regex_note

    @property
    def text(self):
        """
        Access to the text attribute of an outline node. If a tag regex string has been defined then look for a tag
        and if there is one extract the tag before returning the remainder

        :return: The text attribute of self.node
        """
        field_text = self.outline_node.text
        text, tag = self._extract_tag_and_text(field_text, self.tag_regex_text)
        return text

    @property
    def note(self):
        """
        Access to the text attribute of an outline node.

        :return: The _note attribute of self.node
        """
        field_text = self.outline_node.note
        text, tag = self._extract_tag_and_text(field_text, self.tag_regex_note)
        return text

    @property
    def text_tag(self):
        field_text = self.outline_node.text
        text, tag = self._extract_tag_and_text(field_text, self.tag_regex_text)
        return tag

    @property
    def note_tag(self):
        field_text = self.outline_node.note
        text, tag = self._extract_tag_and_text(field_text, self.tag_regex_note)
        return tag

    @staticmethod
    def _extract_tag_and_text(text: str, regex_delim: Tuple[str, str]):
        if regex_delim is None:
            return text, None
        else:
            tag_field_descriptor = TagFieldDescriptor(regex_delim)

            return tag_field_descriptor.parse_tag(text)

    def iter_unleashed_nodes(self):
        for outline_node_ancestry_record in self.outline_node.iter_nodes():
            yield UnleashedNodeAncestryRecord(outline_node_ancestry_record,
                                              text_tag_regex=self.tag_regex_text,
                                              note_tag_regex=self.tag_regex_note)

    def list_unleashed_nodes(self):
        return list(self.iter_unleashed_nodes())

    def get_node(self, node_number):
        return UnleashedNodeAncestryRecord(self.outline_node.get_node(node_number),
                                           text_tag_regex=self.tag_regex_text,
                                           note_tag_regex=self.tag_regex_note)

    def clone_unleashed_node(self, text_tag_regex=None, note_tag_regex=None):
        if text_tag_regex is None:
            text_regex = self.tag_regex_text
        else:
            text_regex = text_tag_regex

        if note_tag_regex is None:
            note_regex = self.tag_regex_note
        else:
            note_regex = note_tag_regex

        return UnleashedOutlineNode(self.outline_node, tag_regex_text=text_regex, tag_regex_note=note_regex)
