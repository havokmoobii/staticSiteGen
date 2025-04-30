from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif delimiter in node.text:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception("Missing closing Markdown delimiter.")
            for i in range(len(split_text)):
                if i % 2 == 0:
                    if len(split_text[i]) != 0:
                        new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_text[i], text_type))
        else:
            new_nodes.append(node)
    return new_nodes