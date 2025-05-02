import unittest

from markdown_to_html import BlockType, markdown_to_blocks, block_to_block_type

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





if __name__ == "__main__":
    unittest.main()