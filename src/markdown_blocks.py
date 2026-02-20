from enum import Enum
from textnode import TextType, TextNode, text_node_to_html_node
from inline_markdown import text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block):
    for i in range(1, 7):
        if block.startswith("#" * i + " "):
            return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith("> "):
        lines = block.split("\n")
        is_valid = True
        for line in lines:
            if not line.startswith(">"):
                is_valid = False
                break  # no need to keep checking
        if is_valid:
            return BlockType.QUOTE
    elif block.startswith("- "):
        lines = block.split("\n")
        is_valid = True
        for line in lines:
            if not line.startswith("- "):
                is_valid = False
                break  # no need to keep checking
        if is_valid:
            return BlockType.ULIST
    elif block.startswith("1. "):
        lines = block.split("\n")
        is_valid = True
        num = 1
        for line in lines:
            if not line.startswith(f"{num}. "):
                is_valid = False
                break  # no need to keep checking
            num += 1
        if is_valid:
            return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH
    
def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    blocks = []
    for line in lines:
        if line.strip() == "":
            continue
        blocks.append(line.strip())
    return blocks
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    HTML_blocks = []
    for block in blocks:
        #convert block to html node here based on block type
        html_node = block_to_html_node(block)
        HTML_blocks.append(html_node)
    return ParentNode(tag="div", children=HTML_blocks)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    elif block_type == BlockType.OLIST:
        return olist_to_html_node(block)

def paragraph_to_html_node(block):
    cleaned_block = block.replace("\n", " ")
    children = text_to_children(cleaned_block)
    return ParentNode(tag="p", children=children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level+1:]
    children = text_to_children(text)
    return ParentNode(tag=f"h{level}", children=children)

def code_to_html_node(block):
    code_text = block[3:-3].strip()
    raw_text = TextNode(code_text, TextType.TEXT)
    child = text_node_to_html_node(raw_text)
    code_node = ParentNode("code", [child])
    return ParentNode(tag="pre", children=[code_node])

def quote_to_html_node(block):
    lines = block.split("\n")
    stripped_lines = ""
    for line in lines:
        line = line[1:].strip()
        stripped_lines += line + " "
    children = text_to_children(stripped_lines.strip())
    return ParentNode(tag="blockquote", children=children)

def ulist_to_html_node(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        line = line.lstrip("- ").strip()
        children = text_to_children(line)
        html_items.append(ParentNode("li", children))
    return ParentNode(tag="ul", children=html_items)

def olist_to_html_node(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        number, text = line.split(". ", 1)
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode(tag="ol", children=html_items)

