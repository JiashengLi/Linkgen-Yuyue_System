#!/usr/bin/env python
import time,json,urllib3
from Cryptodome import Random
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Cryptodome.Hash import MD5
from Cryptodome.Cipher import AES
import base64


class wd_check:
    def __init__(self):
        self.testcode = ''
        

    def __AES_encode(self,data):
        data = data.encode()
        #print (len(data),16-len(data)%16)
        add_k = 16-len(data)%16
        data = data + chr(add_k).encode()*add_k
        #print (data)
        # 密钥key需要为16, 24, 32长度的字节类型数据.
        aesKey = 'f46a793bfa6b4b6780028b72b5f15713'.encode()   # 16bytes
        # 还需要使用一个向量.
        aesIv = 'd265aed9515f4f60'.encode()  # 生成一个长度等于AES块大小并且不重复的密钥向量对象.
        # 使用key和iv初始化AES对象, 使用MODE_CBC模式.
        aesobj = AES.new(aesKey, AES.MODE_CBC, aesIv)
        # 加密的数据的长度需为16的倍数, 不足16则补足.
        return aesobj.encrypt(data).hex()

    def __AES_decode(self,data):
        data = bytes.fromhex(data)
        # 密钥key需要为16, 24, 32长度的字节类型数据.
        aesKey = 'f46a793bfa6b4b6780028b72b5f15713'.encode()   # 16bytes
        # 还需要使用一个向量.
        aesIv = 'd265aed9515f4f60'.encode()  # 生成一个长度等于AES块大小并且不重复的密钥向量对象.
        # 使用key和iv初始化AES对象, 使用MODE_CBC模式.
        aesobj = AES.new(aesKey, AES.MODE_CBC, aesIv)
        content = aesobj.decrypt(data)
        content = content[:-content[-1]]
        return content.decode('utf-8')

    #RSA签名
    def __RSA_sign(self,data):
        private_key = open('private.pem','r',encoding='utf8').read()
        #print (private_key)
        private_key_byte = base64.b64decode(private_key)
        #print (private_key_byte)
        rsakey = RSA.importKey(private_key_byte)
        signer = Signature_pkcs1_v1_5.new(rsakey)
        digest = MD5.new(data.encode())
        sign = signer.sign(digest)
        signature = base64.b64encode(sign)
        return signature.decode('utf-8')

    def get_barcode(self,time_stamp,registerId):
        url = r'https://api.wdjky.com/%s'%(self.__AES_encode('nad-biz-third-sample-submitSingle'))
        print (url)
        appid = 'bb8b084171104d57a6b0bcb84dc2b536'
        body = json.dumps({
            "registerId":registerId,
            "sampTypeId":2,
            "sampTargetId":10,
            "sampOperator":"何侃",
            "sampTime":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time_stamp/1000)),
            "sampOrgId":"7489a5baddf44fcf89bf860027d36fda",
            },ensure_ascii=False)
        print (body)
        coded_body = self.__AES_encode(body)
        print (coded_body)
        #decoded_body = self.__AES_decode(coded_body)
        #print (decoded_body)
        sign = '_'.join([appid,str(time_stamp),body])
        print (sign)
        sign = self.__RSA_sign(sign)#
        #print (sign)
        header={
            'appid':appid,
            'sign':sign,
            'timestamp':time_stamp,
            }
        print (header)
        urllib3.disable_warnings()
        http = urllib3.PoolManager()
        try:
            req = http.request(
                'POST',
                url,
                headers=header,
                body=coded_body,
                timeout=2)
            resp = req.data.decode('utf-8')
            print (str(type(resp)),resp)
            content = self.__AES_decode(resp)
            content = json.loads(content)
            print (content)
            if content["code"]==0:
                return content["data"]
            else:
                print (content["msg"])
        except Exception as e:
            #open('test.log','a',encoding='utf8').write('获取openid错误，%s'%(str(e))+'\n')
            print ('获取条码错误，%s'%(str(e)))
        

if __name__ == '__main__':
    wd_check().get_barcode(int(time.time()*1000),'e83cb11ab1d342e999589f82cd840720')
