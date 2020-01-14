class DataNodeTable:
    """
    Data structure which encapsulates the data extracted from a data node within an outline.

    There may be other ways of extracting data from an outline but this will be the main one, and other
    transformations, such as into CSV, Excel, PPT etc., will be driven from a basic tabular structure.

    This structure will allow fields to be defined, with a type, and then rows can be added.  The class
    will ensure that only the right fields  get added and that all fields have a value (even if it is
    a default).

    The class will also include utility methods for conversion to output formats (or to facilitate this).
    """

    def __init__(self):
        pass

    def add_field(self, field_name, field_type):
        pass

    def add_row(self):
        pass

    def add_value(self, field_name, value):

    @classmethod
    def from_list_of_dicts(cls, list_of_dicts, field_names=None):
        """
        Creates a DNT from an existing list of dictionaries where each row is a dict containing the same
        fields.

        Will add fields based on what is in the dicts, handling any inconsistencies within rows (there
        shouldn't be any) and also allocating a type based on the type of the data.

        :param list_of_dicts:
        :return:
        """
        table = DataNodeTable()
        if field_names is not None:
            for field in field_names:
                table.add_field(field, get_field_type())

                ### Need to think about this!!!

