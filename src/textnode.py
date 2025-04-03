from enum import Enum
# For extract_markdown_images(text) and extract_markdown_links(text)
import re

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
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) == 0:
            nodes.append(node)
            continue
        if len(split_text) % 2 == 0:
            raise Exception("Invalid markdown. Formatted section not closed.")
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 1:
                nodes.append(TextNode(split_text[i], text_type))
            else:
                nodes.append(TextNode(split_text[i], TextType.TEXT))
    return nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            nodes.extend(split_single_node_image(node.text, images))
    return nodes

def split_single_node_image(node_text, images):
    nodes = []
    if images == []:
        if node_text != "":
            return [TextNode(node_text, TextType.TEXT)]
    if node_text == "":
        return nodes

    split_text = node_text.split(f"![{images[0][0]}]({images[0][1]})")
    if split_text[0] != "":
        nodes.append(TextNode(split_text[0], TextType.TEXT))
    nodes.append(TextNode(images[0][0], TextType.IMAGE, images[0][1]))

    if split_text != []:
        nodes.extend(split_single_node_image(split_text[1], images[1:]))
    return nodes

def split_nodes_link(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            nodes.extend(split_single_node_link(node.text, links))
    return nodes

def split_single_node_link(node_text, links):
    nodes = []
    if links == []:
        if node_text != "":
            return [TextNode(node_text, TextType.TEXT)]
    if node_text == "":
        return nodes
    
    split_text = node_text.split(f"[{links[0][0]}]({links[0][1]})")
    if split_text[0] != "":
        nodes.append(TextNode(split_text[0], TextType.TEXT))
    nodes.append(TextNode(links[0][0], TextType.LINK, links[0][1]))

    if split_text != []:
        nodes.extend(split_single_node_link(split_text[1], links[1:]))
    return nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes