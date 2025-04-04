from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        html_string = ""
        for prop in self.props:
            html_string = html_string + f' {prop}="{self.props[prop]}"'
        return html_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode must have a value.")
        if self.tag == None:
            return self.value
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()} />" 
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag.")
        if self.children == None:
            raise ValueError("ParentNode must have children")
        html_out = ""
        for child in self.children:
            html_out += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{html_out}</{self.tag}>"
