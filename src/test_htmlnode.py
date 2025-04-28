import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("This is an HTML node.")
        self.assertEqual(node, HTMLNode("This is an HTML node.", None, None, None))

    def test_not_eq(self):
        node = HTMLNode("This is an HTML node")
        self.assertNotEqual(node, HTMLNode())

    def test_to_html(self):
        node = HTMLNode("This is an HTML node.")
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode(None, None, None, {
            "href": "https://www.google.com",
            "target": "_blank",
            })
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')

        node2 = HTMLNode("This is an HTML node.")
        self.assertEqual("", node2.props_to_html())

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')

        node3 = LeafNode("p", None)
        self.assertRaises(ValueError, node3.to_html)

        node4 = LeafNode(None, "Raw text")
        self.assertEqual(node4.to_html(), "Raw text")

if __name__ == "__main__":
    unittest.main()