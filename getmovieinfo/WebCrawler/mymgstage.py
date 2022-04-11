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

class Mgstage(getVideoInfoBase):
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()

    def getTitle(self,html):
        try:
            result = str(html.xpath('//*[@id="center_column"]/div[1]/h1/text()')).strip(" ['']")
            return result.replace('/', ',')
        except:
            return ''
    def getActor(self,html): #//*[@id="center_column"]/div[2]/div[1]/div/table/tbody/tr[1]/td/text()
        result1=str(html.xpath('//th[contains(text(),"出演：")]/../td/a/text()')).strip(" ['']").strip('\\n    ').strip('\\n')
        result2=str(html.xpath('//th[contains(text(),"出演：")]/../td/text()')).strip(" ['']").strip('\\n    ').strip('\\n')
        return str(result1+result2).strip('+').replace("', '",'').replace('"','').replace('/',',')
    def getStudio(self,html):
        result1=str(html.xpath('//th[contains(text(),"メーカー：")]/../td/a/text()')).strip(" ['']").strip('\\n    ').strip('\\n')
        result2=str(html.xpath('//th[contains(text(),"メーカー：")]/../td/text()')).strip(" ['']").strip('\\n    ').strip('\\n')
        return str(result1+result2).strip('+').replace("', '",'').replace('"','')
    def getRuntime(self,html):
        result1 = str(html.xpath('//th[contains(text(),"収録時間：")]/../td/a/text()')).strip(" ['']").strip('\\n    ').strip('\\n')
        result2 = str(html.xpath('//th[contains(text(),"収録時間：")]/../td/text()')).strip(" ['']").strip('\\n    ').strip('\\n')
        return str(result1 + result2).strip('+').rstrip('mi')
    def getLabel(self,html):
        result1 = str(html.xpath('//th[contains(text(),"シリーズ：")]/../td/a/text()')).strip(" ['']").strip('\\n    ').strip(
            '\\n')
        result2 = str(html.xpath('//th[contains(text(),"シリーズ：")]/../td/text()')).strip(" ['']").strip('\\n    ').strip(
            '\\n')
        return str(result1 + result2).strip('+').replace("', '",'').replace('"','')
    def getNum(self,html):
        result1 = str(html.xpath('//th[contains(text(),"品番：")]/../td/a/text()')).strip(" ['']").strip('\\n    ').strip(
            '\\n')
        result2 = str(html.xpath('//th[contains(text(),"品番：")]/../td/text()')).strip(" ['']").strip('\\n    ').strip(
            '\\n')
        return str(result1 + result2).strip('+')
    def getRelease(self,html):
        result1 = str(html.xpath('//th[contains(text(),"配信開始日：")]/../td/a/text()')).strip(" ['']").strip('\\n    ').strip(
            '\\n')
        result2 = str(html.xpath('//th[contains(text(),"配信開始日：")]/../td/text()')).strip(" ['']").strip('\\n    ').strip(
            '\\n')
        return str(result1 + result2).strip('+').replace('/','-')

    def getYear(self,html):
        try:
            result = str(re.search('\d{4}',self.getRelease(html)).group())
            return result
        except:
            return ''
    def getTag(self,html):
        result1 = str(html.xpath('//th[contains(text(),"ジャンル：")]/../td/a/text()')).strip(" ['']").strip('\\n    ').strip(
            '\\n')
        result2 = str(html.xpath('//th[contains(text(),"ジャンル：")]/../td/text()')).strip(" ['']").strip('\\n    ').strip(
            '\\n')
        result = str(result1 + result2).strip('+').replace("', '\\n",",").replace("', '","").replace('"','').replace(',,','').split(',')
        return result
    def getCover(self,html):
        result = str(html.xpath('//*[@id="EnlargeImage"]/@href')).strip(" ['']")
        # result = str(html.xpath('//*[@id="center_column"]/div[1]/div[1]/div/div/h2/img/@src')).strip(" ['']")
        #                    /html/body/div[2]/article[2]/div[1]/div[1]/div/div/h2/img/@src
        return result
    def getDirector(self,html):
        result1 = str(html.xpath('//th[contains(text(),"シリーズ")]/../td/a/text()')).strip(" ['']").strip('\\n    ').strip(
            '\\n')
        result2 = str(html.xpath('//th[contains(text(),"シリーズ")]/../td/text()')).strip(" ['']").strip('\\n    ').strip(
            '\\n')
        return str(result1 + result2).strip('+').replace("', '",'').replace('"','')
    def getOutline(self,html):
        result = str(html.xpath('//p/text()')).strip(" ['']").replace(u'\\n', '').replace("', '', '", '')
        return result
    def getSeries(self,html):
        result1 = str(html.xpath('//th[contains(text(),"シリーズ")]/../td/a/text()')).strip(" ['']").strip('\\n    ').strip(
            '\\n')
        result2 = str(html.xpath('//th[contains(text(),"シリーズ")]/../td/text()')).strip(" ['']").strip('\\n    ').strip(
            '\\n')
        return str(result1 + result2).strip('+').replace("', '", '').replace('"', '')

    def getExtrafanart(self,html):  # 获取剧照
        elements = html.xpath('//dl[@id="sample-photo"]')
        print(elements)
        imgs = []
        if elements:
            for a in elements[0].findall(".//a[@class='sample_image']"):
                imgs.append(a.attrib["href"])
                
        #print(imgs)
        if not imgs:
            return ''
        return imgs

    def main(self,number):
        number=number.upper()
        self.fx = firefox()
        url  = 'https://www.mgstage.com/product/product_detail/'+str(number)+'/'
        #print(url)
        htmlcode=self.fx.get_html(url,time=1,cookies={"name": "adc","value": "1"})
        #print(htmlcode)
        print(url)
        self.lx = etree.fromstring(htmlcode,etree.HTMLParser())
        self.getVideoInfo(self.lx)
        return self.info
        

if __name__ == '__main__':
    jav = Mgstage()
    #print(jav.main('SIRO-4149'))
    print(jav.main('SSIS-313'))
