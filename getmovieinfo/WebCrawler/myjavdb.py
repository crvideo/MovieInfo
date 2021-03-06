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

class Javdb(getVideoInfoBase):
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()

    def getMagnetLink(self,html):
        elements = html.xpath('//td[@class="magnet-name"]')
        video_lists = []
        for element in elements:
            #print(etree.tostring(element))
            info = VideoDownloadInfo()
            a = element.findall("./a[@href]")
            if a :
                info["magnetlink"] = a[0].attrib["href"]
                #print(element.attrib['onclick'])
                for text in element.itertext():
                    if re.findall("HD",text):
                        info["isHD"] = 1
                    if re.findall("GB",text):
                        info["size"] = re.findall("[0-9\.]+GB",text)[0]
                video_lists.append(info)

            if not video_lists:
                return ""
            else:
                video_lists = sorted(video_lists,key = lambda i:(i["isHD"],i["size"]),reverse=True)
        return video_lists


    def getTitle(self,html):
        browser_title = str(html.xpath("/html/head/title/text()")[0])
        return browser_title[:browser_title.find(' | JavDB')].strip()
    def getActor(self,html):
        actors = html.xpath('//span[@class="value"]/a[contains(@href,"/actors/")]/text()')
        genders = html.xpath('//span[@class="value"]/a[contains(@href,"/actors/")]/../strong/@class')
        r = []
        idx = 0
        actor_gendor = "female" # only female
        if not actor_gendor in ['female','male','both','all']:
            actor_gendor = 'female'
        for act in actors:
            if((actor_gendor == 'all')
            or (actor_gendor == 'both' and genders[idx] in ['symbol female', 'symbol male'])
            or (actor_gendor == 'female' and genders[idx] == 'symbol female')
            or (actor_gendor == 'male' and genders[idx] == 'symbol male')):
                r.append(act)
            idx = idx + 1
        return r

    def getaphoto(url, session):
        html_page = session.get(url).text if session is not None else get_html(url)
        img_prether = re.compile(r'<span class\=\"avatar\" style\=\"background\-image\: url\((.*?)\)')
        img_url = img_prether.findall(html_page)
        if img_url:
            return img_url[0]
        else:
            return ''

    def getActorPhoto(self,html, javdb_site, session):
        actorall = html.xpath('//strong[re:match(text(),"??????:|Actor(s)")]/../span/a[starts-with(@href,"/actors/")]')
        if not actorall:
            return {}
        a = getActor(html)
        actor_photo = {}
        for i in actorall:
            if i.text in a:
                actor_photo[i.text] = getaphoto(urljoin(f'https://{javdb_site}.com', i.attrib['href']), session)
        return actor_photo

    def getStudio(self,html):
        # html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
        # result1 = str(html.xpath('//strong[contains(text(),"??????")]/../span/text()')).strip(" ['']")
        # result2 = str(html.xpath('//strong[contains(text(),"??????")]/../span/a/text()')).strip(" ['']")
        # return str(result1 + result2).strip('+').replace("', '", '').replace('"', '')
        a = etree.tostring(html,encoding="unicode")
        patherr = re.compile(r'<strong>(??????|Maker)\:</strong>[\s\S]*?<a href=\".*?>(.*?)</a></span>')
        pianshang = patherr.findall(a)
        if pianshang:
            result = pianshang[0][1].strip()
            if len(result):
                return result
        # ????????????????????????
        try:
            result = str(html.xpath('//strong[contains(text(),"??????:")]/../span/a/text()')).strip(" ['']")
        except:
            result = ''
        return result

    def getRuntime(self,html):
        result1 = str(html.xpath('//strong[re:match(text(),"??????|Duration")]/../span/text()')).strip(" ['']")
        result2 = str(html.xpath('//strong[re:match(text(),"??????|Duration")]/../span/a/text()')).strip(" ['']")
        return str(result1 + result2).strip('+').rstrip('mi')
    def getLabel(self,html):
        result1 = str(html.xpath('//strong[re:match(text(),"??????|Series")]/../span/text()')).strip(" ['']")
        result2 = str(html.xpath('//strong[re:match(text(),"??????|Series")]/../span/a/text()')).strip(" ['']")
        return str(result1 + result2).strip('+').replace("', '", '').replace("\"", '')
    def getNum(self,html):
        result1 = str(html.xpath('//strong[re:match(text(),"??????|ID:")]/../span/text()')).strip(" ['']")
        result2 = str(html.xpath('//strong[re:match(text(),"??????|ID:")]/../span/a/text()')).strip(" ['']")
        return str(result2 + result1).strip('+')
    def getYear(self,html):
        # try:
        #     result = str(re.search('\d{4}', getRelease).group())
        #     return result
        # except:
        #     return getRelease
        a = etree.tostring(html,encoding="unicode")
        patherr = re.compile(r'<strong>(??????|Released Date)\:</strong>\s*?.*?<span class="value">(.*?)\-.*?</span>')
        dates = patherr.findall(a)
        if dates:
            result = dates[0][1]
        else:
            result = ''
        return result

    def getRelease(self,html):
        # html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
        # result1 = str(html.xpath('//strong[contains(text(),"??????")]/../span/text()')).strip(" ['']")
        # result2 = str(html.xpath('//strong[contains(text(),"??????")]/../span/a/text()')).strip(" ['']")
        # return str(result1 + result2).strip('+')
        a = etree.tostring(html,encoding="unicode")
        patherr = re.compile(r'<strong>(??????|Released Date)\:</strong>\s*?.*?<span class="value">(.*?)</span>')
        dates = patherr.findall(a)
        if dates:
            result = dates[0][1]
        else:
            result = ''
        return result
    def getTag(self,html):
        try:
            result = html.xpath('//strong[re:match(text(),"??????|Tags")]/../span/a/text()')
            return result
        except:
            result = html.xpath('//strong[re:match(text(),"??????|Tags")]/../span/text()')
            return result

    def getCover_small(self,html, index=0):
        # same issue mentioned below,
        # javdb sometime returns multiple results
        # DO NOT just get the firt one, get the one with correct index number
        try:
            result = html.xpath("//div[@class='item-image fix-scale-cover']/img/@src")[index]
            if not 'https' in result:
                result = 'https:' + result
            return result
        except: # 2020.7.17 Repair Cover Url crawl
            try:
                result = html.xpath("//div[@class='item-image fix-scale-cover']/img/@data-src")[index]
                if not 'https' in result:
                    result = 'https:' + result
                return result
            except:
                result = html.xpath("//div[@class='item-image']/img/@data-src")[index]
                if not 'https' in result:
                    result = 'https:' + result
                return result


    def getTrailer(self,html):  # ???????????????
        video_pather = re.compile(r'<video id\=\".*?>\s*?<source src=\"(.*?)\"')
        video = video_pather.findall(htmlcode)
        # ??????????????????
        if video and video[0] != "":
            if not 'https:' in video[0]:
                video_url = 'https:' + video[0]
            else:
                video_url = video[0]
        else:
            video_url = ''
        return video_url

    def getExtrafanart(self,html):  # ????????????
        result = []
        try:
            result = html.xpath("//article[@class='message video-panel']/div[@class='message-body']/div[@class='tile-images preview-images']/a[contains(@href,'/samples/')]/@href")
        except:
            pass
        return result
    def getCover(self,html):
        result = ''
        try:
            res = html.xpath("//div[contains(@class, 'column-video-cover')]/a/img/@src")
            if res:
                result =  res[0]
        except: # 2020.7.17 Repair Cover Url crawl
            res = html.xpath("//div[contains(@class, 'column-video-cover')]/img/@src")
            if res:
                result =  res[0]
        return result
    def getDirector(self,html):
        result1 = str(html.xpath('//strong[re:match(text(),"??????|Director")]/../span/text()')).strip(" ['']")
        result2 = str(html.xpath('//strong[re:match(text(),"??????|Director")]/../span/a/text()')).strip(" ['']")
        return str(result1 + result2).strip('+').replace("', '", '').replace("\"", '')
    def getOutline(self,html):  #?????????????????? ?????????????????????
        return ""
    def getSeries(self,html):
        result1 = str(html.xpath('//strong[re:match(text(),"??????|Series")]/../span/text()')).strip(" ['']")
        result2 = str(html.xpath('//strong[re:match(text(),"??????|Series")]/../span/a/text()')).strip(" ['']")
        return str(result1 + result2).strip('+').replace("', '", '').replace("\"", '')

    def main(self,number):
        # javdb?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????javdb*.json?????????????????????
        # ?????????.json????????????????????????????????????????????????????????????
        javdb_sites = [""]
        for i in javdb_sites:
            javdb_sites[javdb_sites.index(i)] = "javdb" + i
        javdb_sites.append("javdb")
        ## print(javdb_sites)
        javdb_site = secrets.choice(javdb_sites)
        #print(f'[!]javdb:select site {javdb_site}')
        javdb_url = 'https://' + javdb_site + '.com/search?q=' + number + '&f=all'
        self.fx = firefox()
        htmlcode = self.fx.get_html(url = javdb_url, time = 1)
        #print(htmlcode)
        #print(javdb_url)
        html = etree.fromstring(htmlcode, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
        # javdb sometime returns multiple results,
        # and the first elememt maybe not the one we are looking for
        # iterate all candidates and find the match one
        urls = html.xpath('//*[@id="videos"]/div/div/a/@href')
        # ?????????????????????ids  ['Blacked','Blacked']
        if re.search(r'[a-zA-Z]+\.\d{2}\.\d{2}\.\d{2}', number):
            correct_url = urls[0]
        else:
            ids = html.xpath('//*[@id="videos"]/div/div/a/div[contains(@class, "uid")]/text()')
            #print(ids)
            try:
                correct_url = urls[ids.index(number)]
            except:
                # ?????????????????????????????????????????????????????????
                if ids[0].upper() != number:
                    raise ValueError("number not found")
        # get faster benefit from http keep-alive
        # print(correct_url)
        javdb_detail_url = 'https://' + javdb_site + '.com' + correct_url
        # print(javdb_detail_url)
        detail_page = self.fx.get_html(javdb_detail_url,time = 1)
        # etree.fromstring?????????????????????????????????????????????xpath????????????bs4 find/select??????????????????
        #print(detail_page)
        self.lx = etree.fromstring(detail_page, etree.HTMLParser())
        #no cut image by default
        #If gray image exists ,then replace with normal cover
        self.getVideoInfo(self.lx)
        return self.info

    def getUrls(self, html):
        pagination = html.xpath("//ul[@class=\"pagination-list\"]")
        #print(pagination)
        urls = []
        if pagination:
            pages = pagination[0].findall('.//a[@class="pagination-link"]')
            #print(pages)
            if pages:
                for page in pages:
                    #print(page)
                    urls.append(self.urlbase + page.attrib["href"])
        #print(urls)
        ## only return three pages
        n = 3 if len(urls) >=3 else len(urls)
        return urls[0:(n-1)]

    def getVideoList(self,html):
        elements = html.xpath('//div[contains(@class,"grid-item column")]')
        if elements:
            for element in elements:
                info = VideoInfo()
                id = element.findall('.//div[@class="uid"]')
                if id:
                    info["number"] = id[0].text
                title = element.findall('.//a[@href][@class="box"][@title]')
                if title:
                    info["website"] = self.urlbase + title[0].attrib['href']
                    info["title"] = title[0].attrib['title']
                cover = element.findall(".//img")
                if cover:
                    info["cover"] = cover[0].attrib['data-src']
                    self.videoList.append(info)

    def search(self,keyword):
        javdb_sites = ["33","34"]
        for i in javdb_sites:
            javdb_sites[javdb_sites.index(i)] = "javdb" + i
        javdb_sites.append("javdb")
        ## print(javdb_sites)
        javdb_site = secrets.choice(javdb_sites)
        #print(f'[!]javdb:select site {javdb_site}')
        self.fx = firefox()
        self.urlbase = 'https://' + javdb_site + '.com'
        url = self.urlbase +  '/search?q=' + keyword + '&f=all'
        #wait_for = "//a[@rel][@title]"
        htmlcode = self.fx.get_html(url,time =1)
        #print(htmlcode)
        #print(url)
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




# main('DV-1562')
# input("[+][+]Press enter key exit, you can check the error messge before you exit.\n[+][+]?????????????????????????????????????????????????????????????????????")
if __name__ == "__main__":
    jav = Javdb()
    # print(main('blacked.20.05.30'))
    #print(jav.main('AGAV-042'))
    print(jav.searchKeyword('????????????'))
    # print(main('BANK-022'))
    # print(main('070116-197'))
    # print(main('093021_539'))  # ???????????? ??????pacopacomama
    #print(main('FC2-2278260'))
    # print(main('FC2-735670'))
    # print(main('FC2-1174949')) # not found
    #print(main('MVSD-439'))
    # print(main('EHM0001')) # not found
    # print(jav.main('FC2-2314275'))
    # print(main('EBOD-646'))
    # print(main('LOVE-262'))
    #print(main('ABP-890'))
