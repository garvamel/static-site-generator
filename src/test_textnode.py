import unittest

from textnode import (TextNode,
                      text_node_to_html_node,
                      TextType,
                      )


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
        self.assertIsNone(node.url)

    def test_url(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold", "http:///www.thisisafakeurl.com")
        self.assertNotEqual(node.url, node2.url)

    def test_text(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is also a text node", "bold")
        self.assertNotEqual(node.text, node2.text)

    def test_text_type(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is also a text node", "bold")
        self.assertNotEqual(node.text_type, node2.text_type)


class TestTextNodToHtml(unittest.TestCase):
    def test_text(self):

        text_node = TextNode("This is a text node", "text")

        leaf_node = text_node_to_html_node(text_node)

        self.assertEqual(leaf_node.tag, None)
        self.assertEqual(leaf_node.value, "This is a text node")
    
    def test_bold(self):

        text_node = TextNode("This is a text node in bold", "bold")

        leaf_node = text_node_to_html_node(text_node)

        self.assertEqual(leaf_node.tag, "b")
        self.assertEqual(leaf_node.value, "This is a text node in bold")

    def test_italic(self):

        text_node = TextNode("This is a text node in italic", "italic")

        leaf_node = text_node_to_html_node(text_node)

        self.assertEqual(leaf_node.tag, "i")
        self.assertEqual(leaf_node.value, "This is a text node in italic")
       
    def test_code(self):

        text_node = TextNode("a = c + b", "code")

        leaf_node = text_node_to_html_node(text_node)

        self.assertEqual(leaf_node.tag, "code")
        self.assertEqual(leaf_node.value, text_node.text)
    
    def test_link(self):

        text_node = TextNode("Link Name", "link", "http:///www.thisisafakeurl.com")

        leaf_node = text_node_to_html_node(text_node)

        self.assertEqual(leaf_node.tag, "a")
        self.assertEqual(leaf_node.value, "Link Name")
        self.assertEqual(leaf_node.props, {"href": "http:///www.thisisafakeurl.com"})

    def test_image(self):
        text_node = TextNode("Img Name", "image", "http:///www.thisisafakeurl.com/image.jpg")

        leaf_node = text_node_to_html_node(text_node)

        self.assertEqual(leaf_node.tag, "img")
        self.assertEqual(leaf_node.value, None)
        self.assertEqual(leaf_node.props, {"src": "http:///www.thisisafakeurl.com/image.jpg","alt":"Img Name"})

    def test_error(self):
        
        text_node = TextNode("Text", "other")
    
        with self.assertRaises(Exception):
            leaf_node = text_node_to_html_node(text_node)

if __name__ == "__main__":
    unittest.main()
