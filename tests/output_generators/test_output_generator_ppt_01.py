from unittest import TestCase

from opml.outline import Outline
from output_generators.ppt_output_generators import PowerPointGenerator
from resources.test.test_data_node_specifiers import test_data_node_specifier_ppt_01

ppt_opml_file = "/Users/thomasdeveloper/Documents/Projects/outlines-unleashed/resources/test/opml_data_extraction_webapp_test_01.opml"
template_path = "/Users/thomasdeveloper/Documents/Projects/outlines-unleashed/resources/test/ppt_template_01.pptx"
output_path = "/Users/thomasdeveloper/Documents/Projects/outlines-unleashed/resources/test/ppt_output_01.pptx"


class TestOutputGeneratorsPpt01(TestCase):
    def test_output_generator_ppt_01(self):
        outline = Outline.from_opml(ppt_opml_file)
        nodes = list(outline.list_all_nodes())
        data_node = nodes[1].node()
        ppt_driver_table = data_node.extract_data_node(test_data_node_specifier_ppt_01)

        output_generator = PowerPointGenerator()
        output_generator.create_power_point_skeleton(
            ppt_driver_table,
            template_path,
            output_path
        )

        pass