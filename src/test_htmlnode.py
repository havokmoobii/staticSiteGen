import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p")
        node2 = HTMLNode("p", "This is some text")
        node3 = HTMLNode("a", "This is a link", None, {"href": "https://www.google.com", "target": "_blank"})
        print(node)
        print(node2)
        print(node3)
    
if __name__ == "__main__":
    unittest.main()