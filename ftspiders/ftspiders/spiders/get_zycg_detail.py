# -*- coding: utf-8 -*-
import scrapy, json
from ftspiders import secrets

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

class ZYCGDetailSpider(scrapy.Spider):
    name="get_zycg_detail"
    allowed_domains = ['*']

    def spider_closed(self,spider):
        print("spider close:" + str(spider.name))
        self.f.close()
        self.f_detail.close()

    def closed(self, reason):
        print("closed:" + str(reason))
        self.f.close()
        self.f_detail.close()

    def start_requests(self):
        self.f = open("zycg.csv", "r")
        self.f_detail = open("zycg_detail.csv","a")
        for cnt in range(0): # add 180 per day
            line = self.f.readline()
        for cnt in range(180):
            line = self.f.readline()
            line = line.replace("\n","").split(",")
            if len(line) == 2:
                [tag, name] = line
                yield scrapy.Request(
                    "https://rong.36kr.com/n/api/search/company?kw={}&sortField=MATCH_RATE".format(quote(name)),
                    callback=self.get_detail,
                    dont_filter=True,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
                        "Referer": "https://rong.36kr.com/landing/detail?type=company&sortField=MATCH_RATE&kw={}".format(
                            quote(name)),
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Encoding": "gzip, deflate, sdch, br",
                        "Accept-Language": "zh-CN,zh;q=0.8",
                        "Connection": "keep-alive",
                        "X-Tingyun-Id": "Dio1ZtdC5G4;r=39133050",
                        "Cookie": secrets.cookie_36kr,
                        "Host": "rong.36kr.com",
                    },
                    meta={
                        "name": name,
                        "tag": tag
                    })


    def get_detail(self, response):
        info = json.loads(response.body_as_unicode())
        page_data = info.get("data").get("pageData")
        try:
            if page_data.get("totalCount") > 0:
                data = page_data.get("data")[0]
                self.f_detail.write(",".join([response.meta["tag"],
                                       response.meta["name"],
                                       data.get("industryStr","无行业信息"),
                                       data.get("phase","无轮次信息"),
                                       data.get("cityStr","无地区信息"),
                                       str(data.get("funding","融资状态不详"))])+ "\n")
                print(",".join([response.meta["tag"],
                                       response.meta["name"],
                                       data.get("industryStr","无行业信息"),
                                       data.get("phase","无轮次信息"),
                                       data.get("cityStr","无地区信息")]) + "\n")
            else:
                self.f_detail.write(",".join([
                    response.meta["tag"],
                    response.meta["name"],
                    "36kr未查到信息"
                ])+ "\n")
        except Exception as e:
            self.f_detail.write(",".join([
                response.meta["tag"],
                response.meta["name"],
                "36kr报错"
            ]) + "\n")


