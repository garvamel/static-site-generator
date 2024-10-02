from block_markdown import markdown_to_blocks, block_to_blocktype, BlockType
from md_to_html_children import clean_heading
from markdown_to_html import markdown_to_html_node
import os, shutil

def extract_title(markdown):
    
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_blocktype(block) == BlockType.heading:
            text, heading_level = clean_heading(block)
            if heading_level == 1:
                return text
    else:
        raise Exception("No h1 header present")
    
def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    print(from_path)
    print(template_path)
    print(dest_path)


    md_file = open(from_path) 
    markdown = md_file.read()
    md_file.close()

    tmplt_file = open(template_path)
    template = tmplt_file.read()
    tmplt_file.close()

    md_nodes = markdown_to_html_node(markdown)
    md_nodes_as_html = md_nodes.to_html()

    web_title = extract_title(markdown)

    template = template.replace('{{ Title }}', web_title)
    website = template.replace('{{ Content }}', md_nodes_as_html)

    index_file = open(os.path.join(dest_path, 'index.html'), "w+")
    index_file.write(website)
    index_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    ld = []
    if os.path.exists(dir_path_content):
        ld = os.listdir(dir_path_content)

    if (item := ".DS_Store") in ld:
        ld.remove(item)


    if os.path.exists(dest_dir_path):
        pass
    else:
        os.mkdir(dest_dir_path)

    for item in ld:
        s = os.path.join(dir_path_content, item)
        if os.path.isdir(s):
            dest_dir_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(s):
            generate_page(s, template_path, dest_dir_path)
        else:
            generate_pages_recursive(s, template_path, dest_dir_path)