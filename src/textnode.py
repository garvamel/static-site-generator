from htmlnode import LeafNode

class TextType():
    text = "text"
    bold = "bold"
    italic = "italic"
    code = "code"
    link = "link"
    image = "image"

class TextNode():
    def __init__(self, text, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
        

def text_node_to_html_node(text_node: TextNode):
    node = None
    match text_node.text_type:
        case TextType.text:
            node = LeafNode(None, text_node.text)
        case TextType.bold:
            node = LeafNode("b", text_node.text)
        case TextType.italic:
            node = LeafNode("i", text_node.text)
        case TextType.code:
            node = LeafNode("code", text_node.text)
        case TextType.link:
            node = LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.image:
            node = LeafNode("img", "",{"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception
    return node
