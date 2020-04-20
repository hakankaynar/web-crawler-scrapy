import re
import json
import logging
import scrapy


class DouglasProductCrawler(scrapy.Spider):
    name = "doug_crawler"

    def start_requests(self):
        url = 'https://www.douglas.de/13-sitemap.xml'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield from response.follow_all(xpath='//url/loc/text()', callback=DouglasProductCrawler.parse_product)

    @staticmethod
    def parse_product(response):
        full_js_statement = response.css('script::text').re_first(r'document\.productData.*;')
        if full_js_statement is not None:
            match = re.match(r'document\.productData\s*\=\s*(.*);', full_js_statement, re.M | re.I)
            if match is not None:
                product_data = json.loads(match.group(1))
                name, brand, price, currency, size, \
                stock, details, application, ingredients, brand_img, \
                thumbnail, preview = DouglasProductCrawler.get_product_values(product_data)

                yield {
                    'name': name,
                    'brand': brand,
                    'price': price,
                    'currency': currency,
                    'size': size,
                    'stock': stock,
                    'details': details,
                    'application': application,
                    'ingredients': ingredients,
                    'brand_img': brand_img,
                    'thumbnail': thumbnail,
                    'preview': preview,
                    'url': response.url
                }
            else:
                logging.warning("Did not match, url: " + response.url)
        else:
            logging.warning("javascript statement cannot be found. url: " + response.url)

    @staticmethod
    def get_product_values(product_data):
        name = product_data['productname']
        brand = product_data['brand']['name']
        brand_img = product_data['brand']['image']['src']
        price = product_data['variants']['items'][0]['trackingStandardProductParameter']['productCost']
        currency = product_data['variants']['items'][0]['trackingStandardProductParameter']['currency']
        size = product_data['variants']['items'][0]['size']
        stock = product_data['variants']['items'][0]['stockState']
        thumbnail = product_data['variants']['items'][0]['images'][0]['thumbnail']['src']
        preview = product_data['variants']['items'][0]['images'][0]['preview']['src']
        ingredients = ''

        for a_content in product_data['accordionContent']:
            if a_content['title'] == 'Produktdetails':
                details = DouglasProductCrawler.clean_html(a_content['content'])
            if a_content['title'] == 'Anwendung':
                application = DouglasProductCrawler.clean_html(a_content['content'])
            if a_content['title'] == 'Inhaltsstoffe' or a_content['name'] == 'ingredients':
                if a_content['content'] is not None:
                    ingredients = a_content['content'].split(', ')

        return name, brand, price, currency, size, stock, details, application, ingredients, brand_img, thumbnail, preview

    @staticmethod
    def clean_html(raw_html):
        if raw_html is not None:
            html_clean_re = re.compile('<.*?>')
            return re.sub(html_clean_re, '', raw_html)
