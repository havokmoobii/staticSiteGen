import unittest

from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()