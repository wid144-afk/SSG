from unittest import TestCase
from inline_markdown import (
    BlockType,
    block_to_block_type,
)

def test_block_to_blocktype(self):
    self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("## Subheading"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH)
    self.assertEqual(block_to_block_type("```\nCode block\n```"), BlockType.CODE)
    self.assertEqual(block_to_block_type("> This is a quote."), BlockType.QUOTE)