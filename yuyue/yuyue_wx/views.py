from django.shortcuts import render,redirect,HttpResponse
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from .models import *
import time,datetime,json,random,string,urllib,qrcode
from tools.wx_check import wx_check
from tools.err_center import err_record

# Create your views here.

@csrf_exempt
def yuyue_wx(request):
    if request.method == 'POST':
        #url = request.POST.get('url')
        #err_record(url+'\n')
        try:
            noncestr = ''.join(random.sample(string.digits + string.ascii_letters,16))
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
        except Exception as e:
            appinfo = json.dumps(
                {
                    'appId':str(e),
                    }
                )
        #open('test.log','a',encoding='utf8').write(appinfo+'\n')
        return HttpResponse(appinfo)
            
    else:
        request.session['openid']='test'
        request.session['orderId'] = 3
        openid = request.session.get('openid')
        if not openid:
            addinfo = urllib.parse.urlencode({"url_from":request.build_absolute_uri()})
            redirect_url = '/wx_auth?%s'%(addinfo)
            return redirect(redirect_url)
        yuyue_list_openid = yuyue.objects.filter(openid=openid).order_by('-opr_time').values_list('id','name','sex','phone','id_code','yuyue_date','yuyue_time','barcode','status')
        #print('yuyue_list_openid: ',yuyue_list_openid)
        files = []
        if len(yuyue_list_openid)>0:
            for line in yuyue_list_openid:
                if line[8]=='待支付':
                    print('info_form_out(line):',info_form_out(line))
                    files.append('''<table id="table_%s" border="2" cellpadding="5" cellspacing="2">
        <tr><th>%s</th><th>联系电话</th><th>%s</th></tr><tr><th>身份证</th><td colspan="2">%s</td></tr>
        <tr><th>预约时间</th><td>%s</td><td>%s</td></tr><tr><th>条码号</th><td colspan="2">%s</td></tr><tr><th>状态</th><td colspan="2">%s</td></tr>
        <tr><td colspan="3" align=center>
        <input type="button" value="支付检测费用" class="pay_table" id="pay_%s" style="width:150px;height:50px;background-color:#3CB371;color: #FFFFFF;font-size: 16pt;border:1px solid #3CB371;" />
        <input type="button" value="删除预约" class="del_table" id="del_%s" style="width:120px;height:50px;background-color:#CD3333;color: #FFFFFF;font-size: 16pt;border:1px solid #CD3333;" />
        </td></tr>
        </table>'''%(info_form_out(line)))
                elif line[8]=='待提交问卷':
                    files.append('''<table id="table_%s" border="2" cellpadding="5" cellspacing="2">
        <tr><th>%s</th><th>联系电话</th><th>%s</th></tr><tr><th>身份证</th><td colspan="2">%s</td></tr>
        <tr><th>预约时间</th><td>%s</td><td>%s</td></tr><tr><th>条码号</th><td colspan="2">%s</td></tr><tr><th>状态</th><td colspan="2">%s</td></tr>
        <tr><td colspan="3" align=center>
        <input type="button" value="填写流调问卷" class="wenjuan_table" id="wenjuan_%s" style="width:150px;height:50px;background-color:#3CB371;color: #FFFFFF;font-size: 16pt;border:1px solid #3CB371;" />
        </td></tr>
        </table>'''%(info_form_out(line)))
                elif line[8]=='待采样':
                    files.append('''<table id="table_%s" border="2" cellpadding="5" cellspacing="2">
        <tr><th>%s</th><th>联系电话</th><th>%s</th></tr><tr><th>身份证</th><td colspan="2">%s</td></tr>
        <tr><th>预约时间</th><td>%s</td><td>%s</td></tr><tr><th>条码号</th><td colspan="2">%s</td></tr><tr><th>状态</th><td colspan="2">%s</td></tr>
        <tr><td colspan="3" align=center>
        <input type="button" value="扫码采样" class="test_table" id="test_%s" style="width:150px;height:50px;background-color:#3CB371;color: #FFFFFF;font-size: 16pt;border:1px solid #3CB371;" />
        <input type="button" value="出示二维码" class="qrcode_table" id="qrcode_%s" style="width:150px;height:50px;background-color:#3CB371;color: #FFFFFF;font-size: 16pt;border:1px solid #3CB371;" />
        </td></tr>
        </table>'''%(info_form_out(line)))
                elif line[8]=='流调未通过':
                    files.append('''<table id="table_%s" border="2" cellpadding="5" cellspacing="2">
        <tr><th>%s</th><th>联系电话</th><th>%s</th></tr><tr><th>身份证</th><td colspan="2">%s</td></tr>
        <tr><th>预约时间</th><td>%s</td><td>%s</td></tr><tr><th>条码号</th><td colspan="2">%s</td></tr><tr><th>状态</th><td colspan="2">%s</td></tr>
        <tr><td colspan="3" align=center>
        <input type="button" value="扫码采样" class="test_table" id="test_%s" style="width:150px;height:50px;background-color:#FFFF00;color: #000000;font-size: 16pt;border:1px solid #FFFF00;" />
        <input type="button" value="出示二维码" class="qrcode_table" id="qrcode_%s" style="width:150px;height:50px;background-color:#FFFF00;color: #000000;font-size: 16pt;border:1px solid #FFFF00;" />
        </td></tr>
        </table>'''%(info_form_out(line)))
                else:
                    files.append('''<table id="table_%s" border="2" cellpadding="5" cellspacing="2">
        <tr><th>%s</th><th>联系电话</th><th>%s</th></tr><tr><th>身份证</th><td colspan="2">%s</td></tr>
        <tr><th>预约时间</th><td>%s</td><td>%s</td></tr><tr><th>条码号</th><td colspan="2">%s</td></tr><tr><th>状态</th><td colspan="2">%s</td></tr>
        </table>'''%(info_form_out(line)))
        else:
            files.append('<br>')
        
        return render(request, 'wx.html', {'pt':'微信服务首页','content':mark_safe('<br><br><br>'.join(files))})
def yuyue_preorder(request):
    files=[]
    return render(request, 'preorder.html', {'pt':'预约填写个人信息','content':mark_safe('<br><br><br>'.join(files))})
def yuyue_alert(request):
    files=[]
    return render(request, 'alert.html', {'pt':'服务流程','content':mark_safe('<br><br><br>'.join(files))})
def yuyue_survey_edit(request):
    files=[]
    return render(request, 'survey.html', {'pt':'编辑问卷儿','content':mark_safe('<br><br><br>'.join(files))})

@csrf_exempt
def yuyue_survey_preview(request):
    #print (request.POST)
    files=[]
    wenjuan_ans = request.POST.getlist('wenjuan_ans[0][]')
    print(wenjuan_ans)
    return render(request, 'questionnaire.html', {'pt':'预览问卷儿','content':mark_safe('<br><br><br>'.join(files))})        
def info_form_out(line):#这个函数只是根据状态返回不同的line填充表格，原数据仍然在tuple中
    try:
        u_name = '%s%s'%(line[1],{'男':'先生','女':'女士'}.get(line[2],''))
    except:
        try:
            u_name = '%s'%(line[1])
        except:
            u_name = ''
    try:
        phone = '%s%s%s'%(line[3][:3],'*'*(len(line[3])-7),line[3][-4:])
    except:
        phone = '%s'%(line[3])
    try:
        id_code = '%s%s%s'%(line[4][:3],'*'*(len(line[4])-6),line[4][-3:])
    except:
        id_code = '%s'%(line[4])
    barcode = line[7]
    if barcode==None:
        barcode = '未扫码'
    if line[8]=='待支付':
        return line[0],u_name,phone,id_code,line[5],line[6],barcode,line[8],line[0],line[0]
    elif line[8]=='待提交问卷':
        return line[0],u_name,phone,id_code,line[5],line[6],barcode,line[8],line[0]
    elif line[8]=='待采样':
        return line[0],u_name,phone,id_code,line[5],line[6],barcode,line[8],line[0],line[0]
    elif line[8]=='流调未通过':
        return line[0],u_name,phone,id_code,line[5],line[6],barcode,line[8],line[0],line[0]
    else:
        return line[0],u_name,phone,id_code,line[5],line[6],barcode,line[8]

