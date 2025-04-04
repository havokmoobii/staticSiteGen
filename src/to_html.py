from from_markdown import markdown_to_blocks, block_to_block_type, text_to_textnodes, BlockType
from textnode import TextType
from htmlnode import LeafNode, ParentNode

#Obviously not done.
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown) 
    parents = []
    for block in blocks:
        block_type = block_to_block_type(block)
        tag = block_type_to_html_tag(block_type)
        children = text_to_textnodes(block.replace("\n", " "))
        if block_type == BlockType.CODE:
            parents.append(LeafNode("code", block))
            continue
        html_children = []
        for child in children:
            html_children.append(text_node_to_html_node(child))
        parents.append(ParentNode(tag, html_children))
    return ParentNode("div", parents)

def block_type_to_html_tag(block_type):
    match(block_type):
        case(BlockType.PARAGRAPH):
            return "p"
    match(block_type):
        case(BlockType.QUOTE):
            return "blockquote"
    match(block_type):
        case(BlockType.UNORDERED_LIST):
            return "ul"
    match(block_type):
        case(BlockType.ORDERED_LIST):
            return "ol"
    match(block_type):
        case(BlockType.CODE):
            return "code"
    match(block_type):
        case(BlockType.HEADING):
            return "h"
        case _:
            raise Exception("Invalid Block Type")
        
def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case(TextType.TEXT):
            return LeafNode(None, text_node.text)
        case(TextType.BOLD):
            return LeafNode("b", text_node.text)
        case(TextType.ITALIC):
            return LeafNode("i", text_node.text)
        case(TextType.CODE):
            return LeafNode("code", text_node.text)
        case(TextType.LINK):
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case(TextType.IMAGE):
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("TextNode type is invalid.")