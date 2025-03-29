from textnode import TextNode, TextType

test = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
test2 = TextNode("This is some anchor text", TextType.CODE, "https://www.boot.dev")
test3 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

print(test)
print(test == test2)
print(test == test3)