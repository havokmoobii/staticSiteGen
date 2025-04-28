import unittest

from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
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
        self.assertRaises(Exception, node2.props_to_html)

if __name__ == "__main__":
    unittest.main()