def yuyue_order(request):
    #files = []
    #files.append('<!DOCTYPE html><html><head>')
    #files.append('<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=5.0, minimum-scale=0.5"/>')
    #files.append('<script type="text/javascript">function redirect_to(){location.href="/yuyue"}</script>')
    #files.append('<title>微信服务页面</title></head><body><br><br><br><br><br><table align=center>')
    #files.append('<tr><th><h2>由于春节假期安排的原因</h2></th></tr>')
    #files.append('<tr><th><h2>本公司即日起停止采样预约</h2></th></tr>')
    #files.append('<tr><th><h2>敬请谅解！</h2></th></tr>')
    #files.append('</table></html>')
    #return HttpResponse(mark_safe('\n'.join(files)))

    qrcode = request.GET.get('qrcode')
    if qrcode:
        try:
            orderId = order.objects.get(qrcode=qrcode).id
        except:
            return redirect('/yuyue_order')
    else:
        try:
            order_to_use = order.objects.get(order_describe='散样接收订单'+time.strftime('%Y%m%d',time.localtime(time.time())))
            orderId = order_to_use.id
        except:
            try:
                order_info = {
                    'order_describe':'散样接收订单'+time.strftime('%Y%m%d',time.localtime(time.time())),
                    'pay_type':pay_type.objects.get(pay_type_name='现结'),
                    'price':'8000',
                    'order_start':time.strftime('%Y-%m-%d',time.localtime(time.time())),
                    'order_end':time.strftime('%Y-%m-%d',time.localtime(time.time()+3600*24)),
                    'organ':organ.objects.get(id=1),
                    }
                order.objects.create(**order_info)
                order_to_use = order.objects.get(order_describe='散样接收订单'+time.strftime('%Y%m%d',time.localtime(time.time())))
                orderId = order_to_use.id
            except Exception as e:
                err_record('订单信息提交1：'+str(e)+'\n')
    request.session['orderId'] = orderId
    order_alive = order.objects.get(id=orderId)
    if time.time()<order_alive.order_end.timestamp() and time.time()>order_alive.order_start.timestamp():
        pass
    else:
        files = []
        files.append('<!DOCTYPE html><html><head>')
        files.append('<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=5.0, minimum-scale=0.5"/>')
        files.append('<script type="text/javascript">function redirect_to(){location.href="/yuyue"}</script>')
        files.append('<title>订单跳转页面</title></head><body><br><br><br><br><br><table align=center><tr><th><h2>当前订单不在有效时间内</h2></th></tr>')
        files.append('<tr><th><h2>请点击</h2><input type="button" value="跳转到有效个人订单" id="redirect_btn"  onclick="redirect_to()" style="width:235px;height:50px;background-color:#3CB371;font-size: 16pt;color: #FFFFFF;border:1px solid #3CB371;" />')
        files.append('</th></tr></table></html>')
        return HttpResponse(mark_safe('\n'.join(files)))
    return redirect('/yuyue_wx')

