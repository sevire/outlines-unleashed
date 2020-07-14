from xml.etree import ElementTree
from outline.outline import Outline


class PreprocessorGeneric:
    """
    Act as an interface by defining some standard methods and other elements which a preprocessor must include.

    An outline preprocessor is used to turn an outline-like data structure or text file into an outline for onward
    unleashing.

    Use cases for pre-processing include the following:
    - Hand typed indented text files where tabs are used to indent text and so the file has an outline-like
      appearance.
    - Text cut and paste from various applications which allow an outline like bulleted list to be created often
      paste as text indented with tabs or spaces, and sometimes with a character used to represent the bullet.

      Applications which support this include email clients, OneNote etc.
    """
    def __init__(self, outline, config_object):
        # Supplied outline must be an iterable where each element represents a node of the outline.
        self.outline = outline
        self.config_object = config_object

    def pre_process_outline(self):
        # Replace with actual code
        return Outline.from_scratch()

    @staticmethod
    def create_outline_element(text, note=None):
        """
        Creates and XML outline element encoding the text and node contents as text and _node attributes.

        (Remember at the heart of an OutlineNode object is an outline xml element.

        :param text:
        :param note:
        :return:
        """

        attributes = {
            'text': text,
            '_note': note
        }

        return ElementTree.Element('outline', attributes)
