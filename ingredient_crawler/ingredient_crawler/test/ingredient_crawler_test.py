import unittest
from ingredient_crawler.ingredient_crawler.spiders.ingredient_crawler import IngredientCrawler


class IngredientCrawlerTest(unittest.TestCase):

    def test_start_requests(self):
        ingredient_crawler = IngredientCrawler()
        start_requests = ingredient_crawler.start_requests()

        for a_req in start_requests:
            self.assertRegex(a_req.url, r'https://incidecoder.com/ingredients/all\?offset\=[0-9]{1,}')
            self.assertEqual(a_req.method, 'GET')
