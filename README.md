The crawlers are implemented by using https://scrapy.org/ framework

### Prerequisites 
- `source venv3/bin/activate`
- `pip3 install -r requirements.txt`

#### First crawler (ingredient_crawler)
crawls ingredients from https://incidecoder.com/ 

##### Crawl ingredients with persistence
- `cd ingredient_crawler -o ingredient_crawler.json`
- `scrapy crawl ingredient_crawler -o ingredient_crawler.json -s JOBDIR=crawls/ingredient_crawler-1`

##### Testing ingredient crawler
`export PYTHONPATH=${PYTHONPATH}:/Users/hakankaynar/PycharmProjects/web-crawler-scrapy`

###### Only unittest
`python3 -m unittest discover './ingredient_crawler/ingredient_crawler/test' '*_test.py'`

###### Coverage
`python3 -m coverage run -m unittest discover './ingredient_crawler/ingredient_crawler/test' '*_test.py'`
`python3 -m coverage report --include **/ingredient_crawler/ingredient_crawler/spiders/ingredient_crawler.py`