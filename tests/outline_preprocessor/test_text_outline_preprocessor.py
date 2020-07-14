import json
import os
from unittest import TestCase, skip
from ddt import ddt, data, unpack

from outline.opml_exceptions import MalformedOutline
from outline_preprocessors.preprocessor_text_indent import PreprocessorTextIndent, TextOutlineDecodeSpecifier

# from tests.test_commons import data_driver_output_path, data_driver_expected_results_path
# from to_outline.indented_text.decode_text_outline import parse_indent, strip_newline
# from to_outline.indented_text.text_outline_decode_specifier import TextOutlineDecodeSpecifier
from tests.test_utilities.test_config import input_files_root, misc_files_root

data_driver_expected_results_path = os.path.join(misc_files_root, "outline_preprocessor", "expected_results_files")
generated_files_relative_path = os.path.join("outline_preprocessor", "generated")
non_generated_files_relative_path = "outline_preprocessor"

generated_test_file_data = {
        "driver_file_01": {
            "noinitial-tab-nobullet": ("\t", ),
            "noinitial-tab-bullet1": ("\t", ["", "o "]),
            "noinitial-tab-bullet2": ("\t", ["o "]),
            "noinitial-tab-bullet3": ("\t", ["o ", "+ ", "- "]),
            "noinitial-4space-nobullet": ("    ", ),
            "noinitial-4space-bullet1": ("    ", ["", "o "]),
            "noinitial-4space-bullet2": ("    ", ["o "]),
            "noinitial-4space-bullet3": ("    ", ["o ", "+ ", "- "]),
            "initial1-tab-nobullet": ("\t", None, 0, "[--]    ", True),
            "initial2-tab-bullet1": ("\t", ["", "o "], 0, "    [--]"),
        }
    }

created_outline_test_data = {
    'outline_indent_test_01.txt': {
        'num_records': 2,
        'record_data': [
            (1, 1, "L1 no indent")
        ]
    },
    'outline_indent_test_02.txt': {
        'num_records': 3,
        'record_data': [
            (1, 1, "L1 no indent"),
            (2, 2, "L2 indent")
        ]
    },
    'outline_indent_test_03.txt': {
        'num_records': 4,
        'record_data': [
            (1, 1, "L1 no indent"),
            (2, 2, "L2 indent"),
            (3, 1, "L1 second node at this level")
        ]
    },
    'outline_indent_test_04.txt': {
        'num_records': 10,
        'record_data': [
            (1, 1, "L1 no indent"),
            (2, 2, "L2 indent"),
            (3, 3, "L3 Xxxxxxxxx"),
            (4, 3, "L3 Yyyyyyyyy"),
            (5, 4, "L4 Zzzzzz"),
            (6, 3, "L3 Wwwwwww"),
            (7, 3, "L3 Vvvvvvvv"),
            (8, 1, "L1 second node at L1"),
            (9, 1, "L1 third node at L1")
        ]
    },
    'outline_indent_test_05.txt': {
        'exception': "MalformedOutline",
    },
}


def created_outline_test_data_generator():
    for file in created_outline_test_data:
        test_record = created_outline_test_data[file]
        if "exception" in test_record:
            yield file, 0, 'exception', test_record['exception']
        else:
            yield file, 0, 'num_records', test_record['num_records']
            for expected_data in test_record['record_data']:
                node_index, depth, text_value = expected_data
                yield file, node_index, 'depth', depth
                yield file, node_index, 'text', text_value


