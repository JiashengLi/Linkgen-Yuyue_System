from django.db import models

# Create your models here.
class pay_type(models.Model):
    pay_type_name = models.CharField(max_length=20, verbose_name="支付方式")

    class Meta:
       verbose_name_plural = '支付方式'

    def __str__(self):
        return self.pay_type_name

class organ(models.Model):
    organ_name = models.CharField(max_length=250,unique=True, verbose_name="机构名称")
    pay_type = models.ForeignKey('pay_type', on_delete=models.SET_NULL, null=True, verbose_name="支付方式")
    p_organ = models.ForeignKey('self',default=0,related_name='children', on_delete=models.SET_NULL, null=True, verbose_name="上级机构")

    class Meta:
       verbose_name_plural = '机构设置'

    def __str__(self):
        return self.organ_name

class order(models.Model):
    order_describe = models.CharField(max_length=250,unique=True, verbose_name="订单描述")
    pay_type = models.ForeignKey('pay_type', on_delete=models.SET_NULL, null=True, verbose_name="支付方式")
    price = models.CharField(max_length=20, verbose_name="订单价格")
    order_start = models.DateTimeField(verbose_name='订单开始时间')
    order_end = models.DateTimeField(verbose_name='订单结束时间')
    organ = models.ForeignKey('organ', on_delete=models.SET_NULL, null=True, verbose_name="所属机构")
    qrcode = models.CharField(max_length=50,null=True,unique=True, verbose_name="二维码")

    class Meta:
       verbose_name_plural = '订单设置'

    def __str__(self):
        return self.order_describe

class yuyue(models.Model):
    name = models.CharField(max_length=20,verbose_name='姓名')
    sex = models.CharField(max_length=20,verbose_name='性别')
    age = models.CharField(max_length=20,verbose_name='年龄')
    yuyue_type = models.CharField(max_length=20,verbose_name='预约项目')
    phone = models.CharField(max_length=20,verbose_name='联系电话')
    id_type = models.CharField(max_length=20,verbose_name='证件类型')
    id_code = models.CharField(max_length=50,verbose_name='证件号')
    yuyue_date = models.DateField(verbose_name='预约日期')
    yuyue_time = models.CharField(max_length=20,verbose_name='预约时间段')
    opr_time = models.DateTimeField(auto_now_add=True,verbose_name='预约提交时间')
    order = models.ForeignKey('order', on_delete=models.SET_NULL, null=True, verbose_name="所属订单")
    openid = models.CharField(max_length=50,blank=True,verbose_name='预约openid')
    barcode = models.CharField(max_length=50,null=True,unique=True,verbose_name='条码号')
    status = models.CharField(max_length=50,verbose_name='订单状态')
    qrcode = models.CharField(max_length=50,null=True,unique=True, verbose_name="二维码")
    last_opr_time = models.DateTimeField(auto_now=True,verbose_name='最后操作时间')
    
    class Meta:
       verbose_name_plural = '样本信息管理'
       unique_together = ("id_code", "yuyue_date")

    def __str__(self):
        return self.name

class wenjuan(models.Model):
    wenjuan_result = models.CharField(max_length=500, verbose_name="问卷详情")
    wenjuan_time = models.DateTimeField(auto_now_add=True,verbose_name='问卷提交时间')
    yuyue = models.ForeignKey('yuyue', on_delete=models.SET_NULL, null=True, verbose_name="所属样本")

    class Meta:
       verbose_name_plural = '调查问卷管理'

    def __str__(self):
        return self.wenjuan_result

class payment(models.Model):
    pay_order_id = models.CharField(max_length=50,null=True,unique=True, verbose_name="付款单编号")
    prepay_id = models.CharField(max_length=50, verbose_name="支付ID")
    pay_amount = models.CharField(max_length=10, verbose_name="支付价格")
    description = models.CharField(max_length=100, verbose_name='订单信息')
    openid = models.CharField(max_length=50, verbose_name='支付openid')
    payment_status = models.CharField(max_length=10, verbose_name='支付状态')
    payment_time = models.DateTimeField(auto_now_add=True,verbose_name='支付时间')
    yuyue = models.ForeignKey('yuyue', on_delete=models.SET_NULL, null=True, verbose_name="所属样本")

    class Meta:
       verbose_name_plural = '支付管理'

    def __str__(self):
        return self.pay_order_id


