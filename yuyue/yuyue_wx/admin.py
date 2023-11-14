from django.contrib import admin
from .models import *
from openpyxl import Workbook
from django.shortcuts import HttpResponse
from django.utils.timezone import localtime
import datetime

# Register your models here.
class ExportExcelMixin(object):
    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='application/msexcel')
        response['Content-Disposition'] = f'attachment; filename={meta}.xlsx'
        wb = Workbook()
        ws = wb.active
        ws.append([field.verbose_name for field in meta.fields])
        for obj in queryset:
            row = []
            for field in field_names:
                data = getattr(obj, field)
                if type(data)==datetime.datetime:
                    data = localtime(data).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    data = str(data)
                row.append(data)
            ws.append(row)

        wb.save(response)
        return response
    export_as_excel.short_description = '导出Excel'

@admin.register(pay_type)
class pay_type_Admin(admin.ModelAdmin):
    list_display = ('pay_type_name',) # list
    readonly_fields = list_display

@admin.register(organ)
class organ_Admin(admin.ModelAdmin):
    list_display = ('organ_name','pay_type','p_organ') # list

@admin.register(order)
class order_Admin(admin.ModelAdmin):
    list_display = ('order_describe','pay_type','price',
                    'order_start','order_end','organ') # list
    readonly_fields = ('qrcode',)

@admin.register(yuyue)
class yuyue_Admin(admin.ModelAdmin,ExportExcelMixin):
    list_display = (
        'name','sex','age','phone','id_type','id_code',
        'yuyue_date','yuyue_time','order',
        'barcode','status','opr_time','last_opr_time') # list
    list_filter =('order','yuyue_date','yuyue_time','status') #过滤器
    search_fields =('name','phone','id_code','barcode') #搜索字段
    date_hierarchy = 'last_opr_time'    # 详细时间分层筛选　
    actions = ['export_as_excel']  # 增加动作, 对应相应的方法名
    readonly_fields = ('order','openid','barcode','qrcode','status')

@admin.register(wenjuan)
class wenjuan_Admin(admin.ModelAdmin):
    list_display = ('wenjuan_result','wenjuan_time','yuyue') # list
    readonly_fields = list_display
    list_filter =('wenjuan_result',)

@admin.register(payment)
class payment_Admin(admin.ModelAdmin,ExportExcelMixin):
    list_display = (
        'pay_order_id','prepay_id','pay_amount','description',
        'openid','payment_status','payment_time','yuyue') # list
    readonly_fields = list_display
    list_filter =('pay_amount','payment_status') #过滤器
    search_fields =('pay_order_id','description') #搜索字段
    date_hierarchy = 'payment_time'    # 详细时间分层筛选
    actions = ['export_as_excel']  # 增加动作, 对应相应的方法名



