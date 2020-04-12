import scrapy
import re


class IngredientCrawler(scrapy.Spider):
    name = "ingredient_crawler"
    html_clean_re = re.compile('<.*?>')

    def start_requests(self):
        for x in range(0, 20):
            url = 'https://incidecoder.com/ingredients/all?offset=' + str(x)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        ingredient_name = response.css("div.detailpage div.ingredinfobox h1.klavikab::text").get()
        what_it_does = response.css("div.detailpage div.ingredinfobox div.itemprop span.value a::text").get(),
        all_functions = response.css("div.detailpage div.std-side-padding div.fs16 div::text").get(),
        cas_ec = response.css("div.detailpage div.std-side-padding div.fs16 div:nth-child(2)::text").getall(),
        content = response.css("div#details div#showmore-section-details div.content p").getall(),

        if ingredient_name is not None:
            yield {
                'ingredient_name': ingredient_name.strip(),
                'what_it_does': self.get_str(what_it_does),
                'all_functions': self.get_str(all_functions),
                'cas_ec': self.get_str(cas_ec),
                'content': self.clean_html(self.get_str(content)),
                'url': response.url
            }

        for href in response.css('div.detailpage div.bggrey a.klavika::attr(href)'):
            if href is not None:
                yield response.follow(href, callback=self.parse)

    def clean_html(self, raw_html):
        return re.sub(self.html_clean_re, '', raw_html)

    def clean_long_ws(self, msg):
        return re.sub(r"\s{2,}", " ", msg, flags=re.UNICODE)

    def get_str(self, msg, default=''):
        if type(msg) is tuple and type(msg[0]) is str:
            return self.clean_long_ws(msg[0].strip()) if msg[0] is not None else default
        if type(msg) is tuple and type(msg[0]) is list:
            return self.clean_long_ws(''.join(msg[0]).replace('\n', '').strip())
        if type(msg) is str:
            return self.clean_long_ws(msg.strip())
        if msg is None:
            return default
        if type(msg) is tuple and msg[0] is None:
            return default
        return 'type is different'
