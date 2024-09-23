import unittest

from textnode import (TextNode,
                      text_node_to_html_node,
                      split_nodes_delimiter,
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


class TestTextNodeToHtml(unittest.TestCase):
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


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_not_text_type(self):

        tnode = [TextNode("this is a **text**", TextType.bold),
                 TextNode("this is a _text_", TextType.italic)]
        new_nodes = split_nodes_delimiter(tnode, '', TextType.text)
        # No delimiter and TextType.text shouldn't fail since tnode is not TextType.text
        # It only tries to split TextType.text, other tyoes are not transformed.

        self.assertEqual(new_nodes[0].text_type, TextType.bold)
        self.assertEqual(new_nodes[1].text_type, TextType.italic)

    def test_no_matching_delimiter(self):
        tnode = [TextNode("this is a **text", TextType.text)]

        with self.assertRaises(ValueError) as cm:
            new_nodes = split_nodes_delimiter(tnode, '**', TextType.bold)
        self.assertEqual(cm.exception.args[0], f"Invalid markdown syntax: ** missing closing character")

    def test_expected_result(self):

        tnode = [TextNode("this is a **text**", TextType.bold),
                 TextNode("*this* is a text", TextType.italic),
                 TextNode("this *is* a text", TextType.text),
                TextNode("this is a `code`", TextType.code),

                 ]
        new_nodes = split_nodes_delimiter(tnode, '*', TextType.italic)
        # No delimiter and TextType.text shouldn't fail since tnode is not TextType.text
        # It only tries to split TextType.text, other tyoes are not transformed.

        self.assertEqual(new_nodes[0].text_type, TextType.bold)
        self.assertEqual(new_nodes[0].text, "this is a **text**")

        self.assertEqual(new_nodes[1].text_type, TextType.italic)
        self.assertEqual(new_nodes[1].text, "*this* is a text")

        self.assertEqual(new_nodes[2].text_type, TextType.text)
        self.assertEqual(new_nodes[2].text, "this ")
        
        self.assertEqual(new_nodes[3].text_type, TextType.italic)
        self.assertEqual(new_nodes[3].text, "is")
        
        self.assertEqual(new_nodes[4].text_type, TextType.text)
        self.assertEqual(new_nodes[4].text, " a text")
        
        self.assertEqual(new_nodes[5].text_type, TextType.code)
        self.assertEqual(new_nodes[5].text, "this is a `code`")

    def test_bold(self):

        tnode = [TextNode("this **is** a **text**", TextType.text)]
        new_nodes = split_nodes_delimiter(tnode, '**', TextType.bold)
        # No delimiter and TextType.text shouldn't fail since tnode is not TextType.text
        # It only tries to split TextType.text, other tyoes are not transformed.

        self.assertEqual(new_nodes[0].text_type, TextType.text)
        self.assertEqual(new_nodes[0].text, "this ")
        
        self.assertEqual(new_nodes[1].text_type, TextType.bold)
        self.assertEqual(new_nodes[1].text, "is")
        
        self.assertEqual(new_nodes[2].text_type, TextType.text)
        self.assertEqual(new_nodes[2].text, " a ")

        self.assertEqual(new_nodes[3].text_type, TextType.bold)
        self.assertEqual(new_nodes[3].text, "text")

        # self.assertEqual(new_nodes[0].text_type, TextType.text)
        # self.assertEqual(new_nodes[0].text, " a ")
        # self.assertEqual(new_nodes[1].text_type, TextType.bold)
        # self.assertEqual(new_nodes[1].text, "text")

    def test_italic(self):

        tnode = [TextNode("this *is* a text", TextType.text)]
        new_nodes = split_nodes_delimiter(tnode, '*', TextType.italic)
        # No delimiter and TextType.text shouldn't fail since tnode is not TextType.text
        # It only tries to split TextType.text, other tyoes are not transformed.

        self.assertEqual(new_nodes[0].text_type, TextType.text)
        self.assertEqual(new_nodes[0].text, "this ")
        
        self.assertEqual(new_nodes[1].text_type, TextType.italic)
        self.assertEqual(new_nodes[1].text, "is")
        
        self.assertEqual(new_nodes[2].text_type, TextType.text)
        self.assertEqual(new_nodes[2].text, " a text")

    def text_code(self):

        tnode = [TextNode("this `is` a text", TextType.text)]
        new_nodes = split_nodes_delimiter(tnode, '`', TextType.code)
        # No delimiter and TextType.text shouldn't fail since tnode is not TextType.text
        # It only tries to split TextType.text, other tyoes are not transformed.

        self.assertEqual(new_nodes[0].text_type, TextType.text)
        self.assertEqual(new_nodes[0].text, "this ")
        
        self.assertEqual(new_nodes[1].text_type, TextType.code)
        self.assertEqual(new_nodes[1].text, "is")
        
        self.assertEqual(new_nodes[2].text_type, TextType.text)
        self.assertEqual(new_nodes[2].text, " a text")

    def test_multiple_calls(self):

        tnode = [TextNode("this `is` a **text**", TextType.text)]
        new_nodes = split_nodes_delimiter(tnode, '`', TextType.code)

        self.assertListEqual(new_nodes, [ TextNode("this ", TextType.text),
                                         TextNode("is", TextType.code),
                                         TextNode(" a **text**", TextType.text)
                                         ])


        new_nodes2 = split_nodes_delimiter(new_nodes, '**', TextType.bold)

        self.assertListEqual(new_nodes2, [TextNode("this ", TextType.text),
                                         TextNode("is", TextType.code),
                                         TextNode(" a ", TextType.text),
                                         TextNode("text", TextType.bold)
                                         ])

if __name__ == "__main__":
    unittest.main()
