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

# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors = 'replace', line_buffering = True)
class Fc2club(getVideoInfoBase):
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()

    def getTitle(self,html): #获取标题
        result = str(html.xpath('//*[@class="show-top-grids"]/div[1]/h3/text()')).strip(" ['']")
        print(result)
        return result
    def getActor(self,html):
        try:
            result = str(html.xpath('//*[@class="show-top-grids"]/div[1]/h5[5]/a/text()')).strip(" ['']")
            print(result)
            return result
        except:
            return ''
    def getStudio(self,html): #获取厂商
        try:
            result = str(html.xpath('//*[@class="show-top-grids"]/div[1]/h5[3]/a[1]/text()')).strip(" ['']")
            print(result)
            return result
        except:
            return ''
    def getNum(self,html):     #获取番号
        title = str(html.xpath('//*[@class="show-top-grids"]/div[1]/h3/text()')).strip(" ['']")
        num = title.split(' ')[0]
        if num.startswith('FC2') != True:
            num = ''
        return num
    def getRelease(self,html): #
        return ''
    def getCover(self,html): #获取img #
        imgUrl = str(html.xpath('//*[@class="slides"]/li[1]/img/@src')).strip(" ['']")
        imgUrl = imgUrl.replace('../','https://fc2club.net/')
        print(imgUrl)
        return imgUrl
    def getOutline(self,html):     #获取番号 #
        path = str(html.xpath('//*[@id="top"]/div[1]/section[4]/iframe/@src')).strip(" ['']")
        result = str(html.xpath('/html/body/div/text()')).strip(" ['']").replace("\\n",'',10000).replace("'",'',10000).replace(', ,','').strip('  ').replace('。,',',')
        return result
    def getTag(self,html):     #获取tag
        a = html.xpath('//*[@class="show-top-grids"]/div[1]/h5[4]/a')
        tag = []
        for i in range(len(a)):
            tag.append(str(a[i].xpath('text()')).strip("['']"))
        return tag
    def getYear(self,html):
        return ''

    def getExtrafanart(self,html):  # 获取剧照
        imgUrl = str(html.xpath('//*[@class="slides"]/li[1]/img/@src')).strip(" ['']")
        imgUrl = imgUrl.replace('../','https://fc2club.net/')
        return imgUrl

    def getTrailer(self,html):
        return ''

    def main(self,number):
        self.fx = firefox()
        number = number.replace('FC2-', '').replace('fc2-', '')
        url = 'https://fc2club.net/html/FC2-' + number + '.html'
        htmlcode = self.fx.get_html(url,time =1)
        self.lx = etree.fromstring(htmlcode,etree.HTMLParser())
        #print(htmlcode)
        #print(url)
        self.getVideoInfo(self.lx)
        self.info['website'] = url
        self.info['source'] = url
        return self.info
    

if __name__ == '__main__':
    fc = Fc2club()
    print(fc.main('FC2-402422'))

