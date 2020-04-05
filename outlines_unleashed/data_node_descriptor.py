import json

from outlines_unleashed.node_ancestry_matching_criteria import NodeAncestryMatchingCriteria


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
    def from_json(cls, serialized_descriptor):
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

        descriptor_raw = json.loads(serialized_descriptor)

        # For now a very clunky approach to creating a Python descriptor from the JSON
        # sourced dict structure.  Will refactor into an independent class later
        # ToDo: Extract descriptor structure and logic into separate class

        get_or_set = lambda x, y: x[y] if y in x else None

        descriptor = {'header': descriptor_raw['header'], 'descriptor': {}}

        for raw_field_descriptor in descriptor_raw['descriptor']:
            descriptor['descriptor'][raw_field_descriptor] = {}
            for field_property in descriptor_raw['descriptor'][raw_field_descriptor]:
                if field_property == 'ancestry_matching_criteria':
                    # We need to replace the list of dicts with a list of NodeAncestryMatchingCriteria objects
                    descriptor['descriptor'][raw_field_descriptor][field_property] = []

                    criteria_list = descriptor_raw['descriptor'][raw_field_descriptor][field_property]
                    for criteria_set in criteria_list:
                        criteria_object = NodeAncestryMatchingCriteria(
                            child_number=get_or_set(criteria_set, 'child_number'),
                            text=get_or_set(criteria_set, 'text'),
                            note=get_or_set(criteria_set, 'note'),
                            text_tag=get_or_set(criteria_set, 'text_tag'),
                            note_tag=get_or_set(criteria_set, 'note_tag')
                        )
                        descriptor['descriptor'][raw_field_descriptor][field_property].append(criteria_object)
                else:
                    descriptor['descriptor'][raw_field_descriptor][field_property] = \
                        descriptor_raw['descriptor'][raw_field_descriptor][field_property]

        return descriptor
    def to_json_str(self):
        pass

    def to_json_file(self):
        pass

    @staticmethod
    def extract_field(field_node, field_criteria):
        """
        Extracts the field value from the node according to the field_specifier for the field.  Usually will
        be called once the field has been matched to confirm it is meets the criteria for a specific field
        name.

        :param field_node:
        :param field_criteria:
        :return:
        """

        value_specifier = field_criteria['field_value_specifier']

        if value_specifier == 'text_value':
            field_value = field_node.text
        elif value_specifier == 'text_tag':
            field_value = field_node.text_tag
        elif value_specifier == 'note_value':
            field_value = field_node.note
        elif value_specifier == 'note_tag':
            field_value = field_node.note_tag
        else:
            raise ValueError(f"Unrecognised field specifier {value_specifier}")

        return field_value

    @staticmethod
    def to_json(descriptor):
        """
        Takes a full descriptor (with header) and converts it to a json string.

        Tries to use common code for all versions of the descriptor structure, but where there
        is a need for specific logic for a given version it will be included.

        :param descriptor:
        :return:
        """
        # Note this is a fairly generic approach which may not work as structure evolves.
        serialized_descriptor = json.dumps(descriptor, default=lambda o: o.__dict__, indent=4)

        return serialized_descriptor

    def extract_data_node(self, data_node_specifier_version):
        """
        Dispatcher method which works out which version of the descriptor structure is being
        passed in and then forwards the descriptor to the appropriate version specific extract
        method.

        :param data_node_specifier_version:
        :return:
        """
        version = data_node_specifier_version['header']['descriptor_version_number']
        descriptor = data_node_specifier_version['descriptor']

        if version == '0.1':
            return self._extract_data_node_v0_1(descriptor)

    def _extract_data_node_v0_1(self, data_node_specifier):
        """
        Parse the sub_tree with self as a root and extract all the nodes which match the criteria defined
        in the data_node_specifier.

        Based on how the primary key is defined, assemble records as the tree is parsed.  This is the
        essence of unleashing outlines, because nodes with a common parent which is a primary key node
        will share that element of the primary key, and this is how a tree structure is transformed to a
        table structure with fixed format records.

        Note: At this point we are only dealing with cases where all the key fields are closer
        to the root of the data node and all the data fields are deeper.  We don't deal with key fields
        being defined deeper than a non-key field.  I think this is almost certainly right and I haven't
        thought of any meaningful use cases yet where this may not be true, but there may be some. For now
        the logic depends upon this.

        The records are created with fields (and types) according to the field definitions within the
        data_node_specifier, and then added to a list in the order in wihch they appear in the tree.

        This is what is then returned to the caller.

        :param data_node_specifier:
        :return:
        """
        match_list = self.match_data_node(data_node_specifier)
        data_node_table = []
        primary_key_field_list = self.extract_field_names(data_node_specifier, primary_key_only=True)
        non_primary_key_field_list = self.extract_field_names(data_node_specifier, primary_key_only=False)
        empty_data_node_record = {key: None for key in primary_key_field_list + non_primary_key_field_list}

        # Initialise record for first row
        data_node_record = empty_data_node_record

        for match in match_list:
            field_name, field_value = match
            if data_node_record[field_name] is None:
                data_node_record[field_name] = field_value
            else:
                # We have already populated this field, so either it's a new primary key value (end of record)
                # or an error.
                if field_name in primary_key_field_list:
                    # A primary key field is about to be overwritten.
                    # There are a few cases to process here:
                    # - Current record must be complete now so can be written (all cases I think)
                    # - If this is not the last primary key field of the set then we have effectively
                    #   moved to a new branch and so we need to blank out any key fields in the data record
                    #   we are constructing as well as all non-key fields
                    # - Any fields which aren't populated will trigger a warning and an appropriate
                    #   default value assigned.

                    # Check whether any fields un-filled and issue warning but update with default value.
                    for field in data_node_record:
                        if data_node_record[field] is None:
                            data_node_record[field] = '(unfilled)'

                    # Append copy of record to output table so don't keep updating same pointer.
                    data_node_table.append(copy.deepcopy(data_node_record))

                    # Now update new primary key field as part of next record.
                    data_node_record[field_name] = field_value

                    # If this field isn't the last key field in the primary key, then blank out deeper
                    # elements within the current data node record as it doesn't apply to the new branch.
                    key_index = [index for index, value in enumerate(primary_key_field_list) if value == field_name]

                    assert (len(key_index) == 1)
                    if key_index[0] < len(primary_key_field_list) - 1:
                        # Key field which isn't last one has changed so need to blank out deeper key
                        # values in the data node record as they should be re-filled from next branch
                        # of node tree.

                        for index in range(key_index[0] + 1, len(primary_key_field_list)):
                            data_node_record[primary_key_field_list[index]] = None

                    # Initialise record for next row.  Key fields should be maintained apart from the one which has
                    # changed. So just initialise non key fields and then update current key field.
                    for field_name in non_primary_key_field_list:
                        data_node_record[field_name] = None
                else:
                    # New value for non-primary key field.  That's an error (but only a warning to be issued)
                    # ToDo: Add logging to allow warnings to be issued which don't stop programme.
                    pass

        # All data fields have been processed, so just clean up the final record and add to the list.
        for field_name in data_node_record:
            if data_node_record[field_name] is None:
                data_node_record[field_name] = '(unfilled)'

        data_node_table.append(copy.copy(data_node_record))

        return data_node_table

    @staticmethod
    def _key_field_check(primary_key_filter, primary_key_flag):
        if primary_key_filter is None:
            return True
        elif primary_key_filter is True and primary_key_flag == 'yes':
            return True
        elif primary_key_filter is False and primary_key_flag == 'no':
            return True
        else:
            return False

    @staticmethod
    def extract_field_names(data_node_specifier, primary_key_only: Optional[bool] = None):

        fields = [
            field_name for field_name in data_node_specifier
            if OutlineNode._key_field_check(primary_key_only, data_node_specifier[field_name]['primary_key'])
        ]
        return fields

    def match_data_node(self, field_specifications):
        """
        Treat this node as the root of a data node embedded within a larger outline structure.  Using the
        field_specifications provided identify all nodes within the data_node sub-tree structure which match
        the supplied criteria, and extract the information required to fully define each extracted field

        :param field_specifications: A structure which defines the properties of a field to be extracted and
               also the criteria which define the properties of nodes which map to that field.

        :return: Information required to create a field object for each matched field and construct records
                 from the fields.
        """
        match_list = []
        for data_node_list_entry in self.iter_nodes():
            matched_field_data = self.match_field_node(data_node_list_entry, field_specifications)
            if matched_field_data is not None:
                match_list.append(matched_field_data)

        return match_list

    @staticmethod
    def match_field_node(field_node_list_entry, field_specifications):
        """
        Checks a supplied candidate field node against all the field specifiers to look for a match. If we
        find a match then return the field value as defined within the field specifier for the matched field.

        :param field_node_list_entry:
        :param field_specifications:
        :return:
        """
        for field_name in field_specifications:
            field_specification = field_specifications[field_name]
            criteria = field_specification['ancestry_matching_criteria']

            if OutlineNode.match_field(field_node_list_entry, criteria):
                field_value = OutlineNode.extract_field(field_node_list_entry.node(), field_specification)
                return field_name, field_value

    @staticmethod
    def match_field(node_ancestry_record, field_ancestry_criteria):
        """
        Check whether an outline node (field node) from within a data node sub-tree matches the criteria
        for a specific field specifier.

        Goes through ancestry of node and tests each generation against the corresponding criteria

        :param node_ancestry_record:
        :param field_ancestry_criteria:
        :return:
        """
        # First check whether depths match.  If not then definitely not a match.
        if node_ancestry_record.depth != len(field_ancestry_criteria) - 1:
            return False
        else:
            # Depth matches so we now need to test against provided criteria.  Each criterion corresponds to
            # a generation in the ancestry, so we need to test each generation against the appropriate criterion.
            # So we walk down the ancestry from root to current generation and check for a match.  As soon as
            # we fail to get a match, we know the node doesn't match.  If we don't fail at all generations then
            # we have a match.
            match = True

            # Create list of pairs from depth 1 to depth of node we are testing against.  Note that
            # a node list entry has ancestry starting at zero to represent the root of the outline, and
            # criteria need to start there too.
            paired_gen_and_criteria = zip(node_ancestry_record, field_ancestry_criteria)
            for pair in paired_gen_and_criteria:
                generation, gen_criteria = pair
                if not gen_criteria.matches_criteria(generation):
                    match = False

        return match


