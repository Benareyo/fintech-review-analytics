import os
import unittest

class TestFintechPipeline(unittest.TestCase):
    def test_raw_data_exists(self):
        """Verify that Task 1 data collection output file is preserved"""
        self.assertTrue(os.path.exists("data/raw/raw_scraped_reviews.csv"))

    def test_analyzed_data_exists(self):
        """Verify that Task 2 deep learning sentiment pipeline generated outputs"""
        # If your file is named slightly differently, adjust the string name below
        self.assertTrue(os.path.exists("data/raw/analyzed_reviews.csv"))

if __name__ == '__main__':
    unittest.main()