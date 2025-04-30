import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT or not delimiter in node.text:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception("Missing closing Markdown delimiter.")
            for i in range(len(split_text)):
                if i % 2 == 0:
                    if len(split_text[i]) != 0:
                        new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            if images == []:
                new_nodes.append(node)
            else:
                remaining_text = node.text
                for image in images:
                        split_text = remaining_text.split(f"![{image[0]}]({image[1]})", 1)
                        if len(split_text[0]) != 0:
                            new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                        new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                        remaining_text = split_text[1]
                if len(remaining_text) != 0:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            if links == []:
                new_nodes.append(node)
            else:
                remaining_text = node.text
                if "![" in remaining_text:
                    raise Exception("Image Markdown found. Pass the list of TextNodes to split_nodes_image before split_nodes_link.")
                for link in links:
                        split_text = remaining_text.split(f"[{link[0]}]({link[1]})", 1)
                        if len(split_text[0]) != 0:
                            new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                        new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                        remaining_text = split_text[1]
                if len(remaining_text) != 0:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes