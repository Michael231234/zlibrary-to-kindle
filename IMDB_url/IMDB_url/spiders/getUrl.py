# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import re
from ..items import ImdbUrlItem
import time
import random


def get_movies(path):
    texts = []
    data = pd.read_csv(path)
    movies = data['movie']
    for i in movies:
        movie = re.sub(r'[\s,]', '%20', i)
        text = movie + '%20IMDB'
        data = re.sub(r"\'", '%27', text)
        m = re.sub(r'\&', '', data)
        texts.append(m)

    return texts


class GeturlSpider(scrapy.Spider):
    start = time.clock()
    name = 'getUrl'
    allowed_domains = ['baidu.com', 'bing.com']

    def start_requests(self):
        links = ['https://www.bing.com/search?q=']
        movies = get_movies('/Users/konglingtong/PycharmProjects/machine_learning/FP/data/box.csv')
        for i in range(len(movies)):
            url = links + movies[i]
            if (i % 100) == 0:
                time.sleep(5)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = []
        item = ImdbUrlItem()
        item['url'] = response.xpath('//*[@id="b_results"]/li[1]/h2/a/@href').extract()
        items.append(item)
        yield item

    stop = time.clock()
    print(stop - start)
