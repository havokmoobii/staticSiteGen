from enum import Enum
from textnode import TextNode, TextType
# For extract_markdown_images(text) and extract_markdown_links(text)
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    sections = markdown.split("\n\n")
    blocks = []
    for section in sections:
        if section == "":
            continue
        stripped_section = ""
        lines = section.split("\n")
        for line in lines:
            if stripped_section == "":
                stripped_section = line.strip()
            else:
                stripped_section = stripped_section + "\n" + line.strip()
        if stripped_section != "":
            blocks.append(stripped_section.strip())
    return blocks

def block_to_block_type(block):
    if block.startswith("#"):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    quote, unordered, ordered = True, True, True
    for i in range(len(lines)):
        if not lines[i].startswith(">"):
            quote = False
        if not lines[i].startswith("- "):
            unordered = False
        if not lines[i].startswith(f"{i+1}. "):
            ordered = False
    if quote:
        return BlockType.QUOTE
    if unordered:
        return BlockType.UNORDERED_LIST
    if ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

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