import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from to_html import text_node_to_html_node


class TestHTMLNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node1.to_html(), '<a href="https://www.google.com">Click me!</a>')
        node2 = LeafNode("h1", "This is a header")
        self.assertEqual(node2.to_html(), "<h1>This is a header</h1>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_text(self):
        node = TextNode("text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "text")
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "text")
        node2 = TextNode("bold", TextType.BOLD)
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node2.to_html(), "<b>bold</b>")
        node3 = TextNode("italic", TextType.ITALIC)
        html_node3 = text_node_to_html_node(node3)
        self.assertEqual(html_node3.to_html(), "<i>italic</i>")
        node4 = TextNode("This is code", TextType.CODE)
        html_node4 = text_node_to_html_node(node4)
        self.assertEqual(html_node4.to_html(), "<code>This is code</code>")
        node5 = TextNode("link", TextType.LINK, "https://www.google.com")
        html_node5 = text_node_to_html_node(node5)
        self.assertEqual(html_node5.to_html(), '<a href="https://www.google.com">link</a>')
        node6 = TextNode("Description of image", TextType.IMAGE, "url/of/image.jpg")
        html_node6 = text_node_to_html_node(node6)
        self.assertEqual(html_node6.to_html(), '<img src="url/of/image.jpg" alt="Description of image" />')

if __name__ == "__main__":
    unittest.main()