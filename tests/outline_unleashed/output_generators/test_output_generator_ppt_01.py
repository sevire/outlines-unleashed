from unittest import TestCase

from outline.outline import Outline
from outlines_unleashed.data_node_specifier import DataNodeSpecifier
from outlines_unleashed.unleashed_outline import UnleashedOutline
from output_generators.ppt_output_generators import PowerPointGenerator
from tests.python_test_data.data_node_specifier_data.data_node_test_specifiers import test_data_node_specifier_ppt_01

ppt_opml_file = "/Users/thomasdeveloper/Documents/Projects/outlines-unleashed/resources/test/opml_data_extraction_webapp_test_01.opml"
template_path = "/Users/thomasdeveloper/Documents/Projects/outlines-unleashed/resources/test/ppt_template_01.pptx"
output_path = "/Users/thomasdeveloper/Documents/Projects/outlines-unleashed/resources/test/output_files/ppt_output_01.pptx"


class TestOutputGeneratorsPpt01(TestCase):
    def test_output_generator_ppt_01(self):
        outline = Outline.from_opml(ppt_opml_file)
        unleashed_outline = UnleashedOutline(outline)
        nodes = unleashed_outline.list_unleashed_nodes()
        data_node = nodes[1].node()
        specifier = DataNodeSpecifier(test_data_node_specifier_ppt_01)
        ppt_driver_table = specifier.extract_data_node_dispatch(data_node)

        output_generator = PowerPointGenerator()
        output_generator.create_power_point_skeleton(
            data_node,
            template_path,
            output_path
        )

        pass
