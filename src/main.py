from copy_static import copy_static_to_public
from html_builder import generate_pages_recursive
import os

def main():
    source_dir = 'static'
    source_path = 'content'
    dest = 'public'
    template_file = 'template.html'
    copy_static_to_public(source_dir, dest)
    generate_pages_recursive(source_path, template_file, dest)

main()
