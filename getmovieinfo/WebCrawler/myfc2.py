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

class Fc2(getVideoInfoBase):
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()

    def getTitle(self,html): #获取厂商
        elements = html.xpath('//div[@class="items_article_headerInfo"]/h3/text()')
        if elements:
            result = elements[0]
            return result
        else:
            return ''
    def getActor(self,html):
        try:
            result = html.xpath('//*[@id="top"]/div[1]/section[1]/div/section/div[2]/ul/li[3]/a/text()')[0]
            return result
        except:
            return ''
    def getStudio(self,html): #获取厂商
        try:
            result = str(html.xpath('//*[@id="top"]/div[1]/section[1]/div/section/div[2]/ul/li[3]/a/text()')).strip(" ['']")
            return result
        except:
            return ''
    def getNum(self,html):     #获取番号
        result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[1]/span[2]/text()')).strip(" ['']")
        return result
    def getRelease(self,html): #
        result = str(html.xpath('//*[@id="top"]/div[1]/section[1]/div/section/div[2]/div[2]/p/text()')).strip(" ['販売日 : ']").replace('/','-')
        return result
    def getCover(self,html): #获取厂商 #
        cover = str(html.xpath("//div[@class='items_article_MainitemThumb']/span/img/@src")).strip(" ['']")
        #result = str(html.xpath('//*[@id="top"]/div[1]/section[1]/div/section/div[1]/span/img/@src')).strip(" ['']")
        cover = urljoin('https://adult.contents.fc2.com', cover)
        return cover
    # def getOutline(htmlcode2):     #获取番号 #
    #     xpath_html = etree.fromstring(htmlcode2, etree.HTMLParser())
    #     path = str(xpath_html.xpath('//*[@id="top"]/div[1]/section[4]/iframe/@src')).strip(" ['']")
    #     html = etree.fromstring(ADC_function.get_html('https://adult.contents.fc2.com/'+path), etree.HTMLParser())
    #     print('https://adult.contents.fc2.com'+path)
    #     print(ADC_function.get_html('https://adult.contents.fc2.com'+path,cookies={'wei6H':'1'}))
    #     result = str(html.xpath('/html/body/div/text()')).strip(" ['']").replace("\\n",'',10000).replace("'",'',10000).replace(', ,','').strip('  ').replace('。,',',')
    #     return result
    def getTag(self,html):
        result = html.xpath("//a[@class='tag tagTag']/text()")
        return result
    def getYear(self,html):
        try:
            result = re.search('\d{4}',self.getRelease(html)).group()
            return result
        except:
            return ''

    def getExtrafanart(self,html):  # 获取剧照
        elements = html.xpath('//ul[@class="items_article_SampleImagesArea"]')
        imgs = []
        if elements:
            for a in elements[0].findall(".//img"):
                imgs.append(a.attrib["src"])
        if not imgs:
            return ''
        return imgs


    def getTrailer(self,html, number=""):
        video_pather = re.compile(r'\'[a-zA-Z0-9]{32}\'')
        video = video_pather.findall(self,html)
        if video:
            try:
                video_url = video[0].replace('\'', '')
                video_url = 'https://adult.contents.fc2.com/api/v2/videos/' + number + '/sample?key=' + video_url
                url_json = eval(ADC_function.get_html(video_url))['path'].replace('\\', '')
                return url_json
            except:
                return ''
        else:
            video_url = ''

    def main(self,number):
        self.fx = firefox()
        number = number.replace('FC2-', '').replace('fc2-', '')
        url = 'https://adult.contents.fc2.com/article/' + number + '/'
        htmlcode = self.fx.get_html(url,time =1)
        self.lx = etree.fromstring(htmlcode,etree.HTMLParser())
        #print(htmlcode)
        #print(url)
        actor = self.getActor(self.lx)
        self.getVideoInfo(self.lx)
        self.info['website'] = 'https://adult.contents.fc2.com/article/' + number + '/'
        self.info['source'] = 'https://adult.contents.fc2.com/article/' + number + '/'
        return self.info


if __name__ == '__main__':
    fc = Fc2()
    #print(fc.main('FC2-1787685'))
    print(fc.main('FC2-2086710'))

