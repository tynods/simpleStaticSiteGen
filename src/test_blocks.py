import unittest

from blocks import *

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_identify_block_type1(self):
            block = """## Heaging"""
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_identify_block_type2(self):
            block = """```
import os
os.exit()
```"""
            self.assertEqual(block_to_block_type(block), BlockType.CODE)
            
    def test_identify_block_type3(self):
            block = """> quote line1\n> line2"""
            self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_identify_block_type4(self):
            block = """- liist item 1\n- list item 2"""
            self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_identify_block_type5(self):
            block = """1. liist item 1\n2. list item 2\n3. item 3"""
            self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_identify_block_type6(self):
            block = """- liist item 1\n> list item 2\n3. item 3"""
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestBlocksToHTML(unittest.TestCase):
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

    def test_paragraph_with_image(self):
        md = """
This is **bolded** paragraph
text with an inline image ![alt text](https://img.jpg) inside
tag here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><p>This is <b>bolded</b> paragraph text with an inline image <img src="https://img.jpg" alt="alt text"></img> inside tag here</p></div>""",
        )