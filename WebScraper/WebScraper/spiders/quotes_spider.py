import scrapy
import numpy
import sklearn
import pandas

class Quotes_spider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            "http://quotes.toscrape.com/page/1/",
            "http://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()
            yield {
                'text': text,
                'author': author,
                'tags': tags
            }
        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
