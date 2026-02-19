from enum import Enum
from textnode import TextType, TextNode
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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
            return BlockType.UNORDERED_LIST
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
            return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH