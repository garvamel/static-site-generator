from typing import Iterator
import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: str) -> list[TextNode]:
    
    new_nodes = list()

    for old_node in old_nodes:
        if old_node.text_type != TextType.text:
            new_nodes.append(old_node)
            continue
        else:
            split_text = old_node.text.split(delimiter)
            if len(split_text) == 1:
                new_nodes.append(old_node)
                continue
            if len(split_text) == 2:
                raise ValueError(f"Invalid markdown syntax: {delimiter} missing closing character")
            for i,text in enumerate(split_text):
                if text == '':
                    continue
                elif i%2 == 0:
                    new_nodes.append(TextNode(text, TextType.text))
                else:
                    new_nodes.append(TextNode(text, text_type))
    
    return new_nodes

def extract_markdown_images(text: str) -> Iterator[re.Match]:
    pattern = r"!\[([^\[\]]*?)\]\(([^\(\)]*?)\)"

    matches = re.finditer(pattern, text)
    return matches

def extract_markdown_links(text: str) -> Iterator[re.Match]:
    pattern = r"(?<!!)\[([^\[\]]*?)\]\(([^\(\)]*?)\)"

    matches = re.finditer(pattern, text)
    return matches

def split_nodes_images(old_nodes: list) -> list[TextNode]:
    new_nodes = list()
    for old_node in old_nodes:
        if old_node.text_type != TextType.text:
            new_nodes.append(old_node)
            continue
        else:
            matches = extract_markdown_images(old_node.text)            
            start = 0
            end = 0
            match = False

            for match in matches:
                match_start = match.start()
                match_end = match.end()
                if start < match_start:
                    new_nodes.append(TextNode(old_node.text[start:match_start], TextType.text))

                    new_nodes.append(TextNode(match.group(1), TextType.image, match.group(2)))
                    start = match_end
                    end = match_end

                elif start == match_start:
                    new_nodes.append(TextNode(match.group(1), TextType.image, match.group(2)))
                    start = match_end
                    end = match_end
            if not match:
                new_nodes.append(old_node)
                continue            
            #     raise ValueError(f"No markdown images found")

            # if end == 0:
            #     new_nodes.append(old_node)
            #     continue

            if len(old_node.text) != end:
                new_nodes.append(TextNode(old_node.text[end:], TextType.text))

    return new_nodes

def split_nodes_links(old_nodes: list) -> list:

    new_nodes = list()
    for old_node in old_nodes:
        if old_node.text_type != TextType.text:
            new_nodes.append(old_node)
            continue
        else:
            matches = extract_markdown_links(old_node.text)              
            start = 0
            end = 0
            match = False

            for match in matches:
                match_start = match.start()
                match_end = match.end()
                if start < match_start:
                    new_nodes.append(TextNode(old_node.text[start:match_start], TextType.text))

                    new_nodes.append(TextNode(match.group(1), TextType.link, match.group(2)))
                    start = match_end
                    end = match_end

                elif start == match_start:
                    new_nodes.append(TextNode(match.group(1), TextType.link, match.group(2)))
                    start = match_end
                    end = match_end
            if not match:
                new_nodes.append(old_node)
                continue
                # raise ValueError(f"No markdown links found")
            
            # if end == 0:
            #     new_nodes.append(old_node)
            #     continue
            
            if len(old_node.text) != end:
                new_nodes.append(TextNode(old_node.text[end:], TextType.text))

    return new_nodes

def text_to_textnode(text: str) -> list[TextNode]:

    input_nodes = [TextNode(text, TextType.text)]
    input_nodes = split_nodes_delimiter(input_nodes, '**', TextType.bold)
    input_nodes = split_nodes_delimiter(input_nodes, '*', TextType.italic)
    input_nodes = split_nodes_delimiter(input_nodes, '`', TextType.code)
    input_nodes = split_nodes_images(input_nodes)
    input_nodes = split_nodes_links(input_nodes)

    return input_nodes
