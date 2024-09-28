from functools import reduce
import re


def markdown_to_blocks(markdown: str) -> list[str]:
    
    if len(markdown) == 0 or type(markdown) != str:
        return []
    
    # md_blocks = map(lambda x: x.strip(),markdown.splitlines())
    md_blocks = map(str.strip, markdown.splitlines())
    md_blocks = reduce(lambda a, b: a + '\n' + b, md_blocks)
    md_blocks = md_blocks.split('\n\n') # split at empty line
    blocks = list(filter(lambda a: a != '', md_blocks))
    
    return blocks

def block_to_blocktype(block):

    '''
    block types:
        -paragraph: no symbol
        -heading: # (up to 6) followed by a space then the text
        -code: ```code block```
        -quote: > at the start of every line in the quote block
        -unordered_list: * or - at the start of every line, followed by a space
        -ordered_list: incremental number followed by a dot and space every line
    '''
    if type(block) != str:
        raise TypeError

    if len(block) == 0:
        raise ValueError("Empty block")
    
    test_funcs = [match_heading, match_code, match_quote, match_unordered_list, match_ordered_list]

    for func in test_funcs:
        if res := func(block):
            return res
    else:
        return "paragraph"

def match_heading(block):

    if re.findall(r"^#{1,6} ", block):
        return "heading"
    else:
        return False
    
def match_code(block):

    if block[0:3] =='```' and block[-3:] == '```':
        return "code"
    else:
        return False
    
def match_quote(block):

    for line in block.splitlines():
        if len(line) > 0 and line[0] =='>':
            continue
        else:
            return False    
    return "quote"

def match_unordered_list(block):

    lines = block.splitlines()
    ul_char = ''

    if m := re.findall(r"^([*-]) ", lines[0]):
        ul_char = m[0]
        for line in lines[1:]:
            m = re.findall(r"^([*-]) ", line)
            if m and m[0] == ul_char:
                continue
            else:
                return False
        return "unordered_list"
    else:
        return False

def match_ordered_list(block):
    index = 0
    
    for line in block.splitlines():
        match = re.findall(r"^(\d+)\. ", line)
        if len(match) > 0:
            if (n := int(match[0])) == index + 1:
                index = n
                continue
            else:
                return False
        else:
            return False
    else: 
        return "ordered_list" 
