#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/18 14:50
# @Author  :
# @Email   :
# @File    : FOFA_SPIDER.py

import sys
import base64
import requests
import optparse
from bs4 import BeautifulSoup


class Client:
    def __init__(self, num):
        self.base_url = "http://fofa.so"
        self.search_api_url = "/result"
        self.num = num

    def http_post(self, q, page, cookie):
        try:
            req = requests.Session()
            tmp = req.get(
                url=self.base_url + self.search_api_url,
                params={
                    'q': q,
                    'qbase64': base64.b64encode(q.encode("utf-8")),
                    'page': page
                },
                headers={
                    'cookie': cookie,
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-User': '1',
                    'Sec-Fetch-Dest': 'document'
                }
            )
            req.close()
        except Exception as e:
            print("errmg:", e)
            raise e
        else:
            self.__get_res(tmp.text)

    def __get_res(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        url_lust = soup.findAll("a", {'target': '_blank'})
        for ip in url_lust:
            if self.num == 0:
                sys.exit(0)
            if "FOFA经典版" not in str(ip) and "https://github.com/FOFAPRO" not in str(ip):
                if ':' in str(ip):
                    print(ip['href'])
                elif "host" in str(ip):
                    pass
                else:
                    self.num = self.num - 1


if __name__ == '__main__':
    usage = "%prog By 98k\r\n%prog -n/--num <number> -c/--cookie <cookie> -p/--page <page> -q/--query <str>"
    parser = optparse.OptionParser(usage)
    parser.add_option('-n', '--num', dest='number', type='string', help='target number,number is retry count')
    parser.add_option('-c', '--cookie', dest='cookie', type='string', help='target cookie')
    parser.add_option('-p', '--page', dest='page', type='int', help='target page number')
    parser.add_option('-q', '--query', dest='query', help='target query')
    optparse, args = parser.parse_args()
    if 'None' not in str(optparse):
        num = optparse.number
        cookie = optparse.cookie
        page = optparse.page
        query = optparse.query
        fofa = Client(num=num)
        for i in range(page):
            fofa.http_post(
                q=query,
                page=i,
                cookie=cookie
            )
    else:
        print("参数不全，请-h查看帮助。")