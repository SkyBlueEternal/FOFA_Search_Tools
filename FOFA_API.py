#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/18 10:09
# @Author  : 
# @Email   : 
# @File    : FOFA_API.py

import base64
import json
import requests
import optparse


class Client:
    def __init__(self,email,key):
        self.email = email
        self.key = key
        self.base_url = "http://fofa.so"
        self.search_api_url = "/api/v1/search/all"
        self.login_api_url = "/api/v1/info/my"
        self.get_userinfo() #check email and key

    def get_userinfo(self):
        api_full_url = "%s%s" % (self.base_url,self.login_api_url)
        param = {"email":self.email,"key":self.key}
        res = self.__http_get(api_full_url,param)
        return json.loads(res)

    def get_data(self,query_str,page=1,fields=""):
        res = self.get_json_data(query_str,page,fields)
        return json.loads(res)

    def get_json_data(self,query_str,page=1,fields=""):
        api_full_url = "%s%s" % (self.base_url,self.search_api_url)
        param = {"qbase64":base64.b64encode(query_str.encode("utf-8")),"email":self.email,"key":self.key,"page":page,"fields":fields}
        res = self.__http_get(api_full_url,param)
        return res

    def __http_get(self, url, param):
        try:
            tmp = requests.get(url=url, params=param)
            res = tmp.text
            if "errmsg" in res:
                raise RuntimeError(res)
        except requests.HTTPError as e:
            print("errmsg："+e.read(),)
            raise e
        return res

def run(email, key, query_str, page):
    fofa = Client(email=email, key=key)
    res = fofa.get_data(query_str=query_str, page=page, fields="")
    if res['results']:
        for i in res['results']:
            print(i)


if __name__ == '__main__':
    usage = "%prog By 98K\r\n%prog -e/--email <email> -k/--key <key> -p/--page <page> -q/--query <str>"
    parser = optparse.OptionParser(usage)
    parser.add_option('-e', '--email', dest='email', type='string', help='target email')
    parser.add_option('-k', '--key', dest='key', type='string', help='target key')
    parser.add_option('-p', '--page', dest='page', type='int', help='target page number')
    parser.add_option('-q', '--query', dest='query', help='target query')
    optparse, args = parser.parse_args()
    if 'None' not in str(optparse):
        run(
            email=optparse.email,
            key=optparse.key,
            query_str=optparse.query,
            page=optparse.page
        )
    else:
        print("参数不全，请-h查看帮助。")
