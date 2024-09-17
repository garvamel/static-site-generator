import unittest

from textnode import TextNode


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

if __name__ == "__main__":
    unittest.main()
