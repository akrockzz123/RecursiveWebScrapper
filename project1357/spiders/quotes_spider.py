from urllib import parse
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes_spider"

    def start_requests(self):
        urls = [
            "http://quotes.toscrape.com/page/2/"
        ]


        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
    
    def parse(self,response):
        page_id = response.url.split("/")[-2]
        filename = "quotes-%s"%page_id
        with open(filename,'wb') as f:
            f.write(response.body)
        self.log('Saved file %s'% filename)

        for q in response.css("div.quote"):
            text = q.css("span.text::text").get()
            author = q.css("small.author::text").get()
            tags = q.css("a.tag::text").get()
            yield {
                'text': text,
                'author': author,
                'tags': tags,
            }

            next_page = response.css('li.next::attr(href)').get()

            if next_page is not None:
                url2 = response.urljoin(next_page)
                yield scrapy.Request(url = url2 ,callback=self.parse)
