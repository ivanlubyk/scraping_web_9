import scrapy


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        # Отримуємо дані про автора
        for author in response.css('div.quote small.author'):
            author_name = author.css('::text').get()
            author_link = author.xpath('../@href').get()
            if author_link:
                yield response.follow(author_link, self.parse_author, meta={'author_name': author_name})

        # Перехід на наступну сторінку
        next_page_url = response.css('li.next a::attr(href)').get()
        if next_page_url is not None:
            yield response.follow(next_page_url, self.parse)

    def parse_author(self, response):
        # Отримуємо дані про автора
        author_name = response.request.meta['author_name']
        author_birthday = response.css('span.author-born-date::text').get()
        author_bio = response.css('div.author-description::text').get()

        yield {
            'name': author_name.strip(),
            'birthday': author_birthday.strip(),
            'bio': author_bio.strip()
        }

