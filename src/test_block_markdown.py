import unittest

from block_markdown import (markdown_to_blocks,
                            block_to_blocktype,
                            BlockType
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

    def test_type_error(self):

        block = 5
        block1 = 1.1
        block2 = None
        block3 = list()
        block4 = tuple()
        block5 = dict()
        
        with self.assertRaises(TypeError):
            block_to_blocktype(block)
            block_to_blocktype(block1)
            block_to_blocktype(block2)
            block_to_blocktype(block3)
            block_to_blocktype(block4)
            block_to_blocktype(block5)



    def test_empty_block(self):

        block = ""

        with self.assertRaises(ValueError) as cm:
            block_to_blocktype(block)
        
        self.assertEqual(cm.exception.args[0],"Empty block")

    def test_heading_case(self):

        heading1 = "# This is a heading"
        heading2 = "## This is a heading"
        heading3 = "### This is a heading"
        heading4 = "#### This is a heading"
        heading5 = "##### This is a heading"
        heading6 = "###### This is a heading"
        heading7 = "####### This is a heading"

        self.assertEqual(block_to_blocktype(heading1), BlockType.heading)
        self.assertEqual(block_to_blocktype(heading2), BlockType.heading)
        self.assertEqual(block_to_blocktype(heading3), BlockType.heading)
        self.assertEqual(block_to_blocktype(heading4), BlockType.heading)
        self.assertEqual(block_to_blocktype(heading5), BlockType.heading)
        self.assertEqual(block_to_blocktype(heading6), BlockType.heading)
        self.assertEqual(block_to_blocktype(heading7), BlockType.paragraph)

    def test_code_case(self):

        code1 = "```This is a code block```"
        code2 = "```\nThis\nis\nalso\na\ncode\nblock\n```"
        code3 = "``This is not a code block``"
        code4 = "`This is also not a code block`"
        code5 = "```This is absolutely not a code block"


        self.assertEqual(block_to_blocktype(code1), BlockType.code)
        self.assertEqual(block_to_blocktype(code2), BlockType.code)
        self.assertEqual(block_to_blocktype(code3), BlockType.paragraph)
        self.assertEqual(block_to_blocktype(code4), BlockType.paragraph)
        self.assertEqual(block_to_blocktype(code5), BlockType.paragraph)

    def test_quote_case(self):

        quote1 = """>Quote title
>newline
>quote content
>endline"""

        quote2 = """>Quote title
newline
>quote content
>endline"""

        quote3 = """>>Quote title

>>quote content
>>endline
"""

        self.assertEqual(block_to_blocktype(quote1), BlockType.quote)
        self.assertEqual(block_to_blocktype(quote2), BlockType.paragraph)
        self.assertEqual(block_to_blocktype(quote3), BlockType.paragraph)

    def test_ul_case(self):

        ul1 = """* Hola
* como
* te
* va"""

        ul2 = """- Hola
- como
- te
- va"""

        ul3 = """- Hola
- como
* te
* va"""

        ul4 = """- Hola
- como
- te
va"""

        self.assertEqual(block_to_blocktype(ul1), BlockType.unordered_list)
        self.assertEqual(block_to_blocktype(ul2), BlockType.unordered_list)
        self.assertEqual(block_to_blocktype(ul3), BlockType.paragraph)
        self.assertEqual(block_to_blocktype(ul4), BlockType.paragraph)

    def test_ol_case(self):

        ol1 = """1. Hola
2. como
3. te
4. va"""

        ol2 = """2. Hola
-3. como
-4. te
-5. va"""

        ol3 = """1. Hola
3. como
4. te
5. va"""

        ol4 = """ Hola
2. como
3. te
4. va"""

        self.assertEqual(block_to_blocktype(ol1), BlockType.ordered_list)
        self.assertEqual(block_to_blocktype(ol2), BlockType.paragraph)
        self.assertEqual(block_to_blocktype(ol3), BlockType.paragraph)
        self.assertEqual(block_to_blocktype(ol4), BlockType.paragraph)