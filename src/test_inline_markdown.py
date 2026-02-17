import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "Check out [Boot.dev](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)