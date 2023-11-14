from django.shortcuts import render,redirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import signing
from .models import *
from yuyue_wx.models import payment
import time,json,random,string,urllib
from bs4 import BeautifulSoup
from tools.wx_check import wx_check
from tools.err_center import err_record

# Create your views here.

def wx(request):
    #open('test.log','a',encoding='utf8').write('req'+'\n')
    if request.method == 'POST':
        appinfo = json.dumps(
            {
                'statu':'success',
                'data':request.POST.get('appId'),
                }
            )
        return HttpResponse(appinfo)
    else:
        try:
            noncestr = ''.join(random.sample(string.ascii_letters,16))
            time_stamp = int(time.time())
            signature = wx_check().get_sign(noncestr,time_stamp,'/yuyue_wx')
            appinfo = json.dumps(
                {
                    'appId':'wxd2e0f4e4ad52b8d9',
                    'timestamp':time_stamp,
                    'nonceStr':noncestr,
                    'signature':signature,
                    }
                )
            #open('test.log','a',encoding='utf8').write(appinfo+'\n')
        except Exception as e:
            appinfo = json.dumps(
                {
                    'appId':str(e),
                    }
                )
        return HttpResponse(appinfo)

def wx_auth(request):
    url_from = request.GET.get('url_from')
    openid = request.session.get('openid')
    if not openid:
        request.session['openid']='test'
        '''code = request.GET.get('code')
        if not code:
            appid = 'wxd2e0f4e4ad52b8d9'
            redirect_uri = {"redirect_uri":"/wx_auth?url_from=%s"%(url_from)}
            redirect_uri = urllib.parse.urlencode(redirect_uri)
            #open('test.log','a',encoding='utf8').write(redirect_uri+'\n')
            redirect_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&%s&response_type=code&scope=snsapi_base#wechat_redirect'%(appid,redirect_uri)
            #open('test.log','a',encoding='utf8').write(redirect_url+'\n')
            return redirect(redirect_url)
        openid = wx_check().get_openid(code)#'''
        request.session['openid'] = openid
        #open('test.log','a',encoding='utf8').write('get_openid'+'\n')
    #open('test.log','a',encoding='utf8').write('openid：'+openid+'\n')
    url_from = urllib.parse.unquote(url_from)
    if url_from=='/yuyue_wx':
        return redirect(url_from)
    elif '?' in url_from:
        return redirect(r'%s&openid=%s'%(url_from,openid))
    else:
        return redirect(r'%s?openid=%s'%(url_from,openid))

def trans_xml_to_dict(data_xml):
    soup = BeautifulSoup(data_xml, features='xml')
    xml = soup.find('xml')  # 解析XML
    if not xml:
        return {}
    data_dict = dict([(item.name, item.text) for item in xml.find_all()])
    return data_dict

@csrf_exempt
def wx_pay(request):
    if request.method == 'POST':
        try:
            open('Logs/pay_back.log','a',encoding='utf8').write('POST\n'+str(dict(request.POST))+'\n')
            back_info = trans_xml_to_dict(request.body.decode('utf-8'))
            try:
                payment.objects.filter(pay_order_id=back_info['out_trade_no']).update(payment_status='支付完成')
            except Exception as e:
                open('Logs/pay_back_err.log','a',encoding='utf8').write('支付LOG接收1'+str(e)+'\n')
            open('Logs/pay_back.log','a',encoding='utf8').write('body\n'+json.dumps(back_info,ensure_ascii=False)+'\n')
            return HttpResponse('<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>')
        except Exception as e:
            open('Logs/pay_back_err.log','a',encoding='utf8').write('支付LOG接收2'+str(e)+'\n')
            return HttpResponse('<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>')
    else:
        open('Logs/pay_back.log','a',encoding='utf8').write('GET\n'+str(dict(request.GET))+'\n')
        return HttpResponse('<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>')

@csrf_exempt
def wx_err(request):
    if request.method == 'POST':
        try:
            err_record('config反馈错误1：'+str(dict(request.POST))+'\n')
            return HttpResponse('')
        except Exception as e:
            err_record('ERROR接收1'+str(e)+'\n')
            return HttpResponse('')
    else:
        err_record('config反馈错误2：'+str(dict(request.GET))+'\n')
        return HttpResponse('')
