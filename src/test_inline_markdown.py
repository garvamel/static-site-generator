import unittest

from textnode import (TextNode,
                      TextType,
                      )

from inline_markdown import (extract_markdown_links, 
                             extract_markdown_images, 
                             split_nodes_delimiter,
                             split_nodes_images,
                             split_nodes_links,
                             )

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

class TestExtractFuncs(unittest.TestCase):
    
    def test_images_multiple(self):

        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg). This is text with a link (treated as an image) ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)."
        
        matches = extract_markdown_images(text)
        matches = [match.groups() for match in matches]


        self.assertEqual(matches,[("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])


    def test_link_multiple(self):

        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev). This is text with an image (treated as a link) [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        matches = extract_markdown_links(text)
        matches = [match.groups() for match in matches]

        self.assertEqual(matches,[("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev"),("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])


    def test_link_error(self):

        #There's a space in between the [to boot dev] and (link url). Wrong syntaxt. Should only match the second link.

        text = "This is text with a link [to boot dev] (https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)."

        matches = extract_markdown_links(text)
        matches = [match.groups() for match in matches]

        self.assertEqual(matches,[("to youtube","https://www.youtube.com/@bootdotdev")])

class TestSplitNodeFuncs(unittest.TestCase):

    def test_no_matches_links_and_images(self):
        
        old_nodes = [TextNode("aa", TextType.text)]

        with self.assertRaises(ValueError) as cm:
            new_nodes = split_nodes_links(old_nodes)
        self.assertEqual(cm.exception.args[0], "No markdown links found")

        with self.assertRaises(ValueError) as cm:
            new_nodes = split_nodes_links(old_nodes)
        self.assertEqual(cm.exception.args[0], "No markdown links found")

    def test_split_node_link(self):
        old_nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and lalala",TextType.text)]
        
        new_nodes = split_nodes_links(old_nodes)
        self.assertListEqual(new_nodes,[
                                        TextNode("This is text with a link ", TextType.text),
                                        TextNode("to boot dev", TextType.link, "https://www.boot.dev"),
                                        TextNode(" and ", TextType.text),
                                        TextNode(
                                            "to youtube", TextType.link, "https://www.youtube.com/@bootdotdev"
                                        ),
                                        TextNode(" and lalala", TextType.text)
                                        ])

    def test_split_node_image(self):
        old_nodes = [TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and lalala",TextType.text)]
        
        new_nodes = split_nodes_images(old_nodes)
        self.assertListEqual(new_nodes,[
                                        TextNode("This is text with a ", TextType.text),
                                        TextNode("rick roll", TextType.image, "https://i.imgur.com/aKaOqIh.gif"),
                                        TextNode(" and ", TextType.text),
                                        TextNode(
                                            "obi wan", TextType.image, "https://i.imgur.com/fJRm4Vk.jpeg"
                                        ),
                                        TextNode(" and lalala", TextType.text)
                                        ])

    def test_split_node_link_single_match(self):
        old_nodes = [TextNode("[to boot dev](https://www.boot.dev)",TextType.text)]
        
        new_nodes = split_nodes_links(old_nodes)
        self.assertListEqual(new_nodes,[                                     TextNode("to boot dev", TextType.link, "https://www.boot.dev"),
                                        ])
        
    def test_split_node_image_single_match(self):
        old_nodes = [TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)",TextType.text)]
        
        new_nodes = split_nodes_images(old_nodes)
        self.assertListEqual(new_nodes,[                                      TextNode("rick roll", TextType.image, "https://i.imgur.com/aKaOqIh.gif")])

    def test_split_node_link_multi_match_no_text(self):
        old_nodes = [TextNode("[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",TextType.text)]
        
        new_nodes = split_nodes_links(old_nodes)
        self.assertListEqual(new_nodes,[
            TextNode("to boot dev", TextType.link,"https://www.boot.dev"), TextNode("to youtube", TextType.link, "https://www.youtube.com/@bootdotdev")
                                        ])
        
    def test_split_node_image_multi_match_not_text(self):
        old_nodes = [TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",TextType.text)]
        
        new_nodes = split_nodes_images(old_nodes)
        self.assertListEqual(new_nodes,[
            TextNode("rick roll", TextType.image, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode("obi wan", TextType.image, "https://i.imgur.com/fJRm4Vk.jpeg")
            ])

if __name__ == "__main__":
    unittest.main()
