import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "hola loco")
        node2 = HTMLNode("h1", "hola loco")
        self.assertEqual(node, node2)

    def test_rep(self):
        
        node = HTMLNode(tag="p", value="Test text", props={"href": "http:///www.thisisafakeurl.com", 
                                                           "target": "_blank",
                                                           })
        self.assertEqual(node.__repr__, 
                        "HTML Node data\ntag: p\nvalue: hola loco\nchildren:  None\nprops: None\n")

    def test_to_html(self):
        node = HTMLNode(tag="p", value="Test text", props={
                                                                    "href": "http:///www.thisisafakeurl.com", 
                                                                    "target": "_blank",
                                                                   })
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode(tag="p", value="Test text", props={
                                                                    "href": "http:///www.thisisafakeurl.com", 
                                                                    "target": "_blank",
                                                                   })
                
        node2 = HTMLNode(tag="h", value="Test text2", props={
                                                                    "href": "http:///www.holahello.com", 
                                                                    "target": "me",
                                                                   })
        print(node.props_to_html())

    def test_children(self):
        node = LeafNode(tag="p", value="Test text", props={
                                                                    "href": "http:///www.thisisafakeurl.com", 
                                                                    "target": "_blank",
                                                                   })
        with self.assertRaises(AttributeError):
            self.assertIn(node.children,[None, 0])
        

if __name__ == "__main__":
    unittest.main()
