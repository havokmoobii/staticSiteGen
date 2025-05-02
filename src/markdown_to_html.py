from enum import Enum
from markdown_to_textnode import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import ParentNode, LeafNode

class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "Unordered List"
    ORDERED_LIST = "Ordered List"

def markdown_to_blocks(markdown):
    blocks = []
    split_md = markdown.split("\n\n")
    for block in split_md:
        if len(block.strip()) != 0:
            blocks.append(block.strip())
    return blocks

def block_to_block_type(block):
    if len(block) == 0:
        raise Exception("Block cannot be empty.")

    if block.startswith("# "):
        return BlockType.HEADING
    if block.startswith("## "):
        return BlockType.HEADING
    if block.startswith("### "):
        return BlockType.HEADING
    if block.startswith("#### "):
        return BlockType.HEADING
    if block.startswith("##### "):
        return BlockType.HEADING
    if block.startswith("###### "):
        return BlockType.HEADING    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    quote = True
    unordered = True
    ordered = True
    splitblock = block.split("\n")
    for i in range(len(splitblock)):
        if not splitblock[i].startswith(">"):
            quote = False
        if not splitblock[i].startswith("- "):
            unordered = False
        if not splitblock[i].startswith(f"{i+1}. "):
            ordered = False
    if quote:
        return BlockType.QUOTE
    if unordered:
        return BlockType.UNORDERED_LIST
    if ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    block_nodes = []

    for block in blocks:
        type = block_to_block_type(block)
        tag = block_to_tag(block, type)
        
        if type == BlockType.CODE:
            children = [LeafNode(None, f"<code>{block.strip("```").lstrip("\n")}</code>")]
        else:
            formatted_block = format_block_text(block, type)
            children = []
            child_nodes = text_to_textnodes(formatted_block)
            for node in child_nodes:
                children.append(text_node_to_html_node(node))
        block_nodes.append(ParentNode(tag, children))

    return ParentNode("div", block_nodes)

def format_block_text(text, type):
    output = text
    if type == BlockType.PARAGRAPH or type == BlockType.HEADING:
        split_block = output.split("\n")
        output = " ".join(split_block)
    output = output.strip("#")
    if type == BlockType.QUOTE or type == BlockType.UNORDERED_LIST or type == BlockType.ORDERED_LIST:
        split_block = output.split("\n")
        new_block = ""
        for line in split_block:
            match(type):
                case(BlockType.QUOTE):
                    new_block = new_block + line[1:] + "\n"
                case(BlockType.UNORDERED_LIST):
                    new_block = new_block + f"<li>{line[2:]}</li>\n"
                case(BlockType.ORDERED_LIST):
                    new_block = new_block + f"<li>{line[3:]}</li>\n"
        output = new_block
    return output.strip()
    

def trim_block_newlines(block):
    split_block = block.split("\n")
    return " ".join(split_block)

def block_to_tag(block, block_type):
    match(block_type):
        case(BlockType.PARAGRAPH):
            return "p"
        case(BlockType.HEADING):
            if block.startswith("# "):
                return "h1"
            if block.startswith("## "):
                return "h2"
            if block.startswith("### "):
                return "h3"
            if block.startswith("#### "):
                return "h4"
            if block.startswith("##### "):
                return "h5"
            if block.startswith("###### "):
                return "h6"
            raise Exception("Heading block type on a non-heading block")
        case(BlockType.CODE):
            return "pre"
        case(BlockType.QUOTE):
            return "blockquote"
        case(BlockType.UNORDERED_LIST):
            return "ul"
        case(BlockType.ORDERED_LIST):
            return "ol"
        case _:
            raise Exception("Invalid BlockType")
