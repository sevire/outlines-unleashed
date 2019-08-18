from outlinesunleashed.outline_node import OutlineNode
#from outlinesunleashed.types import AncestryEntry
#import outlinesunleashed.exceptions as ex
import xml.etree.ElementTree as eTree
import copy


class Outline:
    def __init__(self, outline):
        """
        Outline is a representation of an object which is derived from OPML, an XML markup language.

        OPML is a way of representing an outline, which is a hierarchical tree structure used by outliners, some
        mind mapping tools and various other applications.

        This implementation is intended to be a fair implementation of the OPML language, but with one eye on the
        requirements of Outlines Unleashed.  Initially it isn't intended to be a full and comprehensive implementation
        of OPML but just enough to support the functionality of Outlines Unleashed.

        Because OPML is an XML language, the Outline class (and related classes such as OutlineNode) employ
        xml.etree.ElementTree (part of Python Standard Library) as the method to store and manipulate the xml tree
        which forms the outline.

        While this library implements the OPML language, an outline could theoretically be represented in a number of
        different ways (e.g. indented text, indented bullets from an MS Word document).  For this reason there are a
        number of ways of creating an outline which are implemented through factory methods.  More of these will be
        added over time to provide a comprehensive set of ways of creating an outline.  These factory methods will parse
        input in a given format and output an Outline object which will be identical to that which would have been
        created if the outline had been provided in an OPML file.

        See http://dev.opml.org/ for details of the OPML spec.

        Note that when the Outline instance is created, the full structure of the tree isn't checked to see whether it
        is valid.  Rather, as each node is processed it is checked that it is valid and an exception raised if not.
        This lazy approach is thought to be preferable to committing an unpredictable amount of time at the beginning
        checking every node in the tree.

        A deep copy of the outline is made as all the nodes will be references and we want to protect both the internal
        tree structure from outside changes and also protect the external structure from changes (extensions) we may
        wish to make to the structure as we impose the unleashed outline structure upon it.

        :param outline: An eTree element which is the root of the outline tree structure, represented as an
                        ElementTree object.
        """

        # Deep copy to de-couple from the external structure that was passed in.
        self.outline = copy.deepcopy(outline)

        # We are creating an outline from a passed in ElementTree.
        self.root = outline

    def __iter__(self, start_node=None, level=0, node_ancestry=None):
        """
        Parse an outline and collect key information on the way.  We can't use the ElementTree.Element.iter()
        function here because this doesn't provide the important context information we need to create the ancestry.
        """

        if start_node is None:
            outline_node = OutlineNode(self.root)
        else:
            outline_node = start_node

        # print('Iterator: Processing: Level={}, Text={}'.format(level, outline_node.text))
        if node_ancestry is None:
            node_ancestry_to_use = []
        else:
            node_ancestry_to_use = node_ancestry

        if len(outline_node) == 0:
            # We have reached the bottom of the tree on this branch so pop back up
            return
        else:
            # We iterate through each of the child nodes of current node, process it, yield the ancestry and then
            # call recursively to go down, so we keep doing down until we reach the deepest node of the branch,
            # then pop back up and continue iterating to the next node.

            for child_number, child_outline in enumerate(outline_node):
                # We have been passed node_ancestry as a reference so in order for the recursion to work
                # we need to take a copy of it so that when we pop we go back to the passed in value.
                new_node_ancestry = copy.deepcopy(node_ancestry_to_use)

                # Package up this node to add to the ancestry.
                ancestry_entry = AncestryEntry(child_number + 1, child_outline.text)

                # Now add details of this node to the ancestry and we are ready to yield it back out.
                new_node_ancestry.append(ancestry_entry)

                # yield current node then call next level down (depth first)
                yield child_outline, level + 1, new_node_ancestry
                yield from self.__iter__(child_outline, level + 1, new_node_ancestry)
            return

    def __repr__(self):
        total_number_of_nodes = len(self.outline.findall('outline'))
        return 'Outline: num_nodes = {}'.format(total_number_of_nodes)

    @classmethod
    def from_opml(cls, opml_path):
        outline = eTree.parse(opml_path)
        top_outline, head = Outline.initialise_opml_tree(outline)

        return cls(top_outline)

    @classmethod
    def from_etree(cls, e_tree):
        outline = e_tree
        top_outline, head = Outline.initialise_opml_tree(outline)

        return cls(top_outline)

    @classmethod
    def from_list_of_lists(cls, list_of_lists):
        """
        Constructs an outline from a recursively structured list of lists.

        Each list in the structure contains, in each element:
        - [0]: The text value of the node:
        - [1]-[n] Sub-lists which represent the child nodes for this node.  Each sub-list has the same structure
                  as the root node, and so on recursively.
        - A leaf-node (node with no children) is represented by a list with just the node value and no other elements.
        - An empty list will be interpreted as a non-existent element (shouldn't really be there).


        :param list_of_lists:
        :return:
        """

        node = list_of_lists
        node_value = node[0]
        node_children = node[1:]

        root = add_root()





    @staticmethod
    def initialise_opml_tree(tree):
        # Takes a full tree extracted from an OPML file and extracts head and places all the outline elements from
        # the body under an outline element (this ensures that all nodes in the tree are outline elements and makes
        # for easier processing).

        root = tree.getroot()

        should_be_body = root.findall('body')
        body = Outline.validate_matched_node(should_be_body)
        if body is None:
            top_outline = eTree.Element('outline')
        else:
            raise ex.MalformedOutline('Should be only one body element but {} were found'.format(len(should_be_body)))

        for outline in body:
            top_outline.append(outline)

        should_be_head = root.findall('head')
        if len(should_be_head) == 1 and should_be_head[0].tag == 'head':
            head = should_be_head[0]
        else:
            head = None

        return top_outline, head

    @property
    def number_of_nodes(self):
        return len(self.outline.findall('outline'))

    def visualise(self):
        chars_per_level = 3
        for outline, level, ancestry in self:



            # print((' ' * (chars_per_level-1) + '|')  * level)
            #print((' ' * (chars_per_level-1) + '|')  * (level-1) + '  o--o-[' + outline.__str__() + ']')
