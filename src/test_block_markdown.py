import unittest

from block_markdown import (markdown_to_blocks,
                             )

class TestMarkdownToBlocks(unittest.TestCase):

    def test_normal_case(self):
        
        md_text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        blocks =  markdown_to_blocks(md_text)

        self.assertListEqual(blocks, ["# This is a heading",
                                      "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                                      """* This is the first list item in a list block
* This is a list item
* This is another list item"""])

    def test_empty_string(self):

        md_text = ''

        blocks = markdown_to_blocks(md_text)

        self.assertListEqual(blocks, [])


    def test_dirty_string(self):

        md_text = """   # This is a heading
       
    This is a paragraph of text. It has some **bold** and *italic* words inside of it.    
     
* This is the first list item in a list block
* This is a list item
* This is another list item     """


        blocks = markdown_to_blocks(md_text)

        self.assertListEqual(blocks, ["# This is a heading",
                                      "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                                      """* This is the first list item in a list block
* This is a list item
* This is another list item"""])