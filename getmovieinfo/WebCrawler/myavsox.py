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
import secrets
import json


# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors = 'replace', line_buffering = True)


class Avsox(getVideoInfoBase):
    __metaclass__ = ABCMeta
    
    def __init__(self):
        super().__init__()

    def getMagnetLink(self,html):
        return ''
    def getActorPhoto(self,html):
        a = html.xpath('//a[@class="avatar-box"]')
        d = {}
        for i in a:
            l = i.find('.//img').attrib['src']
            t = i.find('span').text
            p2 = {t: l}
            d.update(p2)
        return d
    def getTitle(self,html):
        try:
            result = str(html.xpath('/html/body/div[2]/h3/text()')).strip(" ['']") #[0]
            return result.replace('/', '')
        except:
            return ''
    def getActor(self,html):
        a = html.xpath('//a[@class="avatar-box"]')
        d = []
        for i in a:
            d.append(i.find('span').text)
        return d
    def getStudio(self,html):
        result1 = str(html.xpath('//p[contains(text(),"制作商: ")]/following-sibling::p[1]/a/text()')).strip(" ['']").replace("', '",' ')
        return result1
    def getRuntime(self,html):
        result1 = str(html.xpath('//span[contains(text(),"长度:")]/../text()')).strip(" ['分钟']")
        return result1
    def getLabel(self,html):
        result1 = str(html.xpath('//p[contains(text(),"系列:")]/following-sibling::p[1]/a/text()')).strip(" ['']")
        return result1
    def getNum(self,html):
        result1 = str(html.xpath('//span[contains(text(),"识别码:")]/../span[2]/text()')).strip(" ['']")
        return result1
    def getYear(self,html):
        try:
            result = str(re.search('\d{4}',self.getRelease(html)))
            return result
        except:
            return ""
    def getRelease(self,html):
        result1 = str(html.xpath('//span[contains(text(),"发行时间:")]/../text()')).strip(" ['']")
        return result1
    def getCover(self,html):
        result = str(html.xpath('/html/body/div[2]/div[1]/div[1]/a/img/@src')).strip(" ['']")
        return result
    def getCover_small(self,html):
        result = str(html.xpath('//*[@id="waterfall"]/div/a/div[1]/img/@src')).strip(" ['']")
        return result
    def getTag(self,html):
        x = html.xpath('/html/head/meta[@name="keywords"]/@content')
        if x:
            x =x [0].split(',')
            if len(x) > 2:
                return [i.strip() for i in x[2:]]
            else:
                return []
    def getSeries(self,html):
        try:
            result1 = str(html.xpath('//span[contains(text(),"系列:")]/../span[2]/text()')).strip(" ['']")
            return result1
        except:
            return ''

    def main(self,number):
        self.fx = firefox()
        html = self.fx.get_html('https://tellme.pw/avsox',time=1)
        site = etree.HTML(html).xpath('//div[@class="container"]/div/a/@href')[0]
        a = self.fx.get_html(site + '/cn/search/' + number,time=1)
        #print(site + '/cn/search/' + number)
        html = etree.fromstring(a, etree.HTMLParser())
        alert = str(html.xpath('//div[@class="alert alert-danger"]'))
        if alert:
            return self.info
        result1 = str(html.xpath('//*[@id="waterfall"]/div/a/@href')).strip(" ['']")
        if result1 == '' or result1 == 'null' or result1 == 'None':
            a = self.fx.get_html(site + '/cn/search/' + number.replace('-', '_'),time=1)
            html = etree.fromstring(a, etree.HTMLParser())
            result1 = str(html.xpath('//*[@id="waterfall"]/div/a/@href')).strip(" ['']")
            if result1 == '' or result1 == 'null' or result1 == 'None':
                a = self.fx.get_html(site + '/cn/search/' + number.replace('_', ''),time=1)
                html = etree.fromstring(a, etree.HTMLParser())
                result1 = str(html.xpath('//*[@id="waterfall"]/div/a/@href')).strip(" ['']")
        detail = self.fx.get_html("https:" + result1,time=1)
        self.lx = etree.fromstring(detail, etree.HTMLParser())
        self.getVideoInfo(self.lx)
        self.info['source'] = "avsox.py"
        self.info['website'] = "https:" + result1
        return self.info
        

if __name__ == "__main__":
    avs = Avsox()
    #print(avs.main('012717_472'))
    print(avs.main('SSIS-313'))
    #print(main('1')) # got fake result raise 'number not found'