def test_data_generator():
    """
    Generates combinations of test data files, test cases and expected results.

    This series of tests works by by encoding the same outline in many different text formats. For a given
    driver file which represents a specific outline, a test data file will be generated for each of the different
    formats to be generated, but the expected results will always the same, as the encoding added in the test files
    is stripped off if the decoding functionality works correctly.

    The expected results are generated for each line in the driver file but apply to each of the generated files as
    each one represents the same outline so once the outline is decoded the results should be the same.
    The tests simply check that the indent level and text content of each node is correct.

    This function takes a driver data structure which defines what driver files there are and what formats need to be
    tested, and generates the parmeters to feed into a data driven test case to tell it what file to read, which line
    to check and what the expected result should be.

    :return:
    """
    for generator_file in generated_test_file_data:
        file_record = generated_test_file_data[generator_file]

        expected_result_filename = os.path.join(data_driver_expected_results_path,
                                                generator_file + "_expected_results" + ".json")
        with open(expected_result_filename) as fp_in:
            expected_results = json.load(fp_in)

        for encoding_format in file_record:
            indent_token = file_record[encoding_format]
            test_data_file = generator_file + "-" + encoding_format + ".txt"

            for expected_result in expected_results:
                test_line_number = expected_result["line_number"]
                expected_indent_level = expected_result["indent_level"]
                expected_content = expected_result["content"]

                yield test_data_file, indent_token, test_line_number, expected_indent_level, expected_content


def get_nth_line_of_text_file(path, n):
    with open(path) as fp:
        for line_num, line in enumerate(fp):
            if line_num+1 == n:
                line_without_break = PreprocessorTextIndent.strip_newline(line)
                return line_without_break
        raise Exception(f"Line number {n} in path {path} doesn\'t exist")


def iter_file(path):
    with open(path) as fp:
        for line_num, line in enumerate(fp):
            line_without_break = PreprocessorTextIndent.strip_newline(line)
            yield line_without_break


@ddt
class TestTextOutlinePreprocessor(TestCase):
    @data(*test_data_generator())
    @unpack
    def test_generated_files(self,
                             file_name,
                             decode_specification,
                             test_line_number,
                             expected_indent,
                             expected_content
                             ):
        file_path = os.path.join(generated_files_relative_path, file_name)
        decode_specifier = TextOutlineDecodeSpecifier(*decode_specification)
        full_pathname = os.path.join(input_files_root, file_path)
        test_line = get_nth_line_of_text_file(full_pathname, test_line_number)

        preprocessor = PreprocessorTextIndent.from_textfile(full_pathname, decode_specifier)

        indent_level, content = preprocessor.parse_indent(test_line, decode_specifier)
        self.assertEqual(expected_indent, indent_level)
        self.assertEqual(expected_content, content)

    def test_manual_files(self):
        file_name = "onenote_bullet_paste_01.txt"
        file_path = os.path.join(input_files_root, non_generated_files_relative_path, file_name)
        decode_specifier = TextOutlineDecodeSpecifier("\t",
                                                      ["• ", "• ", "○ ", "§ ", "□ ", "® ", "◊ ", "} ", "– ", "w "])
        preprocessor = PreprocessorTextIndent.from_textfile(file_path, decode_specifier)
        for line in iter_file(file_path):
            indent_level, content = preprocessor.parse_indent(line, decode_specifier)
            pass

    @data(*created_outline_test_data_generator())
    @unpack
    def test_created_outline(self, file, node_index, value_to_check, value):
        file_path = os.path.join(input_files_root, non_generated_files_relative_path, file)

        decode_specifier = TextOutlineDecodeSpecifier("    ")
        preprocessor = PreprocessorTextIndent.from_textfile(file_path, decode_specifier)

        if value_to_check == "exception":
            try:
                preprocessor.pre_process_outline()
            except MalformedOutline:
                if value != "MalformedOutline":
                    self.fail(f"{value} exception expected")
            except Exception as ex:
                self.fail(f"Unexpected exception raised {ex}")
            else:
                self.fail("Exception expected")
        else:
            outline = preprocessor.pre_process_outline()

            list = outline.list_nodes()

            if value_to_check == 'num_records':
                self.assertEqual(value, len(list))
            elif value_to_check == 'text':
                self.assertEqual(value, list[node_index].node().text)
            elif value_to_check == 'depth':
                self.assertEqual(value, list[node_index].depth)
