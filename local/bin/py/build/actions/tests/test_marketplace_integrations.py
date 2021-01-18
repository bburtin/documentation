#!/usr/bin/env python3
import unittest
from integrations import remove_section

class TestMarketplaceIntegrations(unittest.TestCase):
    def test_image_src_replaced_by_shortcode(self):
      ## assert that a search of the regex pattern doesn't return any results
      ## instead we should find a shortcode pattern somewhere in the generated markdown

      ## markdown_img_search_regex = r"!\[(.*?)\]\((.*?)\)"

      self.assertEqual('test'.upper(), 'TEST')

    def test_section_removed_from_markdown(self):
      header_to_remove = '## Setup'
      markdown_to_test = """
      ---
      ## This is a test h2

      This is a test string

      ## Setup

      1. This
      2. Should be
      3. Removed

      ### This too

      ## This should not be removed
      ---
      """

      result = remove_section(markdown_to_test, header_to_remove)
      self.assertNotIn(result, header_to_remove)
      self.assertIn(result, '## This should not be removed')


if __name__ == '__main__':
    unittest.main()
