import unittest

from textnode import TextNode, TextType, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node3 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node3)
        node4 = TextNode("This is a url node", TextType.LINK, "https://www.google.com")
        node5 = TextNode("This is a url node", TextType.LINK, "https://www.google.com")
        self.assertEqual(node4, node5)
        self.assertNotEqual(node, node4)
    
    def test_split_nodes(self):
        nodes = [TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)]
        test_nodes = [
            TextNode("This is text with a", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode("in the middle", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(test_nodes, new_nodes)
        nodes2 = [TextNode("This is text with a _italic phrase_ in the middle", TextType.TEXT)]
        test_nodes2 = [
            TextNode("This is text with a", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode("in the middle", TextType.TEXT)
        ]
        new_nodes2 = split_nodes_delimiter(nodes2, "_", TextType.ITALIC)
        self.assertEqual(test_nodes2, new_nodes2)
        nodes3 = [TextNode("This is text with a ```code``` in the middle", TextType.TEXT)]
        test_nodes3 = [
            TextNode("This is text with a", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("in the middle", TextType.TEXT)
        ]
        new_nodes3 = split_nodes_delimiter(nodes3, "`", TextType.CODE)
        self.assertEqual(test_nodes3, new_nodes3)
        nodes4 = [TextNode("This is text with a **bolded phrase** an _italic phrase_ and some `code`", TextType.TEXT)]
        test_nodes4 = [
            TextNode("This is text with a", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode("an", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode("and some", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ]
        new_nodes4 = split_nodes_delimiter(nodes4, "*", TextType.BOLD)
        new_nodes4 = split_nodes_delimiter(new_nodes4, "_", TextType.ITALIC)
        new_nodes4 = split_nodes_delimiter(new_nodes4, "`", TextType.CODE)
        self.assertEqual(test_nodes4, new_nodes4)


if __name__ == "__main__":
    unittest.main()