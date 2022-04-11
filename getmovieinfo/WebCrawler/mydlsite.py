import os
import sys
sys.path.append('../..')
from abc import abstractmethod, ABCMeta
from .htmlclass import *
from .firefox import firefox
#import test
from lxml import etree#need install
import re
import pprint
from urllib.parse import urljoin
import inspect
import json


# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors = 'replace', line_buffering = True)
#print(get_html('https://www.dlsite.com/pro/work/=/product_id/VJ013152.html'))
#title //*[@id="work_name"]/a/text()
#studio //th[contains(text(),"ブランド名")]/../td/span[1]/a/text()
#release //th[contains(text(),"販売日")]/../td/a/text()
#story //th[contains(text(),"シナリオ")]/../td/a/text()
#senyo //th[contains(text(),"声優")]/../td/a/text()
#tag //th[contains(text(),"ジャンル")]/../td/div/a/text()
#jianjie //*[@id="main_inner"]/div[3]/text()
#photo //*[@id="work_left"]/div/div/div[2]/div/div[1]/div[1]/ul/li/img/@src

#https://www.dlsite.com/pro/work/=/product_id/VJ013152.html
class Dlsite(getVideoInfoBase):
    __metaclass__ = ABCMeta
    
    def __init__(self):
        super().__init__()

    def getTitle(self,html):
        result = html.xpath('//*[@id="work_name"]/text()')
        return result[0] if result else ''
    def getActor(self,html):  # //*[@id="center_column"]/div[2]/div[1]/div/table/tbody/tr[1]/td/text()
        try:
            result1 = html.xpath('//th[contains(text(),"声优")]/../td/a/text()')
        except:
            result1 = ''
        return result1
    def getActorPhoto(self,html): #//*[@id="star_qdt"]/li/a/img
        a = actor.split(',')
        d={}
        for i in a:
            p={i:''}
            d.update(p)
        return d
    def getStudio(self,html):
        try:
            try:
                result = html.xpath('//th[contains(text(),"系列名")]/../td/span[1]/a/text()')[0]
            except:
                result = html.xpath('//th[contains(text(),"社团名")]/../td/span[1]/a/text()')[0]
        except:
            result = ''
        return result
    def getRuntime(self,html):
        result1 = str(html.xpath('//strong[contains(text(),"時長")]/../span/text()')).strip(" ['']")
        result2 = str(html.xpath('//strong[contains(text(),"時長")]/../span/a/text()')).strip(" ['']")
        return str(result1 + result2).strip('+').rstrip('mi')
    def getLabel(self,html):
        try:
            try:
                result = html.xpath('//th[contains(text(),"系列名")]/../td/span[1]/a/text()')[0]
            except:
                result = html.xpath('//th[contains(text(),"社团名")]/../td/span[1]/a/text()')[0]
        except:
            result = ''
        return result
    def getYear(self,html):
        try:
            result = str(re.search('\d{4}', self.getRelease(html)).group())
            return result
        except:
            return self.getRelease(html)
    def getRelease(self,html):
        result1 = html.xpath('//th[contains(text(),"贩卖日")]/../td/a/text()')
        return result1[0].replace('年','-').replace('月','-').replace('日','') if result1 else ''
    def getTag(self,html):
        try:
            result = html.xpath('//th[contains(text(),"分类")]/../td/div/a/text()')
            return result
        except:
            return ''
    def getCover_small(self,html,index=0):
        # same issue mentioned below,
        # javdb sometime returns multiple results
        # DO NOT just get the firt one, get the one with correct index number
        try:
            result = html.xpath("//div[@class='item-image fix-scale-cover']/img/@src")[index]
            if not 'https' in result:
                result = 'https:' + result
            return result
        except: # 2020.7.17 Repair Cover Url crawl
            result = html.xpath("//div[@class='item-image fix-scale-cover']/img/@data-src")[index]
            if not 'https' in result:
                result = 'https:' + result
            return result
    def getCover(self,html):
        result = html.xpath('//img/@srcset')
        return result[0] if result else ''
    def getDirector(self,html):
        try:
            result = html.xpath('//th[contains(text(),"剧情")]/../td/a/text()')[0]
        except:
            result = ''
        return result
    def getOutline(self,html):
        total = []
        result = html.xpath('//div[@class="work_parts_area"]/p/text()')
        for i in result:
            total.append(i.strip('\r\n'))
        return str(total).strip(" ['']").replace("', '', '",r'\n').replace("', '",r'\n').strip(", '', '")
    def getSeries(self,html):
        try:
            try:
                result = html.xpath('//th[contains(text(),"系列名")]/../td/span[1]/a/text()')[0]
            except:
                result = html.xpath('//th[contains(text(),"社团名")]/../td/span[1]/a/text()')[0]
        except:
            result = ''
        return result
    def main(self,number):
        self.fx = firefox()
        number = number.upper()
        url = 'https://www.dlsite.com/pro/work/=/product_id/' + number + '.html' +'/?locale=zh_cn'
        #print(url)
        htmlcode = self.fx.get_html(url,time =1)
        #print(htmlcode)
        self.lx = etree.fromstring(htmlcode,etree.HTMLParser())
        self.getVideoInfo(self.lx)
        self.info["website"] = url
        self.info["source"] = "dlsite.py"
        return self.info
    
# main('DV-1562')
# input("[+][+]Press enter key exit, you can check the error messge before you exit.\n[+][+]按回车键结束，你可以在结束之前查看和错误信息。")
if __name__ == "__main__":
    dl = Dlsite()
    print(dl.main('VJ013178'))
