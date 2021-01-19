#!/usr/bin/env python3
import unittest
from integrations import Integrations

class TestMarketplaceIntegrations(unittest.TestCase):
    def test_image_src_replaced_by_shortcode(self):
      ## assert that a search of the regex pattern doesn't return any results
      ## instead we should find a shortcode pattern somewhere in the generated markdown

      ## markdown_img_search_regex = r"!\[(.*?)\]\((.*?)\)"

      self.assertEqual('test'.upper(), 'TEST')

    def test_section_removed_from_markdown(self):
      header_string = '## Setup'
      test_markdown_string = ("This is a test markdown string\n\n"
        "## Setup\n\n"
        "1. This\n"
        "2. and this\n"
        "3. should be removed\n\n"
        "### This too\n\n"
        "## This should not be removed")

      result = Integrations.remove_section(test_markdown_string, header_string)
      self.assertNotIn(header_string, result)
      self.assertIn('## This should not be removed', result)


if __name__ == '__main__':
    unittest.main()
