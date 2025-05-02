from enum import Enum
from markdown_to_textnode import text_to_textnodes

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
