import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_valid_markdown(self):
        markdown = "# My Title\n\nSome content here."
        self.assertEqual(extract_title(markdown), "My Title")

    def test_extract_title_no_h1_header(self):
        markdown = "No title here.\nJust some content."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "no h1 header found")

    def test_extract_title_multiple_h1_headers(self):
        markdown = "# First Title\n\n# Second Title\n\nContent here."
        self.assertEqual(extract_title(markdown), "First Title")

    def test_does_not_accept_h2(self):
        markdown = "## Not the title\n\n# Real Title"
        self.assertEqual(extract_title(markdown), "Real Title")