import unittest

from markdown_to_html import BlockType, markdown_to_blocks, block_to_block_type, block_to_tag, markdown_to_html_node, extract_title

class TestMarkdownToBlocks(unittest.TestCase):
    def test_eq(self):
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

    def test_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("Test"))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("2. Test"))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("####### Test"))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("#Test"))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("``Test``"))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("-Test"))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("1.Test"))
        self.assertNotEqual(BlockType.PARAGRAPH, block_to_block_type("1. Test"))

    def test_heading(self):
        self.assertEqual(BlockType.HEADING, block_to_block_type("# Test"))
        self.assertEqual(BlockType.HEADING, block_to_block_type("## Test"))
        self.assertEqual(BlockType.HEADING, block_to_block_type("### Test"))
        self.assertEqual(BlockType.HEADING, block_to_block_type("#### Test"))
        self.assertEqual(BlockType.HEADING, block_to_block_type("##### Test"))
        self.assertEqual(BlockType.HEADING, block_to_block_type("###### Test"))
        self.assertNotEqual(BlockType.HEADING, block_to_block_type("####### Test"))

    def test_code(self):
        self.assertEqual(BlockType.CODE, block_to_block_type("```Test```"))
        self.assertEqual(BlockType.CODE, block_to_block_type("``` Test ```"))
        self.assertEqual(BlockType.CODE, block_to_block_type("`````````Test```````````````"))
        self.assertNotEqual(BlockType.CODE, block_to_block_type("```#### Test``"))

    def test_quote(self):
        self.assertEqual(BlockType.QUOTE, block_to_block_type(">Test\n>more test\n>even more test"))
        self.assertNotEqual(BlockType.QUOTE, block_to_block_type(">Test\nmore test\n>even more test"))

    def test_unordered(self):
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type("- Test\n- more test\n- even more test"))
        self.assertNotEqual(BlockType.UNORDERED_LIST, block_to_block_type("-Test\n-more test\n-even more test"))
        self.assertNotEqual(BlockType.UNORDERED_LIST, block_to_block_type("- Test\nmore test\n- even more test"))

    def test_ordered(self):
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type("1. Test\n2. more test\n3. even more test"))
        self.assertNotEqual(BlockType.ORDERED_LIST, block_to_block_type("2. Test\n3. more test\n4. even more test"))
        self.assertNotEqual(BlockType.ORDERED_LIST, block_to_block_type("1.Test\n2.more test\n3.even more test"))

class TestBlockToTag(unittest.TestCase):
    def test_tags(self):
        self.assertEqual(block_to_tag("Literally whatever", BlockType.PARAGRAPH), "p")
        self.assertEqual(block_to_tag("# Literally whatever", BlockType.HEADING), "h1")
        self.assertEqual(block_to_tag("## Literally whatever", BlockType.HEADING), "h2")
        self.assertEqual(block_to_tag("### Literally whatever", BlockType.HEADING), "h3")
        self.assertEqual(block_to_tag("#### Literally whatever", BlockType.HEADING), "h4")
        self.assertEqual(block_to_tag("##### Literally whatever", BlockType.HEADING), "h5")
        self.assertEqual(block_to_tag("###### Literally whatever", BlockType.HEADING), "h6")
        self.assertRaises(Exception, block_to_tag, "####### Literally whatever", BlockType.HEADING)
        self.assertEqual(block_to_tag("Literally whatever", BlockType.CODE), "pre")
        self.assertEqual(block_to_tag("Literally whatever", BlockType.QUOTE), "blockquote")
        self.assertEqual(block_to_tag("Literally whatever", BlockType.UNORDERED_LIST), "ul")
        self.assertEqual(block_to_tag("Literally whatever", BlockType.ORDERED_LIST), "ol")
        self.assertRaises(Exception, block_to_tag, "####### Literally whatever", "Not a BlockType")

class TestMarkdownToHtmlNode(unittest.TestCase):
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

    def test_heading(self):
        md = """

# _This is italic text with a heading._

## **This is bold text with a heading.**

### This is regular text with a heading.

"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><h1><i>This is italic text with a heading.</i></h1><h2><b>This is bold text with a heading.</b></h2><h3>This is regular text with a heading.</h3></div>",
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

    def test_quote(self):
        md = """

>_This is italic text with a heading._
>**This is bold text with a heading.**

### This is regular text with a heading.

"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><blockquote><i>This is italic text with a heading.</i>\n<b>This is bold text with a heading.</b></blockquote><h3>This is regular text with a heading.</h3></div>",
        )


    def test_unordered(self):
        md = """

- _This is italic text with a heading._
- **This is bold text with a heading.**

### This is regular text with a heading.

"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        #print(f"\n\n{html}\n\n")

        self.assertEqual(
            html,
            "<div><ul><li><i>This is italic text with a heading.</i></li>\n<li><b>This is bold text with a heading.</b></li></ul><h3>This is regular text with a heading.</h3></div>",
        )

    def test_ordered(self):
        md = """

1. _This is italic text with a heading._
2. **This is bold text with a heading.**

### This is regular text with a heading.

"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        #print(f"\n\n{html}\n\n")

        self.assertEqual(
            html,
            "<div><ol><li><i>This is italic text with a heading.</i></li>\n<li><b>This is bold text with a heading.</b></li></ol><h3>This is regular text with a heading.</h3></div>",
        )


class TestExtractTitle(unittest.TestCase):
    def test_valid(self):
        md = """

1. _This is italic text with a heading._
2. **This is bold text with a heading.**

# This is regular text with a heading.

"""
        title = extract_title(md)
        self.assertEqual(title, "This is regular text with a heading.")

    def test_missing(self):
        md = """

1. _This is italic text with a heading._
2. **This is bold text with a heading.**

This is regular text without a heading.

"""
        self.assertRaises(Exception, extract_title, md)

    def test_misplaced(self):
        md = """

1. _This is italic text with a heading._
2. **This is bold text with a heading.**

This # is regular text without a heading.

"""
        self.assertRaises(Exception, extract_title, md)

if __name__ == "__main__":
    unittest.main()