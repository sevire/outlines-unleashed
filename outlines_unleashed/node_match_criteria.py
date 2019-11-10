class NodeMatchCriteria:
    def __init__(self,
                 level=None,
                 child_number=None,
                 text_value=None,
                 note_value=None,
                 text_tag_value=None,
                 note_tag_value=None
                 ):
        """
        Represents the criteria to apply at a specific generation (level)
        when trying to locate nodes to extract as part of the parsing of an
        outline to unleash.

        :param level:
        :param child_number:
        :param text_value:
        :param note_value:
        :param text_tag_value:
        :param note_tag_value:
        """
        self.level = level
        self.child_number = child_number
        self.text_value = text_value
        self.note_value = note_value
        self.text_tag_value = text_tag_value
        self.note_tag_value = note_tag_value
