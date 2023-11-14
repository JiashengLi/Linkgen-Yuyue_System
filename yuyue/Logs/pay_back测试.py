#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time,urllib3,json,random,string,hashlib
from bs4 import BeautifulSoup
#from yuyue.yuyue_wx.models import payment

def trans_dict_to_xml(data_dict):  # 定义字典转XML的函数
    data_xml = []
    for k in sorted(data_dict.keys()):  # 遍历字典排序后的key
        v = data_dict.get(k)  # 取出字典中key对应的value
        if k == 'detail' and not v.startswith('<![CDATA['):  # 添加XML标记
            v = f'<![CDATA[{v}]]>'
        data_xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    return '<xml>{}</xml>'.format(''.join(data_xml)).encode('utf-8')  # 返回XML，并转成utf-8，解决中文的问题

def trans_xml_to_dict(data_xml):
    soup = BeautifulSoup(data_xml, features='xml')
    xml = soup.find('xml')  # 解析XML
    if not xml:
        return {}
    data_dict = dict([(item.name, item.text) for item in xml.find_all()])
    return data_dict

infos = open ('pay_back_old.log','r',encoding='utf8').read()
infos = json.loads(infos)
print (type(infos))
open ('pay_back_old1.log','w',encoding='utf8').write('\n'.join(infos))
