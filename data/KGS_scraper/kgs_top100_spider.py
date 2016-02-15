import json
import numpy as np
from path import path
import scrapy
# from tutorial.items import KGSItem
from items import KGSItem
import urllib
#
from ipdb import set_trace as BP


class KGStop100Spider(scrapy.Spider):
    name = "KGStop100"
    allowed_domains = ["gokgs.com/top100.jsp"]
    start_urls = [
        # "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        # "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
        "https://www.gokgs.com/top100.jsp"
    ]

    def parse(self, response):
        item = KGSItem()
        # href = response.xpath('//body//a/@href').extract()
        users_ = response.xpath('//body//a/@href').re(r'user=.{1,}')
        users = []
        for u in users_:
            users.append(u[5:])
        item['users'] = users
        yield item


class KGSarchives(scrapy.Spider):
    name = "KGSarchives"
    allowed_domains = ["gokgs.com/gameArchives.jsp"]
    # start_urls = [
    #     "https://www.gokgs.com/gameArchives.jsp"
    # ]
    pth = path('top100.json')
    with path.open(pth, 'rb') as fid:
        users = json.load(fid)[0]['users']
    start_urls = []
    BP()
    for user in users:
        start_urls.append(
            "https://www.gokgs.com/gameArchives.jsp?user={}".format(user))

    def parse(self, response):
        item = KGSItem()
        # pth = path('top100.json')
        # with path.open('rb') as fid:
        #     users = json.load(fid)
        # urls = []
        # for u in start_urls:
        #     urls.extend(response.xpath('//table//tr//td//a/@href').extract())
        print '\n'
        print '\n'
        print "Inside parse: "
        print '\n'
        for url in response.xpath('//table//tr//td//a/@href').extract():
            request = scrapy.Request(url, callback=self.parse_page2)
            request.meta['item'] = response.url
            print "making request for {}".format(url)
            # yield request
            print "request completed"

    def parse_page2(self, response):
        hrefs = response.xpath('//table//tr//td//a/@href').extract()[1:]
        BP()
        # print '\n'
        # print "hrefs: ", hrefs
        # print '\n'
        for h in hrefs:
            f = urllib.URLopener()
            f.retrieve(h, "test.gz")
        return







