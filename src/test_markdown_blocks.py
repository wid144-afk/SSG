from unittest import TestCase
from markdown_blocks import (
    BlockType,
    block_to_block_type,
)
from markdown_blocks import markdown_to_html_node

def test_block_to_blocktype(self):
    self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("## Subheading"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH)
    self.assertEqual(block_to_block_type("```\nCode block\n```"), BlockType.CODE)
    self.assertEqual(block_to_block_type("> This is a quote."), BlockType.QUOTE)

def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

def test_ulist(self):
    md = """
A list of all my friends:

- Gandalf
- Frodo
- Sam
- Merry
- Pippin
- Aragorn
- Legolas
- Gimli
- Boromir
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>A list of all my friends:</p><ul><li>Gandalf</li><li>Frodo</li><li>Sam</li><li>Merry</li><li>Pippin</li><li>Aragorn</li><li>Legolas</li><li>Gimli</li><li>Boromir</li></ul></div>",
    )
