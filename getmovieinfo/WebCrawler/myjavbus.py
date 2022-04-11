import os
import sys
sys.path.append('../..')
from abc import abstractmethod, ABCMeta
from .htmlclass import *
from .firefox import firefox
#import test
from lxml import etree#nimport re
import pprint
from urllib.parse import urljoin
import inspect
import re
import secrets

class Javbus(getVideoInfoBase):
      __metaclass__ = ABCMeta

      def __init__(self):
            super().__init__()
            

      def getMagnetLink(self,html):
            elements = html.xpath('//tr[@onmouseover]')
            video_lists = []
            for element in elements:
                  #print(etree.tostring(element))
                  info = VideoDownloadInfo()
                  a = element.findall("./td/a[@rel]")
                  if a :
                        info["magnetlink"] = a[0].attrib["href"]
                        #print(element.attrib['onclick'])
                        for text in element.itertext():
                              if re.findall("高清",text):
                                    info["isHD"] = 1
                              if re.findall("字幕",text):
                                    info["isChn"] = 1
                              if re.findall("GB",text):
                                    info["size"] = re.findall(".+GB",text)[0]
                              if re.findall("\d+-\d+-\d+",text):
                                    info["date"] = re.findall("\d+-\d+-\d+",text)[0]
                        video_lists.append(info)

            if not video_lists:
                  return ""
            else:
                  video_lists = sorted(video_lists,key = lambda i:(i["isChn"],i["isHD"],i["date"]),reverse=True)
                  return video_lists

      def getActorPhoto(self,html):
          actors = html.xpath('//div[@class="star-name"]/a')
          d={}
          for i in actors:
              url=i.attrib['href']
              t=i.attrib['title']
              html = etree.fromstring(self.fx.get_html(url), etree.HTMLParser())
              p=urljoin("https://www.javbus.com",
                        str(html.xpath('//*[@id="waterfall"]/div[1]/div/div[1]/img/@src')).strip(" ['']"))
              p2={t:p}
              d.update(p2)
          return d
      def getTitle(self,html):  #获取标题
            title = str(html.xpath('/html/head/title/text()')[0])
            title = str(re.findall('^.+?\\s+(.*) - JavBus$', title)[0]).strip()
            return title
      def getStudioJa(self,html):
            x = html.xpath('//span[contains(text(),"メーカー:")]/../a/text()')
            return str(x[0]) if len(x) else ''
      def getStudio(self,html): #获取厂商
            x = html.xpath('//span[contains(text(),"製作商:")]/../a/text()')
            return str(x[0]) if len(x) else ''
      def getYear(self,html):   #获取年份
            result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[2]/text()')).strip(" ['']").strip()
            return result[:4] if len(result)>=len('2000-01-01') else ''
      def getCover(self,html):  #获取封面链接
            image = html.xpath('//a[@class="bigImage"]/@href')
            if image:
                  image = str([0])
                  return urljoin("https://www.javbus.com", image)
            else:
                  return ''
      def getRelease(self,html): #获取出版日期
          result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[2]/text()')).strip(" ['']")
          return result
      def getRuntime(self,html): #获取分钟 已修改
          result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[3]/text()')).strip(" ['']分鐘")
          return result
      def getActor(self,html):   #获取女优
          b=[]
          actors = html.xpath('//div[@class="star-name"]/a')
          for i in actors:
              b.append(i.attrib['title'])
          return b
      def getNum(self,html):     #获取番号
          kwdlist = html.xpath('/html/head/meta[@name="keywords"]/@content')[0].split(',')
          return kwdlist[0]
      def getDirectorJa(self,html):
          x = html.xpath('//span[contains(text(),"監督:")]/../a/text()')
          return str(x[0]) if len(x) else ''
      def getDirector(self,html): #获取导演
          x = html.xpath('//span[contains(text(),"導演:")]/../a/text()')
          return str(x[0]) if len(x) else ''
      def getCID(self,html):
          string = html.xpath("//a[contains(@class,'sample-box')][1]/@href")[0].replace('https://pics.dmm.co.jp/digital/video/','')
          result = re.sub('/.*?.jpg','',string)
          return result
      def getOutline(self,html):  #获取剧情介绍 多进程并发查询
            return ""
      def getSeriseJa(self,html):
          x = html.xpath('//span[contains(text(),"シリーズ:")]/../a/text()')
          return str(x[0]) if len(x) else ''
      def getSeries(self,html):   #获取系列
          x = html.xpath('//span[contains(text(),"系列:")]/../a/text()')
          return str(x[0]) if len(x) else ''
      def getTag(self,html):  # 获取标签
          klist = html.xpath('/html/head/meta[@name="keywords"]/@content')[0].split(',')
          return klist[1:]
      def getExtrafanart(self,html):  # 获取剧照
            elements = html.xpath('//div[@id="sample-waterfall"]')
            imgs = []
            if elements:
                  for a in elements[0].findall(".//img"):
                        imgs.append(urljoin('https://www.javbus.com',a.attrib["src"]))

            #print(imgs)
            if not imgs:
                  return ''
            return imgs
            
      def main(self,number):
            self.info['source'] = "javbus.py"
            self.info['website'] = urljoin("https://www.javbus.com/",number)
            self.fx = firefox()
            self.urlbase = "https://www." + secrets.choice([
                'buscdn.fun', 'busdmm.fun', 'busfan.fun', 'busjav.fun',
                'cdnbus.fun',
                'dmmbus.fun', 'dmmsee.fun',
                'fanbus.us',
                'seedmm.fun',
            ])
            url = self.urlbase + "/" +number
            #print(url)
            #wait_for = "//a[@rel][@title]"
            htmlcode = self.fx.get_html(url,time =1)
            #print(htmlcode)
            self.lx = etree.fromstring(htmlcode,etree.HTMLParser())
            self.getVideoInfo(self.lx)
            return self.info

      def getUrls(self, html):
            pagination = html.xpath("//ul[@class=\"pagination pagination-lg\"]")
            urls = []
            if pagination:
                  for page in pagination[0].findall(".//a[@href]"):
                        urls.append(self.urlbase + page.attrib["href"])
            n = 3 if len(urls) >=3 else len(urls)
            return urls[0:(n-1)]

      def getVideoList(self,html):
            elements = html.xpath('//a[@class="movie-box"]')
            if elements:
                  for element in elements:
                        info = VideoInfo()
                        id = element.findall('.//date')
                        if id:
                              info["website"] = self.urlbase + element.attrib['href']
                              info["number"] = id[0].text
                              cover = element.findall(".//img")
                              if cover:
                                    info["cover"] = self.urlbase + cover[0].attrib['src']
                                    info["title"] = cover[0].attrib['title']
                        self.videoList.append(info)

      def search(self,keyword):
            self.info['source'] = "javbus.py"
            self.info['website'] = urljoin("https://www.javbus.com/search/",keyword)
            self.fx = firefox()
            self.urlbase = "https://www." + secrets.choice([
                'buscdn.fun', 'busdmm.fun', 'busfan.fun', 'busjav.fun',
                'cdnbus.fun',
                'dmmbus.fun', 'dmmsee.fun',
                'fanbus.us',
                'seedmm.fun',
            ])
            url = self.urlbase + "/search/" + keyword
            #wait_for = "//a[@rel][@title]"
            htmlcode = self.fx.get_html(url,time =1)
            #print(htmlcode)
            self.lx = etree.fromstring(htmlcode,etree.HTMLParser())

      def searchKeyword(self,keyword):
            self.search(keyword)
            self.videoList = []
            urls = self.getUrls(self.lx)
            if urls:
                  for url in urls:
                        htmlcode = self.fx.get_html(url,time = 1)
                        lx = etree.fromstring(htmlcode,etree.HTMLParser())
                        self.getVideoList(lx)
            else:
                  self.getVideoList(self.lx)
                  return self.videoList


if __name__ == "__main__":
      jav = Javbus()
      info = jav.main("SSIS-313")
      print(info)
      # jb = JavBus()
      # info = jb.main("SSIS-356")
      # print(info)
      #jav.searchKeyword("三上悠亜")
        
