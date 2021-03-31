import os
from unittest import TestCase
from ddt import data, unpack, ddt
from outline.outline import Outline
from outlines_unleashed.data_node_specifier import DataNodeSpecifier
from outlines_unleashed.unleashed_outline import UnleashedOutline
from output_generators.csv_output_generator import CsvOutputGenerator
from tests.test_resources.input_files.output_generator.test_csv_data import data_node_specifier_csv_test_01
from tests.test_utilities.csv_test_utilities import CsvTestChecker
from tests.test_utilities.test_config import input_files_root, output_files_root

test_data = [
    (
        "opml_data_csv_output_test_01.opml",
        "opml_csv_output_test_01.csv",
        "custom_json_test_descriptors_risk_01.json",
        [
            (0, 0, "There is a possibility that the world might end"),
            (2, 3, "(unfilled)")
        ]
    )
]


def test_data_generator():
    for test_record in test_data:
        input_file, output_file, json_file, expected_results = test_record
        for test_case in expected_results:
            row, column, expected_result = test_case
            yield input_file, output_file, json_file, row, column, expected_result


@ddt
class TestOutputGeneratorCsv01(TestCase):
    @data(*test_data_generator())
    @unpack
    def test_output_generator_csv_01(self, opml_filename, output_filename, ignored_json_file, row, col, expected_result):
        """
        Creates csv file from outline using in memory data node specifier.

        NOTE: A JSON file name is passed in as the generator is used across both test methods, but
        in this method is ignored.

        :param opml_filename:
        :param output_filename:
        :param row:
        :param col:
        :param expected_result:
        :return:
        """
        test_data_file = os.path.join(input_files_root,
                                      "output_generator",
                                      opml_filename)

        test_csv_output_path = os.path.join(output_files_root,
                                            "output_generator",
                                            output_filename)
        outline = Outline.from_opml(test_data_file)
        unleashed_outline = UnleashedOutline(outline, default_text_tag_delimiter=['[*', '*]'])

        data_nodes = unleashed_outline.extract_data_nodes()
        data_node_name = data_nodes[0]['data_node_name']

        self.assertEqual('data_node_01', data_node_name)

        data_node_list_index = data_nodes[0]['data_node_list_index']
        data_node = unleashed_outline.list_unleashed_nodes()[data_node_list_index].node()

        data_node_descriptor = DataNodeSpecifier(data_node_specifier_csv_test_01)

        data_table = data_node_descriptor.extract_data_node_dispatch(data_node)

        CsvOutputGenerator.create_csv_file(data_table, test_csv_output_path)

        result_checker = CsvTestChecker(test_csv_output_path)
        self.assertTrue(result_checker.check(row, col, expected_result))

    @data(*test_data_generator())
    @unpack
    def test_output_generator_csv_02(self, opml_filename, output_filename, json_dns_file, row, col, expected_result):
        """
        Creates csv file from outline using JSON data node specifier.

        :param opml_filename:
        :param output_filename:
        :param row:
        :param col:
        :param expected_result:
        :return:
        """
        test_data_file = os.path.join(input_files_root,
                                      "output_generator",
                                      opml_filename)

        test_csv_output_path = os.path.join(output_files_root,
                                            "output_generator",
                                            output_filename)

        data_node_descriptor_file = os.path.join(input_files_root, "data_node_descriptor", json_dns_file)

        outline = Outline.from_opml(test_data_file)
        unleashed_outline = UnleashedOutline(outline, default_text_tag_delimiter=['[*', '*]'])

        data_nodes = unleashed_outline.extract_data_nodes()
        data_node_name = data_nodes[0]['data_node_name']

        self.assertEqual('data_node_01', data_node_name)

        data_node_list_index = data_nodes[0]['data_node_list_index']
        data_node = unleashed_outline.list_unleashed_nodes()[data_node_list_index].node()

        data_node_descriptor = DataNodeSpecifier.from_json_file(data_node_descriptor_file)

        data_table = data_node_descriptor.extract_data_node_dispatch(data_node)

        CsvOutputGenerator.create_csv_file(data_table, test_csv_output_path)

        result_checker = CsvTestChecker(test_csv_output_path)
        self.assertTrue(result_checker.check(row, col, expected_result))
