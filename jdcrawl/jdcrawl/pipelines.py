# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook

class JdcrawlPipeline(object):
    wb = Workbook()
    ws = wb.active
    ws.append(['手机名称', '店名', '价格', '成交量'])  # 设置表头

    def process_item(self, item, spider):
        print("process item")
        line = [item['phoneName'], item['phoneShop'], item['price'], item['comments']]  # 把数据中每一项整理出来
        print(line)
        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        self.wb.save('phoneinfo.xlsx')  # 保存xlsx文件
        return item
#