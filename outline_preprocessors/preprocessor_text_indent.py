from xml.etree import ElementTree

from outline.opml_exceptions import MalformedOutline
from outline.outline import Outline
from outline_preprocessors.preprocessor_generic import PreprocessorGeneric


class TextOutlineDecodeSpecifier:
    def __init__(
                    self,
                    indent_token,
                    bullet_token=None,
                    level1_indent_count=0,
                    initial_token=None,
                    include_initial_if_blank=False,
                 ):
        """
        Encapsulates specification for an outline which is formatted into an indented text file.

        There are various variable aspects of an indented text file which has been created to represent a hierarchichal
        structure, and could therefore converted to an outline.  This includes things like how is the indent level
        represented? Tabs, groups of spaces etc are possible answers.  Also is there a character included to represent
        a bullet character?  When indented, bulleted text is cut and paste from an application such as an email,
        OneNote, Word etc, sometimes a bullet character is included to make the plain text representation of the
        indented text more readable.

        There are also variants in what happens for the left most indent level.  Does no indent mean one indent level
        or is it an error?  Do you need a bullet character on the first indent level?  It is quite common to use the
        topmost indent level.

        The specification also allows for the case when there is a fixed character (or string) at the beginning of
        every line.  I don't remember encountering this case, but I can imagine that there may be apps which place a
        tab character, for example at the beginning of every line, even if the string used for indent levels is
        four spaces.  Even considering YAGNI I have decided to include it as it's easy to include and makes the code
        a little more resilient.

        This class allows a user to specify precisely what

        :param initial_token:
        :param indent_token:
        :param bullet_token:
        :param level1_indent_count:
        :param include_initial_if_blank:
        """
        self.initial_token = initial_token
        self.indent_token = indent_token
        self.bullet_token = bullet_token
        self.include_initial_if_blank = include_initial_if_blank
        self.level1_indent_count = level1_indent_count

    def decode_initial_token(self, text_string):
        """
        Takes a string and checks whether the initial token is correctly present in the string if it needs to be.
        Returns a flag to say whether the string was found, and also the string, with initial token removed if it was
        there.

        Note that at this stage of parsing, not all error conditions can be detected.  If the token is specified but
        not included, it may not be an error if the include_initial_if_blank flag is not set and the content of the
        line turns out to be blank, which we can't know until all the indent characters and bullets have been
        removed.  So just return a flag to say everything's definitely ok or everything may not be ok - watch this
        space and see whether the content is blank.

        :param text_string:
        :return: found_flag, reduced_string:
                    found_flag: True if all as expected (token either not expected or was present).
                                False if was expected but not found (note not always an error).
        """
        if self.initial_token is None:
            return True, text_string
        else:
            initial_token_length = len(self.initial_token)
            if text_string[:initial_token_length] == self.initial_token:
                return True, text_string[initial_token_length:]
            else:
                if self.include_initial_if_blank is True:
                    raise ValueError(f"Initial string ({self.initial_token}) expected but not found")
                else:
                    return False, text_string

    def decode_indent_token(self, text_string):
        """
        Works out how many occurrences of the indent token there are, and depending upon level1 indent count, calculate
        the indent level that indicates.  Then strip off the indent tokens and return the string.

        :param text_string:
        :return: reduced_text_string
        """
        repeat_len = len(self.indent_token)
        repeating = True
        indent_token_count = 0
        line_index = 0
        while repeating:
            maybe_repeat = text_string[line_index:(line_index + repeat_len)]
            if maybe_repeat == self.indent_token:
                indent_token_count += 1
                line_index += repeat_len
            else:
                repeating = False
        indent_level = indent_token_count + 1 - self.level1_indent_count
        if indent_level < 1:
            # Number of indent tokens not valid for this specification, e.g. Level 1 needs 1 indent count not zero
            raise ValueError(f"Number of indent tokens ({indent_token_count})  invalid for supplied specification")
        else:
            return indent_level, text_string[(repeat_len * indent_token_count):]

    def decode_bullet_token(self, text_string, indent_level):
        """
        Checks whether there should be a bullet character for this level of node, and then checks whether the right
        character exists.  If the level is beyond the deepest level for which a bullet character is defined, then use
        the deepest one that is defined.

        Return the text minus the bullet.

        :param text_string:
        :param indent_level:
        :return:
        """
        # ToDo: Clean up the logic in the final step of decoding a text line (bullet checking)
        if self.bullet_token is None:
            remaining_text_cleaned = text_string.strip()
            if remaining_text_cleaned == "":
                return None
            else:
                return remaining_text_cleaned
        else:
            # Work out which bullet token we are using for this level.
            highest_level_bullet_token = len(self.bullet_token)
            if indent_level > highest_level_bullet_token:
                token_for_level = self.bullet_token[-1]
            else:
                token_for_level = self.bullet_token[indent_level - 1]

            token_length = len(token_for_level)
            should_be_bullet = text_string[:token_length]
            remaining_text_cleaned = text_string[token_length:].strip()
            if should_be_bullet == token_for_level:
                # Bullet found, but if the remaining text is blank (or whitespace) then we should ignore the line
                if remaining_text_cleaned == "":
                    return None
                else:
                    return remaining_text_cleaned
            else:
                # There's no bullet character, but it it's a blank line then it's not an error (blank lines are ignored)
                if remaining_text_cleaned == "":
                    return None
                else:
                    raise ValueError(f"No bullet character ({token_for_level}) found")

    def __repr__(self):
        return f"{self.indent_token}-{self.bullet_token}"


