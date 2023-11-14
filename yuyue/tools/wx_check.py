#!/usr/bin/env python
import time,json,urllib3,hashlib,random,string
from bs4 import BeautifulSoup
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from base64 import b64encode


class wx_check:
    access_token = None
    jsapi_ticket = None
    token_time = 0
    def __init__(self):
        self.__check_token()
        

    def __check_token(self):
        if wx_check.token_time==0:
            infos = self.__read_conf()
            wx_check.access_token=infos['access_token']
            wx_check.jsapi_ticket=infos['jsapi_ticket']
            wx_check.token_time=int(infos['time_out'])
        else:pass
        if wx_check.access_token and wx_check.jsapi_ticket and int(time.time())<wx_check.token_time:
            pass
        else:
            self.__login()
            #wx_check.token_time = int(time.time())
            if wx_check.access_token:
                pass
            else:
                return 0,'报告服务器网络连接超时...'

    def __read_conf(self):
        infos = open('wx.conf','r',encoding='utf8').readlines()
        return dict([line.strip().split('：')for line in infos[1:]])

    def __write_conf(self,infos):
        out = ['#weixin']
        for key in infos:
            out.append('：'.join([key,infos[key]]))
        open('wx.conf','w',encoding='utf8').write('\n'.join(out))

    def __login(self):
        infos = self.__read_conf()
        AppID = infos['AppID']
        AppSecret = infos['AppSecret']
        url = r'https://api.weixin.qq.com/cgi-bin/token'
        urllib3.disable_warnings()
        http = urllib3.PoolManager()
        try:
            req = http.request(
                'GET',
                url,
                fields={"grant_type":"client_credential",
                        "appid":AppID,
                        "secret":AppSecret},
                timeout=2)
            content = json.loads(req.data.decode('utf-8'))
            #print (content)
            wx_check.access_token = content["access_token"]
            infos["access_token"] = wx_check.access_token
            wx_check.token_time = int(time.time())+content["expires_in"]-300
            infos["time_out"] = str(wx_check.token_time)
        except Exception as e:
            raise '获取access_token错误，%s'%(str(e))
        url = r'https://api.weixin.qq.com/cgi-bin/ticket/getticket'
        urllib3.disable_warnings()
        http = urllib3.PoolManager()
        try:
            req = http.request(
                'GET',
                url,
                fields={"access_token":wx_check.access_token,
                        "type":'jsapi'},
                timeout=2)
            content = json.loads(req.data.decode('utf-8'))
            #print (content)
            wx_check.jsapi_ticket = content["ticket"]
            infos["jsapi_ticket"] = wx_check.jsapi_ticket
        except Exception as e:
            raise '获取jsapi_ticket错误，%s'%(str(e))
        self.__write_conf(infos)

    def get_sign(self,noncestr,time_stamp,page):
        self.__check_token()
        ticket=wx_check.jsapi_ticket
        string1 = 'jsapi_ticket=%s&noncestr=%s&timestamp=%d&url=%s'%(ticket,noncestr,time_stamp,page)
        #open('test.log','a',encoding='utf8').write(string1+'\n')
        sha = hashlib.sha1(string1.encode('utf8'))
        encrypts = sha.hexdigest()
        #open('test.log','a',encoding='utf8').write(encrypts+'\n')
        return encrypts

    def get_prepay_sign(self,data_dict):
        self.__check_token()
        infos = self.__read_conf()
        key = infos['API_KEY']
        params_list = sorted(data_dict.items(), key=lambda e: e[0], reverse=False)
        params_str = "&".join(f"{k}={v}" for k,v in params_list) + '&key=' + key
        md5 = hashlib.md5()
        md5.update(params_str.encode('utf-8'))
        sign = md5.hexdigest().upper()
        return sign

    def get_pay_sign(self,data_dict):
        self.__check_token()
        infos = self.__read_conf()
        data_dict['appId'] = infos['AppID']
        data_dict['signType'] = 'MD5'
        data_dict['paySign'] = self.get_prepay_sign(data_dict)
        #open('test.log','a',encoding='utf8').write(str(data_dict)+'\n')
        return data_dict

    def get_prepay_id(self,openid,order_id,time_stamp,pay_amount,description):
        self.__check_token()
        infos = self.__read_conf()
        AppID = infos['AppID']
        AppSecret = infos['AppSecret']
        MchID = infos['MchID']
        MyIP = infos['MyIP']
        sub_info = {
            'appid':AppID,
            'mch_id':MchID,
            'nonce_str':''.join(random.sample(string.digits + string.ascii_letters,16)),
            'body':description,
            'out_trade_no':order_id,
            'total_fee':pay_amount,
            'spbill_create_ip':MyIP,
            'notify_url':'http://yuyue.yiruibio.com/wx_pay',
            'openid':openid,
            'trade_type':'JSAPI',
            }
        sub_info['sign'] = self.get_prepay_sign(sub_info)
        url = r'https://api.mch.weixin.qq.com/pay/unifiedorder'
        urllib3.disable_warnings()
        http = urllib3.PoolManager()
        try:
            req = http.request(
                'POST',
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
            sign_back_check = self.get_prepay_sign(data_dict)
            if sign_back==sign_back_check:
                return data_dict["prepay_id"]
            else:
                raise '获取prepay_id错误，数据签名错误！'
        except Exception as e:
            #open('test.log','a',encoding='utf8').write('获取openid错误，%s'%(str(e))+'\n')
            raise '获取prepay_id错误，%s'%(str(e))
        
    def get_openid(self,code):
        self.__check_token()
        infos = self.__read_conf()
        AppID = infos['AppID']
        AppSecret = infos['AppSecret']
        url = r'https://api.weixin.qq.com/sns/oauth2/access_token'
        urllib3.disable_warnings()
        http = urllib3.PoolManager()
        try:
            req = http.request(
                'GET',
                url,
                fields={"appid":AppID,
                        "secret":AppSecret,
                        "code":code,
                        "grant_type":'authorization_code',
                        },
                timeout=2)
            content = json.loads(req.data.decode('utf-8'))
            #open('test.log','a',encoding='utf8').write(str(content)+'\n')
            return content["openid"]
        except Exception as e:
            #open('test.log','a',encoding='utf8').write('获取openid错误，%s'%(str(e))+'\n')
            raise '获取openid错误，%s'%(str(e))
        
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
