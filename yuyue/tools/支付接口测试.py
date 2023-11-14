#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time,urllib3,json,random,string,hashlib
from bs4 import BeautifulSoup
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from base64 import b64encode

def get_prepay_sign(method,url,time_stamp,noncestr,body):
        sign_str = '\n'.join([method,url,str(time_stamp),noncestr,body])+'\n'
        print (method,url,time_stamp,noncestr,body)
        print (sign_str)
        private_key = open('apiclient_key.pem','r',encoding='utf8').read()
        rsa_key = RSA.importKey(private_key)
        signer = pkcs1_15.new(rsa_key)
        digest = SHA256.new(sign_str.encode('utf8'))
        sign = b64encode(signer.sign(digest)).decode('utf8')
        return sign

def get_sign(data_dict, key):
    # 签名函数，参数为签名的数据和密钥
    params_list = sorted(data_dict.items(), key=lambda e: e[0], reverse=False)  # 参数字典倒排序为列表
    params_str = "&".join(f"{k}={v}" for k,v in params_list) + '&key=' + key
    # 组织参数字符串并在末尾添加商户交易密钥
    md5 = hashlib.md5()  # 使用MD5加密模式
    md5.update(params_str.encode('utf-8'))  # 将参数字符串传入
    sign = md5.hexdigest().upper()  # 完成加密并转为大写
    return sign

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

def get_prepay_id(openid,order_id,time_stamp,pay_amount,description):
    sub_info = {
            'appid':'wxd2e0f4e4ad52b8d9',
            'mch_id':"1508214841",
            'nonce_str':''.join(random.sample(string.digits + string.ascii_letters,16)),
            'body':description,
            'out_trade_no':order_id,
            'total_fee':pay_amount,
            'spbill_create_ip':'180.167.55.84',
            'notify_url':'http://yuyue.yiruibio.com/wx_pay',
            'openid':openid,
            'trade_type':'JSAPI',
            }
    API_KEY = 'shanghaiyiruiyixuejianyansuoyou1'
    sub_info['sign'] = get_sign(sub_info, API_KEY)
    url = r'https://api.mch.weixin.qq.com/pay/unifiedorder'#r'https://api.mch.weixin.qq.com/v3/pay/partner/transactions/jsapi'
    method = 'POST'
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    try:
        req = http.request(
            method,
            url,
            headers={'Content-Type':'application/json',
                     'Accept':'application/json',
                     },
            body=trans_dict_to_xml(sub_info),
            timeout=2)
        content = req.data.decode('utf-8')
        #print (content)
        data_dict = trans_xml_to_dict(content)
        sign_back = data_dict['sign']
        del data_dict['sign']
        sign_back_check = get_sign(data_dict, API_KEY)
        if sign_back==sign_back_check:
                return data_dict["prepay_id"]
        else:
                raise '获取prepay_id错误，数据签名错误！'
    except Exception as e:
        #open('test.log','a',encoding='utf8').write('获取openid错误，%s'%(str(e))+'\n')
        raise '获取prepay_id错误，%s'%(str(e))

prepay_id = get_prepay_id('oWuW704UFklG6rUgqRFVhr_dQAzY','EP1374029308132',int(time.time()),1,'test')
print (prepay_id)