class PreprocessorTextIndent(PreprocessorGeneric):
    @classmethod
    def from_textfile(cls, file_path, config_object):
        with open(file_path, "r") as fh:
            lines = [line for line in fh.readlines()]
        return cls(lines, config_object)

    def pre_process_outline(self):
        parse_output = self.parse_text()
        outline = self.create_outline(parse_output)

        return outline

    def parse_text(self):
        """
        Reads in a text file and parses it into to a hierarchical structure to imitate the structure of an outline.

        :param decode_specifier:
        :return:
        """

        parse_output = []
        for line_num, raw_line in enumerate(self.outline):
            # Strip off the newline
            line = self.strip_newline(raw_line)

            # Check whether any non whitespace characters in text.  If not then treat as a blank line and ignore.
            no_whitespace_line = line.strip()
            if len(no_whitespace_line) > 0:
                indent_level, content_line = self.parse_indent(line, self.config_object)
                parse_output.append((indent_level, content_line))

        return parse_output

    def parse_indent(self, line, decode_specifier: TextOutlineDecodeSpecifier):
        """
        Takes a line of text from an indented outline and works out what indent level it is and strips out the indent
        text to extract the actual content, returning the indent level and the content.

        The indent string at the beginning of the line can be structured in a number of different ways.  Broadly:

        - LEVEL 1: A line of text with no special characters at the beginning will usually be deemed to be Level 1. It
          may be that we will add a variant which forces all lines to have the indent string.

        - BEGINNING: There may be a fixed string at the beginning of each line.  Actually I'm not sure this will be a
          common use case but is here for completeness.

          If there is then in general we would expect to see that for all lines (with the exception of Level 1 lines
          where there may be no special characters at all).

        - REPEATING STRING: There will be a string which is repeated to indicate the indent level.  Typically this will be
          a tab or a sequence of spaces (e.g. 4 spaces is one indent level).

        - END: There may be a character or string at the end of the indent string which is not repeated.  Typically, when
          an indented bulleted structure is cut and paste from an application (email, OneNote etc) it translates indent
          levels to tabs followed by a character to represent the bullet, such as an 'o', followed by a space.  Sometimes
          there may be a different character for different indent levels which I may need to cater for at some point.

        It then strips out the indent segment and returns the string content and the indent level.

        :param line: Sequence of characters forming a line from the text outline.
        :param decode_specifier: TextOutlineDecodeSpecifier which holds the three elements of the indent so that the line can be parsed and
                             the indent level can be calculated.

        :return: (indent_level, content)
        """

        initial_string_status, processed_string_01 = decode_specifier.decode_initial_token(line)
        indent_level, processed_string_02 = decode_specifier.decode_indent_token(processed_string_01)
        node_text = decode_specifier.decode_bullet_token(processed_string_02, indent_level)

        # If None has been returned, it means we should ignore the line (probably a blank)
        if node_text is None:
            return None, None
        else:
            return indent_level, node_text

    @staticmethod
    def strip_newline(string_from_file):
        """
        Removes any file control characters from a line read from a file.

        When reading text files, each line will have a new line character apart from the last one (typically).  This
        function will remove the character if it's present.

        :param string_from_file:
        :return:
        """
        if string_from_file[-1] == "\n":
            return string_from_file[:-1]
        else:
            return string_from_file

    def add_child_nodes(self, node, level, nodes_data, nodes_data_index):
        """
        Recursive method which constructs a tree of outline elements from the parsed text file records.

        When called the method will iterate through the remaining node records and:
        - If the next node is a level higher, call recursively
        - If the next node is at the same level, add to an array of


        :param node:
        :param level:
        :param nodes_data:
        :param nodes_data_index:
        :return:
        """
        child_nodes = []
        end_of_nodes_data = False
        index = nodes_data_index - 1
        while not end_of_nodes_data:
            if index < len(nodes_data) - 1:
                index += 1
            else:
                end_of_nodes_data = True
            if not end_of_nodes_data:
                new_node_data = nodes_data[index]
                new_level, text = new_node_data
                new_node = self.create_outline_element(text)
                if new_level == level + 1:
                    # Child node so add to array of child nodes
                    child_nodes.append(new_node)
                elif new_level == level + 2:
                    # Next level down the tree so call recursively, to add to the last node at this level
                    # which is the last element in child_nodes.
                    index = self.add_child_nodes(child_nodes[-1], level + 1, nodes_data, index)
                elif new_level > level + 2:
                    raise MalformedOutline(f"Text indented outline jumped two generations at '{text}'")
                elif new_level <= level:
                    # We are at a leaf node so can append all children and return to the last recursive call
                    node.extend(child_nodes)
                    return index - 1
        node.extend(child_nodes)
        return index


    def create_outline(self, outline_spec):
        """
        After parsing a text file, calculating the indent level and extracting the text from each line, we can now
        construct the outline itself.

        In an opml file, the outline nodes at the top of the tree hang off the body element.  But in order to simplify
        the use of recursion to generate the tree, we will initially generate the tree hanging from an outline element,
        and then once the tree is created, create the well-formed xml tree to correctly drive the Outline object.

        :param outline_spec:
        :return:
        """

        top_level_node = self.create_outline_element(None)

        self.add_child_nodes(top_level_node, 0, outline_spec, 0)
        outline_child_nodes = [outline_element for outline_element in top_level_node]

        return Outline.from_scratch(outline_child_nodes)
