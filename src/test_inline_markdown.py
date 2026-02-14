from node_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType
import unittest

def test_split_nodes_delimiter_code_single():
    old_nodes = [TextNode("This is `code` here", TextType.TEXT)]
    new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)

    assert [(n.text, n.text_type) for n in new_nodes] == [
        ("This is ", TextType.TEXT),
        ("code", TextType.CODE),
        (" here", TextType.TEXT),
    ]

def test_split_nodes_delimiter_unbalanced_raises():
    old_nodes = [TextNode("This is `code here", TextType.TEXT)]
    try:
        split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        assert False, "expected an exception for unbalanced delimiter"
    except Exception:
        assert True