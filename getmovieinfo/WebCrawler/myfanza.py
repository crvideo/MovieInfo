# -*- coding: utf-8 -*-
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
from urllib.parse import urljoin, urlencode
import inspect

import secrets

# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors = 'replace', line_buffering = True)

class Fanza(getVideoInfoBase):
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()

    def getTitle(self,html):
        result = html.xpath('//*[starts-with(@id, "title")]/text()')[0]
        return result
    def getActor(self,html):
        # //*[@id="center_column"]/div[2]/div[1]/div/table/tbody/tr[1]/td/text()
        result = (
            str(
                html.xpath(
                    "//td[contains(text(),'出演者')]/following-sibling::td/span/a/text()"
                )
            )
            .strip(" ['']")
            .replace("', '", ",")
        )
        return result


    def getStudio(self,html):
        try:
            result = html.xpath(
                "//td[contains(text(),'メーカー')]/following-sibling::td/a/text()"
            )[0]
        except:
            result = html.xpath(
                "//td[contains(text(),'メーカー')]/following-sibling::td/text()"
            )[0]
        return result


    def getRuntime(self,html):
        result = html.xpath("//td[contains(text(),'収録時間')]/following-sibling::td/text()")[0]
        return re.search(r"\d+", str(result)).group()


    def getLabel(self,html):
        try:
            result = html.xpath(
                "//td[contains(text(),'レーベル：')]/following-sibling::td/a/text()"
            )[0]
        except:
            result = html.xpath(
                "//td[contains(text(),'レーベル：')]/following-sibling::td/text()"
            )[0]
        return result


    def getNum(self,html):
        try:
            result = html.xpath(
                "//td[contains(text(),'品番：')]/following-sibling::td/a/text()"
            )[0]
        except:
            result = html.xpath(
                "//td[contains(text(),'品番：')]/following-sibling::td/text()"
            )[0]
        return result


    def getYear(self,html):
        try:
            result = str(re.search(r"\d{4}", self.getRelease(html)).group())
            return result
        except:
            return self.getRelease(html)


    def getRelease(self,html):
        try:
            result = html.xpath(
                "//td[contains(text(),'発売日：')]/following-sibling::td/a/text()"
            )[0].lstrip("\n")
        except:
            try:
                result = html.xpath(
                    "//td[contains(text(),'発売日：')]/following-sibling::td/text()"
                )[0].lstrip("\n")
            except:
                result = "----"
        if result == "----":
            try:
                result = html.xpath(
                    "//td[contains(text(),'配信開始日：')]/following-sibling::td/a/text()"
                )[0].lstrip("\n")
            except:
                try:
                    result = html.xpath(
                        "//td[contains(text(),'配信開始日：')]/following-sibling::td/text()"
                    )[0].lstrip("\n")
                except:
                    pass
        return result.replace("/", "-")


    def getTag(self,html):
        try:
            result = html.xpath(
                "//td[contains(text(),'ジャンル：')]/following-sibling::td/a/text()"
            )
            return result
        except:
            result = html.xpath(
                "//td[contains(text(),'ジャンル：')]/following-sibling::td/text()"
            )
            return result


    def getCover(self,html):
        cover_number = self.getNum(html)
        try:
            result = html.xpath('//*[@id="' + cover_number + '"]/@href')[0]
        except:
            # sometimes fanza modify _ to \u0005f for image id
            if "_" in cover_number:
                cover_number = cover_number.replace("_", r"\u005f")
            try:
                result = html.xpath('//*[@id="' + cover_number + '"]/@href')[0]
            except:
                # (TODO) handle more edge case
                # print(html)
                # raise exception here, same behavior as before
                # people's major requirement is fetching the picture
                raise ValueError("can not find image")
        return result


    def getDirector(self,html):
        try:
            result = html.xpath(
                "//td[contains(text(),'監督：')]/following-sibling::td/a/text()"
            )[0]
        except:
            result = html.xpath(
                "//td[contains(text(),'監督：')]/following-sibling::td/text()"
            )[0]
        return result


    def getOutline(self,html):
        try:
            result = str(html.xpath("//div[@class='mg-b20 lh4']/text()")[0]).replace(
                "\n", ""
            )
            if result == "":
                result = str(html.xpath("//div[@class='mg-b20 lh4']//p/text()")[0]).replace(
                    "\n", ""
                )
        except:
            # (TODO) handle more edge case
            # print(html)
            return ""
        return result


    def getSeries(self,html):
        try:
            try:
                result = html.xpath(
                    "//td[contains(text(),'シリーズ：')]/following-sibling::td/a/text()"
                )[0]
            except:
                result = html.xpath(
                    "//td[contains(text(),'シリーズ：')]/following-sibling::td/text()"
                )[0]
            return result
        except:
            return ""

    def getExtrafanart(self,html):  # 获取剧照
        elements = html.xpath('//div[@id="sample-image-block"]')
        imgs = []
        if elements:
            for a in elements[0].findall(".//img"):
                imgs.append(a.attrib["src"])

            #print(imgs)
        if not imgs:
            return ''
        return imgs


    def main(self,number):
        # fanza allow letter + number + underscore, normalize the input here
        # @note: I only find the usage of underscore as h_test123456789
        fanza_search_number = number
        # AV_Data_Capture.py.getNumber() over format the input, restore the h_ prefix
        if fanza_search_number.startswith("h-"):
            fanza_search_number = fanza_search_number.replace("h-", "h_")

        fanza_search_number = re.sub(r"[^0-9a-zA-Z_]", "", fanza_search_number).lower()

        fanza_urls = [
            "https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=",
            "https://www.dmm.co.jp/mono/dvd/-/detail/=/cid=",
            "https://www.dmm.co.jp/digital/anime/-/detail/=/cid=",
            "https://www.dmm.co.jp/mono/anime/-/detail/=/cid=",
            "https://www.dmm.co.jp/digital/videoc/-/detail/=/cid=",
            "https://www.dmm.co.jp/digital/nikkatsu/-/detail/=/cid=",
            "https://www.dmm.co.jp/rental/-/detail/=/cid=",
        ]
        chosen_url = ""
        self.fx = firefox()
        for url in fanza_urls:
            chosen_url = url + fanza_search_number
            htmlcode = self.fx.get_html(
                "https://www.dmm.co.jp/age_check/=/declared=yes/?{}".format(
                    urlencode({"rurl": chosen_url})
                )
            )
            if "404 Not Found" not in htmlcode:
                break
        if "404 Not Found" in htmlcode:
            return json.dumps({"title": "",})
        #print(htmlcode)
        self.lx = etree.fromstring(htmlcode,etree.HTMLParser())
        self.getVideoInfo(self.lx)
        #print(chosen_url)
        self.info['source'] = "fanza.py"
        self.info['website'] = chosen_url
        return self.info



if __name__ == "__main__":
    # print(main("DV-1562"))
    # print(main("96fad1217"))
    fz = Fanza()
    print(fz.main("pred00251"))
