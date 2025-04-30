import unittest

from textnode import TextNode, TextType
from markdown_to_textnode import split_nodes_delimiter

class TestSplitLineDelimiter(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is just text", TextType.TEXT)
        self.assertEqual([node], split_nodes_delimiter([node], "`", TextType.CODE))
    
    def test_bold(self):
        node = TextNode("**bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])

        node2 = TextNode("*bold* word", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([node2], "**", TextType.BOLD)
        self.assertEqual(new_nodes2, [
            TextNode("*bold* word", TextType.TEXT),
        ])

    def test_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])

    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_code_multiple(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This text `has` two `code blocks`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This text ", TextType.TEXT),
            TextNode("has", TextType.CODE),
            TextNode(" two ", TextType.TEXT),
            TextNode("code blocks", TextType.CODE),
        ])

    def test_error(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, node, "`", TextType.CODE)

if __name__ == "__main__":
    unittest.main()