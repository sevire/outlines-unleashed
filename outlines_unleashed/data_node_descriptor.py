class DataNodeDescriptor:
    """
    Encapsulates the logic required to define nodes which match criteria for a data node and carry out
    the matching.  Includes the following functionality:

    - Reads and validates a JSON representation of a data node descriptor (in multiple versions and formats
      potentially.
    - Takes an outline node as a root and parses it according to a descriptor, extracting fields into a
      standard data node table format for onward transformation and output.
    """

    def __init__(self, dnd_structure):
        """
        Initialises the DND based on input.  If nothing is passed in, then an empty structure will be created
        which needs to have field definitions added to it.  Otherwise a data structure will be passed in which
        represents the definitions for each field within the outline.

        ToDo: Consider possibility that there may be more than one field definition for a field.
        :param dnd_structure:
        """
        pass

    @classmethod
    def from_json(json_file):
        """
        Overloaded function which will take one of:
        - A string containing a JSON representation of a DND
        - File object for a file containing a JSON representation of a DND
        - A file path to a file containing a JSON representation of a DND

        The function will parse the JSON according to which version of the JSON format is encapsulated, and
        create a new DND object.
        :return:
        """
        pass

    def to_json_str(self):
        pass

    def to_json_file(self):
        pass


