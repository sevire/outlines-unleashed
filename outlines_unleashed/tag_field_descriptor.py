import re
from functools import reduce
from typing import Tuple

from opml.opml_exceptions import MalformedTagRegex

whitespace_characters_regex = r'\s*'
tag_characters_regex = '[a-zA-Z-_]+'
text_characters_regex = '.+'


def escape_regex_match(pattern):
    """
    Args:
        pattern:
    """
    value = reduce(lambda y, z: y + z, map(lambda x: '\\' + x, pattern), '')

    return value


class TagFieldDescriptor:
    def __init__(self, regex_delimiter: Tuple[str, str]):
        # We don't know whether the delimiter includes any reserved regex characters so escape all characters.

        """
        Args:
            regex_delimiter:
        """
        left_delim, right_delim = regex_delimiter
        self.left_delim = escape_regex_match(left_delim)
        self.right_delim = escape_regex_match(right_delim)
        self.tag_regex = re.compile(
            r'\s*' + re.escape(left_delim) + r'\s*(.*)\s*' + re.escape(right_delim) + r'\s*(.*)',
            re.DOTALL
        )

        # matches = re.match(enhanced_regex, text, re.DOTALL)
        # if matches is None:
        #     return text, None
        # else:
        #     groups = matches.groups()
        #     if len(groups) == 2:
        #         tag = matches.group(1).strip()
        #         extracted_text = matches.group(2).strip()
        #         return extracted_text, tag
        #     else:
        #         raise MalformedTagRegex(
        #             f"Number of matching groups in regex {len(groups)} invalid for tag matching, must be 0 or 2")
        #
        # tag_string = \
        #     whitespace_characters_regex + \
        #     '(' + \
        #     self.left_delim + \
        #     whitespace_characters_regex + \
        #     '(' + \
        #     tag_characters_regex + \
        #     ')' + \
        #     whitespace_characters_regex + \
        #     self.right_delim + \
        #     '){0,1}'
        #
        # text_string = \
        #     whitespace_characters_regex + \
        #     '(' + \
        #     text_characters_regex + \
        #     ')' + \
        #     whitespace_characters_regex
        #
        # regex_string = tag_string + text_string
        #
        # self.tag_regex = re.compile(regex_string, re.DOTALL)

    def parse_tag(self, text_string):
        """
        Args:
            text_string:
        """
        matches = self.tag_regex.match(text_string)
        if matches is None:
            return text_string.strip(), None
        else:
            groups = matches.groups()
            tag = groups[0].strip()
            text = groups[1].strip()
            return text, tag
