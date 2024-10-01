from block_markdown import (markdown_to_blocks,
                            block_to_blocktype,
                            BlockType
                            )
from htmlnode import ParentNode
from inline_markdown import text_to_textnode
from md_to_html_children import text_to_children

def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)
    HTMLnode_blocks = []
    for block in blocks:
        block_type = block_to_blocktype(block)        
        if block_type == BlockType.paragraph:
            children = text_to_children(block, block_type)
            HTMLnode_blocks.append(ParentNode("p", children=children[0]))

        if block_type == BlockType.heading:
            children = text_to_children(block, block_type)
            HTMLnode_blocks.append(ParentNode(f"h{children[1]}", children=children[0]))
            
        if block_type == BlockType.code:
            children = text_to_children(block, block_type)
            HTMLnode_blocks.append(ParentNode("pre",children=children[0]))
            
        if block_type == BlockType.quote:
            children = text_to_children(block, block_type)
            HTMLnode_blocks.append(ParentNode("blockquote", children=children[0]))
            
        if block_type == BlockType.unordered_list:
            children = text_to_children(block, block_type)
            HTMLnode_blocks.append(ParentNode("ul", children=children[0]))
            
        if block_type == BlockType.ordered_list:
            children = text_to_children(block, block_type)
            HTMLnode_blocks.append(ParentNode("ol", children=children[0]))

    return ParentNode("div", children=HTMLnode_blocks)

