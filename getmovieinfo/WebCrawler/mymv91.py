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

etree.FunctionNamespace("http://exslt.org/regular-expressions").prefix = 're'
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors = 'replace', line_buffering = True)

class Mv91(getVideoInfoBase):
    __metaclass__ = ABCMeta

    host = 'https://www.91mv.org'
    def __init__(self):
        super().__init__()

    def getActorPhoto(self,html):
        return ''

    def getTitle(self,html):  #获取标题
        try:
            title = str(html.xpath('//div[@class="player-title"]/text()')[0])
            result = str(re.findall('(.*)(91.*-\d*)',title)[0][0])
            return result.strip()
        except:
            return ''

    def getStudio(self,html): #获取厂商 已修改
        return '91制片厂'

    def getYear(self,html):   #获取年份
        try:
            result = str(html.xpath('//p[@class="date"]/text()')[0])
            date = result.replace('日期：','')
            if isinstance(date, str) and len(date):
                return date
        except:
            return ''
        return ''

    def getCover(self,html):  #获取封面图片
        htmlcode = etree.tostring(html,encoding="unicode")
        try:
            url = str(re.findall('var pic_url = "(.*?)"',htmlcode)[0])
            return url.strip()
        except:
            return ''

    def getRelease(self,html): #获取出版日期
        try:
            result = str(html.xpath('//p[@class="date"]/text()')[0])
            date = result.replace('日期：','')
            if isinstance(date, str) and len(date):
                return date
        except:
            return ''
        return ''

    def getRuntime(self,html): #获取播放时长
        return ''

    def getActor(self,html):   #获取女优
        b=[]
        for player in html.xpath('//p[@class="player-name"]/text()'):
            player = player.replace('主演：','')
            b.append(player)
        return b

    def getNum(self,html):     #获取番号
        try:
            title = str(html.xpath('//div[@class="player-title"]/text()')[0])
            result = str(re.findall('(.*)(91.*-\d*)',title)[0][1])
            return result.strip()
        except:
            return ''

    def getDirector(self,html): #获取导演 已修改
        return ''

    def getOutline(self,html):  #获取概述
        try:
            result = str(html.xpath('//div[@class="play-text"]/text()')[0])
            return result.strip()
        except:
            return ''


    def getSerise(self,html):   #获取系列 已修改
        return ''

    def getTag(self,html):  # 获取标签
        return html.xpath('//div[@class="player-tag"]/text()')

    def getExtrafanart(self,html):  # 获取剧照
        return ''

    def search(self,keyword): #搜索，返回结果
        self.fx = firefox()
        search_html = self.fx.get_html(self.host + '/index/search?keywords=' + keyword)
        html = etree.fromstring(search_html, etree.HTMLParser())
        video_list = html.xpath('//a[@class="video-list"]/@href')
        return video_list[0] if video_list else ''

    def main(self,number):
        number = number.replace('91CM-','').replace('91MS-','')
        url = self.host + str(self.search(number))
        self.fx = firefox()
        htmlcode = self.fx.get_html(url,time = 1)
        self.lx = etree.fromstring(htmlcode,etree.HTMLParser())
        #print(htmlcode)
        #print(url)
        self.getVideoInfo(self.lx)
        return self.info



if __name__ == '__main__':
    jav = Mv91()
    print(jav.main('91CM-121'))
    #print(main('91CM-122'))
    #print(main('91CM-143'))
    #print(main('91MS-006'))
