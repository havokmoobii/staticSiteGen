import unittest

from textnode import TextNode, TextType
from from_markdown import markdown_to_blocks, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(test_nodes, new_nodes)
        nodes2 = [TextNode("This is text with a _italic phrase_ in the middle", TextType.TEXT)]
        test_nodes2 = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" in the middle", TextType.TEXT)
        ]
        new_nodes2 = split_nodes_delimiter(nodes2, "_", TextType.ITALIC)
        self.assertEqual(test_nodes2, new_nodes2)
        nodes3 = [TextNode("This is text with a ```code``` in the middle", TextType.TEXT)]
        test_nodes3 = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" in the middle", TextType.TEXT)
        ]
        new_nodes3 = split_nodes_delimiter(nodes3, "`", TextType.CODE)
        self.assertEqual(test_nodes3, new_nodes3)
        nodes4 = [TextNode("This is text with a **bolded phrase** an _italic phrase_ and some `code`", TextType.TEXT)]
        test_nodes4 = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" an ", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" and some ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ]
        new_nodes4 = split_nodes_delimiter(nodes4, "**", TextType.BOLD)
        new_nodes4 = split_nodes_delimiter(new_nodes4, "_", TextType.ITALIC)
        new_nodes4 = split_nodes_delimiter(new_nodes4, "`", TextType.CODE)
        self.assertEqual(test_nodes4, new_nodes4)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        matches2 = extract_markdown_images(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        matches3 = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertEqual(matches2, [])
        matches3 = extract_markdown_links(
            "This is text with a link [](https://www.boot.dev) and [to youtube]()"
        )
        self.assertEqual(matches3, [('', 'https://www.boot.dev'), ('to youtube', '')])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode(
                    "link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_to_textnodes(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertEqual(nodes, 
                         [
                            TextNode("This is ", TextType.TEXT),
                            TextNode("text", TextType.BOLD),
                            TextNode(" with an ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word and a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" and an ", TextType.TEXT),
                            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", TextType.TEXT),
                            TextNode("link", TextType.LINK, "https://boot.dev"),
                        ])
        
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    
    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

if __name__ == "__main__":
    unittest.main()