#!/usr/bin/env python
import time
import json
import urllib3


class xk_op:
    token = None
    token_time = 0
    def __init__(self):
        self.__check_token()
        

    def __check_token(self):
        if xk_op.token and int(time.time())<xk_op.token_time:
            pass
        else:
            self.__login()
            #xk_op.token_time = int(time.time())
            if xk_op.token:
                pass
            else:
                return 0,'报告服务器网络连接超时...'

    def __login(self):
        u_id = "download report"
        pw = "e1r2a3"
        url = r'http://yr.wiki361.com/user/login/auth'
        urllib3.disable_warnings()
        http = urllib3.PoolManager()
        try:
            req = http.request(
                'POST',
                url,
                fields={"userName":u_id,
                        "password":pw},
                timeout=2)
            content = json.loads(req.data.decode('utf-8'))
            #print (content)
            xk_op.token = content["data"]["accessToken"]
            xk_op.token_time = int(time.time())+content["data"]["expireTime"]
            #open('log.log','a').write(str(content)+'\n'+str(int(time.time()))+'\n'+str(content["data"]["expireTime"])+'\n'+str(xk_op.token_time)+'\n')
            #token = content["data"]["accessToken"]
            return None
        except:
            return None

    def get_info(self,term,term_value,page = 1,size=10):
        #url = r'http://yr.wiki361.com/sample/sample/search?search[sampleSn]=%s&accessToken=%s'%(c_id,token)
        url = r'http://yr.wiki361.com/sample/sample/search'
        urllib3.disable_warnings()
        http = urllib3.PoolManager()
        req = http.request(
            'POST',
            url,
            fields={"search[%s]"%(term):term_value,
                    "page":page,
                    "size":size,
                    "accessToken":xk_op.token})
        content = json.loads(req.data.decode('utf-8'))
        #print (content)
        try:
            s_id = content["data"]
        except:
            s_id = []
        return s_id

    def upload_file(self,b_code,p_name,r_name,file):
        url = r'http://yr.wiki361.com/sample/report/do-add'
        urllib3.disable_warnings()
        http = urllib3.PoolManager()
        file_data = open(file,'rb').read()
        req = http.request(
            'POST',
            url,
            fields={
                "report[reportName]":p_name,
                "report[reportCustomName]":r_name,
                "report[barcode]":b_code,
                "report[reportTime]":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "accessToken":xk_op.token,
                "fileDocuments":('%s.pdf'%(b_code),file_data,"application/pdf"),
                })
        try:
            code = json.loads(req.data.decode('utf-8'))['code']
            return code
        except:
            return 0
            