@csrf_exempt
def yuyue_list(request):
    openid = request.session.get('openid')
    orderId = request.session.get('orderId')
    if request.method == 'POST':
        try:
            yuyue_info = {}
            for k in ['name','sex','age','yuyue_type','phone','id_type','id_code','yuyue_date','yuyue_time']:
                yuyue_info[k] = request.POST.get(k)
            if '' in list(yuyue_info.values()):
                return HttpResponse('以上信息均为必填项，请认真填写')
        except Exception as e:
            err_record('样本信息提交1：'+str(e)+'\n')
            return HttpResponse('预约信息提交失败')
        yuyue_info['openid'] = openid
        order_alive = order.objects.get(id=orderId)
        yuyue_date = yuyue_info.get('yuyue_date')
        yuyue_date = datetime.datetime.strptime(yuyue_date,'%Y-%m-%d')
        #open('test.log','a',encoding='utf8').write(str(type(yuyue_date))+'\t'+str(yuyue_date)+'\n')
        time_stamp_today = time.mktime(time.strptime(time.strftime("%Y-%m-%d 00:00:00", time.localtime(time.time())), "%Y-%m-%d %H:%M:%S"))
        if yuyue_date.timestamp()<time_stamp_today:
            return HttpResponse('请提前预约')
        else:pass
        if time.time()<order_alive.order_end.timestamp() and time.time()>order_alive.order_start.timestamp():
            yuyue_info['order'] = order_alive
        else:
            return HttpResponse('当前订单不在有效时间内\n请选择有效订单')
        if yuyue_date.weekday() in [5,6]:
            return HttpResponse('本公司周末不提供检测服务')
        else:pass
        if yuyue_info['id_type']=='身份证' and len(yuyue_info['id_code'])!=18:
            #open('test.log','a',encoding='utf8').write(str(yuyue_info['id_code'])+str(len(yuyue_info['id_code']))+'\n')
            return HttpResponse('请填写18位有效身份证号')
        else:pass
        if yuyue_info['id_type']=='身份证' and id_code_check(yuyue_info['id_code']):
            #open('test.log','a',encoding='utf8').write(str(yuyue_info['id_code'])+str(len(yuyue_info['id_code']))+'\n')
            return HttpResponse('为配合检测数据上报\n请填写有效身份证号')
        else:pass
        if len(yuyue_info['phone'])!=11:
            #open('test.log','a',encoding='utf8').write(str(yuyue_info['id_code'])+str(len(yuyue_info['id_code']))+'\n')
            return HttpResponse('请填写11位有效手机号')
        else:pass
        yuyue_info['status'] = {'现结':'待提交问卷','月结':'待提交问卷'}[order_alive.pay_type.pay_type_name]#待支付
        print('预约表信息： ',yuyue_info)###
        try:
            testid = yuyue.objects.create(**yuyue_info).id
            print("testid:",testid,type(testid))####得到的预约id
            return HttpResponse("预约信息提交成功%d"%(testid))
        except Exception as e:
            if 'Duplicate entry' in str(e):
                return HttpResponse('同一人员只能每天预约一次')
            else:
                err_record('样本信息提交2：'+str(e)+'\n')
                return HttpResponse('预约信息提交失败')
            
    else:
        yuyue_id = request.GET.get('table_id').replace('pay_','')
        #open('test.log','a',encoding='utf8').write(str(yuyue_id)+'\n')
        try:
            yuyue_info = yuyue.objects.get(id=yuyue_id)
            if yuyue_info.barcode==None:
                barcode = '未扫码'
            else:
                barcode = yuyue_info.barcode
            result = '''<table id="table_select_%s" border="2" cellpadding="5" cellspacing="2">
<tr><th>姓名</th><th>%s</th></tr><tr><th>性别</th><th>%s</th></tr><tr><th>年龄</th><th>%s</th></tr><tr><th>预约项目</th><th>%s</th></tr>
<tr><th>联系电话</th><th>%s</th></tr><tr><th>证件类型</th><th>%s</th></tr><tr><th>证件号</th><th>%s</th></tr>
<tr><th>预约日期</th><th>%s</th></tr><tr><th>预约时间段</th><th>%s</th></tr><tr><th>条码号</th><th>%s</th></tr><tr><th>状态</th><th>%s</th></tr>
'''%(yuyue_info.id,yuyue_info.name,yuyue_info.sex,yuyue_info.age,yuyue_info.yuyue_type,yuyue_info.phone,yuyue_info.id_type,yuyue_info.id_code,yuyue_info.yuyue_date,yuyue_info.yuyue_time,barcode,yuyue_info.status)
        except Exception as e:
            err_record('样本信息提交3：'+str(e)+'\n')
        return HttpResponse(result)

