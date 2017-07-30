# -*- coding: utf-8 -*-
import scrapy, json

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

class ZYCGSpider(scrapy.Spider):
    name="get_zycg"
    allowed_domains = ['*']

    def closed(self, reason):
        self.f.close()

    def start_requests(self):
        self.f = open("zycg.csv", "w+")
        yield scrapy.Request("http://www.zycg.cn/rjcg/platform",
                             callback=self.parse_tag,
                             dont_filter=True,
                             headers={
                                 "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
                                 "Referer":"http://www.zycg.gov.cn/rjcg/index",
                                 "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                                 "Accept-Encoding":"gzip, deflate, sdch"
                             })

    def parse_tag(self, response):
        tags = response.xpath("//td[@class='grade3']/a/span/text()").extract()
        tags = [tag.split("\r\n")[0] for tag in tags]
        print(tags)
        links = response.xpath("//td[@class='grade3']/a")
        for link in links:
            yield scrapy.Request("http://www.zycg.cn" + link.xpath("@href").extract()[0],
                                 callback=self.save_company_name,
                                 dont_filter=True,
                                 headers={
                                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
                                     "Referer": "http://www.zycg.gov.cn/rjcg/index",
                                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                                     "Accept-Encoding": "gzip, deflate, sdch"
                                 },
                                 meta={"tag":link.xpath("span/text()").extract()[0].split("\r\n")[0]})

    def save_company_name(self, response):
        names = response.xpath("//div[@class='smid']/a/text()").extract()
        for name in names:
            print(response.meta["tag"], name)
            self.f.write("\n{},{}".format(response.meta["tag"], name))

