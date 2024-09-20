import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_inputs(self):
        node = HTMLNode("h1", "hola loco", None, {"href": "http:///www.thisisafakeurl.com", 
                                                           "target": "_blank"
                                                           })

        self.assertEqual(node.tag, "h1")        
        self.assertEqual(node.value, "hola loco")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "http:///www.thisisafakeurl.com", 
                                                           "target": "_blank"
                                                           })

    def test_eq(self):
        node = HTMLNode("h1", "hola loco")
        node2 = HTMLNode("h1", "hola loco")

        self.assertEqual(node, node2)

    def test_rep(self):
        
        node = HTMLNode(tag="p", value="Test text", props={"href": "http:///www.thisisafakeurl.com", 
                                                           "target": "_blank"
                                                           })
        
        self.assertEqual(node.__repr__(), "HTML Node data\ntag: p\nvalue: Test text\nchildren: None\nprops: {'href': 'http:///www.thisisafakeurl.com', 'target': '_blank'}\n")
    def test_to_html(self):
        node = HTMLNode(tag="p", value="Test text", props={"href": "http:///www.thisisafakeurl.com", 
                                                                    "target": "_blank"
                                                                   })
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode(tag="p", value="Test text", props={"href": "http:///www.thisisafakeurl.com", 
                                                                    "target": "_blank"
                                                                   })
    
        self.assertEqual(node.props_to_html(), ' href="http:///www.thisisafakeurl.com" target="_blank"')

    def test_leaf_to_html_no_children(self):
        node = LeafNode(tag="p", value="Test text", props={"href": "http:///www.thisisafakeurl.com", 
                                                                    "target": "_blank"
                                                                   })

        self.assertEqual(node.to_html(), '<p href="http:///www.thisisafakeurl.com" target="_blank">Test text</p>')
        
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, value="Test text", props={"href": "http:///www.thisisafakeurl.com", 
                                                                    "target": "_blank"
                                                                   })
        self.assertEqual(node.to_html(), "Test text")

    def test_parent_many_children_to_html(self):
        node = ParentNode("p",[LeafNode("b", "Bold text"),LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")],)

        self.assertEqual(node.to_html(),"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_child_parentnode(self):
        childnode = LeafNode("i", "italic text")
        panode = ParentNode("div", [childnode])
        grandpanode = ParentNode("p", [panode])
        
        self.assertEqual(grandpanode.to_html(), "<p><div><i>italic text</i></div></p>")

    def test_parent_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "Bold text")])
        
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        msg = cm.exception.args[0]
        self.assertEqual(msg, "No tag")

    def test_parent_no_children(self):
        node = ParentNode("span", None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        msg = cm.exception.args[0]
        self.assertEqual(msg, "No children")

if __name__ == "__main__":
    unittest.main()
