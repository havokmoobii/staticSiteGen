from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "`code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        if text_type == TextType.LINK and url == None:
            raise TypeError("LINK type nodes must have a url.")
        if text_type == TextType.IMAGE and url == None:
            raise TypeError("IMAGE type nodes must have a url.")
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    

    # Probably still need to figure out how to handles newlines in code markdown.
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            nodes.append(node)
        else:    
            node_start_index = 0
            node_current_index = -1
            delimiter_found = False
            words = node.text.split()

            for word in words:
                node_current_index += 1

                if word.startswith(delimiter):
                    # Prevent trying to create an empty node if delimiter is at start of node.
                    if node_current_index != 0:
                        nodes.append(TextNode(" ".join(words[node_start_index:node_current_index]), TextType.TEXT))
                    node_start_index = node_current_index
                    delimiter_found = True

                if word.endswith(delimiter) and delimiter_found == True:
                    line = " ".join(words[node_start_index:node_current_index + 1])
                    nodes.append(TextNode(line.strip(delimiter), text_type))
                    # Set start index to next word.
                    node_start_index = node_current_index + 1
                    delimiter_found = False

                if node_current_index == len(words) - 1:
                    if delimiter_found == True:
                        raise Exception(f"Invalid Markdown syntax. Missing closing {delimiter}.")
                    if node_start_index <= node_current_index:
                        nodes.append(TextNode(" ".join(words[node_start_index:]), TextType.TEXT))

    return nodes