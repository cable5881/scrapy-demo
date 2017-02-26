import scrapy
# from tutorial.items import TutorialItem
from tutorial.items import DramaItem
from scrapy.http import HtmlResponse
class dramaSpider(scrapy.Spider):
    name = "drama"

    start_urls = [
        'http://www.meijutt.com/file/list1.html'
    ]

    # start_urls = [
    #     'http://quotes.toscrape.com/page/1/',
    #     'http://quotes.toscrape.com/page/2/'
    # ]

    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    # def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)

        # for quote in response.css("div.quote"):
        #     text = quote.css("span.text::text").extract_first()
        #     author = quote.css("small.author::text").extract_first()
        #     tags = quote.css("div.tags a.tag::text").extract()
        #     print(dict(text=text, author=author, tags=tags))

        # print all dicts of data we've just scraped on the console
        # for quote in response.css('div.quote'):
        #     yield {
        #         'text': quote.css('span.text::text').extract_first(),
        #         'author': quote.css('small.author::text').extract_first(),
        #         'tags': quote.css('div.tags a.tag::text').extract(),
        #     }

        # for quote in response.css('div.quote'):
        #     text = quote.css('span.text::text').extract_first()
        #     author = quote.css('small.author::text').extract_first()
        #     tags = quote.css('div.tags a.tag::text').extract()
        #     yield TutorialItem(text = text, author = author, tags = tags)


        # next_page = response.css('li.next a::attr(href)').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     # print('***************Next page is ', response.url)
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parse(self, response):
        # htmlResponse = HtmlResponse(url = response.url, body = response.body)
        # print(htmlResponse.encoding)
        # response.body.decode("gbk")
        for quote in response.css('div.cn_box2'):
            href = quote.css('.bor_img3_right a::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(href), callback = self.parse_drama)

        next_page = response.css('div.page a:nth-last-child(2)::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            # print('***************Next page is ', next_page)
            yield scrapy.Request(next_page, callback = self.parse)

        def parse_drama(self, response):
            def extract_with_css(query):
                return response.css(query).extract_first()

            img_src = response.css('div.o_big_img_bg_b img::attr(src)').extract_first()
            profile = response.css('div.o_r_contact ul').extract_first()
            title_en = profile.css('li:nth-child(2)::text').extract_first()
            title_cn = profile.css('li:nth-child(3)::text').extract_first()
            debut_date = profile.css('li:nth-child(7)::text').extract_first()
            plot = profile.css('li:nth-child(9)::text').extract_first()
            nation = profile.css('li:nth-child(10) label:nth-child(1)::text').extract_first()
            tv = profile.css('li:nth-child(10) label:nth-child(2)::text').extract_first()
            hot = profile.css('li:nth-child(11) label:nth-child(1)::text').extract_first()
            length = profile.css('li:nth-child(11) label:nth-child(2)::text').extract_first()
            category = profile.css('li:nth-child(12) label:nth-child(2)::text').extract_first()
            script_writers = profile.css('div.o_r_contact ul').css('li:nth-child(4) a::text')
            directors = profile.css('div.o_r_contact ul').css('li:nth-child(5) a::text')
            actors = profile.css('div.o_r_contact ul').css('li:nth-child(6) a::text')



            yield DramaItem(img_src = img_src, title_cn = title_cn, title_en = title_en, tv = tv, year = year, plot = plot)
           