@csrf_exempt
def yuyue_detail(request):
    openid = request.session.get('openid')
    if request.method == 'POST':
        opt = request.POST.get('opt')
        #open('test.log','a',encoding='utf8').write(opt+'\n')
        if opt=='pay':
            try:
                yuyue_id = request.POST.get('table_id').replace('pay_','')
                time_stamp = int(time.time()*1000)
                order_id = 'E%s%d'%(yuyue_id,time_stamp)
                time_stamp = int(time_stamp/1000)
                yuyue_info = yuyue.objects.get(id=yuyue_id)
                pay_amount = int(yuyue_info.order.price)
                description = '-'.join([str(yuyue_info.id),yuyue_info.name,yuyue_info.id_code[:6]+yuyue_info.id_code[-4:],str(yuyue_info.yuyue_date)])
                #open('test.log','a',encoding='utf8').write(str([openid,order_id,time_stamp,pay_amount,description])+'\n')
                prepay_id = wx_check().get_prepay_id(openid,order_id,time_stamp,pay_amount,description)
                pay_info = {
                    'pay_order_id':order_id,
                    'prepay_id':prepay_id,
                    'pay_amount':pay_amount,
                    'description':description,
                    'openid':openid,
                    'payment_status':'待支付',
                    'yuyue':yuyue_info,
                    }
                payment.objects.create(**pay_info)
                #open('test.log','a',encoding='utf8').write(str(prepay_id)+'\n')
                noncestr = ''.join(random.sample(string.digits + string.ascii_letters,16))
                pay_info = wx_check().get_pay_sign({'timeStamp':str(time_stamp),'nonceStr':noncestr,'package':'prepay_id='+prepay_id})
                #open('test.log','a',encoding='utf8').write(str(pay_info)+'\n')
                return HttpResponse(json.dumps(pay_info))
            except Exception as e:
                err_record('样本支付提交1：'+str(e)+'\n')
        elif opt=='del':
            try:
                yuyue_id = request.POST.get('table_id').replace('del_','')
                #open('test.log','a',encoding='utf8').write(yuyue_id+'\n')
                try:
                    yuyue.objects.get(id=yuyue_id).delete()
                    return HttpResponse('已删除该预约')
                except Exception as e:
                    err_record('样本删除提交1：'+str(e)+'\n')
                    return HttpResponse('删除预约失败')
            except Exception as e:
                err_record('样本删除提交2：'+str(e)+'\n')
        elif opt=='pay_done':
            try:
                yuyue_id = request.POST.get('table_id').replace('pay_','')
                #open('test.log','a',encoding='utf8').write('支付完的yuyue_id是'+yuyue_id+'\n')
                try:
                    yuyue.objects.filter(id=yuyue_id).update(status='待提交问卷',last_opr_time=datetime.datetime.now())
                    return HttpResponse('已支付该预约')
                except Exception as e:
                    err_record('样本支付提交2：'+str(e)+'\n')
                    return HttpResponse('更新支付状态失败')
            except Exception as e:
                err_record('样本支付提交3：'+str(e)+'\n')
        elif opt=='barcode':
            try:
                yuyue_id = request.POST.get('table_id').replace('test_','')
                barcode = request.POST.get('barcode')
                #open('test.log','a',encoding='utf8').write('支付完的yuyue_id是'+yuyue_id+'\n')
                try:
                    if barcode[:5]=='46641' and len(barcode)==12:
                        pass
                    elif barcode[:4]=='2021' and len(barcode)==11:
                        pass
                    else:
                        return HttpResponse('条码值异常，请重新扫码')
                    yuyue.objects.filter(id=yuyue_id).update(barcode=barcode,status='完成采样',last_opr_time=datetime.datetime.now())
                    return HttpResponse('成功绑定条码')
                except Exception as e:
                    if 'Duplicate entry' in str(e):
                        return HttpResponse('条码已被使用，请更换条码')
                    else:
                        err_record('样本绑定条码1：'+str(e)+'\n')
                        return HttpResponse('绑定条码失败')
            except Exception as e:
                err_record('样本绑定条码2：'+str(e)+'\n')
        elif opt=='wenjuan':
            
            try:
                #yuyue_id = request.POST.get('table_id').replace('wenjuan_','')
                yuyue_id = request.POST.get('yuyue_id')
                print("尝试打印wenjuan_ID：",yuyue_id)
                wenjuan_result = [request.POST.get('wenjuan_%d'%(i)) for i in range(1,8)]
                if None in wenjuan_result:
                    return HttpResponse('请填写所有问题')
                elif '是' in wenjuan_result:
                    yuyue.objects.filter(id=yuyue_id).update(status='流调未通过',last_opr_time=datetime.datetime.now())
                    wenjuan_result = ','.join(wenjuan_result)
                    back_info = '请联系工作人员了解相关政策'
                else:
                    yuyue.objects.filter(id=yuyue_id).update(status='待支付',last_opr_time=datetime.datetime.now())
                    wenjuan_result = ','.join(wenjuan_result)
                    back_info = '问卷提交成功'
                #open('test.log','a',encoding='utf8').write('支付完的yuyue_id是'+yuyue_id+'\n')
                try:
                    yuyue_info = yuyue.objects.get(id=yuyue_id)
                    wenjuan_info = {
                        'wenjuan_result':wenjuan_result,
                       'yuyue':yuyue_info,
                       }
                    wenjuan.objects.create(**wenjuan_info)
                    print(wenjuan_result)
                    return HttpResponse(back_info)
                except Exception as e:
                    err_record('样本流调提交1：'+str(e)+'\n')
                    return HttpResponse('问卷提交失败')
            except Exception as e:
                err_record('样本流调提交2：'+str(e)+'\n')
        elif opt=='qrcode':
            try:
                yuyue_id = request.POST.get('table_id').replace('qrcode_','')
                try:
                    yuyue_qrcode = yuyue.objects.get(id=yuyue_id).qrcode
                    if yuyue_qrcode:
                        return HttpResponse('static/yuyue_qrcode/%s.jpg'%(yuyue_qrcode))
                    else:
                        try:
                            while True:
                                yuyue_qrcode = ''.join(random.sample(string.digits + string.ascii_letters,10))
                                try:
                                    yuyue.objects.filter(id=yuyue_id).update(qrcode=yuyue_qrcode,last_opr_time=datetime.datetime.now())
                                    break
                                except:
                                    continue
                            img = qrcode.make(yuyue_qrcode)
                            img.save('static/yuyue_qrcode/%s.jpg'%(yuyue_qrcode))
                            return HttpResponse('static/yuyue_qrcode/%s.jpg'%(yuyue_qrcode))
                        except Exception as e:
                            err_record('获取二维码1：'+str(e)+'\n')
                            return HttpResponse('获取二维码失败')
                except Exception as e:
                    err_record('获取二维码2：'+str(e)+'\n')
                    return HttpResponse('获取二维码失败')
            except Exception as e:
                err_record('获取二维码3：'+str(e)+'\n')
        else:
            return HttpResponse('')
    else:
        result = ''
        #open('test.log','a',encoding='utf8').write(result+'\n')
        return HttpResponse(result)

def id_code_check(id_code):
    try:
        id_code_list = [int(idc) for idc in id_code[:-1]]
        check_list = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_result = sum([id_code_list[i]*check_list[i] for i in range(len(id_code_list))])%11
        check_seq = '1 0 X 9 8 7 6 5 4 3 2'.split(' ')
        if check_seq[check_result]==id_code[-1]:
            return False
        else:
            return True
    except Exception as e:
        err_record('身份证验证1：'+str(e)+'\n')
        return True
