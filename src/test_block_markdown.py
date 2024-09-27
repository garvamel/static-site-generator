import unittest

from block_markdown import (markdown_to_blocks,
                            block_to_blocktype,
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
        
class TestBlockToBlockType(unittest.TestCase):

    def test_heading_case(self):

        heading1 = "# This is a heading"
        heading2 = "## This is a heading"
        heading3 = "### This is a heading"
        heading4 = "#### This is a heading"
        heading5 = "##### This is a heading"
        heading6 = "###### This is a heading"
        heading7 = "####### This is a heading"

        self.assertEqual(block_to_blocktype(heading1), "heading")
        self.assertEqual(block_to_blocktype(heading2), "heading")
        self.assertEqual(block_to_blocktype(heading3), "heading")
        self.assertEqual(block_to_blocktype(heading4), "heading")
        self.assertEqual(block_to_blocktype(heading5), "heading")
        self.assertEqual(block_to_blocktype(heading6), "heading")
        self.assertEqual(block_to_blocktype(heading7), "paragraph")

    def test_code_case(self):

        code1 = "```This is a code block```"
        code2 = "```\nThis\nis\nalso\na\ncode\nblock\n```"
        code3 = "``This is not a code block``"
        code4 = "`This is also not a code block`"
        code5 = "```This is absolutely not a code block"


        self.assertEqual(block_to_blocktype(code1), "code")
        self.assertEqual(block_to_blocktype(code2), "code")
        self.assertEqual(block_to_blocktype(code3), "paragraph")
        self.assertEqual(block_to_blocktype(code4), "paragraph")
        self.assertEqual(block_to_blocktype(code5), "paragraph")
