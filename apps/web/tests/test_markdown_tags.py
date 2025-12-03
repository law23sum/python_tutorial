from django.template import Context, Template
from django.test import TestCase

from apps.web.templatetags.markdown_tags import render_markdown


class MarkdownTagsTests(TestCase):
    def test_basic_markdown(self):
        """Test that basic markdown syntax is rendered correctly."""
        text = "# Heading\n\nThis is **bold** and this is *italic*."
        result = render_markdown(text)

        self.assertIn("<h1>Heading</h1>", result)
        self.assertIn("This is <strong>bold</strong>", result)
        self.assertIn("this is <em>italic</em>", result)

    def test_code_blocks(self):
        """Test that fenced code blocks are rendered correctly."""
        text = "```python\ndef hello():\n    print('Hello world!')\n```"
        result = render_markdown(text)

        self.assertIn('<code class="language-python">', result)
        self.assertIn("def hello():", result)
        self.assertIn("print('Hello world!')", result)

    def test_sanitize_script_tags(self):
        """Test that script tags are sanitized."""
        text = "Normal text <script>alert('xss');</script> more text"
        result = render_markdown(text)

        self.assertNotIn("<script>", result)
        self.assertNotIn("alert('xss');", result)
        self.assertIn("Normal text", result)
        self.assertIn("more text", result)

    def test_sanitize_onclick_attributes(self):
        """Test that onclick attributes are sanitized."""
        text = "<a href='https://example.com' onclick='alert(\"xss\")'>Link</a>"
        result = render_markdown(text)

        self.assertIn("<a href=", result)
        self.assertIn("https://example.com", result)
        self.assertNotIn("onclick", result)
        self.assertIn("Link</a>", result)

    def test_allowed_html_tags(self):
        """Test that allowed HTML tags are preserved."""
        text = "<p>Paragraph</p><strong>Bold</strong><em>Italic</em>"
        result = render_markdown(text)

        self.assertIn("<p>Paragraph</p>", result)
        self.assertIn("<strong>Bold</strong>", result)
        self.assertIn("<em>Italic</em>", result)

    def test_image_tags(self):
        """Test that image tags are rendered correctly with allowed attributes."""
        text = '![Alt text](https://example.com/image.jpg "Image title")'
        result = render_markdown(text)

        self.assertIn("<img", result)
        self.assertIn('src="https://example.com/image.jpg"', result)
        self.assertIn('alt="Alt text"', result)
        self.assertIn('title="Image title"', result)

    def test_links_with_malicious_protocols(self):
        """Test that links with malicious protocols are sanitized."""
        text = "[Link](javascript:alert('xss'))"
        result = render_markdown(text)

        self.assertIn("<a", result)
        self.assertNotIn("javascript:", result)
        self.assertIn("Link</a>", result)

    def test_as_template_filter(self):
        """Test the filter when used in a Django template."""
        template = Template("{% load markdown_tags %}{{ content|render_markdown }}")
        context = Context({"content": "# Test Heading\n\nTest paragraph."})
        rendered = template.render(context)

        self.assertIn("<h1>Test Heading</h1>", rendered)
        self.assertIn("<p>Test paragraph.</p>", rendered)

    def test_nested_html_tags(self):
        """Test that nested HTML tags are handled correctly."""
        text = "<div><p>Nested <strong>content</strong></p></div>"
        result = render_markdown(text)

        self.assertIn("<div><p>Nested <strong>content</strong></p></div>", result)

    def test_link_with_title(self):
        """Test that links with allowed attributes are preserved."""
        text = '[Link](https://example.com "Title")'
        result = render_markdown(text)

        self.assertIn('<a href="https://example.com"', result)
        self.assertIn('title="Title"', result)
