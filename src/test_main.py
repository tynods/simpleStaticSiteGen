import unittest

from textnode import *
from htmlnode import *
from main import *


class TestMain(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_extract_title1(self):
        title = extract_title("# title")
        self.assertEqual(title, "title")

    def test_extract_title2(self):
        title = extract_title("\n\n#  Long title \nblabla\n\n## sub title")
        self.assertEqual(title, "Long title")
