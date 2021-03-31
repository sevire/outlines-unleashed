import copy
import json
from typing import Optional
from outlines_unleashed.node_ancestry_matching_criteria import NodeAncestryMatchingCriteria
from outlines_unleashed.unleashed_outline_exceptions import InvalidDataNodeSpecifierVersion, InvalidDataNodeSpecifier


class DataNodeSpecifier:
    """
    Data Node Specifier: The object used to represent the instructions for how to find the data fields within a data node.

    Data Node Field Descriptors: The record within the DNS which contains the instruction for decoding the data node.

    Data Node Field Descriptor: Individual instructions for locating a specific field within a Data Node.

    The instructions are contained within a field within the object (dns_structure).  Given a data node, the
    object will find and extract all the data nodes within the node and return in a tabular format (defined within
    a list or records where each record is a dictionary of fixed format depending upon the defined fields).

    Includes the following functionality:

    - Reads and validates a JSON representation of a data node descriptor (in multiple versions and formats
      potentially.
    - Takes an outline node as a root and parses it according to a descriptor, extracting fields into a
      standard data node table format for onward transformation and output.
    """

    def __init__(self, dns_structure):
        """
        Initialises the DND based on an input data structure which defines the fields to be extracted and the
        criteria to be used to locate each field.

        ToDo: Consider possibility that there may be more than one field definition for a field.
        :param dns_structure:
        """
        self.dns_structure = dns_structure
        self.validate_data_node_specifier()

    def validate_data_node_specifier(self):
        """
        If a data structure is passed in from the user for the DNS then it needs to be checked.  If it is passed in
        from the from_json method then it will have been created to be well formed.

        For now carry out cursory checks but will need to be more sophisticated later.

        ToDo: Enhance validation for DNS data structure.  Include version specific checking
        :return:
        """
        if 'header' not in self.dns_structure:
            raise InvalidDataNodeSpecifier(f'[header] record not present in Data Node Specifier')
        if 'descriptor' not in self.dns_structure:
            raise InvalidDataNodeSpecifier(f'[descriptor] record not present in Data Node Specifier')

        header = self.dns_structure['header']
        if 'tag_delimiters' not in header:
            header['tag_delimiters'] = {
                'note_delimiters': [None, None],
                'text_delimiters': [None, None]
            }

    @classmethod
    def from_json_file(cls, json_path):
        with open(json_path, 'r') as json_fp:
            json_object = json.load(json_fp)

            return DataNodeSpecifier._from_json_object(json_object)


    @classmethod
    def from_json_string(cls, serialized_specifier):
        """
        Overloaded function which will take one of:
        - A string containing a JSON representation of a DND
        - File object for a file containing a JSON representation of a DND
        - A file path to a file containing a JSON representation of a DND

        The function will parse the JSON according to which version of the JSON format is encapsulated, and
        create a new DND object.
        :return:
        """
        specifier_json_object = json.loads(serialized_specifier)

        return DataNodeSpecifier._from_json_object(specifier_json_object)



    @classmethod
    def _from_json_object(cls, json_object):
        """
        Common processing from the .from_json_file and .from_json_string methods, once json has been turned into
        a dict object.

        :param json_object:
        :return:
        """

        # For now a very clunky approach to creating a Python descriptor from the JSON
        # sourced dict structure.  Will refactor into an independent class later
        # ToDo: Extract descriptor structure and logic into separate class

        # Set up the empty structure into which we will build the specifier, and initialise header fields from json
        specifier = {'header': json_object['header'], 'descriptor': {}}

        # Add the text and note tag regex delimiters.
        # ToDo: Develop clear rules for the value to use for tag delimiters to indicate not specified etc.
        text_tag_delimiter_left = json_object['header']['tag_delimiters']['text_delimiters'][0]
        text_tag_delimiter_right = json_object['header']['tag_delimiters']['text_delimiters'][1]
        note_tag_delimiter_left = json_object['header']['tag_delimiters']['note_delimiters'][0]
        note_tag_delimiter_right = json_object['header']['tag_delimiters']['note_delimiters'][1]

        specifier['header']['tag_delimiters'] = {}
        specifier['header']['tag_delimiters']['text_delimiters'] = [text_tag_delimiter_left, text_tag_delimiter_right]
        specifier['header']['tag_delimiters']['note_delimiters'] = [note_tag_delimiter_left, note_tag_delimiter_right]

        raw_descriptor = json_object['descriptor']

        for raw_field_descriptor in raw_descriptor:
            specifier['descriptor'][raw_field_descriptor] = {}
            for field_property in json_object['descriptor'][raw_field_descriptor]:
                if field_property == 'ancestry_matching_criteria':
                    # We need to replace the list of dicts with a list of NodeAncestryMatchingCriteria objects
                    specifier['descriptor'][raw_field_descriptor][field_property] = []

                    criteria_list = json_object['descriptor'][raw_field_descriptor][field_property]
                    for criteria_set in criteria_list:
                        criteria_object = NodeAncestryMatchingCriteria(
                            child_number=criteria_set.get('child_number', None),
                            text=criteria_set.get('text', None),
                            note=criteria_set.get('note', None),
                            text_tag=criteria_set.get('text_tag', None),
                            note_tag=criteria_set.get('note_tag', None),
                        )
                        specifier['descriptor'][raw_field_descriptor][field_property].append(criteria_object)
                else:
                    specifier['descriptor'][raw_field_descriptor][field_property] = \
                        raw_descriptor[raw_field_descriptor][field_property]

        return cls(specifier)

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

    def extract_field_default_value(self, field_name):
        """
        Mainly needed when a data node is being extracted and there isn't a sub-node which matches a particular field. The
        record will need a value for each field which is specified and the specifier for a field allows a default value
        to be specified.  If none is specified then None is returned.

        :param field_name:
        :return:
        """
        descriptor = self.dns_structure['descriptor']
        field_specifier = descriptor[field_name]
        if 'default_value' in field_specifier:
            return field_specifier['default_value']
        else:
            return None

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

    def extract_data_node_dispatch(self, data_node, **kwargs):
        """
        Dispatcher method which works out which version of the descriptor structure is being
        passed in and then forwards the descriptor to the appropriate version specific extract
        method.

        :param data_node:
        :return:
        """
        version = self.dns_structure['header']['descriptor_version_number']

        if version == '0.1':
            return self._extract_data_node_v0_1(data_node, **kwargs)
        else:
            raise InvalidDataNodeSpecifierVersion(f'Version of [{version}] not valid for Data Node Specifier.')

    @staticmethod
    def _initialise_data_node_record(field_list):
        return {key: None for key in field_list}

    def _cleanup_extracted_record(self, data_node_record):
        """
        The record is passed in after all fields that are in the data node have been extracted.  This method
        then checks for fields which weren't populated and gives them the default value for the field, taken
        from the data node specifier.

        :param data_node_record:
        :return:
        """
        for field in data_node_record:
            if data_node_record[field] is None:
                data_node_record[field] = self.extract_field_default_value(field)

    def _extract_data_node_v0_1(self, data_node, override_data_node_tag_delim=False):
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

        :param data_node: UnleashedOutlineNode object from UnleashedOutline
        :param override_data_node_tag_delim: If not set, then take tag delimiters from the node (if present). If set
                                             take them from the DNS.  If neither present and the specifier includes
                                             tag criteria, then raise an error.
        :return:
        """
        if override_data_node_tag_delim:
            # We are overriding the tag delimiters from the data node with those from the DNS.
            delimiters = self.dns_structure['header']['tag_delimiters']

            data_node.tag_regex_text = tuple(delimiters['text_delimiters'])
            data_node.tag_regex_note = tuple(delimiters['note_delimiters'])

        match_list = self.match_data_node(data_node)
        data_node_table = []
        primary_key_field_list = self.extract_field_names(primary_key_only=True)
        non_primary_key_field_list = self.extract_field_names(primary_key_only=False)

        # Initialise record for first row
        data_node_record = self._initialise_data_node_record(primary_key_field_list+non_primary_key_field_list)

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

                    self._cleanup_extracted_record(data_node_record)

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
        self._cleanup_extracted_record(data_node_record)
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

    def extract_field_names(self, primary_key_only: Optional[bool] = None):
        descriptor = self.dns_structure['descriptor']

        fields = [
            field_name for field_name in descriptor
            if DataNodeSpecifier._key_field_check(primary_key_only, descriptor[field_name]['primary_key'])
        ]
        return fields

    def match_data_node(self, unleashed_node):
        """
        Treat the supplied node as the root of a data node embedded within a larger outline structure.  Using the
        field_specifications provided identify all nodes within the data_node sub-tree structure which match
        the supplied criteria, and extract the information required to fully define each extracted field

        :param unleashed_node:
        :return: Information required to create a field object for each matched field and construct records
                 from the fields.
        """
        override_node = self._override_tag_regex(unleashed_node)
        match_list = []
        for data_node_list_entry in override_node.iter_unleashed_nodes():
            for matched_field_data in self.match_field_node(data_node_list_entry):
                match_list.append(matched_field_data)

        return match_list

    def match_field_node(self, field_node_list_entry):
        """
        Look for one or more fields within a supplied candidate field node.

        A node could contain more than one field as there are four places within a node where a field
        could live and it is possible to create criteria which match the same node but extract a different
        value.

        This function is built as a generator to continue to return values until there are no more
        matches to look for.

        :param field_node_list_entry:
        :return:
        """
        descriptor = self.dns_structure['descriptor']
        for field_name in descriptor:
            field_specification = descriptor[field_name]
            criteria = field_specification['ancestry_matching_criteria']

            if DataNodeSpecifier.match_field(field_node_list_entry, criteria):
                field_value = DataNodeSpecifier.extract_field(field_node_list_entry.node(), field_specification)
                yield field_name, field_value

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

    def _override_tag_regex(self, unleashed_node):
        """
        If the specifier includes overrides for either tag or note regex, then clone the node to make a new one
        with the updated regex, otherwise just leave alone

        :param unleashed_node:
        :return:
        """
        text_regex_override = self.dns_structure['header']['tag_delimiters']['text_delimiters']
        note_regex_override = self.dns_structure['header']['tag_delimiters']['note_delimiters']

        clone = False
        if text_regex_override is not None and text_regex_override != [None, None]:
            clone = True
            text_val_to_use = text_regex_override
        else:
            text_val_to_use = unleashed_node.tag_regex_text
        if note_regex_override is not None and note_regex_override != [None, None]:
            clone = True
            note_val_to_use = note_regex_override
        else:
            note_val_to_use = unleashed_node.tag_regex_note

        if clone is True:
            return unleashed_node.clone_unleashed_node(text_tag_regex=text_val_to_use,
                                                       note_tag_regex=note_val_to_use)
        else:
            return unleashed_node


