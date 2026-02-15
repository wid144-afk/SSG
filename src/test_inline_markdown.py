import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter_code_single(self):
        old_nodes = [TextNode("This is `code` here", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(
            [(n.text, n.text_type) for n in new_nodes],
            [
                ("This is ", TextType.TEXT),
                ("code", TextType.CODE),
                (" here", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_unbalanced_raises(self):
        old_nodes = [TextNode("This is `code here", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, "`", TextType.CODE)

    def test_extract_markdown_images(self):
        text = "Hello ![cat](https://example.com/cat.png) world"
        self.assertEqual(
            extract_markdown_images(text),
            [("cat", "https://example.com/cat.png")],
        )

    def test_extract_markdown_links(self):
        text = "Go [home](https://example.com) now"
        self.assertEqual(
            extract_markdown_links(text),
            [("home", "https://example.com")],
        )

    def test_extract_markdown_links_does_not_match_images(self):
        text = "Img ![cat](https://example.com/cat.png) and [home](https://example.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("home", "https://example.com")],
        )