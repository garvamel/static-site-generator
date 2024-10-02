import re
from inline_markdown import text_to_textnode
from textnode import text_node_to_html_node
from block_markdown import BlockType
from htmlnode import LeafNode, ParentNode

def text_to_children(block, block_type):

    match block_type:
        case BlockType.paragraph:
            clean = clean_paragraph(block)
            children = text_to_htmlnode(clean)
            return children, None

        case BlockType.heading:
            clean, h_level = clean_heading(block)
            children = text_to_htmlnode(clean)
            return children, h_level
        
        case BlockType.code:
            clean = clean_code(block)
            children = text_to_htmlnode(clean)
            return children, None
        
        case BlockType.quote:
            clean = clean_quote(block)
            children = text_to_htmlnode(clean)
            return children, None
        
        case BlockType.unordered_list:
            clean = clean_unordered_list(block)
            children = text_to_html_list_item_node(clean)
            return children, None
            
        case BlockType.ordered_list:
            clean = clean_ordered_list(block)
            children = text_to_html_list_item_node(clean)
            return children, None
        case _:
            raise Exception("Wrong BlockType")
            

def text_to_htmlnode(text: list | str) -> list[LeafNode]:
    children = []
    obj_type = type(text)

    if obj_type == str:
        tnode = text_to_textnode(text) #type: ignore
        for node in tnode:
            children.append(text_node_to_html_node(node))
    elif obj_type == list:
        for t in text:
            tnode = text_to_textnode(t)
            for node in tnode:
                children.append(text_node_to_html_node(node))
    return children


def text_to_html_list_item_node(block_lines: list[str]) -> list:
    list_items = []
    for line in block_lines:
        children = []
        tnode = text_to_textnode(line)
        for node in tnode:
            children.append(text_node_to_html_node(node))
        list_items.append(ParentNode("li", children=children))

    return list_items

def clean_paragraph(block: str) -> str:
    return block

def clean_heading(block: str) -> tuple[str, int]:

    m = re.findall(r"^#{1,6} ", block)
    return block.replace(m[0], ''), len(m[0].strip())

def clean_code(block: str) -> str:
    # turns it into a single backquoted block so text_to_texnode catches it
    #```code``` -> `code`
    block = block[3:-3].strip()
    return '`' + block + '`'
    
def clean_quote(block: str) -> str:
    clean_block = []
    for line in block.splitlines():
        clean_block.append(line.replace('>', '').strip())
    return '\n'.join(clean_block)

def clean_unordered_list(block: str) -> list[str]:

    clean_block = []
    lines = block.splitlines()
    pattern = lines[0][:2]
    for line in lines:
        clean_block.append(line.lstrip(pattern))
    return clean_block

def clean_ordered_list(block: str) -> list[str]:

    clean_block = []

    for line in block.splitlines():
        match = re.findall(r"^\d+\. ", line)
        clean_block.append(line.replace(match[0], ''))
    return clean_block