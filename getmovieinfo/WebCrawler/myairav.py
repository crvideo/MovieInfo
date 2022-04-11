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
from .myjavbus import Javbus

'''
myAPI
注册：https://www.airav.wiki/api/auth/signup
设置：https://www.airav.wiki/api/get_web_settings
搜索：https://www.airav.wiki/api/video/list?lng=zh-CN&search=
搜索：https://www.airav.wiki/api/video/list?lang=zh-TW&lng=zh-TW&search=
'''


class Airav(getVideoInfoBase):
    __metaclass__ = ABCMeta
    host = 'https://www.airav.wiki/video/'
    def __init__(self):
        super().__init__()
        
    def getMagnetLink(self,html):
        result = self.info.get('magnetlink')
        if isinstance(result, dict) and len(result):
            return result
        return ''
    # airav这个网站没有演员图片，所以直接使用javbus的图
    def getActorPhoto(self,html):
        result = self.info.get('actor_photo')
        if isinstance(result, dict) and len(result):
            return result
        return ''

    def getTitle(self,html):  #获取标题
        title = str(html.xpath('/html/head/title/text()')[0])
        result = str(re.findall('](.*?)- AIRAV-WIKI', title)[0]).strip()
        return result
    def getStudio(self,html): #获取厂商 已修改
        result = self.info.get('studio')
        if isinstance(result, str) and len(result):
            return result
        return str(html.xpath('//a[contains(@href,"?video_factory=")]/text()')).strip(" ['']")
    def getYear(self,html):   #获取年份
        result = self.info.get('year')
        if isinstance(result, str) and len(result):
            return result
        release = self.getRelease(html)
        if len(release) != len('2000-01-01'):
            return ''
        return release[:4]
    def getCover(self,html):  #获取封面图片
        result = self.info.get('cover')
        if isinstance(result, str) and len(result):
            return result
        return html.xpath('//img[contains(@src,"/storage/big_pic/")]/@src')[0]
    def getRelease(self,html): #获取出版日期
        result = self.info.get('release')
        if isinstance(result, str) and len(result):
            return result
        try:
            result = re.search(r'\d{4}-\d{2}-\d{2}', str(html.xpath('//li[contains(text(),"發片日期")]/text()'))).group()
        except:
            return ''
        return result
    def getRuntime(self,html): #获取播放时长
        result = self.info.get('runtime')
        if isinstance(result, str) and len(result):
            return result
        return ''
    # airav女优数据库较多日文汉字姓名，javbus较多日语假名，因此airav优先
    def getActor(self,html):   #获取女优
        b=[]
        a = html.xpath('//ul[@class="videoAvstarList"]/li/a[starts-with(@href,"/idol/")]/text()')
        for v in a:
            v = v.strip()
            if len(v):
                b.append(v)
        if len(b):
            return b
        result = self.info.get('actor')
        if isinstance(result, list) and len(result):
            return result
        return []
    def getNum(self,html):     #获取番号
        result = self.info.get('number')
        if isinstance(result, str) and len(result):
            return result
        title = str(html.xpath('/html/head/title/text()')[0])
        result = str(re.findall('^\[(.*?)]', title)[0])
        return result
    def getDirector(self,html): #获取导演 已修改
        result = self.info.get('director')
        if isinstance(result, str) and len(result):
            return result
        return ''
    def getOutline(self,html):  #获取概述
        try:
            result = html.xpath("string(//div[@class='d-flex videoDataBlock']/div[@class='synopsis']/p)").replace('\n','').strip()
            return result
        except:
            return ''
    def getSeries(self,html):   #获取系列 已修改
        result = self.info.get('series')
        if isinstance(result, str) and len(result):
            return result
        return ''
    def getTag(self,html):  # 获取标签
        tag = []
        result = html.xpath('//a[contains(@href,"?video_tag=")]/text()')
        tag.append(result)
    def getExtrafanart(self,html):  # 获取剧照
        elements = html.xpath('//div[@tabindex][contains(@class,"image-gallery-slid")]')
        imgs = []
        if elements:
            for a in elements[0].findall(".//img"):
                imgs.append(a.attrib["src"])

        #print(imgs)
        if imgs:
            return imgs
        return ''


    def main(self,number):
        self.fx = firefox()
        jb = Javbus()
        self.info = jb.main(number)
        url = self.host + number
        #wait_for = "//a[@rel][@title]"
        htmlcode = self.fx.get_html(url)
        #print(htmlcode)
        self.lx = etree.fromstring(htmlcode,etree.HTMLParser())
        self.getVideoInfo(self.lx)
        self.info['source'] = "airav.py"
        self.info['website'] = urljoin(self.host,number)
        return self.info

        
        #self.lx = etree.fromstring(htmlcode,etree.HTMLParser())
        #self.getVideoInfo(self.lx)
        #return self.info
    

if __name__ == '__main__':
    aa = Airav()
    info = aa.main('ADV-R0624')  # javbus页面返回404, airav有数据
    print(info)
    # print(main('ADV-R0624'))  # javbus页面返回404, airav有数据
    # print(main('ADN-188'))    # 一人
    # print(main('CJOD-278'))   # 多人 javbus演员名称采用日语假名，airav采用日文汉字
