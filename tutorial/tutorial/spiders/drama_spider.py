import scrapy

# from scrapy.http import HtmlResponse
from tutorial.items import DramaItem
from scrapy_splash import SplashRequest

class DramaSpider(scrapy.Spider):
    name = "drama"

    start_urls = [
        'http://www.meijutt.com/file/list1.html'
    ]

    def parse(self, response):
        # htmlResponse = HtmlResponse(url = response.url, body = response.body)
        # print(htmlResponse.encoding)
        # response.body.decode("gbk")
        for quote in response.css('div.cn_box2'):
            href = quote.css('.bor_img3_right a::attr(href)').extract_first()
            # yield SplashRequest(response.urljoin(href), callback = self.parse_drama, args = {'wait': 0.5})
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
        profile = response.css('div.o_r_contact ul')
        title_en = profile.css('li:nth-child(2)::text').extract_first()
        title_cn = profile.css('li:nth-child(3)::text').extract_first()
        debut_date = profile.css('li:nth-child(7)::text').extract_first()
        plot = profile.css('li:nth-child(9)::text').extract_first()
        nation = profile.css('li:nth-child(10) label:nth-child(1)::text').extract_first()
        tv = profile.css('li:nth-child(10) label:nth-child(2)::text').extract_first()
        hot = profile.css('li:nth-child(11) label:nth-child(1)::text').extract_first()
        length = profile.css('li:nth-child(11) label:nth-child(2)::text').extract_first()
        category = profile.css('li:nth-child(12) label:nth-child(2)::text').extract_first()
        script_writers = profile.css('li:nth-child(4) a::text').extract()
        directors = profile.css('li:nth-child(5) a::text').extract()
        actors = profile.css('li:nth-child(6) a::text').extract()

        average_score = response.xpath('//div[@id="average-score"]/text()').extract_first()
        star5_num = response.xpath('//span[@id="small-total-star5"]/text()').extract_first()
        star4_num = response.css('span#small-total-star4::text').extract_first()
        star3_num = response.css('span#small-total-star3::text').extract_first()
        star2_num = response.css('span#small-total-star2::text').extract_first()
        star1_num = response.css('span#small-total-star1::text').extract_first()

        yield DramaItem(
                img_src = img_src, title_cn = title_cn, title_en = title_en, tv = tv, debut_date = debut_date, 
                plot = plot, nation = nation, hot = hot, length = length, category = category, 
                script_writers = script_writers, directors = directors, actors = actors, 
                average_score = average_score, star5_num = star5_num, star4_num = star4_num, 
                star3_num = star3_num, star2_num = star2_num, star1_num = star1_num
        )
           