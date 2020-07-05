import os
from unittest import TestCase

from outline.outline import Outline
from tests.test_utilities.test_config import input_files_root, output_files_root

from ddt import ddt, unpack, data

relative_folder = os.path.join("outline", "opml")

test_opml_input_file_01 = "test_opml_creation_01.opml"
test_opml_output_file_01 = "test_opml_copied_01.opml"

outline_expected_header_results = [
    ("title", "Untitled 2"),
    ("dateCreated", None),
    ("dateModified", None),
    ("ownerName", None),
    ("ownerEmail", None),
    ("ownerId", None),
    ("docs", None),
    ("expansionState", [16, 17, 31]),
    ("vertScrollState", 0),
    ("windowTop", 192),
    ("windowLeft", 0),
    ("windowBottom", 872),
    ("windowRight", 711),
]

outline_expected_node_results = [
    (1, "H1:Heading A", "Notes for Heading A"),
    (2, " (-TAG-TEXT-H2B-)H2: Heading B", "Notes for Heading C"),
    (3, "H3: Heading C", ""),
    (4, "H4: Heading D", ""),
    (5, "H5: Headng E", "Level 5 Note 1"),
    (6, "H3: Heading F", "Notes for Heading AU"),
    (7, "[*ROOT NODE*]H2: Heading G", ""),
    (8, "H3: Heading H", ""),
    (9, "H4: Heading I", ""),
    (10, "H5: Heading J", ""),
    (11, "H4: Heading K", ""),
    (12, "[*TAG-TEXT-H5*]H5: Heading L", "Level 5 Note 2"),
    (13, "H3: Heading M", ""),
    (14, "H4: Heading N", ""),
    (15, "H5: Heading O", "(-TAG-NOTE-H5O-)Level 5 Note 3"),
    (16, "H2: Heading P", ""),
    (17, "H1:Heading Q", ""),
    (18, "H2: Heading R", ""),
    (19, "H3: Heading S", ""),
    (20, "H4: Heading T", ""),
    (21, "[*TAG-TEXT-H5U*]H5: Heading U", "(-TAG-NOTE-H5U-)Level 5 Note 4"),
    (22, "", "Empty text"),
    (23, "H2: Heading V", ""),
    (24, "H3: Heading W", ""),
    (25, "H4: Heading X", ""),
    (26, "H5: Heading Y", ""),
    (27, "H4: Heading Z", ""),
    (28, "H5: Heading AA", "Level 5 \nNote 5"),
    (29, "H3: Heading AB", ""),
    (30, "H4: Heading AC", ""),
    (31, "H5: Heading AD", "   (-TAG-NOTE-WHITESPACE-H5AD-)Level 5 Note 6"),
    (32, "H2: Heading AE", ""),
    (33, "H1: Heading AF", ""),
    (34, "H2: Heading AG", ""),
    (35, "      [*  TEXT-TAG-WHITESPACE-H3AH  *] H3: Heading AH", ""),
    (36, "H4: Heading AI", ""),
    (37, "H5: Heading AJ", "   (-TAG-NOTE-WHITESPACE-H5AJ  -)   Level 5\nNote 7 after newline"),
    (38, "H2: Heading AK", ""),
    (39, "H3: Heading AL", ""),
    (40, "H4: Heading AM", ""),
    (41, "H5: Heading AN", "Level 5 Note 8"),
    (42, "H4: Heading AO", ""),
    (43, "[*TEXT-TAG-WHITESPACE-H5AP   *]H5: Heading AP", "Level 5 Note 9"),
    (44, "H3: Heading AQ", ""),
    (45, "H4: Heading AR", ""),
    (46, "      [*TEXT-TAG-WHITESPACE-H5AS*]H5: Heading AS", "Level 5 Note 10"),
    (47, "H2: Heading AT", ""),
     ]


def test_data_generator_header():
    for result in outline_expected_header_results:
        outline_field_name, outline_field_value = result
        yield test_opml_input_file_01, outline_field_name, outline_field_value


def test_data_generator_nodes():
    for result in outline_expected_node_results:
        node_sequence_number, exp_text_value, exp_note_value = result
        yield test_opml_input_file_01, node_sequence_number, exp_text_value, exp_note_value


@ddt
class TestOpmlDuplicate(TestCase):
    """
    Tests create outline functionality by replicating a bona fida outline, then checking whether it has the same
    content after being written out and read back in.

    Only tests the ability to reliably serialize an Outline object into a .opml file.
    Doesn't test ability to create an outline from scratch.

    """
    @data(*test_data_generator_header())
    @unpack
    def test_opml_creation_header_fields(self, opml_file_name, field_name, expected_field_value):
        """
        Reads an OPML file, writes it out, then reads it in again to check that nothing was changed in writing it.

        :return:
        """
        input_opml_path = os.path.join(input_files_root, relative_folder, opml_file_name)
        output_opml_path = os.path.join(output_files_root, relative_folder, test_opml_output_file_01)

        outline_01 = Outline.from_opml(input_opml_path)
        outline_01.write_opml(output_opml_path)
        outline_02 = Outline.from_opml(output_opml_path)

        actual_field_value = getattr(outline_02, field_name)

        self.assertEqual(expected_field_value, actual_field_value)

    @data(*test_data_generator_nodes())
    @unpack
    def test_opml_creation_nodes(self, opml_file_name, node_sequence_number, exp_text_value, exp_note_value):

        input_opml_path = os.path.join(input_files_root, relative_folder, opml_file_name)
        output_opml_path = os.path.join(output_files_root, relative_folder, test_opml_output_file_01)

        outline_01 = Outline.from_opml(input_opml_path)
        outline_01.write_opml(output_opml_path)
        outline_02 = Outline.from_opml(output_opml_path)

        node_list = outline_02.list_nodes()

        test_node = node_list[node_sequence_number].node()

        self.assertEqual(exp_text_value, test_node.text)
        self.assertEqual(exp_note_value, test_node.note)
