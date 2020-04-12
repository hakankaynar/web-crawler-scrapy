import unittest
from scrapy.http import HtmlResponse, Request
from ingredient_crawler.ingredient_crawler.spiders.ingredient_crawler import IngredientCrawler


class IngredientCrawlerTest(unittest.TestCase):

    def test_start_requests(self):
        ingredient_crawler = IngredientCrawler()
        start_requests = ingredient_crawler.start_requests()

        for a_req in start_requests:
            self.assertRegex(a_req.url, r'https://incidecoder.com/ingredients/all\?offset\=[0-9]{1,}')
            self.assertEqual(a_req.method, 'GET')

    def test_parse_link(self):
        ingredient_crawler = IngredientCrawler()
        links = ingredient_crawler.parse(
            IngredientCrawlerTest.get_response('ingredient_crawler/ingredient_crawler/test/ing_link.html'))

        for a_req in links:
            self.assertEqual(a_req.url, "http://example.com/expected")

    def test_parse_content_1(self):
        ingredient_crawler = IngredientCrawler()
        contents = ingredient_crawler.parse(
            IngredientCrawlerTest.get_response('ingredient_crawler/ingredient_crawler/test/ing_content_1.html'))

        for a_content in contents:
            self.assertEqual(a_content['ingredient_name'], "some-name")
            self.assertEqual(a_content['what_it_does'], "some-what-it-does")
            self.assertEqual(a_content['all_functions'], "some-all-functions")
            self.assertEqual(a_content['cas_ec'], 'some-cas-ec')
            self.assertEqual(a_content['content'], "some-content")
            self.assertEqual(a_content['url'], "http://example.com")

    def test_parse_content_2(self):
        ingredient_crawler = IngredientCrawler()
        contents = ingredient_crawler.parse(
            IngredientCrawlerTest.get_response('ingredient_crawler/ingredient_crawler/test/ing_content_2.html'))

        for a_content in contents:
            self.assertEqual(a_content['ingredient_name'], "some-name")
            self.assertEqual(a_content['what_it_does'], "some-what-it-does")
            self.assertEqual(a_content['all_functions'], "")
            self.assertEqual(a_content['cas_ec'], "")
            self.assertEqual(a_content['content'], "some-content strong bold")
            self.assertEqual(a_content['url'], "http://example.com")

    @staticmethod
    def get_response(file):
        req = Request('http://example.com', encoding='utf-8')
        header = {'content-type': 'text/html; charset=utf-8'}
        body = IngredientCrawlerTest.read_file(file)
        return HtmlResponse(url='http://example.com', status=200,
                            headers=header,
                            body=body, request=req, encoding='utf-8')

    @staticmethod
    def read_file(file):
        with open(file, "r") as in_file:
            return in_file.read()
