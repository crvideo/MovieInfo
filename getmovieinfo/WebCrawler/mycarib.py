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

class Carib(getVideoInfoBase):
    __metaclass__ = ABCMeta
    
    def __init__(self):
        super().__init__()

    def getTitle(self,lx) -> str:
        element = str(lx.xpath("//div[@class='movie-info section']/div[@class='heading']/h1[@itemprop='name']/text()"))
        if element:
            return element[0].strip()
        else:
            return ''
    def getYear(self,lx) -> str:
        element =  lx.xpath("//li[2]/span[@class='spec-content']/text()")
        if element:
            return element[0][:4]
        else:
            return ''

    def getNum(self,lx):
        return self.number
    
    def getOutline(self,lx) -> str:
        o = lx.xpath("//div[@class='movie-info section']/p[@itemprop='description']/text()")
        if o:
            return o[0].strip()
        else:
            return ''

    def getRelease(self,lx) -> str:
        o = lx.xpath("//li[2]/span[@class='spec-content']/text()")
        if o:
            return o[0].replace('/','-')
        else:
            return ''

    def getActor(self,lx):
        r = []
        actors = lx.xpath("//span[@class='spec-content']/a[@itemprop='actor']/span/text()")
        for act in actors:
            if str(act) != '他':
                r.append(act)
        return r

    def getTag(self,lx) -> str:
        genres = lx.xpath("//span[@class='spec-content']/a[@itemprop='genre']/text()")
        return genres

    def getExtrafanart(self,lx) -> str:
        r = []
        genres = lx.xpath("//*[@id='sampleexclude']/div[2]/div/div[@class='grid-item']/div/a/img/@src")
        for g in genres:
            jpg = str(g)
            if '/member/' in jpg:
                break
            else:
                r.append('https://www.caribbeancom.com' + jpg)
        return r

    def getSeries(self,lx) -> str:
        try:
            return str(lx.xpath("//span[@class='spec-title'][contains(text(),'シリーズ')]/../span[@class='spec-content']/a/text()")[0]).strip()
        except:
            return ''

    def getRuntime(self,lx) -> str:
        o = str(lx.xpath("//span[@class='spec-content']/span[@itemprop='duration']/text()"))
        if o:
            return o[0].strip()
        else:
            return ''

    def getActorPhoto(self,lx):
        htmla = lx.xpath("//*[@id='moviepages']/div[@class='container']/div[@class='inner-container']/div[@class='movie-info section']/ul/li[@class='movie-spec']/span[@class='spec-content']/a[@itemprop='actor']")
        names = lx.xpath("//*[@id='moviepages']/div[@class='container']/div[@class='inner-container']/div[@class='movie-info section']/ul/li[@class='movie-spec']/span[@class='spec-content']/a[@itemprop='actor']/span[@itemprop='name']/text()")
        t = {}
        for name, a in zip(names, htmla):
            if name.strip() == '他':
                continue
            p = {name.strip(): a.attrib['href']}
            t.update(p)
        o = {}
        for k, v in t.items():
            if '/search_act/' not in v:
                continue
            r = self.fx.get_html(urljoin(G_SITE, v))
            if not r.ok:
                continue
            html = r.text
            pos = html.find('.full-bg')
            if pos<0:
                continue
            css = html[pos:pos+100]
            cssBGjpgs = re.findall(r'background: url\((.+\.jpg)', css, re.I)
            if not cssBGjpgs or not len(cssBGjpgs[0]):
                continue
            p = {k: urljoin(r.url, cssBGjpgs[0])}
            o.update(p)
        return o


    def main(self,number: str):
        G_SITE = 'https://www.caribbeancom.com'
        self.fx = firefox()
        url = f'{G_SITE}/moviepages/{number}/index.html'
        htmlcode = self.fx.get_html(url, time=1)
        #print(url)
        self.number = number
        #print(result)
        #htmlcode = result.content.decode('euc-jp')
            
        #if not htmlcode or '<title>404' in htmlcode or 'class="movie-info section"' not in htmlcode:
        #    raise ValueError("page not found")
            
        self.lx = etree.fromstring(htmlcode,etree.HTMLParser())
        self.getVideoInfo(self.lx)
        self.info['source'] = "carib.py"
        self.info['website'] = url
        return self.info



if __name__ == "__main__":
    c = Carib()
    print(c.main("070116-197")) # actor have photo
    # print(c.getMagnetLink(c.lx))
    # print(c.getTitle(c.lx))
    # print(c.getNum(c.lx))     #获取番号
    # print(c.getOutline(c.lx))  #获取剧情介绍 多进程并发查询
    # #print(c.getActorPhoto(c.lx))
    # print(c.getStudioJa(c.lx))
    # print(c.getStudio(c.lx)) #获取厂商
    # print(c.getYear(c.lx))   #获取年份
    # print(c.getCover(c.lx))  #获取封面链接
    # print(c.getRelease(c.lx)) #获取出版日期
    # print(c.getRuntime(c.lx)) #获取分钟 已修改
    # print(c.getActor(c.lx))   #获取女优
    # print(c.getDirectorJa(c.lx))
    # print(c.getDirector(c.lx)) #获取导演
    # print(c.getCID(c.lx))
    # print(c.getSeriesJa(c.lx))
    # print(c.getSeries(c.lx))   #获取系列
    # print(c.getTag(c.lx))  # 获取标签
    # print(c.getExtrafanart(c.lx))  # 获取剧照
    #print(c.main("041721-001"))
    #print(c.main("080520-001"))
