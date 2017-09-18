import sys
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtWebEngine
from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QEventLoop, QUrl, QTimer
from jdcrawl.items import JdcrawlItem

class JdSpider(CrawlSpider):
    name = "jdSpider"
    view = None
    app = None
    html = None
    isloadFinish = False
    allowed_domains = ["jd"]
    start_urls = [
        "https://list.jd.com/list.html?cat=9987,653,655&page=1&sort=sort_rank_asc&trans=1&JL=6_0_0&ms=6#J_main"
    ]

    def _callable(self, html):
        self.html = html
        print("app quit")
        self.app.quit()
        self.app.exit(0)
        self.isloadFinish = True
        print("_callable")
        filename = 'response.html'
        fp = open(filename, 'w',encoding='utf-8')
        fp.write(html)
        fp.close()


    def parserHtml(self):
        print("parserHtml..")
        select = Selector(text=self.html)
        for sel in select.xpath('//*[@id="plist"]/ul/li[@class="gl-item"]'):
            item = JdcrawlItem()
            name = sel.xpath('div/div[@class="p-name"]/a/em/text()').extract()
            shop = sel.xpath('div/div[@class="p-shop"]/span/a[@title]/text()').extract()
            price = sel.xpath('div/div[@class="p-price"]/strong[@class="J_price"]/i/text()').extract()
            comment = sel.xpath('div/div[@class="p-commit"]/strong/a/text()').extract()
            item["phoneName"] = name
            item["phoneShop"] = shop
            item["price"] = price
            item["comments"] = comment
            print(name)
            # yield item

    def _timer_for_html(self):
        print("_timer_for_html")
        self.view.page().toHtml(self._callable)

    def _loadFinished(self, result):
        print("load finish.....")
        QTimer.singleShot(2 * 1000, self._timer_for_html)

    def parse(self, response):
        print("parse")
        self.app = QtWidgets.QApplication(sys.argv)
        self.view = QWebEngineView()
        self.view.loadFinished.connect(self._loadFinished)
        self.view.load(QUrl(response.url))
        self.app.exec();
        select = Selector(text=self.html)
        for sel in select.xpath('//*[@id="plist"]/ul/li[@class="gl-item"]'):
            item = JdcrawlItem()
            name = sel.xpath('div/div[@class="p-name p-name-type3"]/a/em/text()').extract()
            shop = sel.xpath('div/div[@class="p-shop"]/span/a[@title]/text()').extract()
            price = sel.xpath('div/div[@class="p-price"]/strong[@class="J_price"]/i/text()').extract()
            comment = sel.xpath('div/div[@class="p-commit"]/strong/a/text()').extract()
            if len(name) > 0:
                name = name[0].strip()
            if len(shop) > 0 :
                shop = shop[0].strip()
            if len(price) > 0:
                price = price[0].strip()
            if len(comment) > 0:
                comment = comment[0].strip()
            item["phoneName"] = name
            item["phoneShop"] = shop
            item["price"] = price
            item["comments"] = comment
            # print(name)
            yield item


