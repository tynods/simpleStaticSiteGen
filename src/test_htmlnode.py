import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_p1(self):
        p = HTMLNode(tag="p", value="test", props={"class":"c1"}).props_to_html()
        self.assertEqual(p, ' class="c1"')

    def test_p2(self):
        p = HTMLNode(tag="img", props={"src":"https://img.jpg"}).props_to_html()
        self.assertEqual(p, ' src="https://img.jpg"')

    def test_p3(self):
        p = HTMLNode(tag="a", props={"href":"https://example.com", "target":"_blank"}).props_to_html()
        self.assertEqual(p, ' href="https://example.com" target="_blank"')


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_3(self):
        b = LeafNode("b", "bold")
        t = LeafNode(None, "text ")
        p = ParentNode("p",[t,b], {"class": "c1"})
        self.assertEqual(
            p.to_html(),
            '<p class="c1">text <b>bold</b></p>'
        )

if __name__ == "__main__":
    unittest.main()
