import scrapy
from scrapy.item import Item

import matplotlib
import matplotlib.pyplot as plt

def draw(kwargs):
    labels = []
    sizes = []
    for key in kwargs.keys():
        labels.append(key)
        sizes.append(int(kwargs[key]))    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()


class MyItem(Item):
    def __setitem__(self, key, val):
        self._values[key] = val

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    result = MyItem()

    def start_requests(self):
        urls = [
            'https://s.weibo.com/top/summary'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        maps = response.css(".data table tbody tr td")
        for i in range(50):
            key = maps.css(".td-01::text")[i].get()
            val = maps.css(".td-02 span::text")[i].get()
            self.result[key] = val
            print(self.result[key])
    def close(self, reason):
        draw(self.result)
        
    
