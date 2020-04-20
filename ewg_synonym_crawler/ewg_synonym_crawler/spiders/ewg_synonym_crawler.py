import re
import scrapy
from scrapy.selector import Selector


class EwgSynonymCrawler(scrapy.Spider):
    name = "ewg_synonym_crawler"

    def start_requests(self):
        """
        The crawling starts from ewg.org's search page.
        Example: https://www.ewg.org/skindeep/search/?per_page=36&page=1
        :return: request generator for scraping ewg.org search page.
        """
        for page_num in range(1, 167):
            url = 'https://www.ewg.org/skindeep/search/?per_page=36&page=' + str(page_num)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        Scrapes a search page in order to find product links
        :param response: http response from ewg search page.
        :return: request generator for product pages
        """
        product_links = response.css('section.product-listings div.product-tile a')
        yield from response.follow_all(product_links, callback=EwgSynonymCrawler.parse_product)

    @staticmethod
    def parse_product(response):
        """
        Scrapes a product page in order to find ingredient links
        :param response: http response from ewg product page.
        :return: request generator for ingredient pages
        """
        ingredient_links = response.css('table.table-ingredient-concerns tr a')
        yield from response.follow_all(ingredient_links, callback=EwgSynonymCrawler.parse_ingredient)

    @staticmethod
    def parse_ingredient(response):
        """
        Scrapes an ingredient page.
        :param response: http response from ewg ingredient page.
        :return: returns json object including name, function and other properties of an ingredient.
        """
        yield {
            'name': response.css('h2.chemical-name::text').get(),
            'function': response.css('.see-all-chemical li p.chemical-functions-text::text').get(),
            'about': response.css('.see-all-chemical li p.chemical-about-text::text').get(),
            'score': EwgSynonymCrawler.__get_score(response.css("#chemical .chemical-score img::attr(src)").get()),
            'data_rating': response.css("#chemical .chemical-score span::text").get(),
            'synonyms': response.css('.see-all-chemical li p.chemical-synonyms-text::text').get(),
            'url': response.url,
            'concerns': EwgSynonymCrawler.__get_concerns(response.css('.gauges .thebigimage').getall()),
            'other_concerns': response.css('.see-all-chemical li p.chemical-concerns-text::text').get()
        }

    @staticmethod
    def __get_concerns(concerns):
        concerns_json = []
        if concerns is not None:
            for a_concern in concerns:
                concern_selector = Selector(text=a_concern)
                concern_name = concern_selector.css('h2::text').get()
                if concern_name is not None:
                    concern_level = 'unknown'
                    if concern_selector.css('div.orient_low') is not None:
                        concern_level = 'low'
                    elif concern_selector.css('div.orient_high') is not None:
                        concern_level = 'high'
                    a_concern_json = {
                        'name': concern_name,
                        'rating': concern_level
                    }
                    concerns_json.append(a_concern_json)

        return concerns_json

    @staticmethod
    def __get_score(src):
        match = re.match(r'(/skindeep.*\?)(score\=)(\d+)(&score_min=)(\d+)', src, re.M | re.I)
        if match is not None:
            return {
                "normal": match.group(3),
                "min": match.group(5)
            }

        return {
            "normal": "0",
            "min": "0"
        }
