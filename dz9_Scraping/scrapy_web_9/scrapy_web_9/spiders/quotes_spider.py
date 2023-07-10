import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        # Отримуємо дані про цитату
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall()
            }

        # Перехід на наступну сторінку
        next_page_url = response.css('li.next a::attr(href)').get()
        if next_page_url is not None:
            yield response.follow(next_page_url, self.parse)
