import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("This is a text node", TextType.ITALIC, None)
        node4 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node3, node4)

        node6 = TextNode("This is a text node", TextType.TEXT, "www.google.com")
        node5 = TextNode("This is a text node", TextType.TEXT, "www.google.com")
        self.assertEqual(node5, node6)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

        node3 = TextNode("This is a text node", TextType.IMAGE, None)
        node4 = TextNode("This is also a text node", TextType.IMAGE)
        self.assertNotEqual(node3, node4)

        node6 = TextNode("This is a text node", TextType.IMAGE, "www.google.com")
        node5 = TextNode("This is a text node", TextType.IMAGE)
        self.assertNotEqual(node5, node6)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<i>This is a text node</i>")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<code>This is a text node</code>")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "www.google.com"})
        self.assertEqual(html_node.to_html(), '<a href="www.google.com">This is a text node</a>')

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "www.google.com", "alt": "This is a text node"})
        self.assertEqual(html_node.to_html(), '<img src="www.google.com" alt="This is a text node" />')

    def test_invalid(self):
        node = TextNode("This is a text node", "cat")
        self.assertRaises(Exception, text_node_to_html_node, node)

if __name__ == "__main__":
    unittest.main()