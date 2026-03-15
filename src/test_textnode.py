import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def text_repr(self):
        node = TextNode("Foo", TextType.LINK, "url")
        self.assertEqual(str(node), "TextNode(Foo, link, url)")

if __name__ == "__main__":
    unittest.main()
