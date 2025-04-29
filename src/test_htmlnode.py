import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        node = ParentNode(
            "p",
            [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

        child_node = LeafNode("span", "child")

        node2 = ParentNode(None, [child_node])
        self.assertRaises(ValueError, node2.to_html)

        node3 = ParentNode("div", None)
        self.assertRaises(ValueError, node3.to_html)

    def test_parent_to_html_with_props(self):
        node = ParentNode(
            "p",
            [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            ],
            {"href": "https://www.google.com"}
        )
        self.assertEqual(node.to_html(), '<p href="https://www.google.com"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node], {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node], {"target": "https://www.facebook.com"})
        self.assertEqual(
            parent_node.to_html(),
            '<div target="https://www.facebook.com"><span href="https://www.google.com"><b>grandchild</b></span></div>',
        )

        child_node2 = ParentNode("span", [grandchild_node])
        parent_node2 = ParentNode("div", [child_node2])
        self.assertEqual(
            parent_node2.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()