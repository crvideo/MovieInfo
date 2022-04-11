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

class Jav321(getVideoInfoBase):
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()

    def getTitle(self,html) -> str:
        res =  html.xpath("/html/body/div[2]/div[1]/div[1]/div[1]/h3/text()")
        if res:
            return res[0].strip()
        return ''

    def parseInfo(self,html):
        elements = html.xpath('//div[@class="row"]/div[@class="col-md-9"]')
        element_html = etree.tostring(elements[0],encoding="unicode")
        str = re.sub("<br/>","\n",element_html)
        str = re.sub("<.*?>","",str)
        info = dict()
        for line in str.splitlines():
            #print(line)
            data = line.split(": ")
            info[data[0]]=data[1]
        return(info)

    def getTrailer(self,html) -> str:
        videourlPather = re.compile(r'<source src=\"(.*?)\"')
        videourl = videourlPather.findall(html)
        if videourl:
            url = videourl[0].replace('awscc3001.r18.com', 'cc3001.dmm.co.jp').replace('cc3001.r18.com', 'cc3001.dmm.co.jp')
            return url
        else:
            return ''

    def getExtrafanart(self,html):  # 获取剧照
        elements = html.xpath('//div[@class="col-md-3"]/div[@class="col-xs-12 col-md-12"]')
        imgs = []
        if elements:
            for element in elements:
                for a in element.findall(".//img[@class='img-responsive']"):
                    imgs.append(a.attrib["src"])
        if not imgs:
            return ''
        return imgs
    def getCover(self,html):
        return html.xpath("/html/body/div[2]/div[2]/div[1]/p/a/img/@src")[0]
    def getOutline(self,html):
        return html.xpath("/html/body/div[2]/div[1]/div[1]/div[2]/div[3]/div/text()")[0]
    def getSeries2(self,html):
        return html.xpath("/html/body/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/a[11]/text()")[0]
    def getActor(self,html):
        data = self.parseInfo(html)
        if "出演者" in data:
            return data["出演者"]
        else:
            return ""
    def getLabel(self,html):
        data = self.parseInfo(html)
        if "メーカー" in data:
            return data["メーカー"]
        else:
            return ""
    def getTag(self,html):
        data = self.parseInfo(html)
        if "ジャンル" in data:
            return data["ジャンル"]
        else:
            return ""
    def getStudio(self,html):
        data = self.parseInfo(html)
        if "メーカー" in data:
            return data["メーカー"]
        else:
            return ""
    def getNum(self,html):
        data = self.parseInfo(html)
        if "品番" in data:
            return data["品番"]
        else:
            return ""
    def getRelease(self,html):
        data = self.parseInfo(html)
        if "配信開始日" in data:
            return data["配信開始日"]
        else:
            return ""
    def getRuntime(self,html):
        data = self.parseInfo(html)
        if "収録時間" in data:
            return data["収録時間"]
        else:
            return ""
    def getYear(self,html):
        data = self.parseInfo(html)
        if "release" in data:
            return data["release"][:4]
        else:
            return ""
    def getSeries(self,html):
        data = self.parseInfo(html)
        if "シリーズ" in data:
            return data["シリーズ"]
        else:
            return ""
    def getWebsite(self,html):
        element_html = etree.tostring(html,encoding="unicode")
        web = re.compile("this.page.url = (.*);")
        webline = web.findall(element_html)
        if webline:
            webline = webline[0]
        if not webline:
            return ''
        return webline
    def getMagnetLink(self,html):
        elements = html.xpath('//table[@class="table table-striped"]/tr')
        video_lists = []
        for element in elements:
            #print(etree.tostring(element))
            info = VideoDownloadInfo()
            a = element.findall("./td/a")
            if a:
                info["magnetlink"] = a[0].attrib["href"]
                #print(element.attrib['onclick'])
                for text in element.itertext():
                    if re.findall("GB",text):
                        info["size"] = re.findall(".+GB",text)[0]
                        video_lists.append(info)

        if not video_lists:
            return ""
        else:
            # video_lists = sorted(video_lists,key = lambda i:(i["isChn"],i["isHD"],i["date"],i["size"]),reverse=True)
            video_lists = video_lists
        return video_lists
    def main(self,number):
        self.fx = firefox()
        htmlcode = self.fx.post_html(url="https://www.jav321.com/search", data={"sn": number})
        #print(htmlcode)
        self.lx = etree.fromstring(htmlcode,etree.HTMLParser())
        self.getVideoInfo(self.lx)
        self.info['website'] = self.getWebsite(self.lx)
        self.info['source'] = self.getWebsite(self.lx)
        htmlcode = self.fx.post_html(url="https://www.jav321.com/emule", data={"sn": number})
        return self.info


if __name__ == "__main__":
    jav = Jav321()
    #print(jav.main("jul-404"))
    #print(jav.main( "FC2-2125351"))
