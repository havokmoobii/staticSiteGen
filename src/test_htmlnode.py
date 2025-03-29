import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p")
        node2 = HTMLNode("p", "This is some text")
        node3 = HTMLNode("a", "This is a link", None, {"href": "https://www.google.com", "target": "_blank"})

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node1.to_html(), '<a href="https://www.google.com">Click me!</a>')
        node2 = LeafNode("h1", "This is a header")
        print(node2.to_html())
    
if __name__ == "__main__":
    unittest.main()