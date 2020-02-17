class DataNodeFieldDefinition:
    """
    A Data Node Descriptor will have a definition for each field within an Data Node within an outline.  This
    class represents that field definition and will be used to help parse a Data Node and find matching nodes,
    and then extracting the data into the appropriate type of field.
    """
    def __init__(self, field_name, field_type, node_ancestry_matching_criteria):
        """
        :param field_name: Name of field.  Will be used in output data structures such as Data Node Table.
        :param field_type: Type of field.  Will allow field to be used for different operations (e.g. addition)
        :param node_ancestry_matching_criteria: A NodeAncestryMatchingCriteria object which defines the
               criteria for matching an outline node for this field.
        """
