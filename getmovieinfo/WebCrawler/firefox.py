import time
from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from lxml import etree#need install
import requests

class firefox(object):

    options = Options()
    options.headless = True

    def __init__(self):
        pass

    

    def get_html(self,url, wait_for= "",time = 10, firefox_locale = 'en-us',cookies=None):
        """
        开始爬虫
        :return:
        """

        # Set the locale
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("intl.accept_languages", firefox_locale)
        firefox_profile.update_preferences()
        self.options.profile = firefox_profile
        # get方式打开网页
        # url = "https://www.busdmm.fun/SSIS-356"
        #wait_for = "//a[@rel][@title]"
        self.driver = webdriver.Firefox(options=self.options)
        self.driver.implicitly_wait(time)

        self.driver.get(str(url))
        if cookies:
            self.driver.add_cookie(cookies)
            self.driver.get(str(url))
            
        if wait_for:
            element = WebDriverWait(self.driver,time).until(
                EC.presence_of_element_located((By.XPATH,wait_for))
            )

        self.page_source = self.driver.page_source
        self.driver.quit()
        return(self.page_source)
    
    def post_html(self,url, data, wait_for= "",time = 10, firefox_locale = 'en-us'):
        # Set the locale
        # get方式打开网页
        # url = "https://www.busdmm.fun/SSIS-356"
        #wait_for = "//a[@rel][@title]"
        self.response = requests.post(str(url),data=data)
        return(self.response.text)

        

# G_USER_AGENT = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
# url = "https://www.busdmm.fun/SSIS-313"
# baseurl = "https://www.busdmm.fun/SSIS-313"
# headers = {"user-Agent": G_USER_AGENT,
#            "referer": baseurl,
#            "x-requested-with": "XMLHttpRequest"}  # noqa
# result = requests.get(str(url), headers=headers)

# with open("tmp.html","w") as f:
#     f.write(result.text)
if __name__ == '__main__':
    # x = firefox()
    # url = "https://www.busdmm.fun/SSIS-356"
    # print(x.get_html(url))
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    myfx = Firefox(options=opts)
    url="https://www.jav321.com/search"
    response = myfx.request('POST',url,data = {"sn": "jul-404"})
    print(response.text)
    myfx.quit()
    
    
