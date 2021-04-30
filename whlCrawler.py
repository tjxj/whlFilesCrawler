import requests
from lxml import etree
import os
import subprocess


class AutoDownWhl:
    def __init__(self):
        # 包地址
        self.url = "https://www.lfd.uci.edu/~gohlke/pythonlibs/"
        # 下载地址
        self.base_url = "https://download.lfd.uci.edu/pythonlibs/w4tscw6k/"
        # 模拟浏览器
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36"
        }

    # 获取选择器与包名
    def getLib(self):
        raw_text = requests.get(self.url, headers=self.headers).content
        seletor = etree.HTML(raw_text)
        lib_names = seletor.xpath('//ul[@class="pylibs"]//li//strong//text()')
        return seletor, lib_names

    def Detail_urls(self):
        seletor, lib_names = self.getLib()
        detail_urls = []
        for each in lib_names:
            index = int(lib_names.index(each)) + 2
            detail_libs = seletor.xpath(
                '//ul[@class="pylibs"]//li[' + str(index) + "]//ul//li//text()"
            )
            detail_urls.append(detail_libs)
        return detail_urls

    def Download(self):
        detail_urls = self.Detail_urls()
        for detail_url in detail_urls:
            for url in detail_url:
                download_urls = self.base_url + url
                download_urls = download_urls.replace("‑", "-")
                cmd = "curl -O %s" % download_urls
                cmd_res = os.system(cmd)
                if cmd_res == 0:
                    print("下载成功!\n")
                    break
                else:
                    print("下载失败!\n")
                    is_try = input("是否重试下载(y|n)： ")
                    if is_try == "y" or is_try == "Y":
                        continue
                    else:
                        break


dw = AutoDownWhl()
dw.Download()