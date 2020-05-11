from outline.outline import Outline


class OutlineParser:
    """
    Class which manages the workflow of reading an outline, identifying the data nodes embedded within it,
    extracting the data from the data nodes, transforming and then outputing it.

    The actual work will be done by other classes, but this class will manage everything.
    """
    def __init__(self, outline_path, default_tag_delimiters):
        """
        :param outline_path: Full path to opml file for outline.
        :param default_tag_delimiters: Tag delimiter to use if one isn't supplied for a given descriptor.
        """
        self.outline = Outline.from_opml(outline_path)
        pass

    def identify_data_nodes(self):
        pass

    def extract_data_node_descriptor(self):
        """
        If a data node desciptor is embedded within the outline as JSON, extract it, otherwise return None.
        If there is no descriptor (or if the user so chooses) a descriptor will need to be passed in to
        decode the outline and extract to a data node table.

        :return:
        """

    def extract_data_node(self, data_node_index, data_node_descriptor):
        node_list = self.outline.list_nodes()
        test_data_node = node_list[data_node_index].node()
        extracted_data_table = test_data_node.extract_data_node_dispatch(data_node_descriptor)
        return extracted_data_table

    def transform_data_node(self):
        pass

    def output_transformed_node(self):
        pass