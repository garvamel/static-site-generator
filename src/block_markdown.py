from functools import reduce

def markdown_to_blocks(markdown: str) -> list[str]:
    
    if len(markdown) == 0 or type(markdown) != str:
        return []
    
    # md_blocks = map(lambda x: x.strip(),markdown.splitlines())
    md_blocks = map(str.strip, markdown.splitlines())
    md_blocks = reduce(lambda a, b: a + '\n' + b, md_blocks)
    md_blocks = md_blocks.split('\n\n') # split at empty line
    blocks = list(filter(lambda a: a != '', md_blocks))
    
    return blocks

