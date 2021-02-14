# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from kafka import KafkaProducer


class IngredientCrawlerPipeline(object):

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='kafka:9092')


    def process_item(self, item, spider):
        try:
            itemStr = json.dumps(item)
            self.producer.send('ingredient-topic', bytes(itemStr, 'utf-8') )
        except:
            print("Something went wrong")

        return item
