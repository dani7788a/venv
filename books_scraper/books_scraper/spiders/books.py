import scrapy
from books_scraper.items import BooksScraperItem

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for book in response.css('article.product_pod'):
            item = BooksScraperItem()
            item['title'] = book.css('h3 a::attr(title)').get()
            item['price'] = book.css('.price_color::text').get()
            item['availability'] = book.css('.availability::text').get().strip()
            item['link'] = response.urljoin(book.css('h3 a::attr(href)').get())
            yield item
        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