#            print(' ' * chars_per_level * level + 'o--o-[' + outline.__str__() + ']')

    def unleash(self):
        """
        This is the method which drives the parsing of outline and allows mapping of nodes for processing.

        The tree is parsed (depth first) and each node is marked with its ancestry which will then allow nodes which
        match the extraction criteria to be found and mapped.

        The ancestry takes the  form of a tuple of tuples where:

        - The sequence of each sub-tuple represents a generation from the root.  So as you follow the sub-tuples from
          left to right, each one represents a child of the previous one.  So the tuples will be arranged something
          like:

          ((gen-01-tuple), (gen-02-tuple), ... (tuple-for-this-node))

        - Each sub-tuple contains the following information:

          o Child Number: Which of the children of the parent node this node is, defined by the sequence in the
            OPML file.

          o The value of any tags found in the text of the node.  Tags are embedded values within the text which
            is one of the ways nodes are identified for mapping purposes.

            Example: If the outline file contains risks, a tag may be used to work out whether a given node is the risk
            likelihood or impact.  Tags are found using regular expressions to find encoded delimiters within the text
            which allow extraction of the tag.  (I think) tags will only be allowed at the beginning of the text.

            Example text with embedded tag: "[*L*] High".  Here the string '[*' and '*]' indicate the start and end
            of the tag value. So the value of the tag is 'L'.  The text for parsing purpose is therefore 'High'.

          o First n characters (n is about 20) of the text (not including the tag and any whitespace before the
            first character). The reason for storing the first 20 characters is that if a match requires the text to
            have a certain value it is likely to be a short string so by extracting it it will save having to check
            the text in the node when searching for a match.  On the rare occasion where the match text is more than 20 characters,
            the node can be checked.
        """

        for node_data in self:
            node, level, ancestry = node_data
            print('\n' + ancestry.__str__())
